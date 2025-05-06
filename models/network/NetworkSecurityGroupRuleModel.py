from typing import Literal, List
from pydantic import BaseModel, Field, field_validator

from annotations.IPv4NetworkOrAddressAnnotaion import IPv4NetworkOrAddressAnnotation
from annotations.PortAnnotation import PortAnnotation

class NetworkSecurityGroupRuleModel(BaseModel):
    """
    Attributes
        name: str = Field(min_length=3, max_length=80, pattern='^[a-zA-Z0-9][a-zA-Z0-9_.-]*[a-zA-Z0-9_]$')
            NSGルールの名前
        priority: int = Field(min=100, max=65000)
            NSGルールのプライオリティ
        direction: Literal['Inbound', 'Outbound']
            NSGルールの通信方向. InboundとOutboundを指定可能
        protocol: Literal['Tcp', 'Udp', 'Icmp', 'Esp', '*', 'Ah']
            NSGルールのプロトコル
        access: Literal['Allow', 'Deny']
            NSGルールをAllow or Deny設定
        description: str | None= Field(max_length=150, default=None)
            NSGルールの説明
        source_address_prefix: Literal['*'] | IPv4NetworkOrAddressAnnotation | None = None
            送信元アドレス。"*", or IPaddress, IPNetworkが指定可能
            Ex) すべての通信を許可する場合: "*"
                特定のNWを許可する場合: "192.168.1.0/24"
                特定のアドレスを許可する場合: "192.168.1.1"
        source_address_prefixes: List[IPv4NetworkOrAddressAnnotation ] | None = None
            送信元アドレスのリスト。IPaddress, IPNetworkが指定可能。特定かつ複数の送信元を制御する際に使用する。
            Ex) 特定のNWを許可する場合: ["192.168.1.0/24", "192.168.1.1"]
        destination_address_prefix: Literal['*'] | IPv4NetworkOrAddressAnnotation | None = None
            宛先アドレス。"*", or IPaddress, IPNetworkが指定可能
            Ex) すべての通信を許可する場合: "*"
                特定のNWを許可する場合: "192.168.1.0/24"
                特定のアドレスを許可する場合: "192.168.1.1"
        destination_address_prefixes: List[IPv4NetworkOrAddressAnnotation ] | None = None
            宛先アドレスのリスト。IPaddress, IPNetworkが指定可能。特定かつ複数の送信元を制御する際に使用する。
            Ex) 特定のNWを許可する場合: ["192.168.1.0/24", "192.168.1.1"]
        source_port_range: Literal['*'] | PortAnnotation | None = None
            port番号. "*"もしくは"80", "80-443"等を指定可能
            Ex) すべてのポートを許可: "*"
                特定のポートを許可: "80"
                特定の範囲のポートを許可: "80-443"
        source_port_ranges: List[PortAnnotation] | None = None
            port番号. 複数のポートを指定する場合にしよう
            Ex) 特定かつ複数のポートを許可: ["80", "443]
                特定のポートとレンジのポートを許可: ["80", "1000-10002"]
        destination_port_range: Literal['*'] | PortAnnotation | None = None
            port番号. "*"もしくは"80", "80-443"等を指定可能
            Ex) すべてのポートを許可: "*"
                特定のポートを許可: "80"
                特定の範囲のポートを許可: "80-443"
        destination_port_ranges: List[PortAnnotation] | None = None
            port番号. 複数のポートを指定する場合にしよう
            Ex) 特定かつ複数のポートを許可: ["80", "443]
                特定のポートとレンジのポートを許可: ["80", "1000-10002"]
                
    TODO:
        - source_address_prefix or source_address_prefixes, destination_address_prefix or destination_address_prefixes
            のいずれか一つが指定されていることを確認するバリデータを追加する
            現状、source_address_prefixとsource_address_prefixesが同時に指定可能となるがその場合の動作は定義されておらず、APIの仕様に依存している状態

        - source_port_range, destination_port_range, source_port_ranges, destination_port_ranges
            のいずれか一つが指定されていることを確認するバリデータを追加する
    """
    name: str = Field(min_length=3, max_length=80, pattern='^[a-zA-Z0-9][a-zA-Z0-9_.-]*[a-zA-Z0-9_]$')
    priority: int = Field(ge=100, le=65000)
    direction: Literal['Inbound', 'Outbound']
    protocol: Literal['Tcp', 'Udp', 'Icmp', 'Esp', '*', 'Ah']
    access: Literal['Allow', 'Deny']
    description: str | None = Field(max_length=150, default=None)
    source_address_prefix: Literal['*', ""] | IPv4NetworkOrAddressAnnotation | None = None
    source_address_prefixes: List[IPv4NetworkOrAddressAnnotation ] | None = None
    destination_address_prefix: Literal['*', ""] | IPv4NetworkOrAddressAnnotation | None = None
    destination_address_prefixes: List[IPv4NetworkOrAddressAnnotation ] | None = None
    source_port_range: Literal['*', ""] | PortAnnotation | None = None
    source_port_ranges: List[PortAnnotation] | None = None
    destination_port_range: Literal['*', ""] | PortAnnotation | None = None
    destination_port_ranges: List[PortAnnotation] | None = None


    @field_validator('direction', 'protocol', 'access', mode='before')
    @classmethod
    def capitalize_string(cls, value: str) -> str:
        """
        文字列を大文字に変換するバリデータ
        :param cls: クラス
        :param value: 文字列
        :return: 大文字に変換された文字列
        """
        return value.capitalize()