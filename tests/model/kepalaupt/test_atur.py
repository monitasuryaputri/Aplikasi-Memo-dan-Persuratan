import pytest
import atur
from google.cloud import datastore

from tests.model.kepalaupt import KEPALAUPT_KIND, Kepalaupt

@pytest.fixture
def id():
    return 5105697184284672
@pytest.fixture    
def nama():
    return "Monita Surya"
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
def kepalaupt(id, nama, email, no_hp, jabatan, picture):
    return [{"id" : id,
             "nama" : nama,
             "email" : email,
             "no_hp" : no_hp,
             "jabatan" : jabatan,
             "picture" : picture            
            }]

@pytest.fixture
def kepalaupt_baru():
    return {"nama" : "Pilar Al Hafist",            
            "email" : "pilar@mhs.unsyiah.ac.id",
            "no_hp" : "08995078669",
            "jabatan" : "5077688091934720",
            "picture" : "https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c"
            }

def test_tambah(nama, email, no_hp, jabatan):
    assert atur.tambah(nama, email, no_hp, jabatan) == [{"nama" : "Monita Surya",
                                                         "email" : "monitasuryaputrii@gmail.com",
                                                         "no_hp" : "08116822256",
                                                         "jabatan" : "5077688091934720",
                                                         "picture" : "TIDAK ADA INFORMASI"}]

def test_daftar(kepalaupt):
    assert atur.daftar() == [{"id" : 5105697184284672,                            
                              "nama" : "Monita Surya",
                              "email" : "monitasuryaputrii@gmail.com",
                              "no_hp" : "08116822256",
                              "jabatan" : "5077688091934720",
                              "picture" : "https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c"
                            }]
    
    assert atur.daftar() == kepalaupt

def test_cari(id, kepalaupt):
    assert atur.cari(id) == kepalaupt

def test_cari_email(email, kepalaupt):
    assert atur.cari_email(email) == kepalaupt

def test_ubah(id, kepalaupt_baru):
    assert atur.ubah(id, kepalaupt_baru) == [{"id" : 5105697184284672,
                                          "nama" : "Pilar Al Hafist",                                          
                                          "email" : "pilar@mhs.unsyiah.ac.id",
                                          "no_hp" : "08995078669",
                                          "jabatan" : "5077688091934720",
                                          "picture" : "https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c"}]