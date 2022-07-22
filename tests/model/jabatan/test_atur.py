""" Controller untuk model jabatan

Deklarasi method:

tambah      :untuk membuat entitas baru
daftar      :untuk select semua entitas yg terdaftar pada datastore
cari_nama  :untuk cari/filter data entitas berdasarkan property nama

"""

import pytest
import atur
from google.cloud import datastore

from tests.model.jabatan import Jabatan, JABATAN_KIND

@pytest.fixture
def id():
    return 5077688091934720
@pytest.fixture    
def nama():
    return "kepala upt laboratorium"
@pytest.fixture
def jabatan(id, nama):
    return [{"id" : id,            
            "nama" : nama}]

def test_tambah(nama):
    assert atur.tambah(nama) == [{"nama" : "kepala upt laboratorium"}]

def test_daftar(jabatan):
    assert atur.daftar() == [{"id" : 5077688091934720,                            
                            "nama" : "kepala upt laboratorium"
                            }]
    
    assert atur.daftar() == jabatan

def test_disposisi(jabatan):
    assert atur.disposisi() == [{"id" : 5077688091934720,                            
                                "nama" : "kepala upt laboratorium"
                                }]
    
    assert atur.daftar() == jabatan

def test_cari(id, jabatan):
    assert atur.cari(id) == jabatan

def test_cari_nama(nama, jabatan):
    assert atur.cari_nama(nama) == jabatan