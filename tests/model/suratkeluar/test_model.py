import pytest
import model

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
def dictionary(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca):
    return {'id': id, 
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
           }

def test_init(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca):
    init = model.Suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca)
    assert init.id == 5725744969809920
    assert init.nomor_surat == "223/FT/255/PL/8"
    assert init.tgl_surat == "2022-01-28"
    assert init.tujuan_surat == "Fakultas Teknik"
    assert init.hal == "Kemahasiswaan"
    assert init.isi_ringkas == "mahasiswa teknik"
    assert init.dokumen == '[{"name": "SIBA (1).png", "url": "https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/223/FT/255/PL/8/SIBA%20%281%29.png"}]'
    assert init.disposisi == ["5665673409724416"]
    assert init.komentar == []
    assert init.tgl_disposisi == 1643355264.304071
    assert init.status == "draf"
    assert init.reply == "[]"
    assert init.dibaca == []

def test_dictionary(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca, dictionary):
    assert model.Suratkeluar.ke_dictionary(model.Suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca)) == {'id': 5725744969809920,
                                                                                                                                                                                                'nomor_surat': '223/FT/255/PL/8', 
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
                                                                                                                                                                                                }
    assert type(model.Suratkeluar.ke_dictionary(model.Suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca))) == dict
    assert model.Suratkeluar.ke_dictionary(model.Suratkeluar(id, nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tgl_disposisi, status, reply, dibaca)) == dictionary