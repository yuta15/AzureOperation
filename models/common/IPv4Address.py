from ipaddress import IPv4Address, AddressValueError, NetmaskValueError

from pydantic import BaseModel, field_validator


class Ipv4NetworkModel(BaseModel):
    """
    IPv4 addressをValidateするモデル。
    IPv4アドレスとして適切な値となっていることをvalidateする
    なお、受ける値はホストアドレスではなく、addressアドレスとする。
    """
    ip_address: str

    @field_validator
    @classmethod
    def validate_ip_address(cls, ip_address: str) -> str:
        """
        適切なIPv4addressアドレスか検証を行う。
        Args:
            ip_address: str
                ex)"192.168.1.1"
        Exception:
            ValueError
        return:
            validated_ip_address: str
        """
        try:
            validated_ip_address = IPv4Address(ip_address)
        except AddressValueError as e:
            raise e
        except NetmaskValueError as e:
            raise e
        except ValueError as e:
            raise e
        return str(validated_ip_address)
        