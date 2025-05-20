from pydantic import BaseModel, model_validator
from typing import Literal
from uuid import UUID


class ManagedIdModel(BaseModel):
    """
    StorageAccountのManagedId用のモデル
    UserAssignedのみ対応可能。
    "SystemAssigned,UserAssigned", "SystemAssigned"の未実装
    """
    type: Literal['UserAssigned', None] = 'UserAssigned'
    principal_id: UUID | None = None
    client_id: UUID | None = None
    
    @model_validator(mode='before')
    @classmethod
    def identity_validate(cls, values: dict) -> dict:
        if values['type'] == None:
            values['principal_id'] = None
            values['client_id'] = None
            return values
        if values['principal_id'] == None or values['client_id'] == None:
            raise ValueError('ManagedIdを使用する場合はprincipal_idとclient_idは必須の値です。')
        return values

    def gen_params(self) -> dict:
        """parameter用dict生成関数"""
        return {
            'type': self.type,
            'user_assigned_identities': {
                'principal_id': self.principal_id,
                'client_id': self.client_id
            }
        }