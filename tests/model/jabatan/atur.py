from google.cloud import datastore

from tests.model.jabatan import JABATAN_KIND, Jabatan

def tambah(nama):
    #tambah jabatan

    # cek parameter
    if nama is not None:
        # buat list 
        data_jabatan = []
        # buat object yang mau disimpan
        jabatan_baru = Jabatan(nama=nama)
        # append atau add elemen ke list
        data_jabatan.append(jabatan_baru.ke_dictionary())
        # kembalikan data jabatan
        return data_jabatan

def daftar():
    data_jabatan = [{"id" : 5077688091934720,                            
                            "nama" : "kepala upt laboratorium"
                            }]
    # buat list
    jabatan = []
    # iterate data jabatan, simpan ke list
    for satu_hasil in data_jabatan:
        satu_jabatan = Jabatan(id=satu_hasil["id"],
                                nama=satu_hasil["nama"])
        # append atau add elemen ke list
        jabatan.append(satu_jabatan)
    # buat list
    daftar_jabatan = []
    # iterate data jabatan, simpan ke list
    for satu_data in jabatan:
        # append atau add elemen ke list
        daftar_jabatan.append(satu_data.ke_dictionary())
    # kembalikan array daftar jabatan
    return daftar_jabatan

def disposisi():
    data_jabatan = [{"id" : 5077688091934720,                            
                            "nama" : "kepala upt laboratorium"
                            }]
    # buat list
    jabatan = []
    # iterate data jabatan, simpan ke list
    for satu_hasil in data_jabatan:
        if satu_hasil["nama"] == "admin":
            continue
        satu_jabatan = Jabatan(id=satu_hasil["id"],
                                nama=satu_hasil["nama"])
        # append atau add elemen ke list
        jabatan.append(satu_jabatan)
    # buat list
    daftar_jabatan = []
    # iterate data jabatan, simpan ke list
    for satu_data in jabatan:
        # append atau add elemen ke list
        daftar_jabatan.append(satu_data.ke_dictionary())
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
            raise (f"Tidak ada jabatan dengan id: {id}.")
        data_jabatan = []
        jabatan = Jabatan(id=hasil.id,nama=hasil["nama"])
        # ubah format data ke dictionary dan append ke list
        data_jabatan.append(jabatan.ke_dictionary())                          
        return data_jabatan

def cari_nama(nama):
    if nama is not None:
         # Buka koneksi ke datastore
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
            data_jabatan.append(satu_hasil.ke_dictionary())
        # kembalikan list 
        return data_jabatan
