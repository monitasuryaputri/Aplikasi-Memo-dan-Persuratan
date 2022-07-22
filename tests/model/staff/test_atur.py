import pytest
import atur
from google.cloud import datastore

from tests.model.staff import STAFF_KIND, Staff

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
def staff(id, nama, email, no_hp, jabatan, picture):
    return [{"id" : id,
             "nama" : nama,
             "email" : email,
             "no_hp" : no_hp,
             "jabatan" : jabatan,
             "picture" : picture            
            }]

@pytest.fixture
def staff_baru():
    return {"nama" : "Pilar Al Hafist",            
            "email" : "pilar@mhs.unsyiah.ac.id",
            "no_hp" : "08995078669",
            "jabatan" : "5731076903272448",
            "picture" : "https://lh3.googleusercontent.com/a-/AOh14GiNrXYHezO1PbGCDMaH3J3vUM0D2N_9jFUhUV4UkQ=s96-c"
            }

def test_tambah(nama, email, no_hp, jabatan):
    assert atur.tambah(nama, email, no_hp, jabatan) == [{"nama" : "Annisa Surya Putri",
                                                         "email" : "anisasptri@gmail.com",
                                                         "no_hp" : "082265443325",
                                                         "jabatan" : "5731076903272448",
                                                         "picture" : "TIDAK ADA INFORMASI"}]

def test_daftar(staff):
    assert atur.daftar() == [{"id" : 5636212517765120,                            
                              "nama" : "Annisa Surya Putri",
                              "email" : "anisasptri@gmail.com",
                              "no_hp" : "082265443325",
                              "jabatan" : "5731076903272448",
                              "picture" : "https://lh3.googleusercontent.com/a-/AOh14GiNrXYHezO1PbGCDMaH3J3vUM0D2N_9jFUhUV4UkQ=s96-c"
                            }]
    
    assert atur.daftar() == staff

def test_cari(id, staff):
    assert atur.cari(id) == staff

def test_cari_email(email, staff):
    assert atur.cari_email(email) == staff

def test_ubah(id, staff_baru):
    assert atur.ubah(id, staff_baru) == [{"id" : 5636212517765120,
                                          "nama" : "Pilar Al Hafist",                                          
                                          "email" : "pilar@mhs.unsyiah.ac.id",
                                          "no_hp" : "08995078669",
                                          "jabatan" : "5731076903272448",
                                          "picture" : "https://lh3.googleusercontent.com/a-/AOh14GiNrXYHezO1PbGCDMaH3J3vUM0D2N_9jFUhUV4UkQ=s96-c"}]