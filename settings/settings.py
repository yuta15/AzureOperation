from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal


class Setting(BaseSettings):
    """
    環境設定用クラス
    
    """
    ENV: Literal['DEV', 'PRD', 'TEST'] = Field(default='DEV')
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_TENANT_ID: str
    
    model_config = SettingsConfigDict(extra='allow')