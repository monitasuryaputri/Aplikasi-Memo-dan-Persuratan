from tests import model

from google.cloud import datastore

from tests.model.staff import STAFF_KIND, Staff

def tambah(nama, email, no_hp, jabatan):
    # tambah staff

    # cek parameter agar tidak kosong
    if nama and email and no_hp and jabatan is not None:
        # buat list 
        data_staff = []
        # buat object yang mau disimpan
        staff_baru = Staff(nama=nama,
                           no_hp=no_hp,
                           email=email,
                           jabatan=jabatan)
                           
        # append atau add elemen ke list
        data_staff.append(staff_baru.ke_dictionary())
        # kembalikan data staff
        return data_staff

def daftar():
    data_staff = [{"id" : 5636212517765120,                            
                        "nama" : "Annisa Surya Putri",
                        "email" : "anisasptri@gmail.com",
                        "no_hp" : "082265443325",
                        "jabatan" : "5731076903272448",
                        "picture" : "https://lh3.googleusercontent.com/a-/AOh14GiNrXYHezO1PbGCDMaH3J3vUM0D2N_9jFUhUV4UkQ=s96-c"
                    }]

    # buat list
    staff = []
    # iterate data staff, simpan ke list
    for satu_hasil in data_staff:
        satu_staff = Staff(id=satu_hasil["id"],
                            nama=satu_hasil["nama"],
                            email=satu_hasil["email"],
                            no_hp=satu_hasil["no_hp"],
                            jabatan=satu_hasil["jabatan"],
                            picture=satu_hasil["picture"])
        #append atau add elemen ke list
        staff.append(satu_staff)
    # buat list
    daftar_staff = []
    # iterate staff, simpan ke list
    for satu_data in staff:
        # append atau add elemen ke list
        daftar_staff.append(satu_data.ke_dictionary())
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
    
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
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
            raise (f"Tidak ada staff dengan id: {id}.")
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
                                nama=satu_hasil_entity["nama"],
                                email=satu_hasil_entity["email"],
                                no_hp=satu_hasil_entity["no_hp"],
                                jabatan=satu_hasil_entity["jabatan"],
                                picture = satu_hasil_entity["picture"])
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
        raise (f"Tidak ada staff dengan id: {id}.")
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
        raise (f"Tidak ada staff dengan id: {id}.")

    # Simpan
    hasil.update(staff_ubah)
    # buat list
    data_staff = []
    # buat objek staff
    staff_baru = Staff(id=id,
                       nama=hasil["nama"],
                       email=hasil["email"],
                       no_hp=hasil["no_hp"],
                       jabatan=hasil["jabatan"],
                       picture=hasil["picture"])
    # append atau add elemen ke list
    data_staff.append(staff_baru.ke_dictionary())
    # kembalikan data staff 
    return data_staff

    


   