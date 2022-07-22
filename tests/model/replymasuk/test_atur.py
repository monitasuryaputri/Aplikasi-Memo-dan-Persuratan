

import pytest
import atur
from google.cloud import datastore

from tests.model.replymasuk import Replymasuk, REPLYMASUK_KIND

@pytest.fixture
def id():
    return 5667711371706368
@pytest.fixture    
def komenmasuk():
    return "5205959873921024"
@pytest.fixture    
def suratmasuk():
    return "5677651805077504"
@pytest.fixture    
def penindak():
    return 6548254560878592
@pytest.fixture    
def isi_replymasuk():
    return "jangan sampai lewat deadline"
@pytest.fixture    
def tgl_replymasuk():
    return 1640699461.076582

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
def replymasuk(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk):
    return [{'id': id, 
            'komenmasuk': komenmasuk, 
            'suratmasuk': suratmasuk, 
            'penindak': penindak, 
            'isi_replymasuk': isi_replymasuk, 
            'tgl_replymasuk': tgl_replymasuk}]

@pytest.fixture
def replymasukpenindak(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk, penindak_komentar):
    return [{"id" : id,            
            "komenmasuk" : komenmasuk,
            "suratmasuk" : suratmasuk,
            "penindak" : penindak,
            "isi_replymasuk" : isi_replymasuk,
            "tgl_replymasuk" : tgl_replymasuk,
            "penindak_komentar" : penindak_komentar}]


def test_tambah(komenmasuk, penindak, suratmasuk, isi_replymasuk):
    assert atur.tambah(komenmasuk, penindak, suratmasuk, isi_replymasuk) == [{'komenmasuk': '5205959873921024', 
                                                                              'suratmasuk': '5677651805077504', 
                                                                              'penindak': 6548254560878592, 
                                                                              'isi_replymasuk': "jangan sampai lewat deadline", 
                                                                              'tgl_replymasuk': 1640699461.076582
                                                                            }]

def test_daftar(replymasuk):
    assert atur.daftar() == [{'id': 5667711371706368,
                            'komenmasuk': '5205959873921024', 
                            'suratmasuk': '5677651805077504', 
                            'penindak': 6548254560878592, 
                            'isi_replymasuk': "jangan sampai lewat deadline", 
                            'tgl_replymasuk': 1640699461.076582
                            }]
    
    assert atur.daftar() == replymasuk

def test_cari(id, replymasuk):
    assert atur.cari(id) == replymasuk

def test_caribysuratmasuk(suratmasuk, replymasukpenindak):
    assert atur.caribysuratmasuk(suratmasuk) == replymasukpenindak
