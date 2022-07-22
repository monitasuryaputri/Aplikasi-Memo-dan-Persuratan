from aplikasi import app, model

import datetime
from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import REPLYMASUK_KIND, Replymasuk
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id_penindak, id, suratmasuk, isi_replymasuk):
    #tambah reply

    # cek parameter
    if isi_replymasuk is not None:

        # buat object yang mau disimpan
        replymasuk_baru = Replymasuk(
             penindak=id_penindak,
             komenmasuk=id,
             suratmasuk=suratmasuk,
             isi_replymasuk=isi_replymasuk,
             tgl_replymasuk=datetime.datetime.now().timestamp()
             )
        

        #Buka koneksi ke datastore
        client = datastore.Client()
        # Minta dibuatkan key baru
        key_baru = client.key(REPLYMASUK_KIND)
        # Buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        # Isi data untuk entity baru
        entity_baru.update(replymasuk_baru.ke_dictionary())
        # Simpan perubahan data entity baru
        client.put(entity_baru)
        # kembalikan pengaduan baru        
        return Replymasuk(id=entity_baru.id,
                    penindak=id_penindak,
                    komenmasuk=id,
                    suratmasuk=suratmasuk,
                    isi_replymasuk=entity_baru["isi_replymasuk"],
                    tgl_replymasuk=entity_baru["tgl_replymasuk"]
                    )

def daftar():
    # Ambil daftar komen yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk komen
    query = client.query(kind=REPLYMASUK_KIND)
    # query untuk ambil seluruh data komen, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_replymasuk = []
    for satu_hasil in hasil:
        satu_replymasuk = Replymasuk(id=satu_hasil.id,
                        isi_replymasuk=satu_hasil["isi_replymasuk"],
                        tgl_replymasuk=satu_hasil["tgl_replymasuk"]
                        )

        # append atau add elemen ke list
        daftar_replymasuk.append(satu_replymasuk)
    # kembalikan array daftar komen
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
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_replymasuk = []
        # buat objek komen
        replymasuk = Replymasuk(id=hasil.id,
                        isi_replymasuk=hasil["isi_replymasuk"],
                        tgl_replymasuk=hasil["tgl_replymasuk"]
                        )

        if(replymasuk.tgl_replymasuk != ""):
            replymasuk.tgl_replymasuk = datetime.datetime.fromtimestamp(float(replymasuk.tgl_replymasuk)).strftime('%d-%m-%y %H:%M')
        
        # ubah format data ke dictionary dan append ke list
        data_replymasuk.append(replymasuk.ke_dictionary())
        return data_replymasuk


def caribysuratmasuk(suratmasuk):

    if suratmasuk is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        query = client.query(kind=REPLYMASUK_KIND).add_filter("suratmasuk", "=", str(suratmasuk))
        hasil = query.fetch()

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {suratmasuk}.")
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

        for data in hasil:
           
            # buat objek komen
            replymasuk = Replymasuk(id=data.id,
                            komenmasuk=data["komenmasuk"],
                            suratmasuk=data["suratmasuk"],
                            penindak=data["penindak"],
                            isi_replymasuk=data["isi_replymasuk"],
                            tgl_replymasuk=data["tgl_replymasuk"]
                            )

            if(replymasuk.tgl_replymasuk != ""):
                replymasuk.tgl_replymasuk = datetime.datetime.fromtimestamp(float(replymasuk.tgl_replymasuk)).strftime('%d-%m-%y %H:%M')
   
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