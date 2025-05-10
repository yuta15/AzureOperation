from pydantic import BaseModel, field_validator
from typing import Literal, List, Dict

from annotations.IPv4NetworkOrAddressAnnotaion import ipv4_network_or_address_validator

class NetworkRuleSetModel(BaseModel):
    """
    StorageAccountのNetwowrkアクセスを指定するためのクラス
    TODO:
        - bypass: upper()を実行して大文字小文字関係無く指定可能にする
        
    """
    default_action: Literal['Allow', 'Deny'] = 'Allow'
    bypass: Literal[None, 'Logging', 'Metrics', 'AzureServices'] = 'AzureServices'
    resource_access_rules: List[Dict] | None = None
    virtual_network_rules: List[Dict]
    ip_rules: List[Dict]
    

    @field_validator('default_action', mode='before')
    @classmethod
    def capitalize_string(cls, value: str) -> str:
        """
        文字列を大文字に変換するバリデータ
        :param cls: クラス
        :param value: 文字列
        :return: 大文字に変換された文字列
        """
        return value.capitalize()
    
    
    @field_validator('ip_rules', mode='before')
    @classmethod
    def ip_rule_validator(cls, ip_rules: List) -> List:
        """
        ip_rulesをValidateする
        """
        for ip_rule in ip_rules:
            ip_address_or_range = ip_rule.get('ip_rule', None)
            action = ip_rule.get('action', None)
            
            if ip_address_or_range == None or action == None:
                raise ValueError(f"""
                                 ip_rulesには`ip_address_or_range`と`action`をキーとするDictを指定してください。
                                 """)
            ipv4_network_or_address_validator()