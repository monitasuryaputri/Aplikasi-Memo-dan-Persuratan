from aplikasi import app

from aplikasi import model
from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException


from .model import STAFF_KIND, Staff

def tambah(nama, no_hp, email, jabatan):
    # tambah staff

    # cek parameter agar tidak kosong
    if nama and no_hp and email and jabatan is not None:
        # buat object yang mau disimpan
        staff_baru = Staff(nama=nama,
                           no_hp=no_hp,
                           email=email,
                           jabatan=jabatan)
                           
        # Buka koneksi ke datastore
        client = datastore.Client()
        # Minta dibuatkan key baru
        key_baru = client.key(STAFF_KIND)
        # Buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        # Isi data untuk entity baru
        entity_baru.update(staff_baru.ke_dictionary())
        # Simpan perubahan data entity baru
        client.put(entity_baru)
        # kembalikan staff baru
        return Staff(id=entity_baru.id,
                        nama=entity_baru["nama"], 
                        no_hp=entity_baru["no_hp"],
                        email=entity_baru["email"],
                        jabatan=entity_baru["jabatan"]
                        )

def daftar():
    # Ambil daftar staff yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk staff
    query = client.query(kind=STAFF_KIND)
    # query untuk ambil seluruh data staff, hasilnya dalam iterator
    hasil = query.fetch()

    # buat list
    daftar_staff = []

    # iterate data staff, simpan ke list
    for satu_hasil in hasil:
        satu_staff = Staff(id=satu_hasil.id,
                        nama=satu_hasil["nama"],
                        no_hp=satu_hasil["no_hp"],
                        email=satu_hasil["email"],
                        jabatan=satu_hasil["jabatan"])

        # append atau add elemen ke list
        daftar_staff.append(satu_staff)
    # kembalikan list daftar staff
    return daftar_staff

def daftarjabatan():
    # Ambil daftar staff yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk staff
    query = client.query(kind=STAFF_KIND)
    # query untuk ambil seluruh data staff, hasilnya dalam iterator
    hasil = query.fetch()

    # buat list
    daftar_staff = []
    
    # ambil daftar seluruh jabatan dari kind jabatan
    jabatan = model.jabatan.atur.daftar()

    # buat dictionary
    jabatan_nama = {}

    # iterasi data jabatan
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama

    # iterate data staff, simpan ke list
    for satu_hasil in hasil:
        satu_staff = Staff(id=satu_hasil.id,
                        nama=satu_hasil["nama"],
                        no_hp=satu_hasil["no_hp"],
                        email=satu_hasil["email"],
                        jabatan=jabatan_nama[satu_hasil["jabatan"]])

        # append atau add elemen ke list
        daftar_staff.append(satu_staff)
    # kembalikan list daftar staff
    return daftar_staff

def cari(id):
    if id is not None:
        """ Mencari satu staff berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_staff = client.key(STAFF_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_staff)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada staff dengan id: {id}.")
        # buat list
        data_staff = []
        # buat objek staff
        staff = Staff(id=hasil.id,
                      nama=hasil["nama"],
                      no_hp=hasil["no_hp"],
                      email=hasil["email"],
                      jabatan=hasil["jabatan"],
                      picture = hasil["picture"])
        # ubah format data ke dictionary dan append ke list
        data_staff.append(staff.ke_dictionary())
        return data_staff

def cari_email(email):
    if email is not None:
        """ Mencari satu staff berdasarkan email-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # buat query filter email
        query = client.query(kind=STAFF_KIND)
        query.add_filter('email','=',email)
        query.order = ['email']
        # ambil hasil filter
        hasil = query.fetch()

        # ubah hasil ke format yang dibutuhkan
        data_staff = []
        for satu_hasil_entity in hasil:
            satu_hasil = Staff(id=satu_hasil_entity.id,
                                    nama=satu_hasil_entity['nama'],
                                    no_hp=satu_hasil_entity['no_hp'],
                                    email=satu_hasil_entity['email'],
                                    jabatan=satu_hasil_entity['jabatan'])
            data_staff.append(satu_hasil.ke_dictionary())
        # kembalikan list data staff
        return data_staff

def hapus(id):
    # Hapus data dari datastore
    
    # Buka koneksi ke datastore
    client = datastore.Client()

    # Buat query baru khusus untuk staff
    key_staff = client.key(STAFF_KIND, id)
    # Jalankan query, hasilnya berupa iterator
    hasil = client.get(key_staff)

    # Cek apakah id ditemukan
    if hasil is None:
        # Jika tidak ditemukan tampilkan exception
        raise EntityNotFoundException(f"Tidak ada staff dengan id: {id}.")
    else:
        # Jika ditemukan hapus entitas
        client.delete(hasil.key)
    # Kembalikan kode 200
    return 200

def ubah(id, staff_ubah):

    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data staff berdasar property id
    key_staff = client.key(STAFF_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key_staff)
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada staff dengan id: {id}.")

    # Simpan
    hasil.update(staff_ubah)
    client.put(hasil)

    # kembalikan data staff
    return Staff(id=id,
                    nama=hasil["nama"],
                    no_hp=hasil["no_hp"],
                    email=hasil["email"],
                    jabatan=hasil["jabatan"],
                    picture=hasil["picture"])
    


   