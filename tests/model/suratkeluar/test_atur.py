

import pytest
import atur
from google.cloud import datastore

from tests.model.suratkeluar import Suratkeluar, SURATKELUAR_KIND

@pytest.fixture
def id():
    return 5725744969809920
@pytest.fixture    
def nomor_surat():
    return "223/FT/255/PL/8"
@pytest.fixture    
def tgl_surat():
    return "2022-01-28"
@pytest.fixture    
def tujuan_surat():
    return "Fakultas Teknik"
@pytest.fixture    
def hal():
    return "Kemahasiswaan"
@pytest.fixture    
def isi_ringkas():
    return "mahasiswa teknik"
@pytest.fixture    
def dokumen():
    return '[{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}]'
@pytest.fixture    
def disposisi():
    return ["5665673409724416"]
@pytest.fixture    
def id_jabatan():
    return 5665673409724416
@pytest.fixture    
def komentar():
    return []
@pytest.fixture    
def tgl_disposisi():
    return 1643355264.304071
@pytest.fixture    
def status():
    return "draf"
@pytest.fixture    
def reply():
    return "[]"
@pytest.fixture    
def dibaca():
    return []
@pytest.fixture    
def tanggal_surat():
    return "2022/01/28"

@pytest.fixture
def suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'tujuan_surat': tujuan_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': dokumen,
            'disposisi': disposisi,
            'komentar': komentar,
            'tgl_disposisi': tgl_disposisi,
            'status': status,
            'reply': reply,
            'dibaca': dibaca
            }]

@pytest.fixture
def daftar_suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca, tanggal_surat):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'tujuan_surat': tujuan_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': dokumen,
            'disposisi': disposisi,
            'komentar': komentar,
            'tgl_disposisi': '28/01/2022',            
            'status': status,
            'reply': reply,
            'dibaca': dibaca,
            'tanggal_surat': tanggal_surat
            }]

@pytest.fixture
def cari_suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, disposisi, komentar, status, reply, dibaca):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'tujuan_surat': tujuan_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': [{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}],
            'disposisi': disposisi,
            'komentar': komentar,
            'tgl_disposisi': '28/01/2022 14:34',
            'status': status,
            'reply': reply,
            'dibaca': ['5077688091934720']
            }]
@pytest.fixture
def detail_suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, disposisi, komentar, status, reply, dibaca):
    return [{'id': id, 
            'nomor_surat': nomor_surat, 
            'tgl_surat': tgl_surat, 
            'tujuan_surat': tujuan_surat, 
            'hal': hal, 
            'isi_ringkas': isi_ringkas,
            'dokumen': [{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}],
            'disposisi': ['koordinator divisi penjaminan mutu'],
            'komentar': komentar,
            'tgl_disposisi': '28/01/2022 14:34',
            'status': status,
            'reply': reply,
            'dibaca': ['kepala upt laboratorium']
            }]
@pytest.fixture
def suratkeluar_baru():
    return {'disposisi': ["5665673409724416", "5077688091934720"],
            'komentar': ["5724539828830208"],
            'dibaca': ["5077688091934720"]
            }

def test_tambah(nomor_surat, 
                tgl_surat, 
                tujuan_surat, 
                hal, 
                isi_ringkas, 
                dokumen, 
                disposisi):
    assert atur.tambah(nomor_surat, 
                       tgl_surat, 
                       tujuan_surat, 
                       hal, 
                       isi_ringkas, 
                       dokumen, 
                       disposisi) == [{'nomor_surat': '223/FT/255/PL/8', 
                                        'tgl_surat': '2022-01-28', 
                                        'tujuan_surat': 'Fakultas Teknik', 
                                        'hal': 'Kemahasiswaan', 
                                        'isi_ringkas': 'mahasiswa teknik',
                                        'dokumen': '[{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}]',
                                        'disposisi': ["5665673409724416"],
                                        'komentar': [],
                                        'tgl_disposisi': 1643355264.304071,
                                        'status': 'draf',
                                        'reply': '[]',
                                        'dibaca': []
                                        }]

def test_daftar(daftar_suratkeluar):
    assert atur.daftar() == [{'id': 5725744969809920,
                            'nomor_surat': '223/FT/255/PL/8', 
                            'tgl_surat': '2022-01-28', 
                            'tujuan_surat': 'Fakultas Teknik', 
                            'hal': 'Kemahasiswaan', 
                            'isi_ringkas': 'mahasiswa teknik',
                            'dokumen': '[{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}]',
                            'disposisi': ["5665673409724416"],
                            'komentar': [],
                            'tgl_disposisi': '28/01/2022',
                            'status': 'draf',
                            'reply': '[]',
                            'dibaca': [],
                            'tanggal_surat': '2022/01/28'
                            }]
    
    assert atur.daftar() == daftar_suratkeluar

def test_daftarbyjabatan(daftar_suratkeluar, id_jabatan):
    assert atur.daftarbyjabatan(id_jabatan) == [{'id': 5725744969809920,
                                            'nomor_surat': '223/FT/255/PL/8', 
                                            'tgl_surat': '2022-01-28', 
                                            'tujuan_surat': 'Fakultas Teknik', 
                                            'hal': 'Kemahasiswaan', 
                                            'isi_ringkas': 'mahasiswa teknik',
                                            'dokumen': '[{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}]',
                                            'disposisi': ["5665673409724416"],
                                            'komentar': [],
                                            'tgl_disposisi': '28/01/2022',
                                            'status': 'draf',
                                            'reply': '[]',
                                            'dibaca': [],
                                            'tanggal_surat': '2022/01/28'
                                            }]
    
    assert atur.daftarbyjabatan(id_jabatan) == daftar_suratkeluar

def test_cari(id, cari_suratkeluar):
    assert atur.cari(id) == [{'id': 5725744969809920,
                        'nomor_surat': '223/FT/255/PL/8', 
                        'tgl_surat': '2022-01-28', 
                        'tujuan_surat': 'Fakultas Teknik', 
                        'hal': 'Kemahasiswaan', 
                        'isi_ringkas': 'mahasiswa teknik',
                        'dokumen': [{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}],
                        'disposisi': ["5665673409724416"],
                        'komentar': [],
                        'tgl_disposisi': '28/01/2022 14:34',
                        'status': 'draf',
                        'reply': '[]',
                        'dibaca': ['5077688091934720']
                        }]

    assert atur.cari(id) == cari_suratkeluar

def test_detail(id, detail_suratkeluar):
    assert atur.detail(id) == [{'id': 5725744969809920,
                        'nomor_surat': '223/FT/255/PL/8', 
                        'tgl_surat': '2022-01-28', 
                        'tujuan_surat': 'Fakultas Teknik', 
                        'hal': 'Kemahasiswaan', 
                        'isi_ringkas': 'mahasiswa teknik',
                        'dokumen': [{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}],
                        'disposisi': ['koordinator divisi penjaminan mutu'],
                        'komentar': [],
                        'tgl_disposisi': '28/01/2022 14:34',
                        'status': 'draf',
                        'reply': '[]',
                        'dibaca': ['kepala upt laboratorium']
                        }]

    assert atur.detail(id) == detail_suratkeluar

def test_update(id, suratkeluar_baru):
    assert atur.update(id, suratkeluar_baru) == [{'id': 5725744969809920,
                                                'nomor_surat': '223/FT/255/PL/8', 
                                                'tgl_surat': '2022-01-28', 
                                                'tujuan_surat': 'Fakultas Teknik', 
                                                'hal': 'Kemahasiswaan', 
                                                'isi_ringkas': 'mahasiswa teknik',
                                                'dokumen': [{'name':'SIBA (1).png','url':'https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png'}],
                                                'disposisi': ["5665673409724416", "5077688091934720"],
                                                'komentar': ["5724539828830208"],
                                                'tgl_disposisi': 1643355240.0,
                                                'status': 'draf',
                                                'reply': '[]',
                                                'dibaca': ["5077688091934720"]
                                                }]