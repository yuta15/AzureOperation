from ipaddress import IPv4Network, AddressValueError, NetmaskValueError

from typing import Annotated
from pydantic import PlainValidator


def ipv4_network_validator(ip_network: str) -> str:
    """ipv4 network アドレスを検証する為の関数"""
    try:
        network_address = IPv4Network(ip_network)
    except AddressValueError as e:
        raise ValueError(f"Invalid IPv4 address: {ip_network}") from e
    except NetmaskValueError as e:
        raise ValueError(f"Invalid IPv4 netmask: {ip_network}") from e
    else:
        return str(network_address)

IPv4NetworkAnnotation = Annotated[str, PlainValidator(ipv4_network_validator)]