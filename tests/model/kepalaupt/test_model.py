"""
Model Untuk Kepalaupt

Property Kepalaupt:
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
    return 5105697184284672
@pytest.fixture    
def nama():
    return "Monita Surya Putri"
@pytest.fixture    
def email():
    return "monitasuryaputrii@gmail.com"
@pytest.fixture    
def no_hp():
    return "08116822256"
@pytest.fixture    
def jabatan():
    return "5077688091934720"
@pytest.fixture    
def picture():
    return "https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c"

@pytest.fixture
def dictionary(id, nama, email, no_hp, jabatan, picture):
    return {'id': id, 'nama': nama, 'email': email, 'no_hp': no_hp, 'jabatan': jabatan, 'picture': picture}

def test_init(id, nama, email, no_hp, jabatan, picture):
    init = model.Kepalaupt(id, nama, email, no_hp, jabatan, picture)
    assert init.id == 5105697184284672
    assert init.nama == "Monita Surya Putri"
    assert init.email == "monitasuryaputrii@gmail.com"
    assert init.no_hp == "08116822256"
    assert init.jabatan == "5077688091934720"
    assert init.picture == "https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c"


def test_dictionary(id, nama, email, no_hp, jabatan, picture, dictionary):
    assert model.Kepalaupt.ke_dictionary(model.Kepalaupt(id, nama, email, no_hp, jabatan, picture)) == {'id': 5105697184284672, 'nama': 'Monita Surya Putri', 'email': 'monitasuryaputrii@gmail.com', 'no_hp': '08116822256', 'jabatan': '5077688091934720', 'picture': 'https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c'}
    assert type(model.Kepalaupt.ke_dictionary(model.Kepalaupt(id, nama, email, no_hp, jabatan, picture))) == dict
    assert model.Kepalaupt.ke_dictionary(model.Kepalaupt(id, nama, email, no_hp, jabatan, picture)) == dictionary