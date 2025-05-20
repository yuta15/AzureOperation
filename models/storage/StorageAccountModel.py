from datetime import datetime, timezone, timedelta

from typing import List, Literal
from pydantic import Field, model_validator

from models.resource.ResourceGroupModel import ResourceGroupModel
from models.storage.ManagedIdModel import ManagedIdModel
from models.storage.SasPolicyModel import SasPolicyModel
from models.storage.NetworkRuleSetModel import NetworkRuleSetModel
from annotations.StorageSkuAnnotation import StorageSkuAnnotation


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
    sku: StorageSkuAnnotation
    kind: Literal['StorageV2', 'BlobStorage', 'FileStorage', 'BlockBlobStorage'] = 'StorageV2'
    access_tier: Literal['Hot', 'Cool', 'Premium', 'Cold'] = 'Hot'
    sas_policy: SasPolicyModel | None = None
    managed_id: ManagedIdModel | None = None
    public_network_access: Literal['Enabled', 'Disabled'] = 'Enabled'
    network_rule_set: NetworkRuleSetModel | None = None
    dns_endpoint_type: Literal['Standard', 'AzureDnsZone'] = 'Standard'
    tls_version: Literal['TLS1_0', 'TLS1_1', 'TLS1_2', 'TLS1_3'] = 'TLS1_2'
    enable_https_traffic_only: bool = True
    allow_shared_key_access: bool = True
    allow_cross_tenant_replication: bool = False
    allow_blob_public_access: bool = True
    default_to_o_auth_authentication: bool = False


    @model_validator
    @classmethod
    def identity_validate(cls, values:dict) -> dict:
        """
        managed_idがNoneの場合はuser_assigned_identitiesの値もNoneにする。
        
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