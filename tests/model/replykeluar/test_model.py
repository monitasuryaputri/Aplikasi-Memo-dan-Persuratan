import pytest
import model

@pytest.fixture
def id():
    return 6264989119676416
@pytest.fixture    
def komenkeluar():
    return "5139920456777728"
@pytest.fixture    
def suratkeluar():
    return "5657791876300800"
@pytest.fixture    
def penindak():
    return 5659336621686784
@pytest.fixture    
def isi_replykeluar():
    return "oke"
@pytest.fixture    
def tgl_replykeluar():
    return 1641549519.706046


@pytest.fixture
def dictionary(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar):
    return {'id': id, 
            'komenkeluar': komenkeluar, 
            'suratkeluar': suratkeluar, 
            'penindak': penindak, 
            'isi_replykeluar': isi_replykeluar, 
            'tgl_replykeluar': tgl_replykeluar}

def test_init(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar):
    init = model.Replykeluar(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar)
    assert init.id == 6264989119676416
    assert init.komenkeluar == "5139920456777728"
    assert init.suratkeluar == "5657791876300800"
    assert init.penindak == 5659336621686784
    assert init.isi_replykeluar == "oke"
    assert init.tgl_replykeluar == 1641549519.706046

def test_dictionary(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar, dictionary):
    assert model.Replykeluar.ke_dictionary(model.Replykeluar(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar)) == {'id': 6264989119676416,
                                                                                                                                            'komenkeluar': '5139920456777728', 
                                                                                                                                            'suratkeluar': '5657791876300800', 
                                                                                                                                            'penindak': 5659336621686784, 
                                                                                                                                            'isi_replykeluar': "oke", 
                                                                                                                                            'tgl_replykeluar': 1641549519.706046 
                                                                                                                                            }
    assert type(model.Replykeluar.ke_dictionary(model.Replykeluar(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar))) == dict
    assert model.Replykeluar.ke_dictionary(model.Replykeluar(id, komenkeluar, suratkeluar, penindak, isi_replykeluar, tgl_replykeluar)) == dictionary