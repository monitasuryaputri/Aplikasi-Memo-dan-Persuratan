
import pytest
import atur
from google.cloud import datastore

from tests.model.admin import ADMIN_KIND, Admin

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
def admin(id, nama, email, no_hp, jabatan, picture):
    return [{"id" : id,
             "nama" : nama,
             "email" : email,
             "no_hp" : no_hp,
             "jabatan" : jabatan,
             "picture" : picture            
            }]

@pytest.fixture
def admin_baru():
    return {"nama" : "Pilar Al Hafist",            
            "email" : "pilar@mhs.unsyiah.ac.id",
            "no_hp" : "08995078669",
            "jabatan" : "5630815723585536",
            "picture" : "https://lh3.googleusercontent.com/a/AATXAJwgSAduYV8vTxSL5CA7UOxv_DI2zvcTZVvYCeHZ=s96-c"
            }

def test_tambah(nama, email, no_hp, jabatan):
    assert atur.tambah(nama, email, no_hp, jabatan) == [{"nama" : "Monita Surya Putri",
                                                         "email" : "monitasurya@gmail.com",
                                                         "no_hp" : "123456789",
                                                         "jabatan" : "5630815723585536",
                                                         "picture" : "TIDAK ADA INFORMASI"}]

def test_daftar(admin):
    assert atur.daftar() == [{"id" : 6221596528214016,                            
                              "nama" : "Monita Surya Putri",
                              "email" : "monitasurya@gmail.com",
                              "no_hp" : "123456789",
                              "jabatan" : "5630815723585536",
                              "picture" : "https://lh3.googleusercontent.com/a/AATXAJwgSAduYV8vTxSL5CA7UOxv_DI2zvcTZVvYCeHZ=s96-c"
                            }]
    
    assert atur.daftar() == admin

def test_cari(id, admin):
    assert atur.cari(id) == admin

def test_cari_email(email, admin):
    assert atur.cari_email(email) == admin

def test_ubah(id, admin_baru):
    assert atur.ubah(id, admin_baru) == [{"id" : 6221596528214016,
                                          "nama" : "Pilar Al Hafist",                                          
                                          "email" : "pilar@mhs.unsyiah.ac.id",
                                          "no_hp" : "08995078669",
                                          "jabatan" : "5630815723585536",
                                          "picture" : "https://lh3.googleusercontent.com/a/AATXAJwgSAduYV8vTxSL5CA7UOxv_DI2zvcTZVvYCeHZ=s96-c"}]