
import pytest
import atur
from google.cloud import datastore

from tests.model.superadmin import SUPERADMIN_KIND, Superadmin

@pytest.fixture
def id():
    return 6012551879983104
@pytest.fixture    
def email():
    return "monita.sp@mhs.unsyiah.ac.id"

@pytest.fixture
def superadmin(id, email):
    return [{"id" : id,            
            "email" : email}]

def test_tambah(email):
    assert atur.tambah(email) == [{"email" : "monita.sp@mhs.unsyiah.ac.id"}]

def test_daftar(superadmin):
    assert atur.daftar() == [{"id" : 6012551879983104,                            
                            "email" : "monita.sp@mhs.unsyiah.ac.id"
                            }]
    
    assert atur.daftar() == superadmin

def test_cari(id, superadmin):
    assert atur.cari(id) == superadmin

def test_cari_email(email, superadmin):
    assert atur.cari_email(email) == superadmin