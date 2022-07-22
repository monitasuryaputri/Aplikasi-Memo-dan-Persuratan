from aplikasi import app, model

import datetime
from google.cloud import datastore

from tests.model.komenmasuk import KOMENMASUK_KIND, Komenmasuk
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id, id_penindak, isi_komenmasuk):
    #tambah komen

    # cek parameter
    if isi_komenmasuk is not None:

        # buat list 
        data_komenmasuk = []
        # buat object yang mau disimpan
        komenmasuk_baru = Komenmasuk(
                            suratmasuk=id,
                            penindak=id_penindak,             
                            isi_komenmasuk=isi_komenmasuk,
                            tgl_komenmasuk=1643603716.223075,
                            reply="[]"
                            )
        # append atau add elemen ke list
        data_komenmasuk.append(komenmasuk_baru.ke_dictionary())
        # kembalikan komenmasuk baru
        return data_komenmasuk

def daftar():
    data_komenmasuk = [{'id': 5645987863330816, 
                        'suratmasuk': '5183015185547264', 
                        'penindak': 6548254560878592, 
                        'isi_komenmasuk': "komntar", 
                        'tgl_komenmasuk': 1643603716.223075, 
                        'reply': "[]"}]
    # buat list
    komenmasuk = []                
    # iterate data komenmasuk, simpan ke list
    for satu_hasil in data_komenmasuk:
        satu_komenmasuk = Komenmasuk(id=satu_hasil["id"],
                                       suratmasuk=satu_hasil["suratmasuk"],
                                       penindak=satu_hasil["penindak"],
                                       isi_komenmasuk=satu_hasil["isi_komenmasuk"],
                                       tgl_komenmasuk=satu_hasil["tgl_komenmasuk"],
                                       reply=satu_hasil["reply"]
                                        )
        # append atau add elemen ke list
        komenmasuk.append(satu_komenmasuk)
    # buat list
    daftar_komenmasuk = []
    # iterate data komenmasuk, simpan ke list
    for satu_data in komenmasuk:
        # append atau add elemen ke list
        daftar_komenmasuk.append(satu_data.ke_dictionary())
    # kembalikan array daftar komenmasuk
    return daftar_komenmasuk


def cari(id):
    if id is not None:
        """ Mencari satu pengaduan berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_komenmasuk = client.key(KOMENMASUK_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_komenmasuk)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_komenmasuk = []
        # buat objek komen
        komenmasuk = Komenmasuk(id=hasil.id,
                        suratmasuk=hasil["suratmasuk"],
                        penindak=hasil["penindak"],
                        isi_komenmasuk=hasil["isi_komenmasuk"],
                        tgl_komenmasuk=hasil["tgl_komenmasuk"],
                        reply=hasil["reply"]
                        )

        # ubah format data ke dictionary dan append ke list
        data_komenmasuk.append(komenmasuk.ke_dictionary())
        return data_komenmasuk

def caribykomenmasuk(id_suratmasuk, id):

    if id is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_komenmasuk = client.key(KOMENMASUK_KIND, id)
        
        #  ambil hasil carinya
        hasil = client.get(key_komenmasuk)
        
        
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_komenmasuk = []
        
        # buat objek komen
        komenmasuk = Komenmasuk(id=hasil.id,
                        suratmasuk=hasil["suratmasuk"],
                        penindak=hasil["penindak"],
                        isi_komenmasuk=hasil["isi_komenmasuk"],
                        tgl_komenmasuk=hasil["tgl_komenmasuk"],
                        reply=hasil["reply"]
                        )

        data_komenmasuk.append(komenmasuk.ke_dictionary())

        return data_komenmasuk

def caribysuratmasuk(id_suratmasuk):

    if id_suratmasuk is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        daftarkomenmasuk = [{'id': 5645987863330816, 
                              'suratmasuk': '5183015185547264', 
                              'penindak': 6548254560878592, 
                              'isi_komenmasuk': "komntar", 
                              'tgl_komenmasuk': 1643603716.223075, 
                              'reply': "[]"}]

        # buat list
        data_komenmasuk = []

        ad = list_ad()
        list_of_ad = [id for elem in ad
                        for id in elem.values()]
        ka = list_ka()
        list_of_ka = [id for elem in ka
                        for id in elem.values()]
        st = list_st()
        list_of_st = [id for elem in st
                        for id in elem.values()]

        for data in daftarkomenmasuk:
            # buat objek komen
            komenmasuk = Komenmasuk(id=data["id"],
                            suratmasuk=data["suratmasuk"],
                            penindak=data["penindak"],
                            isi_komenmasuk=data["isi_komenmasuk"],
                            tgl_komenmasuk=data["tgl_komenmasuk"],
                            reply=data["reply"]
                            )

            
            # ubah format data ke dictionary dan append ke list
            res = komenmasuk.ke_dictionary()
            if data["penindak"] in list_of_ka:
                cari = model.kepalaupt.atur.cari(data["penindak"])
                if len(cari) == 1 :
                    cari = cari[0] 
                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penindak_komentar'] = cari

            elif data["penindak"] in list_of_ad:
                cari = model.admin.atur.cari(data["penindak"])
                if len(cari) == 1 :
                    cari = cari[0] 
                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penindak_komentar'] = cari

            elif data["penindak"] in list_of_st :
                cari = model.staff.atur.cari(data["penindak"])
                if len(cari) == 1 :
                    cari = cari[0] 

                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penindak_komentar'] = cari

            data_komenmasuk.append(res)

        return data_komenmasuk

def update(id, data):

    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data suratmasuk berdasar property id
    key = client.key(KOMENMASUK_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key)
    # Simpan
    hasil.update(data)
    data_komenmasuk = []

    komenmasuk_baru = Komenmasuk(id=id,
                                suratmasuk=hasil["suratmasuk"],
                                penindak=hasil["penindak"],
                                isi_komenmasuk=hasil["isi_komenmasuk"],
                                tgl_komenmasuk=hasil["tgl_komenmasuk"],
                                reply=hasil["reply"]
                                )
    
    data_komenmasuk.append(komenmasuk_baru.ke_dictionary())
    # kembalikan data komenmasuk
    return data_komenmasuk
        