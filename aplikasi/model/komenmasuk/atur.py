from aplikasi import app, model

import datetime
from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import KOMENMASUK_KIND, Komenmasuk
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id_penindak, id, nomor_surat, isi_komenmasuk):
    #tambah komen

    # cek parameter
    if isi_komenmasuk is not None:

        # buat object yang mau disimpan
        komenmasuk_baru = Komenmasuk(
             penindak=id_penindak,
             suratmasuk=id,
             isi_komenmasuk=isi_komenmasuk,
             tgl_komenmasuk=datetime.datetime.now().timestamp(),
             reply="[]"
             )
        
        #Buka koneksi ke datastore
        client = datastore.Client()
        # Minta dibuatkan key baru
        key_baru = client.key(KOMENMASUK_KIND)
        # Buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        # Isi data untuk entity baru
        entity_baru.update(komenmasuk_baru.ke_dictionary())
        # Simpan perubahan data entity baru
        client.put(entity_baru)
        # kembalikan pengaduan baru
        return Komenmasuk(id=entity_baru.id,
                    penindak=id_penindak,
                    suratmasuk=id,
                    isi_komenmasuk=entity_baru["isi_komenmasuk"],
                    tgl_komenmasuk=entity_baru["tgl_komenmasuk"],
                    reply=entity_baru["reply"]
                    )

def daftar():
    # Ambil daftar komen yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk komen
    query = client.query(kind=KOMENMASUK_KIND)
    # query untuk ambil seluruh data komen, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_komenmasuk = []
    for satu_hasil in hasil:
        satu_komenmasuk = Komenmasuk(id=satu_hasil.id,
                        isi_komenmasuk=satu_hasil["isi_komenmasuk"],
                        tgl_komenmasuk=satu_hasil["tgl_komenmasuk"],
                        reply=satu_hasil["reply"]
                        )

        # append atau add elemen ke list
        daftar_komenmasuk.append(satu_komenmasuk)
    # kembalikan array daftar komen
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
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_komenmasuk = []
        # buat objek komen
        komenmasuk = Komenmasuk(id=hasil.id,
                        isi_komenmasuk=hasil["isi_komenmasuk"],
                        tgl_komenmasuk=hasil["tgl_komenmasuk"],
                        reply=hasil["reply"]
                        )

        if(komenmasuk.tgl_komenmasuk != ""):
            komenmasuk.tgl_komenmasuk = datetime.datetime.fromtimestamp(float(komenmasuk.tgl_komenmasuk)).strftime('%d-%m-%y %H:%M')
        
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
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id}.")
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

        if(komenmasuk.tgl_komenmasuk != ""):
            komenmasuk.tgl_komenmasuk = datetime.datetime.fromtimestamp(float(komenmasuk.tgl_komenmasuk)).strftime('%d-%m-%y %H:%M')
        
        data_komenmasuk.append(komenmasuk.ke_dictionary())

        return data_komenmasuk

def caribysuratmasuk(id_suratmasuk):

    if id_suratmasuk is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        query = client.query(kind=KOMENMASUK_KIND).add_filter("suratmasuk", "=", str(id_suratmasuk))
        hasil = query.fetch()

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id_suratmasuk}.")
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

        for data in hasil:
            # buat objek komen
            komenmasuk = Komenmasuk(id=data.id,
                            suratmasuk=data["suratmasuk"],
                            penindak=data["penindak"],
                            isi_komenmasuk=data["isi_komenmasuk"],
                            tgl_komenmasuk=data["tgl_komenmasuk"],
                            reply=data["reply"]
                            )

            if(komenmasuk.tgl_komenmasuk != ""):
                komenmasuk.tgl_komenmasuk = datetime.datetime.fromtimestamp(float(komenmasuk.tgl_komenmasuk)).strftime('%d-%m-%y %H:%M')
   
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
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada suratmasuk dengan id: {id}.")

    try:
        if(data['tgl_komenmasuk'] != ""):
            data['tgl_komenmasuk'] = datetime.datetime.timestamp(datetime.datetime.strptime(data['tgl_komenmasuk'], '%d-%m-%y %H:%M'))
    except:
        pass

    # Simpan
    hasil.update(data)
    client.put(hasil)
    # kembalikan data suratmasuk
    return Komenmasuk(id=id)
        