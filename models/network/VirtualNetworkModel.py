from typing import List
from pydantic import Field

from annotations.IPv4AddressAnnotation import IPv4AddressAnnotation
from annotations.SubnetPrefixAnnotation import Prefix29Annotation

from models.resource.ResourceGroupModel import ResourceGroupModel
from models.network.SubnetModel import SubnetModel


class VirtualNetworkModel(ResourceGroupModel):
    """
    VNET用のモデル
    Attributes:
        location: str | None = None
        tags: dict | None = None
        resource_group_name: str | None = None
        virtual_network_name: str = Field(min_length=3, max_length=80, pattern='^[a-zA-Z0-9][a-zA-Z0-9\-_\.]*[a-zA-Z0-9\-_]$')
        address_prefixes: list[Ipv4NetworkModel]
        dns_servers: List[IPv4Address] | None = None
        subnets: List[SubnetModel] | None = None
    """
    virtual_network_name: str = Field(min_length=3, max_length=80, pattern='^[a-zA-Z0-9][a-zA-Z0-9\-_\.]*[a-zA-Z0-9\-_]$')
    address_prefixes: list[Prefix29Annotation]
    dns_servers: List[IPv4AddressAnnotation] | None = None
    subnets: List[SubnetModel] | None = None

    def gen_params(self) -> dict:
        """
        VNET作成時のDICTを生成する。
        """
        return {
            'resource_group_name': self.resource_group_name,
            'virtual_network_name': self.virtual_network_name,
            'parameters': {
                'tags': self.tags,
                'location': self.location,
                'address_space': self._gen_params_address_prefixes(),
                'dhcp_options':self._gen_params_dns_servers(),
                'subnets': self._gen_params_subnets()
            }
        }


    def _gen_params_dns_servers(self) -> dict | None: 
        """dns_server設定の値を生成する関数"""
        if self.dns_servers is None:
            return None
        return {'dns_servers': [str(ip) for ip in self.dns_servers]}


    def _gen_params_address_prefixes(self) -> dict:
        """address_prefixesの値を生成する関数"""
        return {'address_prefixes': [str(ip) for ip in self.address_prefixes]}


    def _gen_params_subnets(self) -> List[dict] | None:
        """subnetのパラメータを作成するための関数"""
        if self.subnets is None:
            return None
        return [subnet.gen_params() for subnet in self.subnets]