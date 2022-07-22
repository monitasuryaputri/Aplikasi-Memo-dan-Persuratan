
from google.cloud import datastore

from tests.model.superadmin import SUPERADMIN_KIND, Superadmin

def tambah(email):
    #tambah superadmin

    # cek parameter
    if email is not None:
        # buat list 
        data_superadmin = []
        # buat object yang mau disimpan
        superadmin_baru = Superadmin(email=email)
        # append atau add elemen ke list
        data_superadmin.append(superadmin_baru.ke_dictionary())
        # kembalikan data staff
        return data_superadmin

def daftar():
    data_superadmin =  [{"id" : 6012551879983104,                            
                    "email" : "monita.sp@mhs.unsyiah.ac.id"
                    }]

    # buat list
    superadmin = []
    # iterate data superadmin, simpan ke list
    for satu_hasil in data_superadmin:
        satu_superadmin = Superadmin(id=satu_hasil["id"],
                                    email=satu_hasil["email"])
        #append atau add elemen ke list
        superadmin.append(satu_superadmin)
    # buat list
    daftar_superadmin = []
    # iterate superadmin, simpan ke list
    for satu_data in superadmin:
        # append atau add elemen ke list
        daftar_superadmin.append(satu_data.ke_dictionary())
    # kembalikan list daftar superadmin
    return daftar_superadmin


def cari(id):
    if id is not None:
        """ Mencari satu superadmin berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_superadmin = client.key(SUPERADMIN_KIND, id)
        hasil = client.get(key_superadmin)
        
        if hasil is None:
            raise (f"Tidak ada superadmin dengan id: {id}.")
        # ubah hasil ke format yang kita butuhkan
        data_superadmin = []
        # buat objek staff
        superadmin = Superadmin(id=hasil.id,
                                email=hasil["email"])
        # ubah format data ke dictionary dan append ke list
        data_superadmin.append(superadmin.ke_dictionary())                          
        return data_superadmin

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
            data_superadmin.append(satu_hasil.ke_dictionary())
        # kembalikan list 
        return data_superadmin
