"""
Model Untuk jabatan

Property jabatan:
+ id   : integer
+ nama : string

"""
import pytest
import model

@pytest.fixture
def id():
    return 5077688091934720
@pytest.fixture    
def nama():
    return "kepala upt laboratorium"

@pytest.fixture
def dictionary(id, nama):
    return {'id': id, 'nama': nama}

def test_init(id, nama):
    init = model.Jabatan(id, nama)
    assert init.id == 5077688091934720
    assert init.nama == "kepala upt laboratorium"


def test_dictionary(id, nama, dictionary):
    assert model.Jabatan.ke_dictionary(model.Jabatan(id, nama)) == {'id': 5077688091934720, 'nama': 'kepala upt laboratorium'}
    assert type(model.Jabatan.ke_dictionary(model.Jabatan(id, nama))) == dict
    assert model.Jabatan.ke_dictionary(model.Jabatan(id, nama)) == dictionary