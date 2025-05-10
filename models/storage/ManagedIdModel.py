from pydantic import BaseModel, model_validator
from typing import Literal


class ManagedIdModel(BaseModel):
    """
    StorageAccountのManagedId用のモデル
    
    """
    type: Literal[None, 'UserAssigned'] = None
    principal_id: str | None = None
    client_id: str | None = None
    
    @model_validator
    @classmethod
    def identity_validate(cls, values: dict) -> dict:
        if values['type'] == None:
            values['principal_id'] = None
            values['client_id'] = None
            return values
        if values['principal_id'] == None or values['client_id'] == None:
            raise ValueError(f"""
                             'ManagedIdを有効化する場合には、typeで'UserAssigned'を選択し、
                             principal_idとclient_idを入力してください。
                             """)
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