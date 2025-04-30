import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal
from azure.identity import DefaultAzureCredential

class Setting(BaseSettings):
    """
    環境設定用クラス
    
    """
    ENV: Literal['DEV', 'PRD', 'TEST'] = Field(default='DEV')
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_TENANT_ID: str
    
    model_config = SettingsConfigDict(extra='allow')
    
    
    def _set_environment(self) -> None:
        os.environ['ENV'] = self.ENV
        os.environ['AZURE_CLIENT_ID'] = self.AZURE_CLIENT_ID
        os.environ['AZURE_CLIENT_SECRET'] = self.AZURE_CLIENT_SECRET
        os.environ['AZURE_TENANT_ID'] = self.AZURE_TENANT_ID
    
    
    def gen_credentail(self) -> DefaultAzureCredential:
        """
        default
        """
        self._set_environment()
        return DefaultAzureCredential()