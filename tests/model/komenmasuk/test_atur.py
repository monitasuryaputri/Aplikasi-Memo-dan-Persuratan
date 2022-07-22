

import pytest
import atur
from google.cloud import datastore

from tests.model.komenmasuk import Komenmasuk, KOMENMASUK_KIND

@pytest.fixture
def id():
    return 5645987863330816
@pytest.fixture    
def suratmasuk():
    return "5183015185547264"
@pytest.fixture    
def penindak():
    return 6548254560878592
@pytest.fixture    
def isi_komenmasuk():
    return "komntar"
@pytest.fixture    
def tgl_komenmasuk():
    return 1643603716.223075
@pytest.fixture    
def reply():
    return "[]"

@pytest.fixture    
def penindak_komentar():
    return {'email': 'alhafistp@gmail.com',
            'id': 6548254560878592,
            'jabatan': '5077688091934720',
            'nama': 'Pilar Al Hafist',
            'nama_jabatan': 'kepala upt laboratorium',
            'no_hp': '08995078669',
            'picture': 'https://lh3.googleusercontent.com/a-/AOh14GiFJ8onDed6Conrsp8NkWmMMS851Pmh0pSG7wUH=s96-c'}

@pytest.fixture
def komenmasuk(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply):
    return [{"id" : id,            
            "suratmasuk" : suratmasuk,
            "penindak" : penindak,
            "isi_komenmasuk" : isi_komenmasuk,
            "tgl_komenmasuk" : tgl_komenmasuk,
            "reply" : reply}]

@pytest.fixture
def komenmasukpenindak(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply, penindak_komentar):
    return [{"id" : id,            
            "suratmasuk" : suratmasuk,
            "penindak" : penindak,
            "isi_komenmasuk" : isi_komenmasuk,
            "tgl_komenmasuk" : tgl_komenmasuk,
            "reply" : reply,
            "penindak_komentar" : penindak_komentar}]

@pytest.fixture
def komenmasuk_baru():
    return {"suratmasuk" : "5183015185547264",
            "penindak" : 6548254560878592,
            "isi_komenmasuk" : "komntar",
            "tgl_komenmasuk" : 1643603716.223075,
            "reply" : '["6264989119676416"]'
            }

def test_tambah(suratmasuk, penindak, isi_komenmasuk):
    assert atur.tambah(suratmasuk, penindak, isi_komenmasuk) == [{"suratmasuk" : "5183015185547264",
                                                                "penindak" : 6548254560878592,
                                                                "isi_komenmasuk" : "komntar",
                                                                "tgl_komenmasuk" : 1643603716.223075,
                                                                'reply': "[]"
                                                                }]

def test_daftar(komenmasuk):
    assert atur.daftar() == [{'id': 5645987863330816, 
                              'suratmasuk': '5183015185547264', 
                              'penindak': 6548254560878592, 
                              'isi_komenmasuk': "komntar", 
                              'tgl_komenmasuk': 1643603716.223075, 
                              'reply': "[]"}]
    
    assert atur.daftar() == komenmasuk

def test_cari(id, komenmasuk):
    assert atur.cari(id) == komenmasuk

def test_caribykomenmasuk(id, suratmasuk, komenmasuk):
    assert atur.caribykomenmasuk(suratmasuk, id) == komenmasuk

def test_caribysuratmasuk(suratmasuk, komenmasukpenindak):
    assert atur.caribysuratmasuk(suratmasuk) == komenmasukpenindak

def test_update(id, komenmasuk_baru):
    assert atur.update(id, komenmasuk_baru) == [{"id" : 5645987863330816,
                                                  "suratmasuk" : "5183015185547264",
                                                  "penindak" : 6548254560878592,
                                                  "isi_komenmasuk" : "komntar",
                                                  "tgl_komenmasuk" : 1643603716.223075,
                                                  "reply" : '["6264989119676416"]'
                                                }]