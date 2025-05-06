import pytest

from models.network.NetworkSecurityGroupModel import NetworkSecurityGroupModel


def test_nsg_model_success(load_test_input_data):
    """
    NSGモデルの正常系テスト
    """
    # 正常系のテストデータを取得
    test_data = load_test_input_data['network_security_group'][0]

    # モデルのインスタンスを作成
    nsg_model = NetworkSecurityGroupModel(**test_data)

    # モデルの属性が正しいか確認
    assert nsg_model.resource_group_name == test_data['resource_group_name']
    assert nsg_model.network_security_group_name == test_data['network_security_group_name']
    assert nsg_model.gen_params() == {
        'resource_group_name': test_data['resource_group_name'],
        'network_security_group_name': test_data['network_security_group_name'],
        'parameters': {
            'location': test_data['location'],
            'tags': test_data['tags'],
            'security_rules': test_data['security_rules']
        }
    }
    


@pytest.mark.parametrize(
    'network_security_group_name',
    [
        '1',
        'a'*65,
        '-test',
        'test-'
    ]
)
def test_nsg_failure_by_name(load_test_input_data, network_security_group_name):
    """
    NSGモデルの異常系テスト
    NSG名が不正な場合のチェック
    """
    # 正常系のテストデータを取得
    test_data = load_test_input_data['network_security_group'][0]
    test_data['network_security_group_name'] = network_security_group_name
    # モデルのインスタンスを作成
    with pytest.raises(ValueError):
        NetworkSecurityGroupModel(**test_data)