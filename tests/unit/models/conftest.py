import json
import os

import pytest


@pytest.fixture(scope='function')
def load_test_input_data():
    """
    モデル化に使用するデータを読み込む関数
    関数毎に読み込みを行う
    """
    path = os.path.dirname(__file__)
    with open(f'{path}/test_parameters.json', mode='r') as f:
        content = json.loads(f.read())
        yield content
