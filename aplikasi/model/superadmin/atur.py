from aplikasi import app

from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import SUPERADMIN_KIND, Superadmin

def tambah(email):
    #tambah superadmin

    # cek parameter
    if email is not None:
        superadmin_baru = Superadmin(email=email)

        client = datastore.Client()
        key_baru = client.key(SUPERADMIN_KIND)
        entity_baru = datastore.Entity(key=key_baru)
        entity_baru.update(superadmin_baru.ke_dictionary())
        client.put(entity_baru)
        return Superadmin(id=entity_baru.id,email=entity_baru["email"])

def daftar():
    # Ambil daftar admin yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk admin
    query = client.query(kind=SUPERADMIN_KIND)
    # query untuk ambil seluruh data admin, hasilnya dalam iterator
    hasil = query.fetch()
    
    # ubah dalam format
    daftar_superadmin = []
    for satu_hasil in hasil:
        satu_superadmin = Superadmin(id=satu_hasil.id,email=satu_hasil["email"])

        daftar_superadmin.append(satu_superadmin)
    # kembalikan array daftar admin
    return daftar_superadmin


def cari(id):
    if id is not None:
        """ Mencari satu admin berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_superadmin = client.key(SUPERADMIN_KIND, id)
        hasil = client.get(key_superadmin)
        
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada admin dengan id: {id}.")

        return Superadmin(id=hasil.id,email=hasil["email"])

def cari_email(email):
    if email is not None:
        client = datastore.Client()

        # buat query filter email
        query = client.query(kind=SUPERADMIN_KIND)
        query.add_filter('email', '=', email)
        query.order = ['email']
        # ambil hasil filter
        hasil = query.fetch()

        # ubah hasil ke format yang kita butuhkan
        data_superadmin = []
        for satu_hasil_entity in hasil:
            satu_hasil = Superadmin(id=satu_hasil_entity.id,email=satu_hasil_entity["email"])
            # append atau add elemen ke list
            data_superadmin.append(satu_hasil)
        # kembalikan list 
        return data_superadmin

def hapus(id):
    # Hapus data dari datastore
    
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data admin berdasar property id
    key_superadmin = client.key(SUPERADMIN_KIND, id)
    # ambil hasil carinya
    hasil = client.get(key_superadmin)

    # Cek apakah id ditemukan
    if hasil is None:
        # Jika tidak ditemukan tampilkan exception
        raise EntityNotFoundException(f"Tidak ada Admin dengan id: {id}.")
    else:
        # Jika ditemukan hapus entitas
        client.delete(hasil.key)
    # Kembalikan kode 200
    return 200