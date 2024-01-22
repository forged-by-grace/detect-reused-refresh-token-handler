from core.helper.consumer_helper import consume_event
from core.utils.settings import settings
from core.utils.init_log import logger
from core.helper.token_helper import invalidate_account_tokens, send_threat_notification
from core.model.token_models import ReusedToken

# Processing event msg
event_processing_msg = "Processing event"


async def consume_reused_refresh_token_event():
    # consume event
    consumer = await consume_event(topic=settings.api_reused_refresh_token, group_id=settings.api_reused_refresh_token)
    
    try:
        # Consume messages
        async for msg in consumer: 
            logger.info('Received reused refresh token event.') 
            
            # Deserialize event
            account_data = ReusedToken.deserialize(data=msg.value)
            
            # invalidate token
            logger.info(event_processing_msg)
            await invalidate_account_tokens(id=account_data.id)
            
            # Notify account owner of threat
            await send_threat_notification(id=account_data.id)
    except Exception as err:
        logger.error(f'Failed to process event due to error: {str(err)}')
    finally:
        await consumer.stop()

