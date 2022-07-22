from aplikasi import app, model

import datetime
from google.cloud import datastore

from tests.model.replymasuk import REPLYMASUK_KIND, Replymasuk
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id, id_penindak, suratmasuk, isi_replymasuk):
    #tambah reply

    # cek parameter
    if isi_replymasuk is not None:
        # buat list 
        data_replymasuk = []
        # buat object yang mau disimpan
        replymasuk_baru = Replymasuk(
             penindak=id_penindak,
             komenmasuk=id,
             suratmasuk=suratmasuk,
             isi_replymasuk=isi_replymasuk,
             tgl_replymasuk=1640699461.076582
             )
        
        # append atau add elemen ke list
        data_replymasuk.append(replymasuk_baru.ke_dictionary())
        # kembalikan replymasuk baru
        return data_replymasuk

def daftar():
    data_replymasuk = [{'id': 5667711371706368,
                        'komenmasuk': '5205959873921024', 
                        'suratmasuk': '5677651805077504', 
                        'penindak': 6548254560878592, 
                        'isi_replymasuk': "jangan sampai lewat deadline", 
                        'tgl_replymasuk': 1640699461.076582
                      }]

    # buat list
    replymasuk = [] 
    # iterate data replymasuk, simpan ke list
    for satu_hasil in data_replymasuk:
        satu_replymasuk = Replymasuk(id=satu_hasil["id"],
                                    komenmasuk=satu_hasil["komenmasuk"], 
                                    suratmasuk=satu_hasil["suratmasuk"], 
                                    penindak=satu_hasil["penindak"],
                                    isi_replymasuk=satu_hasil["isi_replymasuk"],
                                    tgl_replymasuk=satu_hasil["tgl_replymasuk"]
                                    )

        # append atau add elemen ke list
        replymasuk.append(satu_replymasuk)
    # buat list
    daftar_replymasuk = []
    # iterate data replymasuk, simpan ke list
    for satu_data in replymasuk:
        # append atau add elemen ke list
        daftar_replymasuk.append(satu_data.ke_dictionary())
    # kembalikan array daftar replymasuk
    return daftar_replymasuk


def cari(id):
    if id is not None:
        """ Mencari satu pengaduan berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_replymasuk = client.key(REPLYMASUK_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_replymasuk)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_replymasuk = []
        # buat objek komen
        replymasuk = Replymasuk(id=hasil.id,
                        komenmasuk=hasil["komenmasuk"], 
                        suratmasuk=hasil["suratmasuk"], 
                        penindak=hasil["penindak"],
                        isi_replymasuk=hasil["isi_replymasuk"],
                        tgl_replymasuk=hasil["tgl_replymasuk"]
                        )

        # ubah format data ke dictionary dan append ke list
        data_replymasuk.append(replymasuk.ke_dictionary())
        return data_replymasuk


def caribysuratmasuk(suratmasuk):

    if suratmasuk is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        daftar_replymasuk = [{'id': 5667711371706368,
                        'komenmasuk': '5205959873921024', 
                        'suratmasuk': '5677651805077504', 
                        'penindak': 6548254560878592, 
                        'isi_replymasuk': "jangan sampai lewat deadline", 
                        'tgl_replymasuk': 1640699461.076582
                      }]
        
        # buat list
        data_replymasuk = []

        ad = list_ad()
        list_of_ad = [id for elem in ad
                        for id in elem.values()]
        ka = list_ka()
        list_of_ka = [id for elem in ka
                        for id in elem.values()]
        st = list_st()
        list_of_st = [id for elem in st
                        for id in elem.values()]

        for data in daftar_replymasuk:
           
            # buat objek komen
            replymasuk = Replymasuk(id=data["id"],
                            komenmasuk=data["komenmasuk"],
                            suratmasuk=data["suratmasuk"],
                            penindak=data["penindak"],
                            isi_replymasuk=data["isi_replymasuk"],
                            tgl_replymasuk=data["tgl_replymasuk"]
                            )

            # ubah format data ke dictionary dan append ke list
            res = replymasuk.ke_dictionary()
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

            elif data["penindak"] in list_of_st:
                cari = model.staff.atur.cari(data["penindak"])
                if len(cari) == 1 :
                    cari = cari[0] 

                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penindak_komentar'] = cari

            data_replymasuk.append(res)

        return data_replymasuk