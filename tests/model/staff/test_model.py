"""
Model Untuk Staff

Property Staff:
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
    return 5636212517765120
@pytest.fixture    
def nama():
    return "Annisa Surya Putri"
@pytest.fixture    
def email():
    return "anisasptri@gmail.com"
@pytest.fixture    
def no_hp():
    return "082265443325"
@pytest.fixture    
def jabatan():
    return "5731076903272448"
@pytest.fixture    
def picture():
    return "https://lh3.googleusercontent.com/a-/AOh14GiNrXYHezO1PbGCDMaH3J3vUM0D2N_9jFUhUV4UkQ=s96-c"

@pytest.fixture
def dictionary(id, nama, email, no_hp, jabatan, picture):
    return {'id': id, 'nama': nama, 'email': email, 'no_hp': no_hp, 'jabatan': jabatan, 'picture': picture}

def test_init(id, nama, email, no_hp, jabatan, picture):
    init = model.Staff(id, nama, email, no_hp, jabatan, picture)
    assert init.id == 5636212517765120
    assert init.nama == "Annisa Surya Putri"
    assert init.email == "anisasptri@gmail.com"
    assert init.no_hp == "082265443325"
    assert init.jabatan == "5731076903272448"
    assert init.picture == "https://lh3.googleusercontent.com/a-/AOh14GiNrXYHezO1PbGCDMaH3J3vUM0D2N_9jFUhUV4UkQ=s96-c"


def test_dictionary(id, nama, email, no_hp, jabatan, picture, dictionary):
    assert model.Staff.ke_dictionary(model.Staff(id, nama, email, no_hp, jabatan, picture)) == {'id': 5636212517765120, 'nama': 'Annisa Surya Putri', 'email': 'anisasptri@gmail.com', 'no_hp': '082265443325', 'jabatan': '5731076903272448', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14GiNrXYHezO1PbGCDMaH3J3vUM0D2N_9jFUhUV4UkQ=s96-c'}
    assert type(model.Staff.ke_dictionary(model.Staff(id, nama, email, no_hp, jabatan, picture))) == dict
    assert model.Staff.ke_dictionary(model.Staff(id, nama, email, no_hp, jabatan, picture)) == dictionary