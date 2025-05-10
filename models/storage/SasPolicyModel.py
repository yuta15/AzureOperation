from pydantic import BaseModel, model_validator
from typing import Literal

from annotations.SasDatetimeAnnotaion import SasDatetimeAnnotaion

class SasPolicyModel(BaseModel):
    """
    StorageAccountのSAS用のモデル
    
    """
    sas_expired_action: Literal['Log', 'Block'] = 'Log'
    sas_expired_datetime: SasDatetimeAnnotaion | None = None
    
    
    def gen_parmas(self) -> dict:
        """パラメータ用関数"""
        return {
            'sas_expiration_period': self.sas_expired_datetime,
            'expiration_action': self.sas_expired_action
        }