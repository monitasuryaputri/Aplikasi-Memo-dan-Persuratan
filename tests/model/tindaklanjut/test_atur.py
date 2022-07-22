

import pytest
import atur
from google.cloud import datastore

from tests.model.tindaklanjut import Tindaklanjut, TINDAKLANJUT_KIND

@pytest.fixture
def id():
    return 5644357755469824
@pytest.fixture    
def suratmasuk():
    return "5729017198018560"
@pytest.fixture    
def penugas():
    return 5652730257342464
@pytest.fixture    
def penanggungjawab():
    return "5731076903272448"
@pytest.fixture    
def tugas():
    return "sediakan ruangan"
@pytest.fixture    
def tgl_tugas():
    return 1643794758.564006
@pytest.fixture    
def tgl_selesai():
    return ""
@pytest.fixture    
def followup():
    return "[]"
@pytest.fixture    
def tenggatwaktu():
    return "2022-02-04"
@pytest.fixture    
def check():
    return "0"
@pytest.fixture    
def notif():
    return "no"

@pytest.fixture
def tindaklanjut(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif):
    return [{'id': id,
            'suratmasuk': suratmasuk, 
            'penugas': penugas, 
            'penanggungjawab': penanggungjawab, 
            'tugas': tugas, 
            'tgl_tugas': tgl_tugas,
            'tgl_selesai': tgl_selesai,
            'followup': followup,
            'tenggatwaktu': tenggatwaktu,
            'check': check,
            'notif': notif
            }]

@pytest.fixture
def cari_tindaklanjut(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_selesai, followup, tenggatwaktu, check, notif):
    return [{'id': id,
            'suratmasuk': suratmasuk, 
            'penugas': penugas, 
            'penanggungjawab': penanggungjawab, 
            'tugas': tugas, 
            'tgl_tugas': '02-02-2022',
            'tgl_selesai': tgl_selesai,
            'followup': followup,
            'tenggatwaktu': tenggatwaktu,
            'check': check,
            'notif': notif
            }]

@pytest.fixture
def suratmasuk_tindaklanjut(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_selesai, followup, tenggatwaktu, check, notif):
    return [{'id': id,
            'suratmasuk': suratmasuk, 
            'penugas': penugas, 
            'penanggungjawab': 'koordinator divisi umum', 
            'tugas': tugas, 
            'tgl_tugas': '02-02-2022',
            'tgl_selesai': tgl_selesai,
            'followup': followup,
            'tenggatwaktu': tenggatwaktu,
            'check': check,
            'notif': "lewat",
            'penugas_tindaklanjut' : {'email': 'zeffry444@gmail.com',
                                    'id': 5652730257342464,
                                    'jabatan': '6268441468076032',
                                    'nama': 'Zeffry Syahputra',
                                    'nama_jabatan': 'analis divisi laboratorium geoteknik',
                                    'no_hp': '085282989182',
                                    'picture': 'https://lh3.googleusercontent.com/a-/AOh14GhJU3JAOOoIfGM6LRTVPT_3j33GGdA4Bv9ttUDheA=s96-c'}
            }]

@pytest.fixture
def tindaklanjut_baru():
    return {'tgl_selesai': 1649754247.885468,
            'followup': '["5118035283148800", "5629545755443200"]',
            'check': "1"
            }

def test_tambah(suratmasuk, penugas, tugas, penanggungjawab, tenggatwaktu):
    assert atur.tambah(suratmasuk, penugas, tugas, penanggungjawab, tenggatwaktu) == [{'suratmasuk': '5729017198018560', 
                                                                                'penugas': 5652730257342464, 
                                                                                'penanggungjawab': '5731076903272448', 
                                                                                'tugas': 'sediakan ruangan', 
                                                                                'tgl_tugas': 1643794758.564006,
                                                                                'tgl_selesai': "",
                                                                                'followup': "[]",
                                                                                'tenggatwaktu': "2022-02-04",
                                                                                'check': "0",
                                                                                'notif': "no"
                                                                                }]

def test_daftar(tindaklanjut):
    assert atur.daftar() == [{'id': 5644357755469824,
                            'suratmasuk': '5729017198018560', 
                            'penugas': 5652730257342464, 
                            'penanggungjawab': '5731076903272448', 
                            'tugas': 'sediakan ruangan', 
                            'tgl_tugas': 1643794758.564006,
                            'tgl_selesai': "",
                            'followup': "[]",
                            'tenggatwaktu': "2022-02-04",
                            'check': "0",
                            'notif': "no"
                            }]
    
    assert atur.daftar() == tindaklanjut


def test_cari(id, cari_tindaklanjut):
    assert atur.cari(id) == [{'id': 5644357755469824,
                            'suratmasuk': '5729017198018560', 
                            'penugas': 5652730257342464, 
                            'penanggungjawab': '5731076903272448', 
                            'tugas': 'sediakan ruangan', 
                            'tgl_tugas': '02-02-2022',
                            'tgl_selesai': "",
                            'followup': "[]",
                            'tenggatwaktu': "2022-02-04",
                            'check': "0",
                            'notif': "no"
                            }]

    assert atur.cari(id) == cari_tindaklanjut

def test_caribysuratmasuk(suratmasuk, suratmasuk_tindaklanjut):
    assert atur.caribysuratmasuk(suratmasuk) == [{'id': 5644357755469824,
                                                    'suratmasuk': '5729017198018560', 
                                                    'penugas': 5652730257342464, 
                                                    'penanggungjawab': 'koordinator divisi umum', 
                                                    'tugas': 'sediakan ruangan', 
                                                    'tgl_tugas': '02-02-2022',
                                                    'tgl_selesai': "",
                                                    'followup': "[]",
                                                    'tenggatwaktu': "2022-02-04",
                                                    'check': "0",
                                                    'notif': "lewat",
                                                    'penugas_tindaklanjut' : {'email': 'zeffry444@gmail.com',
                                                                            'id': 5652730257342464,
                                                                            'jabatan': '6268441468076032',
                                                                            'nama': 'Zeffry Syahputra',
                                                                            'nama_jabatan': 'analis divisi laboratorium geoteknik',
                                                                            'no_hp': '085282989182',
                                                                            'picture': 'https://lh3.googleusercontent.com/a-/AOh14GhJU3JAOOoIfGM6LRTVPT_3j33GGdA4Bv9ttUDheA=s96-c'}
                                                    }]                          

    assert atur.caribysuratmasuk(suratmasuk) == suratmasuk_tindaklanjut

def test_update(id, tindaklanjut_baru):
    assert atur.update(id, tindaklanjut_baru) == [{'id': 5644357755469824,
                                                'suratmasuk': '5729017198018560', 
                                                'penugas': 5652730257342464, 
                                                'penanggungjawab': '5731076903272448', 
                                                'tugas': 'sediakan ruangan', 
                                                'tgl_tugas': 1643794758.564006,
                                                'tgl_selesai': 1649754247.885468,
                                                'followup': '["5118035283148800", "5629545755443200"]',
                                                'tenggatwaktu': "2022-02-04",
                                                'check': "1",
                                                'notif': "no"
                                                }]