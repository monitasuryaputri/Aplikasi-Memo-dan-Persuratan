

import pytest
import atur
from google.cloud import datastore

from tests.model.suratmasuk import Suratmasuk, SURATMASUK_KIND

@pytest.fixture
def id():
    return 5676043608260608
@pytest.fixture    
def nomor_surat():
    return "225/75/PL/2"
@pytest.fixture    
def tgl_surat():
    return "2022-04-12"
@pytest.fixture    
def asal_surat():
    return "Fakultas Teknik"
@pytest.fixture    
def hal():
    return "Perlengkapan"
@pytest.fixture    
def isi_ringkas():
    return "Peminjaman RUangan"
@pytest.fixture    
def dokumen():
    return [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}]
@pytest.fixture    
def disposisi():
    return ["5711226101301248"]
@pytest.fixture    
def id_jabatan():
    return 5711226101301248
@pytest.fixture    
def komentar():
    return '["5668647137705984"]'
@pytest.fixture    
def tindaklanjut():
    return "[]"
@pytest.fixture    
def dibaca():
    return ['5077688091934720']
@pytest.fixture    
def tgl_disposisi():
    return 1649615760
@pytest.fixture    
def status_tindaklanjut():
    return "-"
@pytest.fixture    
def reply():
    return "[]"

@pytest.fixture
def suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'asal_surat': asal_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': dokumen,
            'disposisi': disposisi,
            'komentar': komentar,
            'tindaklanjut': tindaklanjut,
            'dibaca': dibaca,
            'tgl_disposisi': tgl_disposisi,
            'status_tindaklanjut': status_tindaklanjut,
            'reply': reply
           }]

@pytest.fixture
def daftar_suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, status_tindaklanjut, reply):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'asal_surat': asal_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': dokumen,
            'disposisi': disposisi,
            'komentar': komentar,
            'tindaklanjut': tindaklanjut,
            'dibaca': dibaca,
            'tgl_disposisi': '11/04/2022',
            'status_tindaklanjut': status_tindaklanjut,
            'reply': reply,
            'tanggal_surat': '2022/04/11'
           }]

@pytest.fixture
def cari_suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'asal_surat': asal_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': dokumen,
            'disposisi': disposisi,
            'komentar': komentar,
            'tindaklanjut': tindaklanjut,
            'dibaca': dibaca,
            'tgl_disposisi': '11/04/2022 01:36',
            'status_tindaklanjut': status_tindaklanjut,
            'reply': reply
           }]

@pytest.fixture
def detail_suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'asal_surat': asal_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': dokumen,
            'disposisi': ['anggota divisi penjaminan mutu'],
            'komentar': komentar,
            'tindaklanjut': tindaklanjut,
            'dibaca': ['kepala upt laboratorium'],
            'tgl_disposisi': '11/04/2022 01:36',
            'status_tindaklanjut': status_tindaklanjut,
            'reply': reply
           }]

@pytest.fixture
def suratmasuk_baru():
    return {'disposisi': ["5711226101301248", "5077688091934720"],
            'komentar': '["5668647137705984", "5724539828830208"]',
            'dibaca': ["5077688091934720"]
            }

def test_tambah(nomor_surat, 
                tgl_surat, 
                asal_surat, 
                hal, 
                isi_ringkas, 
                dokumen, 
                disposisi):
    assert atur.tambah(nomor_surat, 
                       tgl_surat, 
                       asal_surat, 
                       hal, 
                       isi_ringkas, 
                       dokumen, 
                       disposisi) == [{ 'nomor_surat': '225/75/PL/2', 
                                        'tgl_surat': '2022-04-12', 
                                        'asal_surat': 'Fakultas Teknik', 
                                        'hal': 'Perlengkapan', 
                                        'isi_ringkas': 'Peminjaman RUangan',
                                        'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                                        'disposisi': ["5711226101301248"],
                                        'komentar': '[]',
                                        'tindaklanjut': "[]",
                                        'dibaca': [],
                                        'tgl_disposisi': 1649615760,
                                        'status_tindaklanjut': "-",
                                        'reply': "[]"
                                        }]

def test_daftar(daftar_suratmasuk):
    assert atur.daftar() == [{'id': 5676043608260608,
                            'nomor_surat': '225/75/PL/2', 
                            'tgl_surat': '2022-04-12', 
                            'asal_surat': 'Fakultas Teknik', 
                            'hal': 'Perlengkapan', 
                            'isi_ringkas': 'Peminjaman RUangan',
                            'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                            'disposisi': ["5711226101301248"],
                            'komentar': '["5668647137705984"]',
                            'tindaklanjut': "[]",
                            'dibaca': ['5077688091934720'],
                            'tgl_disposisi': '11/04/2022',
                            'status_tindaklanjut': "-",
                            'reply': "[]",
                            'tanggal_surat': '2022/04/11'
                            }]
    
    assert atur.daftar() == daftar_suratmasuk

def test_daftarbyjabatan(daftar_suratmasuk, id_jabatan):
    assert atur.daftarbyjabatan(id_jabatan) == [{'id': 5676043608260608,
                                                'nomor_surat': '225/75/PL/2', 
                                                'tgl_surat': '2022-04-12', 
                                                'asal_surat': 'Fakultas Teknik', 
                                                'hal': 'Perlengkapan', 
                                                'isi_ringkas': 'Peminjaman RUangan',
                                                'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                                                'disposisi': ["5711226101301248"],
                                                'komentar': '["5668647137705984"]',
                                                'tindaklanjut': "[]",
                                                'dibaca': ['5077688091934720'],
                                                'tgl_disposisi': '11/04/2022',
                                                'status_tindaklanjut': "-",
                                                'reply': "[]",
                                                'tanggal_surat': '2022/04/11'
                                                }]
    
    assert atur.daftarbyjabatan(id_jabatan) == daftar_suratmasuk

def test_cari(id, cari_suratmasuk):
    assert atur.cari(id) == [{'id': 5676043608260608,
                            'nomor_surat': '225/75/PL/2', 
                            'tgl_surat': '2022-04-12', 
                            'asal_surat': 'Fakultas Teknik', 
                            'hal': 'Perlengkapan', 
                            'isi_ringkas': 'Peminjaman RUangan',
                            'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                            'disposisi': ["5711226101301248"],
                            'komentar': '["5668647137705984"]',
                            'tindaklanjut': "[]",
                            'dibaca': ['5077688091934720'],
                            'tgl_disposisi': '11/04/2022 01:36',
                            'status_tindaklanjut': "-",
                            'reply': "[]"
                            }]

    assert atur.cari(id) == cari_suratmasuk

def test_detail(id, detail_suratmasuk):
    assert atur.detail(id) == [{'id': 5676043608260608,
                            'nomor_surat': '225/75/PL/2', 
                            'tgl_surat': '2022-04-12', 
                            'asal_surat': 'Fakultas Teknik', 
                            'hal': 'Perlengkapan', 
                            'isi_ringkas': 'Peminjaman RUangan',
                            'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                            'disposisi': ['anggota divisi penjaminan mutu'],
                            'komentar': '["5668647137705984"]',
                            'tindaklanjut': "[]",
                            'dibaca': ['kepala upt laboratorium'],
                            'tgl_disposisi': '11/04/2022 01:36',
                            'status_tindaklanjut': "-",
                            'reply': "[]"
                            }]

    assert atur.detail(id) == detail_suratmasuk

def test_update(id, suratmasuk_baru):
    assert atur.update(id, suratmasuk_baru) == [{'id': 5676043608260608,
                                                'nomor_surat': '225/75/PL/2', 
                                                'tgl_surat': '2022-04-12', 
                                                'asal_surat': 'Fakultas Teknik', 
                                                'hal': 'Perlengkapan', 
                                                'isi_ringkas': 'Peminjaman RUangan',
                                                'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                                                'disposisi': ["5711226101301248", "5077688091934720"],
                                                'komentar': '["5668647137705984", "5724539828830208"]',
                                                'tindaklanjut': "[]",
                                                'dibaca': ["5077688091934720"],
                                                'tgl_disposisi': 1649615760,
                                                'status_tindaklanjut': "-",
                                                'reply': "[]"
                                                }]