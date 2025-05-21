import copy

import pytest
from pydantic import ValidationError
from azure.mgmt.network.models import VirtualNetwork

from models.network.VirtualNetworkModel import VirtualNetworkModel
from models.network.VirtualNetworkModel import SubnetModel


def test_virtual_network_model_success(load_test_input_data):
    """
    test_virtual_network_modelのテスト関数
    デフォルトではsample/parameters.jsonのデータとdefault_test_dataの両方をテスト用として使用可能。
    外部データからインスタンス化が可能であること、gen_params()関数のリターンが想定通りであることを確認する。
    """
    # 最初のデータのみ使用
    test_data = copy.deepcopy(load_test_input_data['virtual_network'][0])
    print(test_data)

    vnet_params = VirtualNetworkModel(**test_data)
    
    # 属性の確認
    assert vnet_params.resource_group_name == test_data['resource_group_name']
    assert vnet_params.location == test_data['location']
    assert vnet_params.tags == test_data['tags']
    assert vnet_params.virtual_network_name == test_data['virtual_network_name']
    assert vnet_params.address_prefixes == test_data['address_prefixes']
    assert vnet_params.dns_servers == test_data['dns_servers']

    # 関数テスト
    dhcp_result = {'dns_servers': test_data['dns_servers']}
    address_prefixes_result = {'address_prefixes': test_data['address_prefixes']}
    subnets_result = [
        {
            'name': test_data['subnets'][0]['name'],
            'address_prefix': test_data['subnets'][0]['address_prefix'],
        }
    ]
    assert vnet_params._gen_params_dns_servers() == dhcp_result
    assert vnet_params._gen_params_address_prefixes() == address_prefixes_result
    assert vnet_params._gen_params_subnets() == subnets_result
    assert vnet_params.gen_params() == {
        'resource_group_name': test_data['resource_group_name'],
        'virtual_network_name': test_data['virtual_network_name'],
        'parameters': {
            'tags': test_data['tags'],
            'location': test_data['location'],
            'address_space': address_prefixes_result,
            'dhcp_options': dhcp_result,
            'subnets': subnets_result
        }
    }


def test_vnet_model_success_to_instance(load_test_input_data):
    """
    vnetの値をVirtualNetworkをインスタンス化させて問題なくインスタンス化できることを確認する。
    """
    # 最初のデータのみ使用
    test_data = copy.deepcopy(load_test_input_data['virtual_network'][0])
    vnet_params = VirtualNetworkModel(**test_data).gen_params()
    instanced_vnet_params = VirtualNetwork(**vnet_params['parameters'])
    assert test_data['tags'] == instanced_vnet_params.tags
    assert test_data['location'] == instanced_vnet_params.location
    assert {'address_prefixes': test_data['address_prefixes']} == instanced_vnet_params.address_space
    assert {'dns_servers': test_data['dns_servers']} == instanced_vnet_params.dhcp_options
    assert test_data['subnets'] == instanced_vnet_params.subnets


@pytest.mark.parametrize(
    'virtual_network_name',
    [
        '',
        '12',
        'a'*81,
        '-1234', 
        '_DNoe'
    ]
)
def test_virtual_network_model_failuere_by_vnet_name(load_test_input_data, virtual_network_name):
    """
    test_virtual_network_modelのテスト関数
    virtual_network_nameの値によってValidationErrorが発生することを確認する。
    そのほか
    """
    # 最初の要素のみ使用
    test_data = copy.deepcopy(load_test_input_data['virtual_network'][0])
    test_data['virtual_network_name'] = virtual_network_name
    with pytest.raises(ValidationError) as e:
        VirtualNetworkModel(**test_data)


@pytest.mark.parametrize(
    'address_prefixes',
    [
        [''],
        ['12'],
        ['10.10.10.1'],
        ['192.320.0.0/24'], 
        ['192.320.0.0.0/24'], 
        ['192.168.1.1/10']
    ]
)
def test_virtual_network_model_failuere_by_address_space(load_test_input_data, address_prefixes):
    """
    test_virtual_network_modelのテスト関数
    address_prefixesの値によってValidationErrorが発生することを確認する。
    
    """
    # 最初の要素のみ使用
    test_data = copy.deepcopy(load_test_input_data['virtual_network'][0])
    test_data['address_prefixes'] = address_prefixes
    with pytest.raises(ValidationError) as e:
        VirtualNetworkModel(**test_data)


@pytest.mark.parametrize(
    'dns_servers',
    [
        [''],
        ['192.168.1.0/24'],
        '192.168.1.1'
    ]
)
def test_virtual_network_model_failuere_by_dns_servers(load_test_input_data, dns_servers):
    """
    test_virtual_network_modelのテスト関数
    dns_serversの値によってValidationErrorが発生することを確認する。
    
    """
    # 最初の要素のみ使用
    test_data = copy.deepcopy(load_test_input_data['virtual_network'][0])
    test_data['dns_servers'] = dns_servers
    with pytest.raises(ValidationError):
        VirtualNetworkModel(**test_data)