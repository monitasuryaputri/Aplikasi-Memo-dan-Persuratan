import pytest
import model

@pytest.fixture
def id():
    return 5645987863330816
@pytest.fixture    
def suratmasuk():
    return "5183015185547264"
@pytest.fixture    
def penindak():
    return 6548254560878592
@pytest.fixture    
def isi_komenmasuk():
    return "komntar"
@pytest.fixture    
def tgl_komenmasuk():
    return 1643603716.223075
@pytest.fixture    
def reply():
    return "[]"

@pytest.fixture
def dictionary(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply):
    return {'id': id, 'suratmasuk': suratmasuk, 'penindak': penindak, 'isi_komenmasuk': isi_komenmasuk, 'tgl_komenmasuk': tgl_komenmasuk, 'reply': reply}

def test_init(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply):
    init = model.Komenmasuk(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply)
    assert init.id == 5645987863330816
    assert init.suratmasuk == "5183015185547264"
    assert init.penindak == 6548254560878592
    assert init.isi_komenmasuk == "komntar"
    assert init.tgl_komenmasuk == 1643603716.223075
    assert init.reply == "[]"

def test_dictionary(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply, dictionary):
    assert model.Komenmasuk.ke_dictionary(model.Komenmasuk(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply)) == {'id': 5645987863330816, 
                                                                                                                                'suratmasuk': '5183015185547264', 
                                                                                                                                'penindak': 6548254560878592, 
                                                                                                                                'isi_komenmasuk': "komntar", 
                                                                                                                                'tgl_komenmasuk': 1643603716.223075, 
                                                                                                                                'reply': "[]"}
    assert type(model.Komenmasuk.ke_dictionary(model.Komenmasuk(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply))) == dict
    assert model.Komenmasuk.ke_dictionary(model.Komenmasuk(id, suratmasuk, penindak, isi_komenmasuk, tgl_komenmasuk, reply)) == dictionary