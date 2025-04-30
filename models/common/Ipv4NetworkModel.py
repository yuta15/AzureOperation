from ipaddress import IPv4Network, AddressValueError, NetmaskValueError

from pydantic import BaseModel, field_validator


class Ipv4NetworkModel(BaseModel):
    """
    IPv4 NetworkをValidateするモデル。
    IPv4アドレスとして適切な値となっていることをvalidateする
    なお、受ける値はホストアドレスではなく、Networkアドレスとする。
    """
    ip_network: str
    
    @field_validator
    @classmethod
    def validate_ip_network(cls, ip_network: str) -> str:
        """
        適切なIPv4Networkアドレスか検証を行う。
        サブネットの最小サブネットマスクが/29であることからmaskが/29以上の場合はValueError
        Args:
            ip_network: str
                ex)"192.168.1.0/24", "10.0.0.0/8"
        Exception:
            ValueError
        return:
            validated_ip_network: str
        """
        try:
            validated_ip_network = IPv4Network(ip_network)
            if validated_ip_network.prefixlen < 29:
                raise ValueError(f'Network: {ip_network} is an invalid value. Network address must be /29 or higher.')
        except AddressValueError as e:
            raise e
        except NetmaskValueError as e:
            raise e
        except ValueError as e:
            raise e
        return str(validated_ip_network)
        