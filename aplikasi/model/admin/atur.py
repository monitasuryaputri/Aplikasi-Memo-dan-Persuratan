""" Controller untuk model Admin

Deklarasi method:

tambah          : untuk menambah entitas baru
daftar          : untuk select semua entitas yang terdaftar pada datastore
daftar_jabatan  : untuk menampung/mengambil seluruh jabatan yang terdaftar di datastore
cari(id)        : untuk cari data entitas berdasarkan properti id
cari_email      : untuk cari data entitas berdasarkan properti email
hapus           : untuk menghapus data dari datastore
ubah            : untuk mengubah data admin berdasarkan id yang dikirim

"""

from aplikasi import model

from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import ADMIN_KIND, Admin

def tambah(nama, email, no_hp, jabatan):
    #tambah admin
    
    # cek parameter agar tidak kosong
    if nama and email and no_hp and jabatan is not None:
        #buat objek yang mau disimpan
        admin_baru = Admin( nama=nama,
                            email=email,
                            no_hp=no_hp,
                            jabatan=jabatan)

        #buka koneksi ke datastore
        client = datastore.Client()
        #minta dibuatkan key baru
        key_baru = client.key(ADMIN_KIND)
        #buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        #isi data untuk entity baru
        entity_baru.update(admin_baru.ke_dictionary())
        #simpan perubahan data entity baru
        client.put(entity_baru)
        #kembalikan admin baru
        return Admin(   id=entity_baru.id,
                        nama=entity_baru["nama"],
                        email=entity_baru["email"],
                        no_hp=entity_baru["no_hp"],
                        jabatan=entity_baru["jabatan"])

def daftar():
    # Ambil daftar admin yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk admin
    query = client.query(kind=ADMIN_KIND)
    # query untuk ambil seluruh data admin, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_admin = []

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama

    for satu_hasil in hasil:
        satu_admin = Admin( id=satu_hasil.id,
                            nama=satu_hasil["nama"],
                            email=satu_hasil["email"],
                            no_hp=satu_hasil["no_hp"],
                            jabatan=jabatan_nama[satu_hasil["jabatan"]])

        #append atau add elemen ke list
        daftar_admin.append(satu_admin)
    # kembalikan list daftar admin
    return daftar_admin

def daftarjabatan():
    # Ambil daftar admin yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk admin
    query = client.query(kind=ADMIN_KIND)
    # query untuk ambil seluruh data admin, hasilnya dalam iterator
    hasil = query.fetch()

    # buat list
    daftar_admin = []
    
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama

    # iterate data admin, simpan ke list
    for satu_hasil in hasil:
        satu_admin = Admin(id=satu_hasil.id,
                        nama=satu_hasil["nama"],
                        no_hp=satu_hasil["no_hp"],
                        email=satu_hasil["email"],
                        jabatan=jabatan_nama[satu_hasil["jabatan"]])

        # append atau add elemen ke list
        daftar_admin.append(satu_admin)
    # kembalikan list daftar admin
    return daftar_admin

def cari(id):
    if id is not None:
        """ Mencari satu admin berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_admin = client.key(ADMIN_KIND, id)
        hasil = client.get(key_admin)
        
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada admin dengan id: {id}.")

        data_admin = []

        admin = Admin(  id=hasil.id,
                        nama=hasil["nama"],
                        email=hasil["email"],
                        no_hp=hasil["no_hp"],
                        jabatan=hasil["jabatan"],
                        picture = hasil["picture"])

        data_admin.append(admin.ke_dictionary())
        return data_admin

def cari_email(email):
    if email is not None:
        client = datastore.Client()

        # buat query filter email
        query = client.query(kind=ADMIN_KIND)
        query.add_filter('email', '=', email)
        query.order = ['email']
        # ambil hasil filter
        hasil = query.fetch()

        # ubah hasil ke format yang kita butuhkan
        data_admin = []
        for satu_hasil_entity in hasil:
            satu_hasil = Admin( id=satu_hasil_entity.id,
                                nama=satu_hasil_entity["nama"],
                                email=satu_hasil_entity["email"],
                                no_hp=satu_hasil_entity["no_hp"],
                                jabatan=satu_hasil_entity["jabatan"])
            # append atau add elemen ke list
            data_admin.append(satu_hasil.ke_dictionary())
        # kembalikan list 
        return data_admin

def hapus(id):
    # Hapus data dari datastore
    
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data admin berdasar property id
    key_admin = client.key(ADMIN_KIND, id)
    # ambil hasil carinya
    hasil = client.get(key_admin)

    # Cek apakah id ditemukan
    if hasil is None:
        # Jika tidak ditemukan tampilkan exception
        raise EntityNotFoundException(f"Tidak ada Admin dengan id: {id}.")
    else:
        # Jika ditemukan hapus entitas
        client.delete(hasil.key)
    # Kembalikan kode 200
    return 200
    
def ubah(id, admin_ubah):
    """ubah data admin berdasar id yg dikirim"""
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data admin berdasar property id
    key_admin = client.key(ADMIN_KIND, id)
    # ambil hasil carinya
    hasil = client.get(key_admin)
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada Admin dengan id: {id}.")

    # Simpan
    hasil.update(admin_ubah)
    client.put(hasil)
    # kembalikan data admin
    return Admin(id=id,
                 nama=hasil["nama"],
                 email=hasil["email"],
                 no_hp=hasil["no_hp"],
                 jabatan=hasil["jabatan"],
                 picture=hasil["picture"])
