import pytest
from pydantic import ValidationError
from azure.mgmt.resource.resources.models import ResourceGroup

from models.resource.ResourceGroupModel import ResourceGroupModel


def test_resource_group_model_success(load_test_input_data):
    """
    test_resource_group_modelのテスト関数
    デフォルトではsample/parameters.jsonのデータとdefault_test_dataの両方をテスト用として使用可能。
    外部データからインスタンス化が可能であること、gen_params()関数のリターンが想定通りであることを確認する。
    """
    # 最初のデータのみ使用
    test_data = load_test_input_data.get('resource_group')[0]
    
    rg_params = ResourceGroupModel(**test_data)
    assert rg_params.resource_group_name == test_data.get('resource_group_name')
    assert rg_params.location == test_data.get('location')
    assert rg_params.tags == test_data.get('tags')
    assert rg_params.gen_params() == {
        'resource_group_name': test_data.get('resource_group_name'),
        'parameters': {
            'location': test_data.get('location'),
            'tags': test_data.get('tags'),
        }
    }


def test_resource_group_model_success_to_instance(load_test_input_data):
    """
    test_resource_group_modelのテスト関数
    ResourceGroupのインスタンスが作成可能かを確認する。
    name以外は設定される想定
    """
    # 最初のデータのみ使用
    test_data = load_test_input_data['resource_group'][0]
    rg_params = ResourceGroupModel(**test_data).gen_params()
    rg_instanced_parmas = ResourceGroup(**rg_params['parameters'])
    assert test_data['location'] == rg_instanced_parmas.location
    assert test_data['tags'] == rg_instanced_parmas.tags


@pytest.mark.parametrize(
    'resource_group_name',
    [
        '',
        '12',
        'a'*65,
        '-1234', 
        '_DNoe'
    ]
)
def test_resource_group_model_failuer(load_test_input_data, resource_group_name):
    """
    test_resource_group_modelのテスト関数
    resource_group_nameの値によってValidationErrorが発生することを確認する。
    """
    # 最初の要素のみ使用
    test_data = load_test_input_data.get('resource_group')[0]
    test_data['resource_group_name'] = resource_group_name
    with pytest.raises(ValidationError) as e:
        ResourceGroupModel(**test_data)
