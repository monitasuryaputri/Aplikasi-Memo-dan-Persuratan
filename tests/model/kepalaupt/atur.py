from tests import model

from google.cloud import datastore

from tests.model.kepalaupt import KEPALAUPT_KIND, Kepalaupt

def tambah(nama, email, no_hp, jabatan):
    #tambah kepalaupt

    # cek parameter agar tidak kosong
    if nama and email and no_hp and jabatan is not None:
        # buat list 
        data_kepalaupt = []
        #buat objek yang mau disimpan
        kepalaupt_baru = Kepalaupt(nama=nama,
                                   no_hp=no_hp,
                                   email=email,
                                   jabatan=jabatan)

        # append atau add elemen ke list
        data_kepalaupt.append(kepalaupt_baru.ke_dictionary())
        # kembalikan data kepala upt
        return data_kepalaupt

def daftar():
    data_kepalaupt = [{"id" : 5105697184284672,                            
                        "nama" : "Monita Surya",
                        "email" : "monitasuryaputrii@gmail.com",
                        "no_hp" : "08116822256",
                        "jabatan" : "5077688091934720",
                        "picture" : "https://lh3.googleusercontent.com/a/AATXAJwnHo6bP-IexqmEdQv4m46DZ_ftzSWl3DuxivOZ=s96-c"
                      }]

    # buat list
    kepalaupt = []
    # iterate data kepalaupt, simpan ke list
    for satu_hasil in data_kepalaupt:
        satu_kepalaupt = Kepalaupt( id=satu_hasil["id"],
                                    nama=satu_hasil["nama"],
                                    email=satu_hasil["email"],
                                    no_hp=satu_hasil["no_hp"],
                                    jabatan=satu_hasil["jabatan"],
                                    picture=satu_hasil["picture"])
        #append atau add elemen ke list
        kepalaupt.append(satu_kepalaupt)
    # buat list
    daftar_kepalaupt = []
    # iterate kepalaupt, simpan ke list
    for satu_data in kepalaupt:
        # append atau add elemen ke list
        daftar_kepalaupt.append(satu_data.ke_dictionary())
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
            raise (f"Tidak ada kepalaupt dengan id: {id}.")
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
                                jabatan=satu_hasil_entity["jabatan"],
                                picture = satu_hasil_entity["picture"])
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
        raise (f"Tidak ada Kepalaupt dengan id: {id}.")
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
        raise (f"Tidak ada Kepalaupt dengan id: {id}.")

    # Simpan
    hasil.update(kepalaupt_ubah)
    # buat list
    data_kepalaupt = []
    # buat objek kepala upt
    kepalaupt_baru = Kepalaupt(id=id,
                       nama=hasil["nama"],
                       email=hasil["email"],
                       no_hp=hasil["no_hp"],
                       jabatan=hasil["jabatan"],
                       picture=hasil["picture"])
    # append atau add elemen ke list
    data_kepalaupt.append(kepalaupt_baru.ke_dictionary())
    # kembalikan data kepala upt 
    return data_kepalaupt
