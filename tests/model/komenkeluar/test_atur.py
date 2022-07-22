

import pytest
import atur
from google.cloud import datastore

from tests.model.komenkeluar import Komenkeluar, KOMENKELUAR_KIND

@pytest.fixture
def id():
    return 5076466173739008
@pytest.fixture    
def suratkeluar():
    return "5671441819238400"
@pytest.fixture    
def penindak():
    return 6548254560878592
@pytest.fixture    
def isi_komenkeluar():
    return "komentar"
@pytest.fixture    
def tgl_komenkeluar():
    return 1643882750.899903
@pytest.fixture    
def file_komenkeluar():
    return [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}]
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
def komenkeluar(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply):
    return [{"id" : id,            
            "suratkeluar" : suratkeluar,
            "penindak" : penindak,
            "isi_komenkeluar" : isi_komenkeluar,
            "tgl_komenkeluar" : tgl_komenkeluar,
            "file_komenkeluar" : file_komenkeluar,
            "reply" : reply}]

@pytest.fixture
def komenkeluarpenindak(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply, penindak_komentar):
    return [{"id" : id,            
            "suratkeluar" : suratkeluar,
            "penindak" : penindak,
            "isi_komenkeluar" : isi_komenkeluar,
            "tgl_komenkeluar" : tgl_komenkeluar,
            "file_komenkeluar" : file_komenkeluar,
            "reply" : reply,
            "penindak_komentar" : penindak_komentar}]

@pytest.fixture
def komenkeluar_baru():
    return {"suratkeluar" : "5671441819238400",
            "penindak" : 6548254560878592,
            "isi_komenkeluar" : "komentar",
            "tgl_komenkeluar" : 1643882750.899903,
            "file_komenkeluar" : [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}],
            "reply" : '["6264989119676416"]'
            }

def test_tambah(suratkeluar, penindak, isi_komenkeluar, file_komenkeluar):
    assert atur.tambah(suratkeluar, penindak, isi_komenkeluar, file_komenkeluar) == [{"suratkeluar" : "5671441819238400",
                                                                                      "penindak" : 6548254560878592,
                                                                                      "isi_komenkeluar" : "komentar",
                                                                                      "tgl_komenkeluar" : 1643882750.899903,
                                                                                      "file_komenkeluar" : [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}],
                                                                                      'reply': "[]"
                                                                                    }]

def test_daftar(komenkeluar):
    assert atur.daftar() == [{'id': 5076466173739008, 
                              'suratkeluar': '5671441819238400', 
                              'penindak': 6548254560878592, 
                              'isi_komenkeluar': "komentar", 
                              'tgl_komenkeluar': 1643882750.899903, 
                              'file_komenkeluar': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}],
                              'reply': "[]"}]
    
    assert atur.daftar() == komenkeluar

def test_cari(id, komenkeluar):
    assert atur.cari(id) == komenkeluar

def test_caribykomenkeluar(id, suratkeluar, komenkeluar):
    assert atur.caribykomenkeluar(suratkeluar, id) == komenkeluar

def test_caribysuratkeluar(suratkeluar, komenkeluarpenindak):
    assert atur.caribysuratkeluar(suratkeluar) == komenkeluarpenindak

def test_update(id, komenkeluar_baru):
    assert atur.update(id, komenkeluar_baru) == [{"id" : 5076466173739008,
                                                  "suratkeluar" : "5671441819238400",
                                                  "penindak" : 6548254560878592,
                                                  "isi_komenkeluar" : "komentar",
                                                  "tgl_komenkeluar" : 1643882750.899903,
                                                  "file_komenkeluar" : [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}],
                                                  "reply" : '["6264989119676416"]'
                                                }]