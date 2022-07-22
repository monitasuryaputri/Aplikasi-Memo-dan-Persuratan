""" Controller untuk jabatan

Deklarasi method:

tambah      : untuk menambah entitas pada datastore
daftar      : untuk select semua entitas yang terdaftar pada datastore
disposisi   : untuk memilih daftar jabatan pada datastore
cari        : untuk mencari entitas jawbatan berdasarkan id
cari_nama   : untuk mencari entitas jabatan berdasarkan nama jabatan

"""

from aplikasi import app
from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import JABATAN_KIND, Jabatan

def tambah(nama):
    #tambah jabatan

    # cek parameter
    if nama is not None:
        jabatan_baru = Jabatan(nama=nama)

        client = datastore.Client()
        key_baru = client.key(JABATAN_KIND)
        entity_baru = datastore.Entity(key=key_baru)
        entity_baru.update(jabatan_baru.ke_dictionary())
        client.put(entity_baru)
        return Jabatan(id=entity_baru.id,nama=entity_baru["nama"])

def daftar():
    # Ambil daftar jabatan yang telah terdaftar di datastore
    client = datastore.Client()
    # Buat query khusus untuk jabatan
    query = client.query(kind=JABATAN_KIND)
    # query untuk ambil seluruh data jabatan, hasilnya dalam iterator
    hasil = query.fetch()
    # ubah dalam format
    daftar_jabatan = []
    for satu_hasil in hasil:
        satu_jabatan = Jabatan(id=satu_hasil.id,
                            nama=satu_hasil["nama"])

        daftar_jabatan.append(satu_jabatan)

    # kembalikan array daftar jabatan
    return daftar_jabatan

def disposisi():
    # Ambil daftar jabatan yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk jabatan
    query = client.query(kind=JABATAN_KIND)
    # query untuk ambil seluruh data jabatan, hasilnya dalam iterator
    hasil = query.fetch()
    # ubah dalam format
    daftar_jabatan = []
    for satu_hasil in hasil:
        if satu_hasil["nama"] == "admin":
            continue
        satu_jabatan = Jabatan(id=satu_hasil.id,
                            nama=satu_hasil["nama"])

        daftar_jabatan.append(satu_jabatan)

    # kembalikan array daftar jabatan
    return daftar_jabatan

def cari(id):
    if id is not None:
        """ Mencari satu jabatan berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_jabatan = client.key(JABATAN_KIND, id)
        hasil = client.get(key_jabatan)
        
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada jabatan dengan id: {id}.")

        return Jabatan(id=hasil.id,nama=hasil["nama"])

def cari_nama(nama):
    if nama is not None:
        client = datastore.Client()

        # buat query filter nama
        query = client.query(kind=JABATAN_KIND)
        query.add_filter('nama', '=', nama)
        query.order = ['nama']
        # ambil hasil filter
        hasil = query.fetch()

        # ubah hasil ke format yang kita butuhkan
        data_jabatan = []
        for satu_hasil_entity in hasil:
            satu_hasil = Jabatan(id=satu_hasil_entity.id,nama=satu_hasil_entity["nama"])
            # append atau add elemen ke list
            data_jabatan.append(satu_hasil)
        # kembalikan list 
        return data_jabatan
