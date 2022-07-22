from aplikasi import model, app

from flask import json

from google.cloud import datastore
import datetime
from tests.model.suratkeluar import SURATKELUAR_KIND, Suratkeluar

#tambah suratkeluar
def tambah(nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi):
    
    # cek parameter agar tidak kosong
    if nomor_surat and tgl_surat and tujuan_surat and hal and isi_ringkas and dokumen and disposisi is not None:
        
        # buat list 
        data_suratkeluar = []
        #buat objek yang mau disimpan
        suratkeluar_baru = Suratkeluar(nomor_surat=nomor_surat,
                                    tgl_surat=tgl_surat,
                                    tujuan_surat=tujuan_surat,
                                    hal=hal,
                                    isi_ringkas=isi_ringkas,
                                    dokumen=dokumen,
                                    disposisi=disposisi,
                                    komentar=[],
                                    tgl_disposisi=1643355264.304071,
                                    status="draf",
                                    reply="[]",
                                    dibaca=[]
                                    )
        
        # append atau add elemen ke list
        data_suratkeluar.append(suratkeluar_baru.ke_dictionary())
        # kembalikan suratkeluar baru
        return data_suratkeluar

def daftar():

    data_suratkeluar = [{'id': 5725744969809920,
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
                        }]

    # ubah dalam format
    daftar_suratkeluar = []

    # iterate data suratkeluar, simpan ke list
    for satu_hasil in data_suratkeluar:
        satu_suratkeluar = Suratkeluar( id=satu_hasil["id"],
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            tujuan_surat=satu_hasil["tujuan_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status=satu_hasil["status"],
                            reply=satu_hasil["reply"],
                            dibaca=satu_hasil["dibaca"]
                            )
        
        if(satu_suratkeluar.tgl_disposisi != ""):
            satu_suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y')
        res = satu_suratkeluar.ke_dictionary()
        tanggal_surat = datetime.datetime.strptime(satu_suratkeluar.tgl_disposisi, "%d/%m/%Y").strftime('%Y/%m/%d')
        res["tanggal_surat"] = tanggal_surat
        #append atau add elemen ke list
        daftar_suratkeluar.append(res)
    # kembalikan list daftar suratkeluar
    return daftar_suratkeluar

# Ambil daftar suratkeluar yang telah di disposisi berdasarkan jabatan saja
def daftarbyjabatan(id_jabatan):

    data_suratkeluar = [{'id': 5725744969809920,
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
                        }]

    # buat list
    daftar_suratkeluar = []

    # iterate data suratkeluar, simpan ke list
    for satu_hasil in data_suratkeluar:
        satu_suratkeluar = Suratkeluar( id=satu_hasil["id"],
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            tujuan_surat=satu_hasil["tujuan_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status=satu_hasil["status"],
                            reply=satu_hasil["reply"],
                            dibaca=satu_hasil["dibaca"]
                            )

        if(satu_suratkeluar.tgl_disposisi != ""):
            satu_suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y')
        res = satu_suratkeluar.ke_dictionary()
        tanggal_surat = datetime.datetime.strptime(satu_suratkeluar.tgl_disposisi, "%d/%m/%Y").strftime('%Y/%m/%d')
        res["tanggal_surat"] = tanggal_surat

        #append atau add elemen ke list
        daftar_suratkeluar.append(res)            
    # kembalikan list daftar surat masuk
    return daftar_suratkeluar

def cari(id):
    if id is not None:
        """ Mencari satu suratkeluar berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratkeluar = client.key(SURATKELUAR_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratkeluar)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada suratkeluar dengan id: {id}.")
        
        # buat list
        data_suratkeluar = []

        # buat objek suratkeluar
        suratkeluar = Suratkeluar(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        tujuan_surat=hasil["tujuan_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=hasil["disposisi"],
                        komentar=hasil["komentar"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status=hasil["status"],
                        reply=hasil["reply"],
                        dibaca=hasil["dibaca"]
                        )

       
        if(suratkeluar.tgl_disposisi != ""):
            suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
    
        # GATAU, YG GINI2 JGN DIAPUS
        try:
            suratkeluar.dokumen = json.loads(suratkeluar.dokumen)
        except:
            pass
    
        data_suratkeluar.append(suratkeluar.ke_dictionary())
        
        return data_suratkeluar

def detail(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratkeluar = client.key(SURATKELUAR_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratkeluar)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada suratmasuk dengan id: {id}.")
        
        # buat list
        data_suratkeluar = []

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
        suratkeluar = Suratkeluar(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        tujuan_surat=hasil["tujuan_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=penerima["disposisi"],
                        komentar=hasil["komentar"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status=hasil["status"],
                        reply=hasil["reply"],
                        dibaca=pembaca["dibaca"]
                        )

        
        if(suratkeluar.tgl_disposisi != ""):
            suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')

        try:
            suratkeluar.dokumen = json.loads(suratkeluar.dokumen)
        except:
            pass

        data_suratkeluar.append(suratkeluar.ke_dictionary())
        
        return data_suratkeluar

def update(id, data):

    # Buka koneksi ke datastore
    client = datastore.Client()
    # cari/filter data suratkeluar berdasar property id
    key = client.key(SURATKELUAR_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key)
    

    # Simpan
    hasil.update(data)

    data_suratkeluar = []

    suratkeluar_baru = Suratkeluar(id=id,
                                    nomor_surat=hasil["nomor_surat"],
                                    tgl_surat=hasil["tgl_surat"],
                                    tujuan_surat=hasil["tujuan_surat"],
                                    hal=hasil["hal"],
                                    isi_ringkas=hasil["isi_ringkas"],
                                    dokumen=hasil["dokumen"],
                                    disposisi=hasil["disposisi"],
                                    komentar=hasil["komentar"],
                                    tgl_disposisi=hasil["tgl_disposisi"],
                                    status=hasil["status"],
                                    reply=hasil["reply"],
                                    dibaca=hasil["dibaca"]
                                    )
    
    data_suratkeluar.append(suratkeluar_baru.ke_dictionary())
    # kembalikan data suratkeluar
    return data_suratkeluar
