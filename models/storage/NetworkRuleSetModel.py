from pydantic import BaseModel, field_validator
from typing import Literal, List, Dict

from annotations.IPv4NetworkOrAddressAnnotaion import IPv4NetworkOrAddressAnnotation

class NetworkRuleSetModel(BaseModel):
    """
    StorageAccountのNetwowrkアクセスを指定するためのクラス
    TODO:
        - bypass: upper()を実行して大文字小文字関係無く指定可能にする
    """
    default_action: Literal['Allow', 'Deny'] = 'Allow'
    bypass: Literal[None, 'Logging', 'Metrics', 'AzureServices'] = 'AzureServices'
    resource_access_rules: List[Dict] | None = None
    vnet_ids: List[str] | None = None
    ip_rules: List[IPv4NetworkOrAddressAnnotation] | None = None
    
    
    @field_validator('default_action', mode='before')
    @classmethod
    def capitalize_string(cls, default_action: str | None) -> str:
        """
        文字列をCamelCaseへ変換するバリデータ
        :param default_action: 文字列
        :return: CamelCaseへ変換された文字列
        """
        if default_action is None:
            return None
        
        to_camel_case_str = ['logging', 'metrics', 'azureservices', None]
        lower_default_action = default_action.lower()
        if ' ' in lower_default_action:
            # ' 'を削除
            lower_default_action = lower_default_action.replace(' ', '')
        if lower_default_action not in to_camel_case_str:
            # Noneでもto_camel_case_str内の値でもない場合はデフォルト値を使用する
            return 'AzureServices'
        # CamelCaseの文字列をreturn
        if lower_default_action is 'logging':
            return 'Logging'
        elif lower_default_action is 'metrics':
            return 'Metrics'
        elif lower_default_action is 'azureservices':
            return 'AzureServices'


    @field_validator('resource_access_rules', mode='before')
    @classmethod
    def validate_resource_access_rules_key(cls, resource_access_rules: List | None) -> List | None:
        """
        resource_access_rulesの各Dict内に以下のキーが存在することを確認する。
        tenant_id: str
        resource_id: str
        """
        if resource_access_rules is None:
            return None
        for resource_access_rule in resource_access_rules:
            tenant_id = resource_access_rule.get('tenant_id', None)
            resource_id = resource_access_rule.get('resource_id', None)
            keys = resource_access_rule.keys()
            if tenant_id is None or resource_id is None or len(keys) == 2:
                raise ValueError(f"""
                                ValueError:{resource_access_rules}は不正な値です。
                                resource_access_rulesにはtenant_id, resource_idのみを含むDictのリストを代入してください。
                                """)
        return resource_access_rules


    def _append_action_to_vnet_id(self) -> List | None:
        """
        vnet_idに対してactionを追加する。
        現行ホワイトリスト方式のため、追加されたIDのactionをallowに設定する。
        Return：
            formatted_vnet_ids: List | None
            [
                {
                    'virtual_network_resource_id': vnet_id,
                    'action': 'Allow'
                }
            ]
        """
        if self.vnet_ids is None:
            return None
        formatted_vnet_rules = []
        for vnet_id in self.vnet_ids:
            formatted_vnet_rules.append({'action': 'Allow', 'virtual_network_resource_id': vnet_id})
        return formatted_vnet_rules


    def _append_action_to_ip_rule(self) -> List | None:
        """
        ip_rulesに対してactionを追加する。
        現行Allowというactionしか存在しないため、追加されたPrefixのactionsをallowに設定設定する。
        Return:
            formatted_ip_rules: List | None
                以下の形に整形する。
                [
                    {
                        'action': 'Allow',
                        'ip_address_or_range': 許可するIP
                    }
                ]
        """
        if self.ip_rules is None:
            return None
        formatted_ip_rules = []
        for ip_rule in self.ip_rules:
            formatted_ip_rules.append({'action':'Allow','ip_address_or_range': ip_rule})
        return formatted_ip_rules


    def gen_params(self) -> dict:
        """
        Network RuleのDictを生成する
        TODO: 未作成
        """
        return {
            'default_action': self.default_action,
            'bypass': self.bypass,
            'resource_access_rules': self.resource_access_rules,
            'virtual_network_rules': self._append_action_to_vnet_id(),
            'ip_rules': self._append_action_to_ip_rule()
        }
