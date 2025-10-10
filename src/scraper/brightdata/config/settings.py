from pydantic_settings import BaseSettings
from typing import Optional


class BrightDataSettings(BaseSettings):
    api_token: str
    base_url: str = "https://api.brightdata.com"
    trigger_endpoint: str = "/dca/trigger"
    task_endpoint: str = "/dca/tasks/get"
    rate_limit_qps: float = 1.0
    timeout_seconds: int = 30

    # Optional: collector IDs for convenience (configure in .env)
    linkedin_collector_id: Optional[str] = None
    indeed_collector_id: Optional[str] = None

    class Config:
        env_prefix = "BRIGHTDATA_"
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> BrightDataSettings:
    return BrightDataSettings() 
