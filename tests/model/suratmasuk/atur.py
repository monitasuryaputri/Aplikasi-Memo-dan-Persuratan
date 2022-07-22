from aplikasi import model, app

from flask import json

from google.cloud import datastore
import datetime
from tests.model.suratmasuk import SURATMASUK_KIND, Suratmasuk


"""
Controller Untuk Surat Masuk

"""
#tambah surat masuk
def tambah(nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi):
    

    # cek parameter agar tidak kosong
    if nomor_surat and tgl_surat and asal_surat and hal and isi_ringkas and dokumen and disposisi is not None:
        
        # buat list 
        data_suratmasuk = []
        #buat objek yang mau disimpan
        suratmasuk_baru = Suratmasuk(nomor_surat=nomor_surat,
                                    tgl_surat=tgl_surat,
                                    asal_surat=asal_surat,
                                    hal=hal,
                                    isi_ringkas=isi_ringkas,
                                    dokumen=dokumen,
                                    disposisi=disposisi,
                                    komentar="[]",
                                    tindaklanjut="[]",
                                    dibaca=[],
                                    tgl_disposisi=1649615760,
                                    status_tindaklanjut="-",
                                    reply="[]"
                                    )

        # append atau add elemen ke list
        data_suratmasuk.append(suratmasuk_baru.ke_dictionary())
        # kembalikan suratmasuk baru
        return data_suratmasuk

def daftar():
    data_suratmasuk = [{'id': 5676043608260608,
                            'nomor_surat': '225/75/PL/2', 
                            'tgl_surat': '2022-04-12', 
                            'asal_surat': 'Fakultas Teknik', 
                            'hal': 'Perlengkapan', 
                            'isi_ringkas': 'Peminjaman RUangan',
                            'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                            'disposisi': ["5711226101301248"],
                            'komentar': '["5668647137705984"]',
                            'tindaklanjut': "[]",
                            'dibaca': ['5077688091934720'],
                            'tgl_disposisi': 1649615760,
                            'status_tindaklanjut': "-",
                            'reply': "[]"
                            }]

    # ubah dalam format
    daftar_suratmasuk = []

    # iterate data suratmasuk, simpan ke list
    for satu_hasil in data_suratmasuk:
        satu_suratmasuk = Suratmasuk( id=satu_hasil["id"],
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            asal_surat=satu_hasil["asal_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tindaklanjut=satu_hasil["tindaklanjut"],
                            dibaca=satu_hasil["dibaca"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status_tindaklanjut=satu_hasil["status_tindaklanjut"],
                            reply=satu_hasil["reply"]
                            )
        
        if(satu_suratmasuk.tgl_disposisi != ""):
            satu_suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y')
        
        res = satu_suratmasuk.ke_dictionary()
        tanggal_surat = datetime.datetime.strptime(satu_suratmasuk.tgl_disposisi, "%d/%m/%Y").strftime('%Y/%m/%d')
        res["tanggal_surat"] = tanggal_surat
        #append atau add elemen ke list
        daftar_suratmasuk.append(res)
    # kembalikan list daftar suratmasuk
    return daftar_suratmasuk

# Ambil daftar suratmasuk yang telah di disposisi berdasarkan jabatan saja
def daftarbyjabatan(id_jabatan):
    data_suratmasuk = [{'id': 5676043608260608,
                        'nomor_surat': '225/75/PL/2', 
                        'tgl_surat': '2022-04-12', 
                        'asal_surat': 'Fakultas Teknik', 
                        'hal': 'Perlengkapan', 
                        'isi_ringkas': 'Peminjaman RUangan',
                        'dokumen': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Masuk/225/75/PL/2/NOTA%20KEBERATAN.docx","name":"NOTA KEBERATAN.docx"}],
                        'disposisi': ["5711226101301248"],
                        'komentar': '["5668647137705984"]',
                        'tindaklanjut': "[]",
                        'dibaca': ['5077688091934720'],
                        'tgl_disposisi': 1649615760,
                        'status_tindaklanjut': "-",
                        'reply': "[]"
                        }]

    # ubah dalam format
    daftar_suratmasuk = []

    # iterate data suratmasuk, simpan ke list
    for satu_hasil in data_suratmasuk:
        satu_suratmasuk = Suratmasuk( id=satu_hasil["id"],
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            asal_surat=satu_hasil["asal_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tindaklanjut=satu_hasil["tindaklanjut"],
                            dibaca=satu_hasil["dibaca"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status_tindaklanjut=satu_hasil["status_tindaklanjut"],
                            reply=satu_hasil["reply"]
                            )
        
        if(satu_suratmasuk.tgl_disposisi != ""):
            satu_suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y')
        res = satu_suratmasuk.ke_dictionary()
        tanggal_surat = datetime.datetime.strptime(satu_suratmasuk.tgl_disposisi, "%d/%m/%Y").strftime('%Y/%m/%d')
        res["tanggal_surat"] = tanggal_surat
        #append atau add elemen ke list
        daftar_suratmasuk.append(res)
    # kembalikan list daftar surat masuk
    return daftar_suratmasuk

def cari(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratmasuk = client.key(SURATMASUK_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratmasuk)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada suratmasuk dengan id: {id}.")
        
        # buat list
        data_suratmasuk = []

        # buat objek suratmasuk
        suratmasuk = Suratmasuk(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        asal_surat=hasil["asal_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=hasil["disposisi"],
                        komentar=hasil["komentar"],
                        tindaklanjut=hasil["tindaklanjut"],
                        dibaca=hasil["dibaca"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status_tindaklanjut=hasil["status_tindaklanjut"],
                        reply=hasil["reply"]
                        )

       
        if(suratmasuk.tgl_disposisi != ""):
            suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
 
        try:
            suratmasuk.dokumen = json.loads(suratmasuk.dokumen)
        except:
            pass

        data_suratmasuk.append(suratmasuk.ke_dictionary())
        
        return data_suratmasuk


def detail(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratmasuk = client.key(SURATMASUK_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratmasuk)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada suratmasuk dengan id: {id}.")
        
        # buat list
        data_suratmasuk = []

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        penerima = {}
        penerima["disposisi"]=hasil["disposisi"]
        for x in range(len(hasil["disposisi"])):
            penerima["disposisi"][x] = jabatan_nama[hasil["disposisi"][x]]
        
        pembaca = {}
        pembaca["dibaca"]=hasil["dibaca"]
        for x in range(len(hasil["dibaca"])):
            pembaca["dibaca"][x] = jabatan_nama[hasil["dibaca"][x]]
        
        # buat objek suratmasuk
        suratmasuk = Suratmasuk(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        asal_surat=hasil["asal_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=penerima["disposisi"],
                        komentar=hasil["komentar"],
                        tindaklanjut=hasil["tindaklanjut"],
                        dibaca=pembaca["dibaca"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status_tindaklanjut=hasil["status_tindaklanjut"],
                        reply=hasil["reply"]
                        )

        
        if(suratmasuk.tgl_disposisi != ""):
            suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
        
        try:
            suratmasuk.dokumen = json.loads(suratmasuk.dokumen)
        except:
            pass
        data_suratmasuk.append(suratmasuk.ke_dictionary())
        
        return data_suratmasuk

def penanggung(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """
        # Buka koneksi ke datastore
        client = datastore.Client()
        # Cari
        key_suratmasuk = client.key(SURATMASUK_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_suratmasuk)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada suratmasuk dengan id: {id}.")
        # buat list
        data_disposisi = []

        # buat objek suratmasuk
        suratmasuk = Suratmasuk(id=hasil.id,
                        disposisi=hasil["disposisi"]
                        )

        # ubah format data ke dictionary dan append ke list
        res  = suratmasuk.ke_dictionary()
        

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        penerima = {}
        penerima=hasil["disposisi"]
        for x in range(len(hasil["disposisi"])):
            penerima[x] = jabatan_nama[hasil["disposisi"][x]]
        res = penerima
        
        data_disposisi.append(res)
        return data_disposisi

def update(id, data):
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data suratmasuk berdasar property id
    key = client.key(SURATMASUK_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key)

    # Simpan
    hasil.update(data)
    data_suratmasuk = []

    suratmasuk_baru = Suratmasuk(id=id,
                                nomor_surat=hasil["nomor_surat"],
                                tgl_surat=hasil["tgl_surat"],
                                asal_surat=hasil["asal_surat"],
                                hal=hasil["hal"],
                                isi_ringkas=hasil["isi_ringkas"],
                                dokumen=hasil["dokumen"],
                                disposisi=hasil["disposisi"],
                                komentar=hasil["komentar"],
                                tindaklanjut=hasil["tindaklanjut"],
                                dibaca=hasil["dibaca"],
                                tgl_disposisi=hasil["tgl_disposisi"],
                                status_tindaklanjut=hasil["status_tindaklanjut"],
                                reply=hasil["reply"]
                                )
    
    data_suratmasuk.append(suratmasuk_baru.ke_dictionary())
    # kembalikan data suratmasuk
    return data_suratmasuk