import pytest
import model

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
def dictionary(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup):
    return {'id': id, 'tindaklanjut': tindaklanjut, 'penanggungjawab': penanggungjawab, 'isi_followup': isi_followup, 'file_followup': file_followup, 'tgl_followup': tgl_followup}

def test_init(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup):
    init = model.Followup(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup)
    assert init.id == 4824222207574016
    assert init.tindaklanjut == "5656080600268800"
    assert init.penanggungjawab == 5105697184284672
    assert init.isi_followup == "sudah didata"
    assert init.file_followup == '[{"name": "Metodologi Penelitian Hukum.pptx", "url": "https://storage.googleapis.com/surat-labter.appspot.com/followup/Metodologi%20Penelitian%20Hukum.pptx"}]'
    assert init.tgl_followup == 1649753736.719793


def test_dictionary(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup, dictionary):
    assert model.Followup.ke_dictionary(model.Followup(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup)) == {'id': 4824222207574016, 
                                                                                                                                        'tindaklanjut': '5656080600268800', 
                                                                                                                                        'penanggungjawab': 5105697184284672, 
                                                                                                                                        'isi_followup': 'sudah didata', 
                                                                                                                                        'file_followup': '[{"name": "Metodologi Penelitian Hukum.pptx", "url": "https://storage.googleapis.com/surat-labter.appspot.com/followup/Metodologi%20Penelitian%20Hukum.pptx"}]', 
                                                                                                                                        'tgl_followup': 1649753736.719793}
    assert type(model.Followup.ke_dictionary(model.Followup(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup))) == dict
    assert model.Followup.ke_dictionary(model.Followup(id, tindaklanjut, penanggungjawab, isi_followup, file_followup, tgl_followup)) == dictionary