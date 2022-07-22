import pytest
import model

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
def dictionary(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif):
    return {'id': id, 
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
           }

def test_init(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif):
    init = model.Tindaklanjut(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif)
    assert init.id == 5644357755469824
    assert init.suratmasuk == "5729017198018560"
    assert init.penugas == 5652730257342464
    assert init.penanggungjawab == "5731076903272448"
    assert init.tugas == "sediakan ruangan"
    assert init.tgl_tugas == 1643794758.564006
    assert init.tgl_selesai == ""
    assert init.followup == "[]"
    assert init.tenggatwaktu == "2022-02-04"
    assert init.check == "0"
    assert init.notif == "no"


def test_dictionary(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif, dictionary):
    assert model.Tindaklanjut.ke_dictionary(model.Tindaklanjut(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif)) == {'id': 5644357755469824,
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
                                                                                                                                                                                    }
    assert type(model.Tindaklanjut.ke_dictionary(model.Tindaklanjut(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif))) == dict
    assert model.Tindaklanjut.ke_dictionary(model.Tindaklanjut(id, suratmasuk, penugas, penanggungjawab, tugas, tgl_tugas, tgl_selesai, followup, tenggatwaktu, check, notif)) == dictionary