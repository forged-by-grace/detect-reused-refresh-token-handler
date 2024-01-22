from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):    
    # Event Streaming Server
    api_event_streaming_host:str
    api_event_streaming_client_id: str

    # Service metadata
    service_name: str

    # Streaming topics
    api_update_account: str   
    api_notification: str
    api_reused_refresh_token: str    
    
    # Cache credentials
    api_redis_host_local: str

    # DB credentials
    api_db_url: str
   
settings = Settings()
