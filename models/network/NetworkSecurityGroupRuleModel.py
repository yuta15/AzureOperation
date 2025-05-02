from typing import Literal, List
from pydantic import BaseModel, Field

from annotations.IPv4AddressAnnotation import IPv4AddressAnnotation
from annotations.IPv4NetworkAnnotation import IPv4NetworkAnnotation
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
        source_address_prefix: Literal['*'] | IPv4NetworkAnnotation | IPv4AddressAnnotation | None = None
            送信元アドレス。"*", or IPaddress, IPNetworkが指定可能
            Ex) すべての通信を許可する場合: "*"
                特定のNWを許可する場合: "192.168.1.0/24"
                特定のアドレスを許可する場合: "192.168.1.1"
        source_address_prefixes: List[IPv4NetworkAnnotation | IPv4AddressAnnotation ] | None = None
            送信元アドレスのリスト。IPaddress, IPNetworkが指定可能。特定かつ複数の送信元を制御する際に使用する。
            Ex) 特定のNWを許可する場合: ["192.168.1.0/24", "192.168.1.1"]
        destination_address_prefix: Literal['*'] | IPv4NetworkAnnotation | IPv4AddressAnnotation | None = None
            宛先アドレス。"*", or IPaddress, IPNetworkが指定可能
            Ex) すべての通信を許可する場合: "*"
                特定のNWを許可する場合: "192.168.1.0/24"
                特定のアドレスを許可する場合: "192.168.1.1"
        destination_address_prefixes: List[IPv4NetworkAnnotation | IPv4AddressAnnotation ] | None = None
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
    """
    name: str = Field(min_length=3, max_length=80, pattern='^[a-zA-Z0-9][a-zA-Z0-9_.-]*[a-zA-Z0-9_]$')
    priority: int = Field(min=100, max=65000)
    direction: Literal['Inbound', 'Outbound']
    protocol: Literal['Tcp', 'Udp', 'Icmp', 'Esp', '*', 'Ah']
    access: Literal['Allow', 'Deny']
    description: str | None = Field(max_length=150, default=None)
    source_address_prefix: Literal['*', ""] | IPv4NetworkAnnotation | IPv4AddressAnnotation | None = None
    source_address_prefixes: List[IPv4NetworkAnnotation | IPv4AddressAnnotation ] | None = None
    destination_address_prefix: Literal['*', ""] | IPv4NetworkAnnotation | IPv4AddressAnnotation | None = None
    destination_address_prefixes: List[IPv4NetworkAnnotation | IPv4AddressAnnotation ] | None = None
    source_port_range: Literal['*', ""] | PortAnnotation | None = None
    source_port_ranges: List[PortAnnotation] | None = None
    destination_port_range: Literal['*', ""] | PortAnnotation | None = None
    destination_port_ranges: List[PortAnnotation] | None = None

