from tests import model

from google.cloud import datastore

from tests.model.admin import ADMIN_KIND, Admin

def tambah(nama, email, no_hp, jabatan):
    #tambah admin

    # cek parameter agar tidak kosong
    if nama and email and no_hp and jabatan is not None:
        # buat list 
        data_admin = []
        #buat objek yang mau disimpan
        admin_baru = Admin( nama=nama,
                            email=email,
                            no_hp=no_hp,
                            jabatan=jabatan)
        # append atau add elemen ke list
        data_admin.append(admin_baru.ke_dictionary())
        # kembalikan data admin
        return data_admin

def daftar():
    data_admin = [{"id" : 6221596528214016,                            
                    "nama" : "Monita Surya Putri",
                    "email" : "monitasurya@gmail.com",
                    "no_hp" : "123456789",
                    "jabatan" : "5630815723585536",
                    "picture" : "https://lh3.googleusercontent.com/a/AATXAJwgSAduYV8vTxSL5CA7UOxv_DI2zvcTZVvYCeHZ=s96-c"
                    }]
    # buat list
    admin = []
    # iterate data admin, simpan ke list
    for satu_hasil in data_admin:
        satu_admin = Admin( id=satu_hasil["id"],
                            nama=satu_hasil["nama"],
                            email=satu_hasil["email"],
                            no_hp=satu_hasil["no_hp"],
                            jabatan=satu_hasil["jabatan"],
                            picture=satu_hasil["picture"])

        #append atau add elemen ke list
        admin.append(satu_admin)
    # buat list
    daftar_admin = []
    # iterate admin, simpan ke list
    for satu_data in admin:
        # append atau add elemen ke list
        daftar_admin.append(satu_data.ke_dictionary())
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
            raise (f"Tidak ada admin dengan id: {id}.")

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
                                jabatan=satu_hasil_entity["jabatan"],
                                picture = satu_hasil_entity["picture"])
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
        raise (f"Tidak ada Admin dengan id: {id}.")
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
        raise (f"Tidak ada Admin dengan id: {id}.")

    # Simpan
    hasil.update(admin_ubah)
    # buat list
    data_admin = []
    # buat objek admin
    admin_baru = Admin(id=id,
                       nama=hasil["nama"],
                       email=hasil["email"],
                       no_hp=hasil["no_hp"],
                       jabatan=hasil["jabatan"],
                       picture=hasil["picture"])
    # append atau add elemen ke list
    data_admin.append(admin_baru.ke_dictionary())
    # kembalikan data admin
    return data_admin
