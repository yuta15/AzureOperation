from datetime import datetime, timezone, timedelta

from typing import List, Literal
from pydantic import Field, model_validator

from models.resource.ResourceGroupModel import ResourceGroupModel
from models.storage.ManagedIdModel import ManagedIdModel
from models.storage.SasPolicyModel import SasPolicyModel
from annotations.StorageSkuAnnotation import StorageSkuAnnotation
from annotations.SasDatetimeAnnotaion import SasDatetimeAnnotaion



class StorageAccountModel(ResourceGroupModel):
    """
    StorageAccountのバリデーション用クラス
    ResourceGroupModelを継承しているため、location, tagsの値が必要となる
    Attributes:
        location: str | None = None
        tags: dict | None = None
        resource_group_name: str | None = None
        account_name: str | None = None
        sku: str | None = None
        kind: str | None = None
        access_tier: str | None = None
        enable_https_traffic_only: bool | None = None
    """
    account_name: str = Field(max_length=24,min_length=3,pattern='^[0-9a-z][0-9a-z\-]*$',)
    sku: StorageSkuAnnotation = 'PremiumV2_LRS'
    kind: Literal['StorageV2', 'BlobStorage', 'FileStorage', 'BlockBlobStorage'] = 'StorageV2'
    allowed_copy_scope: Literal['PrivateLink', 'AAD', None] = None
    enable_https_traffic_only: bool = Field(default=True)
    sas_policy: SasPolicyModel | None = None
    Managed_id: ManagedIdModel | None = None
    public_network_access: Literal['Enabled', 'Disabled'] = 'Enabled'
    network_rule_set: NetworkRuleSetModel | None = None
    

    @model_validator
    @classmethod
    def identity_validate(cls, values:dict) -> dict:
        """
        identity_typeがNoneの場合はuser_assigned_identitiesの値もNoneにする。
        
        Args:
            values: dict
                classが受け取った各フィールドの情報がdict化されたもの
        Return:
            values: dict
                classが受け取った各フィールドの情報がdict化されたもの
        """
        identity_type = values[identity_type]
        user_assigned_identities = values[user_assigned_identities]
        if identity_type == None:
            values[user_assigned_identities] = None
            return values
        return values