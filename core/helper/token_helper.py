from core.model.update_model import UpdateFieldAvro, UpdateAvro
from core.model.notification_avro_model import Notification

from core.enums.token_enum import NotificationChannel, NotificationTemplate, Role
from core.event.produce_event import produce_event

from core.utils.settings import settings
from core.utils.init_log import logger

from core.helper.db_helper import get_account_by_id

from datetime import datetime



async def invalidate_account_tokens(id: str) -> None:
    # Create database field objs
    tokens_field = UpdateFieldAvro(action='$set', value={'tokens': []})
    last_update_field = UpdateFieldAvro(action='$set', value={'last_update': datetime.utcnow().isoformat()})
    is_active_field = UpdateFieldAvro(action='$set', value={'is_active': False})
    active_device_count_field = UpdateFieldAvro(action='$set', value={'active_device_count': 0})
    active_devices_field = UpdateFieldAvro(action='$set', value={'active_devices': []})
    role_field = UpdateFieldAvro(action='$set', value={'role.name': Role.anonymouse.value})

    # Create update list
    account_updates = UpdateAvro(
        db_metadata={'provider': 'mongoDB', 
                     'database': 'account_db', 
                     'collection': 'accounts'},
        db_filter={'_id': id},
        updates=[
            tokens_field, 
            is_active_field, 
            active_device_count_field, 
            active_devices_field, 
            role_field, 
            last_update_field
        ]
    )

    # Emit update event
    await emit_update_event(account_updates=account_updates)


async def send_threat_notification(id: str) -> None:
    # Fetching account from database    
    account_data = await get_account_by_id(id=id)

    # Check if account exists
    if account_data: 
        # Recipient name
        name = f"{account_data.get('lastname')}, {account_data.get('firstname')}"
        
        # Create notification obj
        notification = Notification(
            recipient_name=name,
            send_to=account_data.get('email'),
            channel=NotificationChannel.email,
            content={},
            template=NotificationTemplate.reused_token_detected.value
        )

        # Serialize
        notification_event = notification.serialize()

        # Emit event
        await produce_event(topic=settings.api_notification, value=notification_event)

   
async def emit_update_event(account_updates: UpdateAvro) -> None:
    # Serialize    
    account_updates_event = account_updates.serialize()

    # Emit event
    logger.info('Emitting update account event')
    await produce_event(topic=settings.api_update_account, value=account_updates_event)

