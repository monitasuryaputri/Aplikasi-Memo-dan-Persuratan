
import pytest
import atur

from tests.model.followup import Followup, FOLLOWUP_KIND

@pytest.fixture
def id():
    return 4824222207574016
@pytest.fixture    
def tindaklanjut():
    return "5656080600268800"
@pytest.fixture    
def penanggungjawab():
    return 5105697184284672
@pytest.fixture    
def isi_followup():
    return "sudah didata"
@pytest.fixture    
def file_followup():
    return '[{"name": "Metodologi Penelitian Hukum.pptx", "url": "https://storage.googleapis.com/surat-labter.appspot.com/followup/Metodologi%20Penelitian%20Hukum.pptx"}]'
@pytest.fixture    
def tgl_followup():
    return 1649753736.719793
@pytest.fixture    
def penanggungjawab_tindaklanjut():
    return {'id': 5105697184284672, 
            'nama': 'Monita Surya', 
            'email': 'monitasuryaputrii@gmail.com', 
            'no_hp': '08116822256', 
            'jabatan': '5077688091934720', 
            'picture': 'https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c',
            'nama_jabatan': 'kepala upt laboratorium'}

@pytest.fixture
def followup(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup):
    return [{"id" : id,
             "tindaklanjut" : tindaklanjut,
             "penanggungjawab" : penanggungjawab,
             "isi_followup" : isi_followup,
             "file_followup" : file_followup,
             "tgl_followup" : tgl_followup            
            }]
@pytest.fixture
def followup_penanggungjawab(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup, penanggungjawab_tindaklanjut):
    return [{"id" : id,
             "tindaklanjut" : tindaklanjut,
             "penanggungjawab" : penanggungjawab,
             "isi_followup" : isi_followup,
             "file_followup" : file_followup,
             "tgl_followup" : tgl_followup,
             "penanggungjawab_tindaklanjut" : penanggungjawab_tindaklanjut
            }]

def test_tambah(tindaklanjut, penanggungjawab, isi_followup, file_followup):
    assert atur.tambah(tindaklanjut, penanggungjawab, isi_followup, file_followup) == [{                            
                                                        "tindaklanjut" : "5656080600268800",
                                                        "penanggungjawab" : 5105697184284672,
                                                        "isi_followup" : "sudah didata",
                                                        "file_followup" : '[{"name": "Metodologi Penelitian Hukum.pptx", "url": "https://storage.googleapis.com/surat-labter.appspot.com/followup/Metodologi%20Penelitian%20Hukum.pptx"}]',
                                                        "tgl_followup" : 1649753736.719793
                                                        }]

def test_daftar(followup):
    assert atur.daftar() == [{"id" : 4824222207574016,                            
                            "tindaklanjut" : "5656080600268800",
                            "penanggungjawab" : 5105697184284672,
                            "isi_followup" : "sudah didata",
                            "file_followup" : '[{"name": "Metodologi Penelitian Hukum.pptx", "url": "https://storage.googleapis.com/surat-labter.appspot.com/followup/Metodologi%20Penelitian%20Hukum.pptx"}]',
                            "tgl_followup" : 1649753736.719793
                            }]
    
    assert atur.daftar() == followup

def test_cari(id, followup):
    assert atur.cari(id) == followup

def test_caribytindaklanjut(tindaklanjut, followup_penanggungjawab):
    assert atur.caribytindaklanjut(tindaklanjut) == followup_penanggungjawab