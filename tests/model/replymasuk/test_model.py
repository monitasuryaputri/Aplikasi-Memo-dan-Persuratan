import pytest
import model

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
def dictionary(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk):
    return {'id': id, 
            'komenmasuk': komenmasuk, 
            'suratmasuk': suratmasuk, 
            'penindak': penindak, 
            'isi_replymasuk': isi_replymasuk, 
            'tgl_replymasuk': tgl_replymasuk}

def test_init(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk):
    init = model.Replymasuk(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk)
    assert init.id == 5667711371706368
    assert init.komenmasuk == "5205959873921024"
    assert init.suratmasuk == "5677651805077504"
    assert init.penindak == 6548254560878592
    assert init.isi_replymasuk == "jangan sampai lewat deadline"
    assert init.tgl_replymasuk == 1640699461.076582

def test_dictionary(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk, dictionary):
    assert model.Replymasuk.ke_dictionary(model.Replymasuk(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk)) == {'id': 5667711371706368,
                                                                                                                                      'komenmasuk': '5205959873921024', 
                                                                                                                                      'suratmasuk': '5677651805077504', 
                                                                                                                                      'penindak': 6548254560878592, 
                                                                                                                                      'isi_replymasuk': "jangan sampai lewat deadline", 
                                                                                                                                      'tgl_replymasuk': 1640699461.076582
                                                                                                                                     }
    assert type(model.Replymasuk.ke_dictionary(model.Replymasuk(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk))) == dict
    assert model.Replymasuk.ke_dictionary(model.Replymasuk(id, komenmasuk, suratmasuk, penindak, isi_replymasuk, tgl_replymasuk)) == dictionary