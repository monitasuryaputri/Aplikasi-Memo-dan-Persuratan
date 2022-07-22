import pytest
import model

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
def dictionary(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply):
    return {'id': id, 'suratkeluar': suratkeluar, 'penindak': penindak, 'isi_komenkeluar': isi_komenkeluar, 'tgl_komenkeluar': tgl_komenkeluar, 'file_komenkeluar': file_komenkeluar, 'reply': reply}

def test_init(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply):
    init = model.Komenkeluar(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply)
    assert init.id == 5076466173739008
    assert init.suratkeluar == "5671441819238400"
    assert init.penindak == 6548254560878592
    assert init.isi_komenkeluar == "komentar"
    assert init.tgl_komenkeluar == 1643882750.899903
    assert init.file_komenkeluar == [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}]
    assert init.reply == "[]"

def test_dictionary(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply, dictionary):
    assert model.Komenkeluar.ke_dictionary(model.Komenkeluar(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply)) == {'id': 5076466173739008, 
                                                                                                                                                        'suratkeluar': '5671441819238400', 
                                                                                                                                                        'penindak': 6548254560878592, 
                                                                                                                                                        'isi_komenkeluar': "komentar", 
                                                                                                                                                        'tgl_komenkeluar': 1643882750.899903, 
                                                                                                                                                        'file_komenkeluar': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}],
                                                                                                                                                        'reply': "[]"}
    assert type(model.Komenkeluar.ke_dictionary(model.Komenkeluar(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply))) == dict
    assert model.Komenkeluar.ke_dictionary(model.Komenkeluar(id, suratkeluar, penindak, isi_komenkeluar, tgl_komenkeluar, file_komenkeluar, reply)) == dictionary