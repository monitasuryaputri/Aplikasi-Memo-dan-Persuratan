"""
Model Untuk Admin

Property Admin:
+ id : integer
+ nama : string
+ email : string
+ no_hp : string
+ jabatan : string
+ picture : string

"""
import pytest
import model

@pytest.fixture
def id():
    return 6221596528214016
@pytest.fixture    
def nama():
    return "Monita Surya Putri"
@pytest.fixture    
def email():
    return "monitasurya@gmail.com"
@pytest.fixture    
def no_hp():
    return "123456789"
@pytest.fixture    
def jabatan():
    return "5630815723585536"
@pytest.fixture    
def picture():
    return "https://lh3.googleusercontent.com/a/AATXAJwgSAduYV8vTxSL5CA7UOxv_DI2zvcTZVvYCeHZ=s96-c"

@pytest.fixture
def dictionary(id, nama, email, no_hp, jabatan, picture):
    return {'id': id, 'nama': nama, 'email': email, 'no_hp': no_hp, 'jabatan': jabatan, 'picture': picture}

def test_init(id, nama, email, no_hp, jabatan, picture):
    init = model.Admin(id, nama, email, no_hp, jabatan, picture)
    assert init.id == 6221596528214016
    assert init.nama == "Monita Surya Putri"
    assert init.email == "monitasurya@gmail.com"
    assert init.no_hp == "123456789"
    assert init.jabatan == "5630815723585536"
    assert init.picture == "https://lh3.googleusercontent.com/a/AATXAJwgSAduYV8vTxSL5CA7UOxv_DI2zvcTZVvYCeHZ=s96-c"


def test_dictionary(id, nama, email, no_hp, jabatan, picture, dictionary):
    assert model.Admin.ke_dictionary(model.Admin(id, nama, email, no_hp, jabatan, picture)) == {'id': 6221596528214016, 'nama': 'Monita Surya Putri', 'email': 'monitasurya@gmail.com', 'no_hp': '123456789', 'jabatan': '5630815723585536', 'picture': 'https://lh3.googleusercontent.com/a/AATXAJwgSAduYV8vTxSL5CA7UOxv_DI2zvcTZVvYCeHZ=s96-c'}
    assert type(model.Admin.ke_dictionary(model.Admin(id, nama, email, no_hp, jabatan, picture))) == dict
    assert model.Admin.ke_dictionary(model.Admin(id, nama, email, no_hp, jabatan, picture)) == dictionary