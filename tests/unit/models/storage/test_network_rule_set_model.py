import copy

import pytest
from pydantic import ValidationError

from models.storage.NetworkRuleSetModel import NetworkRuleSetModel


def test_nw_rule_set_model_success(load_test_input_data):
    """
    NetworkRuleSetModelをテストするための関数。
    """
    test_data = copy.deepcopy(load_test_input_data['storage_account'][0]['network_rule_set'])
    test_params = NetworkRuleSetModel(**test_data).gen_params()
    result_ip_rules = [{'action':'Allow', 'ip_address_or_range': ip_rule} for ip_rule in test_data['ip_rules']]
    result_vnet_rules = [{'action': 'Allow', 'virtual_network_resource_id': vnet_id} for vnet_id in test_data['vnet_ids']]
    assert test_data['default_action'] == test_params['default_action']
    assert test_data['bypass'] == test_params['bypass']
    assert test_data['resource_access_rules'] == test_params['resource_access_rules']
    assert result_ip_rules == test_params['ip_rules']
    assert result_vnet_rules == test_params['virtual_network_rules']


@pytest.mark.parametrize(
    'default_action',
    [
        'allow',
        'deny',
        'Deny',
    ]
)
def test_nw_rule_set_model_success_chage_default_action(load_test_input_data, default_action):
    """
    すべてのdefault_actionのパターンでもエラーが出ないこと。
    値が適切な物に変換されていること
    """
    test_data = copy.deepcopy(load_test_input_data)
    test_data['default_action'] = default_action
    result_default_action = default_action.capitalize()
    test_params = NetworkRuleSetModel(**test_data)
    assert result_default_action == test_params.default_action


@pytest.mark.parametrize(
    'bypass',
    [
        'Logging',
        'Metrics',
        'AzureServices',
        None,
        'logging',
        'metrics',
        'azure services',
    ]
)
def test_nw_rule_set_model_success_chage_bypass(load_test_input_data, bypass):
    """
    すべてのbypassのパターンでもエラーが出ないこと。
    値が適切な物に変換されていること
    """
    test_data = copy.deepcopy(load_test_input_data)
    test_data['bypass'] = bypass
    test_params = NetworkRuleSetModel(**test_data)
    assert test_params.bypass in ['Logging', 'Metrics', 'AzureServices', None]


@pytest.mark.parametrize(
    'default_action',
    [
        'allowss',
        'denysd',
        'a llow',
        'd eny',
        'a$llow'
        'de\ny'
    ]
)
# 非正常系テスト
def test_nw_rule_set_model_failure_by_default_action(load_test_input_data, default_action):
    """
    default_actionの異常系テスト
    """
    test_data = copy.deepcopy(load_test_input_data)
    test_data['default_action'] = default_action
    with pytest.raises(ValidationError) as e:
        test_params = NetworkRuleSetModel(**test_data)


@pytest.mark.parametrize(
    'bypass',
    [
        'loggingg',
        'metricss',
        'azureservsices',
        'l$ogging',
        'Azure-Services',
        'Azure_Services'
    ]
)
def test_nw_rule_set_model_failure_bypass(load_test_input_data, bypass):
    """
    bypassの異常系テスト
    """
    test_data = copy.deepcopy(load_test_input_data)
    test_data['bypass'] = bypass
    with pytest.raises(ValidationError) as e:
        test_params = NetworkRuleSetModel(**test_data)


@pytest.mark.parametrize(
    'ip_rules',
    [
        ['10.01.01.0/24'],
        ['10.1.1.0/230'],
        ['10.1.1.256/32'],
        ['10.01.01.0/1'],
    ]
)
def test_nw_rule_set_model_failure_by_ip_rules(load_test_input_data, ip_rules):
    """
    ip_rulesの異常系テスト
    """
    test_data = copy.deepcopy(load_test_input_data)
    test_data['ip_rules'] = ip_rules
    with pytest.raises(ValidationError) as e:
        test_params = NetworkRuleSetModel(**test_data)