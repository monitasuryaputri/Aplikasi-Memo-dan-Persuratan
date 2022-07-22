""" Controller untuk Kepala UPT
Deklarasi method 
tambah      :untuk membuat entitas baru
daftar      :untuk select semua entitas yg terdaftar pada datastore
hapus       :untuk hapus salah satu entitas berdasarkan property id
ubah        :untuk ubah data salah satu entitas berdasarkan property id
cari        :untuk cari/filter data entitas berdasarkan property id
cari_email  :untuk cari/filter data entitas berdasarkan property email
"""

from aplikasi import model, app

from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import KEPALAUPT_KIND, Kepalaupt
from aplikasi.model.staff import STAFF_KIND


def tambah(nama, email, no_hp, jabatan):
    #tambah kepalaupt

    # cek parameter agar tidak kosong
    if nama and email and no_hp and jabatan is not None:
        #buat objek yang mau disimpan
        kepalaupt_baru = Kepalaupt(nama=nama,
                                   no_hp=no_hp,
                                   email=email,
                                   jabatan=jabatan)

        #buka koneksi ke datastore
        client = datastore.Client()
        #minta dibuatkan key baru
        key_baru = client.key(KEPALAUPT_KIND)
        #buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        #isi data untuk entity baru
        entity_baru.update(kepalaupt_baru.ke_dictionary())
        #simpan perubahan data entity baru
        client.put(entity_baru)
        #kembalikan kepalaupt baru
        return Kepalaupt(   id=entity_baru.id,
                        nama=entity_baru["nama"],
                        email=entity_baru["email"],
                        no_hp=entity_baru["no_hp"],
                        jabatan=entity_baru["jabatan"])

def daftar():
    # Ambil daftar kepalaupt yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk kepalaupt
    query = client.query(kind=KEPALAUPT_KIND)
    # query untuk ambil seluruh data kepalaupt, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_kepalaupt = []

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama

    for satu_hasil in hasil:
        satu_kepalaupt = Kepalaupt( id=satu_hasil.id,
                            nama=satu_hasil["nama"],
                            email=satu_hasil["email"],
                            no_hp=satu_hasil["no_hp"],
                            jabatan=jabatan_nama[satu_hasil["jabatan"]])

        #append atau add elemen ke list
        daftar_kepalaupt.append(satu_kepalaupt)
    # kembalikan list daftar kepalaupt
    return daftar_kepalaupt

def daftarjabatan():
    # Ambil daftar kepalaupt yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk kepalaupt
    query = client.query(kind=KEPALAUPT_KIND)
    # query untuk ambil seluruh data kepalaupt, hasilnya dalam iterator
    hasil = query.fetch()

    # buat list
    daftar_kepalaupt = []
    
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama

    # iterate data kepalaupt, simpan ke list
    for satu_hasil in hasil:
        satu_kepalaupt = Kepalaupt(id=satu_hasil.id,
                        nama=satu_hasil["nama"],
                        no_hp=satu_hasil["no_hp"],
                        email=satu_hasil["email"],
                        jabatan=jabatan_nama[satu_hasil["jabatan"]])

        # append atau add elemen ke list
        daftar_kepalaupt.append(satu_kepalaupt)
    # kembalikan list daftar kepalaupt
    return daftar_kepalaupt

def cari(id):
    if id is not None:
        """ Mencari satu kepalaupt berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_kepalaupt = client.key(KEPALAUPT_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_kepalaupt)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada kepalaupt dengan id: {id}.")
        # buat list
        data_kepalaupt = []
        # buat objek kepalaupt
        kepalaupt = Kepalaupt(id=hasil.id,
                             nama=hasil["nama"],
                             no_hp=hasil["no_hp"],
                             email=hasil["email"],
                             jabatan=hasil["jabatan"],
                             picture = hasil["picture"])

        data_kepalaupt.append(kepalaupt.ke_dictionary())
        return data_kepalaupt

def cari_email(email):
    if email is not None:
        client = datastore.Client()

        # buat query filter email
        query = client.query(kind=KEPALAUPT_KIND)
        query.add_filter('email', '=', email)
        query.order = ['email']
        # ambil hasil filter
        hasil = query.fetch()

        # ubah hasil ke format yang kita butuhkan
        data_kepalaupt = []
        for satu_hasil_entity in hasil:
            satu_hasil = Kepalaupt( id=satu_hasil_entity.id,
                                nama=satu_hasil_entity["nama"],
                                email=satu_hasil_entity["email"],
                                no_hp=satu_hasil_entity["no_hp"],
                                jabatan=satu_hasil_entity["jabatan"])
            # append atau add elemen ke list
            data_kepalaupt.append(satu_hasil.ke_dictionary())
        # kembalikan list 
        return data_kepalaupt

def hapus(id):
    # Hapus data dari datastore
    
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data kepalaupt berdasar property id
    key_kepalaupt = client.key(KEPALAUPT_KIND, id)
    # ambil hasil carinya
    hasil = client.get(key_kepalaupt)

    # Cek apakah id ditemukan
    if hasil is None:
        # Jika tidak ditemukan tampilkan exception
        raise EntityNotFoundException(f"Tidak ada Kepalaupt dengan id: {id}.")
    else:
        # Jika ditemukan hapus entitas
        client.delete(hasil.key)
    # Kembalikan kode 200
    return 200
    
def ubah(id, kepalaupt_ubah):
    """ubah data kepalaupt berdasar id yg dikirim"""
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data kepalaupt berdasar property id
    key_kepalaupt = client.key(KEPALAUPT_KIND, id)
    # ambil hasil carinya
    hasil = client.get(key_kepalaupt)
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada Kepalaupt dengan id: {id}.")

    # Simpan
    hasil.update(kepalaupt_ubah)
    client.put(hasil)

    # kembalikan data kepalaupt
    return Kepalaupt(id=id,
                    nama=hasil["nama"],
                    no_hp=hasil["no_hp"],
                    email=hasil["email"],
                    jabatan=hasil["jabatan"],
                    picture=hasil["picture"])
