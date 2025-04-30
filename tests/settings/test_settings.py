import os
import sys

import pytest
from settings.settings import Setting




@pytest.mark.parametrize(
    [
        'env_file_name',
        'environment'
    ],
    [
        pytest.param(
            '.dev_test',
            'DEV'
        ),
        pytest.param(
            '.prd_test',
            'PRD'
        )
    ]
)
def test_setting(env_file_name, environment):
    """
    Settingのテスト
    環境分離ができること, 指定した.envファイルを問題無く読み込めることを確認する。
    """

    env_file_path = f'{os.path.dirname(__file__)}/{env_file_name}'
    setting = Setting(ENV=environment, _env_file=env_file_path)

    with open(env_file_path, mode='r') as f:
        data = [d.rstrip('\n').split('=')[1] for d in f.readlines()]
    assert setting.AZURE_CLIENT_ID == data[0]
    assert setting.AZURE_CLIENT_ID == data[1]
    assert setting.AZURE_CLIENT_ID == data[2]