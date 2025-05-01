from ipaddress import IPv4Address, AddressValueError, NetmaskValueError

from typing import Annotated
from pydantic import PlainValidator


def ipv4_address_validator(ip_address: str) -> str:
    """ipv4 network アドレスを検証する為の関数"""
    try:
        address = IPv4Address(ip_address)
    except AddressValueError as e:
        raise(e)
    except NetmaskValueError as e:
        raise(e)
    else:
        return str(address)

IPv4AddressAnnotation = Annotated[str, PlainValidator(ipv4_address_validator)]