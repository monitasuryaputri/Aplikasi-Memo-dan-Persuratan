from aplikasi import app, model

import datetime
from google.cloud import datastore

from tests.model.replykeluar import REPLYKELUAR_KIND, Replykeluar
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id, id_penindak, suratkeluar, isi_replykeluar):
    #tambah reply

    # cek parameter
    if isi_replykeluar is not None:
        # buat list 
        data_replykeluar = []
        # buat object yang mau disimpan
        replykeluar_baru = Replykeluar(
             penindak=id_penindak,
             komenkeluar=id,
             suratkeluar=suratkeluar,
             isi_replykeluar=isi_replykeluar,
             tgl_replykeluar=1641549519.706046
             )
        
        # append atau add elemen ke list
        data_replykeluar.append(replykeluar_baru.ke_dictionary())
        # kembalikan replykeluar baru
        return data_replykeluar

def daftar():
    data_replykeluar = [{'id': 6264989119676416,
                        'komenkeluar': '5139920456777728', 
                        'suratkeluar': '5657791876300800', 
                        'penindak': 5659336621686784, 
                        'isi_replykeluar': "oke", 
                        'tgl_replykeluar': 1641549519.706046 
                        }]

    # buat list
    replykeluar = []                
    # iterate data replykeluar, simpan ke list
    for satu_hasil in data_replykeluar:
        satu_replykeluar = Replykeluar(id=satu_hasil["id"],
                                       komenkeluar=satu_hasil["komenkeluar"], 
                                       suratkeluar=satu_hasil["suratkeluar"], 
                                       penindak=satu_hasil["penindak"],
                                       isi_replykeluar=satu_hasil["isi_replykeluar"],
                                       tgl_replykeluar=satu_hasil["tgl_replykeluar"]
                                       )

        # append atau add elemen ke list
        replykeluar.append(satu_replykeluar)
    # buat list
    daftar_replykeluar = []
    # iterate data replykeluar, simpan ke list
    for satu_data in replykeluar:
        # append atau add elemen ke list
        daftar_replykeluar.append(satu_data.ke_dictionary())
    # kembalikan array daftar replykeluar
    return daftar_replykeluar


def cari(id):
    if id is not None:
        """ Mencari satu pengaduan berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_replykeluar = client.key(REPLYKELUAR_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_replykeluar)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_replykeluar = []
        # buat objek komen
        replykeluar = Replykeluar(id=hasil.id,
                        komenkeluar=hasil["komenkeluar"], 
                        suratkeluar=hasil["suratkeluar"], 
                        penindak=hasil["penindak"],
                        isi_replykeluar=hasil["isi_replykeluar"],
                        tgl_replykeluar=hasil["tgl_replykeluar"]
                        )

        # ubah format data ke dictionary dan append ke list
        data_replykeluar.append(replykeluar.ke_dictionary())
        return data_replykeluar


def caribysuratkeluar(suratkeluar):

    if suratkeluar is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        daftar_replykeluar = [{'id': 6264989119676416,
                            'komenkeluar': '5139920456777728', 
                            'suratkeluar': '5657791876300800', 
                            'penindak': 5659336621686784, 
                            'isi_replykeluar': "oke", 
                            'tgl_replykeluar': 1641549519.706046 
                            }]
        
        # buat list
        data_replykeluar = []

        ad = list_ad()
        list_of_ad = [id for elem in ad
                        for id in elem.values()]
        ka = list_ka()
        list_of_ka = [id for elem in ka
                        for id in elem.values()]
        st = list_st()
        list_of_st = [id for elem in st
                        for id in elem.values()]

        for data in daftar_replykeluar:
           
            # buat objek komen
            replykeluar = Replykeluar(id=data["id"],
                            komenkeluar=data["komenkeluar"],
                            suratkeluar=data["suratkeluar"],
                            penindak=data["penindak"],
                            isi_replykeluar=data["isi_replykeluar"],
                            tgl_replykeluar=data["tgl_replykeluar"]
                            )
   
            # ubah format data ke dictionary dan append ke list
            res = replykeluar.ke_dictionary()
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

            data_replykeluar.append(res)

        return data_replykeluar