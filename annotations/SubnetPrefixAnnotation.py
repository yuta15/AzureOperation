from ipaddress import IPv4Network, AddressValueError, NetmaskValueError

from typing import Annotated
from pydantic import PlainValidator

from annotations.IPv4NetworkAnnotation import ipv4_network_validator


def subnet_prefix_validator(ip_network: str) -> str:
    ip_network = ipv4_network_validator(ip_network=ip_network)
    prefix_len = int(ip_network.split('/')[-1])
    if prefix_len > 29:
        raise ValueError(f"Invalid subnet prefix: {ip_network}")
    return ip_network

Prefix29Annotation = Annotated[str, PlainValidator(subnet_prefix_validator)]