from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException, EntityIdException
from aplikasi import app
from .model import MANAJEMEN_KIND, Manajemen
from .model import MANAJEMEN_KIND

def tambah(gmail):
    #tambah manajemen

    # cek parameter
    if gmail is not None:

        manajemen_baru = Manajemen(email=gmail)
        
        client = datastore.Client()

        key_baru = client.key(MANAJEMEN_KIND)

        entity_baru = datastore.Entity(key=key_baru)

        entity_baru.update(manajemen_baru.ke_dictionary())

        client.put(entity_baru)

        return Manajemen(id=entity_baru.id,
                        email=entity_baru["email"])

def daftar():
    # Ambil daftar admin yang telah terdaftar di datastore
    client = datastore.Client()
    # Buat query khusus untuk admin
    query= client.query(kind=MANAJEMEN_KIND)
    # query untuk ambil seluruh data admin, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_manajemen = []
    # app.logger.info("array manajemen")
    # app.logger.info(daftar_manajemen)
    for satu_hasil in hasil:
        # app.logger.info("isi dalam hasil")
        # app.logger.info(satu_hasil)
        satu_manajemen = Manajemen(id=satu_hasil.id,email=satu_hasil["email"])
        # app.logger.info("isi dalam satu manajemen")
        # app.logger.info(satu_manajemen)
        daftar_manajemen.append(satu_manajemen)
        # app.logger.info("isi dalam array manajemen sekarang")
        # app.logger.info(daftar_manajemen)
    # kembalikan array daftar admin
    return daftar_manajemen

def cari(id):
    if id is not None:
        """ Mencari satu admin berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_admin = client.key(MANAJEMEN_KIND, id)
        hasil = client.get(key_admin)
        
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada admin dengan id: {id}.")

        data_admin = []

        admin = Manajemen(  id=hasil.id,
                        email=hasil["email"])

        data_admin.append(admin.ke_dictionary())

        return data_admin

def cari_email(email):
    if email is not None:
        client = datastore.Client()

        # buat query filter email
        query = client.query(kind=MANAJEMEN_KIND)
        query.add_filter('email', '=', email)
        query.order = ['email']
        # ambil hasil filter
        hasil = query.fetch()

        # ubah hasil ke format yang kita butuhkan
        data_manajemen= []
        for satu_hasil_entity in hasil:
            satu_hasil = Manajemen(id=satu_hasil_entity.id,email=satu_hasil_entity["email"])
            # append atau add elemen ke list
            data_manajemen.append(satu_hasil)
        # kembalikan list 
        return data_manajemen

def ubah(id, manajemen_ubah):
    """ubah data admin berdasar id yg dikirim"""
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data admin berdasar property id
    key_manajemen = client.key(MANAJEMEN_KIND, id)
    # ambil hasil carinya
    hasil = client.get(key_manajemen)
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada Admin dengan id: {id}.")

    # Simpan
    hasil.update(manajemen_ubah)
    client.put(hasil)
    # kembalikan data admin
    return Manajemen(id=id,
                 email=hasil["email"]
                 )