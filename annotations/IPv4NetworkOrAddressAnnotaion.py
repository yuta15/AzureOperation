from typing import Annotated
from pydantic import PlainValidator

from annotations.IPv4AddressAnnotation import ipv4_address_validator
from annotations.IPv4NetworkAnnotation import ipv4_network_validator


def ipv4_network_or_address_validator(ipv4_network_or_address: str) -> str:
    """
    ipv4 network or address を検証する為の関数
    CIDR表記のネットワークアドレスもしくはIPアドレスを検証する。
    ipv4_address_validatorとipv4_network_validatorのwrapper関数
    """
    # まずはIPv4Networkとして検証
    if '/' in ipv4_network_or_address:
        # CIDR表記の場合はIPv4Networkとして検証
        ipv4_network_validator(ipv4_network_or_address)
    else:
        # CIDR表記でない場合はIPv4Addressとして検証
        ipv4_address_validator(ipv4_network_or_address)
    return ipv4_network_or_address


IPv4NetworkOrAddressAnnotation = Annotated[str, PlainValidator(ipv4_network_or_address_validator)]
