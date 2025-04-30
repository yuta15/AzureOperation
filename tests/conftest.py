import sys
import os

import pytest


@pytest.fixture(scope='session', autouse=True)
def set_sys_path():
    """
    sys.pathにroot_dirを追加する.
    テスト実行時と終了時にそれぞれ実行する。
    """
    parent_dir = os.path.abspath(os.path.pardir)
    sys.path.insert(0, parent_dir)
    yield
    sys.path.pop(0)