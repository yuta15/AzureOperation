from ipaddress import IPv4Network

import pytest

from models.network.NetworkSecurityGroupRuleModel import NetworkSecurityGroupRuleModel


def test_nsg_success(load_test_input_data):
    """
    NSGルールモデルの正常系テスト
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    assert nsg_rule_params.name == nsg_rule['name']
    assert nsg_rule_params.priority == nsg_rule['priority']
    assert nsg_rule_params.direction == nsg_rule['direction']
    assert nsg_rule_params.protocol == nsg_rule['protocol']
    assert nsg_rule_params.description == nsg_rule['description']
    assert nsg_rule_params.description == nsg_rule['description']
    # port、addressのテストは別途実施


@pytest.mark.parametrize(
    'protocol',
    [
        'tcp',
        'udp',
        'icmp',
        'esp',
        '*',
        'ah',
    ]
)
def test_nsg_rule_success_check_protocol(load_test_input_data, protocol):
    """
    NSGモデルの正常系テスト
    protocolが正常にcapitalizeされvalidationされるかを確認する
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['protocol'] = protocol
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    assert nsg_rule_params.protocol == protocol.capitalize()


@pytest.mark.parametrize(
    'access',
    [
        'allow',
        'deny',
    ]
)
def test_nsg_rule_success_check_access(load_test_input_data, access):
    """
    NSGモデルの正常系テスト
    accessが正常にcapitalizeされvalidationされるかを確認する
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['access'] = access
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    assert nsg_rule_params.access == access.capitalize()


@pytest.mark.parametrize(
    'direction',
    [
        'inbound',
        'outbound',
    ]
)
def test_nsg_rule_success_check_direction(load_test_input_data, direction):
    """
    NSGモデルの正常系テスト
    directionが正常にcapitalizeされvalidationされるかを確認する
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['direction'] = direction
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    assert nsg_rule_params.direction == direction.capitalize()


@pytest.mark.parametrize(
    ['source_address_prefix', 'destination_address_prefix'],
    [
        ['*', '*'],
        ['', ''],
        ['192.168.1.1', '192.168.1.2'],
        ['192.168.1.0/24', '192.168.1.0/24']
    ]
)
def test_nsg_rule_success_check_address(load_test_input_data, source_address_prefix, destination_address_prefix):
    """
    NSGモデルの正常系テスト
    source_address_prefix', 'destination_address_prefixが正常にvalidationされるかを確認する
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_address_prefix'] = source_address_prefix
    nsg_rule['destination_address_prefix'] = destination_address_prefix
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    
    assert nsg_rule_params.source_address_prefix == source_address_prefix
    assert nsg_rule_params.destination_address_prefix == destination_address_prefix


@pytest.mark.parametrize(
    ['source_address_prefixes', 'destination_address_prefixes'],
    [
        [
            ['192.168.1.1','192.168.1.2'], ['192.168.1.3','192.168.1.4']
        ],
        [
            ['192.168.1.0/24','192.168.2.0/24'], ['192.168.3.0/24','192.168.4.0/24']
        ],
        [
            ['192.168.1.0/29','192.168.2.1/32'], ['192.168.3.128/25','192.168.4.0/30']
        ],
    ]
)
def test_nsg_rule_success_check_addresses(load_test_input_data, source_address_prefixes, destination_address_prefixes):
    """
    NSGモデルの正常系テスト
    source/dst_addressesが正常にvalidationされるかを確認する
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_address_prefixes'] = source_address_prefixes
    nsg_rule['destination_address_prefixes'] = destination_address_prefixes
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    
    assert nsg_rule_params.source_address_prefixes == source_address_prefixes
    assert nsg_rule_params.destination_address_prefixes == destination_address_prefixes


@pytest.mark.parametrize(
    ['source_port_range', 'destination_port_range'],
    [
        ['*', '*'],
        ['', ''],
        ['1', '65535'],
        ['1-65535', '1-65535'],
    ]
)
def test_nsg_rule_success_check_port(load_test_input_data, source_port_range, destination_port_range):
    """
    NSGモデルの正常系テスト
    source/dst_port_rangeが正常にvalidationされるかを確認する
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_port_range'] = source_port_range
    nsg_rule['destination_port_range'] = destination_port_range
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    
    assert nsg_rule_params.source_port_range == source_port_range
    assert nsg_rule_params.destination_port_range == destination_port_range


@pytest.mark.parametrize(
    ['source_port_ranges', 'destination_port_ranges'],
    [
        [
            ['443', '80'],
            ['443', '80'],
        ],
        [
            ['1-100', '443'],
            ['1-100', '443'],
        ],
        [
            ['1-100', '150-200', '443'],
            ['1-100', '150-200', '443'],
        ],
    ]
)
def test_nsg_rule_success_check_ports(load_test_input_data, source_port_ranges, destination_port_ranges):
    """
    NSGモデルの正常系テスト
    source/dst_port_rangeが正常にvalidationされるかを確認する
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_port_ranges'] = source_port_ranges
    nsg_rule['destination_port_ranges'] = destination_port_ranges
    nsg_rule_params = NetworkSecurityGroupRuleModel(**nsg_rule)
    
    assert nsg_rule_params.source_port_ranges == source_port_ranges
    assert nsg_rule_params.destination_port_ranges == destination_port_ranges




"""------------異常系テスト------------------"""


@pytest.mark.parametrize(
    'name',
    [
        '12',
        'a'*81,
        '-test',
        'test-'
    ]
)
def test_nsg_rule_failure_by_name(load_test_input_data, name):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['name'] = name
    with pytest.raises(ValueError):
        NetworkSecurityGroupRuleModel(**nsg_rule)


@pytest.mark.parametrize(
    'priority',
    [
        99,
        65001,
    ]
)
def test_nsg_rule_failure_by_priority(load_test_input_data, priority):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['priority'] = priority
    with pytest.raises(ValueError):
        NetworkSecurityGroupRuleModel(**nsg_rule)


@pytest.mark.parametrize(
    'direction',
    [
        'In',
        'Out',
    ]
)
def test_nsg_rule_failure_by_direction(load_test_input_data, direction):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['direction'] = direction
    with pytest.raises(ValueError):
        NetworkSecurityGroupRuleModel(**nsg_rule)


@pytest.mark.parametrize(
    ['source_address_prefix', 'destination_address_prefix'],
    [
        [' ',' '],
        ['192.168.1.0.0/24','192.300.2.0/24'],
        ['192.168.1.1/24','192.168.2.2/24'],
    ]
)
def test_nsg_rule_failure_by_address(load_test_input_data, source_address_prefix, destination_address_prefix):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_address_prefix'] = source_address_prefix
    nsg_rule['destination_address_prefix'] = destination_address_prefix
    with pytest.raises(ValueError):
        NetworkSecurityGroupRuleModel(**nsg_rule)


@pytest.mark.parametrize(
    ['source_address_prefixes', 'destination_address_prefixes'],
    [
        [['*','*'], ['*','*']],
        [['192.168.1.0.0/24','192.300.2.0/24'],['192.168.1.0.0/24','192.300.2.0/24']],
        [['192.168.1.1/24','192.168.2.2/24'],['192.168.1.1/24','192.168.2.2/24']]
    ]
)
def test_nsg_rule_failure_by_addresses(load_test_input_data, source_address_prefixes, destination_address_prefixes):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_address_prefixes'] = source_address_prefixes
    nsg_rule['destination_address_prefixes'] = destination_address_prefixes
    with pytest.raises(ValueError):
        NetworkSecurityGroupRuleModel(**nsg_rule)


@pytest.mark.parametrize(
    ['source_port_range', 'destination_port_range'],
    [
        ['0', '0'],
        [0, 0],
        ['65536', '65536'],
        ['1-100-200', '1-100-200'],
        ['1-100', '1-100-200'],
        ['1-100', 0],
        ['1-100', -443],
        ['1-100', 1.22],
    ]
)
def test_nsg_rule_failure_by_port(load_test_input_data, source_port_range, destination_port_range):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_port_range'] = source_port_range
    nsg_rule['destination_port_range'] = destination_port_range
    with pytest.raises(ValueError):
        NetworkSecurityGroupRuleModel(**nsg_rule)


@pytest.mark.parametrize(
    ['source_port_ranges', 'destination_port_ranges'],
    [
        [['0', '0'], ['0', '0']],
        [[0, 0],[0, 0]],
        [['65536', '65536'], ['65536', '65536']],
        [['443', '1002-65536'],['443', '1002-65535']],
        [['1-100', '1-100-200'], ['443', '1002-65535']],
        [[80, 20, 22], [0, 100, 200]],
        [['1-100', -443],[80]],
        [['1-100', 1.22],[443]]
    ]
)
def test_nsg_rule_failure_by_ports(load_test_input_data, source_port_ranges, destination_port_ranges):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    nsg_rule = load_test_input_data['network_security_group'][0]['security_rules'][0]
    nsg_rule['source_port_ranges'] = source_port_ranges
    nsg_rule['destination_port_ranges'] = destination_port_ranges
    with pytest.raises(ValueError):
        NetworkSecurityGroupRuleModel(**nsg_rule)


