import pytest

from pydantic import ValidationError

from models.network.SubnetModel import SubnetModel


def test_subnet_model_success(load_test_input_data):
    test_data = load_test_input_data['virtual_network'][0]['subnets'][0]
    subnet = SubnetModel(**test_data)
    assert subnet.name == test_data['name']
    assert subnet.address_prefix == test_data['address_prefix']


@pytest.mark.parametrize("name", [
    '12',
    'a' * 81,
    '_test',
    'test 1'
    ]
)
def test_subnet_model_failure_by_name(load_test_input_data, name):
    test_data = load_test_input_data['virtual_network'][0]['subnets'][0]
    test_data['name'] = name
    with pytest.raises(ValidationError):
        SubnetModel(**test_data)


@pytest.mark.parametrize("address_prefix", [
    '192.168.1.12',
    '192.168.1.1.0/28',
    '192.168.1.0/30',
    ['192.168.1.0/24', '10.0.0.0/16']
    ]
)
def test_subnet_model_failure_by_name(load_test_input_data, address_prefix):
    test_data = load_test_input_data['virtual_network'][0]['subnets'][0]
    test_data['address_prefix'] = address_prefix
    with pytest.raises(ValidationError):
        SubnetModel(**test_data)


