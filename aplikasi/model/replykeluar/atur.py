from aplikasi import app, model

import datetime
from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import REPLYKELUAR_KIND, Replykeluar
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id_penindak, id, suratkeluar, isi_replykeluar):
    #tambah reply

    # cek parameter
    if isi_replykeluar is not None:

        # buat object yang mau disimpan
        replykeluar_baru = Replykeluar(
             penindak=id_penindak,
             komenkeluar=id,
             suratkeluar=suratkeluar,
             isi_replykeluar=isi_replykeluar,
             tgl_replykeluar=datetime.datetime.now().timestamp()
             )
        

        #Buka koneksi ke datastore
        client = datastore.Client()
        # Minta dibuatkan key baru
        key_baru = client.key(REPLYKELUAR_KIND)
        # Buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        # Isi data untuk entity baru
        entity_baru.update(replykeluar_baru.ke_dictionary())
        # Simpan perubahan data entity baru
        client.put(entity_baru)
        # kembalikan pengaduan baru
        return Replykeluar(id=entity_baru.id,
                    penindak=id_penindak,
                    komenkeluar=id,
                    suratkeluar=suratkeluar,
                    isi_replykeluar=entity_baru["isi_replykeluar"],
                    tgl_replykeluar=entity_baru["tgl_replykeluar"]
                    )

def daftar():
    # Ambil daftar komen yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk komen
    query = client.query(kind=REPLYKELUAR_KIND)
    # query untuk ambil seluruh data komen, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_replykeluar = []
    for satu_hasil in hasil:
        satu_replykeluar = Replykeluar(id=satu_hasil.id,
                        isi_replykeluar=satu_hasil["isi_replykeluar"],
                        tgl_replykeluar=satu_hasil["tgl_replykeluar"]
                        )

        # append atau add elemen ke list
        daftar_replykeluar.append(satu_replykeluar)
    # kembalikan array daftar komen
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
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_replykeluar = []
        # buat objek komen
        replykeluar = Replykeluar(id=hasil.id,
                        isi_replykeluar=hasil["isi_replykeluar"],
                        tgl_replykeluar=hasil["tgl_replykeluar"]
                        )

        if(replykeluar.tgl_replykeluar != ""):
            replykeluar.tgl_replykeluar = datetime.datetime.fromtimestamp(float(replykeluar.tgl_replykeluar)).strftime('%d-%m-%y %H:%M')
        
        # ubah format data ke dictionary dan append ke list
        data_replykeluar.append(replykeluar.ke_dictionary())
        return data_replykeluar


def caribysuratkeluar(suratkeluar):

    if suratkeluar is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        query = client.query(kind=REPLYKELUAR_KIND).add_filter("suratkeluar", "=", str(suratkeluar))
        hasil = query.fetch()

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {suratkeluar}.")
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

        for data in hasil:
           
            # buat objek komen
            replykeluar = Replykeluar(id=data.id,
                            komenkeluar=data["komenkeluar"],
                            suratkeluar=data["suratkeluar"],
                            penindak=data["penindak"],
                            isi_replykeluar=data["isi_replykeluar"],
                            tgl_replykeluar=data["tgl_replykeluar"]
                            )

            if(replykeluar.tgl_replykeluar != ""):
                replykeluar.tgl_replykeluar = datetime.datetime.fromtimestamp(float(replykeluar.tgl_replykeluar)).strftime('%d-%m-%y %H:%M')
   
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