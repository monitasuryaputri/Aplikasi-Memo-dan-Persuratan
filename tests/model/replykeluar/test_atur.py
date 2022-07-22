

import pytest
import atur
from google.cloud import datastore

from tests.model.replykeluar import Replykeluar, REPLYKELUAR_KIND

@pytest.fixture
def id():
    return 6264989119676416
@pytest.fixture    
def komenkeluar():
    return "5139920456777728"
@pytest.fixture    
def suratkeluar():
    return "5657791876300800"
@pytest.fixture    
def penindak():
    return 5659336621686784
@pytest.fixture    
def isi_replykeluar():
    return "oke"
@pytest.fixture    
def tgl_replykeluar():
    return 1641549519.706046

@pytest.fixture    
def penindak_komentar():
    return {'email': 'pilar@mhs.unsyiah.ac.id',
            'id': 5659336621686784,
            'jabatan': '5731076903272448',
            'nama': 'Pilar',
            'nama_jabatan': 'koordinator divisi umum',
            'no_hp': '08995078669',
            'picture': 'https://lh3.googleusercontent.com/a/AATXAJyq2X3DHAr-GHpV5l4skxGpyM8EEoPbBewDAi64=s96-c'}

@pytest.fixture
def replykeluar(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar):
    return [{'id': id, 
            'komenkeluar': komenkeluar, 
            'suratkeluar': suratkeluar, 
            'penindak': penindak, 
            'isi_replykeluar': isi_replykeluar, 
            'tgl_replykeluar': tgl_replykeluar}]

@pytest.fixture
def replykeluarpenindak(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar, penindak_komentar):
    return [{"id" : id,            
            "komenkeluar" : komenkeluar,
            "suratkeluar" : suratkeluar,
            "penindak" : penindak,
            "isi_replykeluar" : isi_replykeluar,
            "tgl_replykeluar" : tgl_replykeluar,
            "penindak_komentar" : penindak_komentar}]


def test_tambah(komenkeluar, penindak, suratkeluar, isi_replykeluar):
    assert atur.tambah(komenkeluar, penindak, suratkeluar, isi_replykeluar) == [{'komenkeluar': '5139920456777728', 
                                                                                'suratkeluar': '5657791876300800', 
                                                                                'penindak': 5659336621686784, 
                                                                                'isi_replykeluar': "oke", 
                                                                                'tgl_replykeluar': 1641549519.706046 
                                                                                }]

def test_daftar(replykeluar):
    assert atur.daftar() == [{'id': 6264989119676416,
                            'komenkeluar': '5139920456777728', 
                            'suratkeluar': '5657791876300800', 
                            'penindak': 5659336621686784, 
                            'isi_replykeluar': "oke", 
                            'tgl_replykeluar': 1641549519.706046 
                            }]
    
    assert atur.daftar() == replykeluar

def test_cari(id, replykeluar):
    assert atur.cari(id) == replykeluar

def test_caribysuratkeluar(suratkeluar, replykeluarpenindak):
    assert atur.caribysuratkeluar(suratkeluar) == replykeluarpenindak
