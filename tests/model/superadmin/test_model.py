"""
Model Untuk superadmin

Property superadmin:
+ id    : integer
+ email : string

"""
import pytest
import model

@pytest.fixture
def id():
    return 6012551879983104
@pytest.fixture    
def email():
    return "monita.sp@mhs.unsyiah.ac.id"

@pytest.fixture
def dictionary(id, email):
    return {'id': id, 'email': email}

def test_init(id, email):
    init = model.Superadmin(id, email)
    assert init.id == 6012551879983104
    assert init.email == "monita.sp@mhs.unsyiah.ac.id"


def test_dictionary(id, email, dictionary):
    assert model.Superadmin.ke_dictionary(model.Superadmin(id, email)) == {'id': 6012551879983104, 'email': 'monita.sp@mhs.unsyiah.ac.id'}
    assert type(model.Superadmin.ke_dictionary(model.Superadmin(id, email))) == dict
    assert model.Superadmin.ke_dictionary(model.Superadmin(id, email)) == dictionary