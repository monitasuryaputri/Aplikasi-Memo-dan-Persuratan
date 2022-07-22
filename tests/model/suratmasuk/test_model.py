import pytest
import model

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
def komentar():
    return '["5668647137705984"]'
@pytest.fixture    
def tindaklanjut():
    return "[]"
@pytest.fixture    
def dibaca():
    return []
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
def dictionary(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply):
    return {'id': id, 
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
           }

def test_init(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply):
    init = model.Suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply)
    assert init.id == 5676043608260608
    assert init.nomor_surat == "225/75/PL/2"
    assert init.tgl_surat == "2022-04-12"
    assert init.asal_surat == "Fakultas Teknik"
    assert init.hal == "Perlengkapan"
    assert init.isi_ringkas == "Peminjaman RUangan"
    assert init.dokumen == [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}]
    assert init.disposisi == ["5711226101301248"]
    assert init.komentar == '["5668647137705984"]'
    assert init.tindaklanjut == "[]"
    assert init.dibaca == []
    assert init.tgl_disposisi == 1649615760
    assert init.status_tindaklanjut == "-"
    assert init.reply == "[]"

def test_dictionary(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply, dictionary):
    assert model.Suratmasuk.ke_dictionary(model.Suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply)) == {'id': 5676043608260608,
                                                                                                                                                                                                                        'nomor_surat': '225/75/PL/2', 
                                                                                                                                                                                                                        'tgl_surat': '2022-04-12', 
                                                                                                                                                                                                                        'asal_surat': 'Fakultas Teknik', 
                                                                                                                                                                                                                        'hal': 'Perlengkapan', 
                                                                                                                                                                                                                        'isi_ringkas': 'Peminjaman RUangan',
                                                                                                                                                                                                                        'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                                                                                                                                                                                                                        'disposisi': ["5711226101301248"],
                                                                                                                                                                                                                        'komentar': '["5668647137705984"]',
                                                                                                                                                                                                                        'tindaklanjut': "[]",
                                                                                                                                                                                                                        'dibaca': [],
                                                                                                                                                                                                                        'tgl_disposisi': 1649615760,
                                                                                                                                                                                                                        'status_tindaklanjut': "-",
                                                                                                                                                                                                                        'reply': "[]"
                                                                                                                                                                                                                        }
    assert type(model.Suratmasuk.ke_dictionary(model.Suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply))) == dict
    assert model.Suratmasuk.ke_dictionary(model.Suratmasuk(id, nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi, komentar, tindaklanjut, dibaca, tgl_disposisi, status_tindaklanjut, reply)) == dictionary