import uuid

import pytest
from pydantic import ValidationError

from models.storage.ManagedIdModel import ManagedIdModel


def test_managed_id_model_success():
    """
    ManagedId用のモデルをテストする。
    """
    managed_id_type = 'UserAssigned'
    principal_id = uuid.uuid4()
    client_id = uuid.uuid4()
    managed_id = ManagedIdModel(type=managed_id_type, principal_id=principal_id, client_id=client_id)
    assert managed_id_type == managed_id.type
    assert principal_id == managed_id.principal_id
    assert client_id == managed_id.client_id
    assert managed_id.gen_params() == {
        'type': managed_id_type,
        'user_assigned_identities': {
            'principal_id': principal_id,
            'client_id': client_id
        }
    }


def test_managed_id_model_success_type_none():
    """
    ManagedId用のモデルをテストする。
    typeがNoneになったときの動作を検証する。
    """
    managed_id_type = None
    principal_id = uuid.uuid1()
    client_id = uuid.uuid1()
    managed_id = ManagedIdModel(type=managed_id_type, principal_id=principal_id, client_id=client_id)
    assert managed_id.type == None
    assert managed_id.principal_id == None
    assert managed_id.client_id == None
    assert managed_id.gen_params() == {
        'type': None,
        'user_assigned_identities': {
            'principal_id': None,
            'client_id': None
        }
    }


@pytest.mark.parametrize(
    'principal_id',
    [
        f'{uuid.uuid4()}1',
        None,
    ]
)
def test_managed_id_failed_principal_id(principal_id):
    """
    ManagedId用のモデルをテストする。
    principal_idのUUIDが不正な場合の動作をテスト
    """
    managed_id_type = 'UserAssigned'
    client_id = uuid.uuid4()
    with pytest.raises((ValidationError)):
        ManagedIdModel(
            type=managed_id_type, 
            principal_id=principal_id, 
            client_id=client_id
        )


@pytest.mark.parametrize(
    'client_id',
    [
        f'{uuid.uuid4()}1',
        None
    ]
)
def test_managed_id_failed_client_id(client_id):
    """
    ManagedId用のモデルをテストする。
    client_idのUUIDが不正な場合の動作をテスト
    """
    managed_id_type = 'UserAssigned'
    principal_id = uuid.uuid4()
    with pytest.raises((ValidationError)):
        ManagedIdModel(
            type=managed_id_type, 
            principal_id=principal_id, 
            client_id=client_id
        )
