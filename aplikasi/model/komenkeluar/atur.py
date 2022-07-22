""" Controller untuk Komen Keluar

Deskripsi method:
tambah              :untuk membuat entitas baru
daftar              :untuk select semua entitas yg terdaftar pada datastore
cari                :untuk cari/filter data entitas berdasarkan property id
caribykomenkeluar   :untuk cari/filter data entitas berdasarkan property komen keluar
caribysuratkeluar   :untuk cari/filter data entitas berdasarkan property surat keluar
update              :untuk ubah data salah satu entitas berdasarkan property id

"""

from aplikasi import app, model, CLOUD_STORAGE_BUCKET

import datetime
from google.cloud import datastore, storage
from aplikasi.model.exception import EntityNotFoundException

from .model import KOMENKELUAR_KIND, Komenkeluar
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id_penindak, id, nomor_surat, isi_komenkeluar, file_komenkeluar):
    #tambah komen

    # cek parameter
    if isi_komenkeluar is not None:

        # upload ke storage
        # Create a Cloud Storage client.
        gcs = storage.Client()
        
        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        # simpan file dengan format nomor surat/file
        url_list = []
        for dokumen_data in file_komenkeluar:
            dokumen_data_blob  =bucket.blob('Surat Keluar/' + nomor_surat+'/'+dokumen_data.filename)

        # proses upload file
            dokumen_data_blob.upload_from_string(
                    dokumen_data.read(),
                    content_type=dokumen_data.content_type
            )
        
        # ambil link public_url buat disimpan ke datastore
            url_list += [{
                    "name" : dokumen_data.filename,
                    "url" : dokumen_data_blob.public_url
            }]
        

        # buat object yang mau disimpan
        komenkeluar_baru = Komenkeluar(
             penindak=id_penindak,
             suratkeluar=id,
             isi_komenkeluar=isi_komenkeluar,
             tgl_komenkeluar=datetime.datetime.now().timestamp(),
             file_komenkeluar=url_list,
             reply="[]"
             )
        
        #Buka koneksi ke datastore
        client = datastore.Client()
        # Minta dibuatkan key baru
        key_baru = client.key(KOMENKELUAR_KIND)
        # Buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        # Isi data untuk entity baru
        entity_baru.update(komenkeluar_baru.ke_dictionary())
        # Simpan perubahan data entity baru
        client.put(entity_baru)
        # kembalikan pengaduan baru
        return Komenkeluar(id=entity_baru.id,
                    penindak=id_penindak,
                    suratkeluar=id,
                    isi_komenkeluar=entity_baru["isi_komenkeluar"],
                    tgl_komenkeluar=entity_baru["tgl_komenkeluar"],
                    file_komenkeluar=entity_baru["file_komenkeluar"],
                    reply=entity_baru["reply"]
                    )

def daftar():
    # Ambil daftar komen yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk komen
    query = client.query(kind=KOMENKELUAR_KIND)
    # query untuk ambil seluruh data komen, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_komenkeluar = []
    for satu_hasil in hasil:
        satu_komenkeluar = Komenkeluar(id=satu_hasil.id,
                        isi_komenkeluar=satu_hasil["isi_komenkeluar"],
                        tgl_komenkeluar=satu_hasil["tgl_komenkeluar"],
                        file_komenkeluar=satu_hasil["file_komenkeluar"],
                        reply=satu_hasil["reply"]
                        )

        # append atau add elemen ke list
        daftar_komenkeluar.append(satu_komenkeluar)
    # kembalikan array daftar komen
    return daftar_komenkeluar


def cari(id):
    if id is not None:
        """ Mencari satu pengaduan berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_komenkeluar = client.key(KOMENKELUAR_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_komenkeluar)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_komenkeluar = []
        # buat objek komen
        komenkeluar = Komenkeluar(id=hasil.id,
                        isi_komenkeluar=hasil["isi_komenkeluar"],
                        tgl_komenkeluar=hasil["tgl_komenkeluar"],
                        file_komenkeluar=hasil["file_komenkeluar"],
                        reply=hasil["reply"]
                        )

        if(komenkeluar.tgl_komenkeluar != ""):
            komenkeluar.tgl_komenkeluar = datetime.datetime.fromtimestamp(float(komenkeluar.tgl_komenkeluar)).strftime('%d-%m-%y %H:%M')

        # ubah format data ke dictionary dan append ke list
        data_komenkeluar.append(komenkeluar.ke_dictionary())
        return data_komenkeluar
        
def caribykomenkeluar(id_suratkeluar, id):

    if id is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_komenkeluar = client.key(KOMENKELUAR_KIND, id)
        
        #  ambil hasil carinya
        hasil = client.get(key_komenkeluar)
        
        
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_komenkeluar = []
        
        # buat objek komen
        komenkeluar = Komenkeluar(id=hasil.id,
                        suratkeluar=hasil["suratkeluar"],
                        penindak=hasil["penindak"],
                        isi_komenkeluar=hasil["isi_komenkeluar"],
                        tgl_komenkeluar=hasil["tgl_komenkeluar"],
                        file_komenkeluar=hasil["file_komenkeluar"],
                        reply=hasil["reply"]
                        )

        if(komenkeluar.tgl_komenkeluar != ""):
            komenkeluar.tgl_komenkeluar = datetime.datetime.fromtimestamp(float(komenkeluar.tgl_komenkeluar)).strftime('%d-%m-%y %H:%M')
        
        data_komenkeluar.append(komenkeluar.ke_dictionary())

        return data_komenkeluar

def caribysuratkeluar(id_suratkeluar):

    if id_suratkeluar is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        query = client.query(kind=KOMENKELUAR_KIND).add_filter("suratkeluar", "=", str(id_suratkeluar))
        hasil = query.fetch()

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id_suratkeluar}.")
        # buat list
        data_komenkeluar = []

        ad = list_ad()
        list_of_ad = [id for elem in ad
                        for id in elem.values()]
        ka = list_ka()
        list_of_ka = [id for elem in ka
                        for id in elem.values()]
        st = list_st()
        list_of_st = [id for elem in st
                        for id in elem.values()]

        for data in hasil:
           
            # buat objek komen
            komenkeluar = Komenkeluar(id=data.id,
                            suratkeluar=data["suratkeluar"],
                            penindak=data["penindak"],
                            isi_komenkeluar=data["isi_komenkeluar"],
                            tgl_komenkeluar=data["tgl_komenkeluar"],
                            file_komenkeluar=data["file_komenkeluar"],
                            reply=data["reply"]
                            )

            if(komenkeluar.tgl_komenkeluar != ""):
                komenkeluar.tgl_komenkeluar = datetime.datetime.fromtimestamp(float(komenkeluar.tgl_komenkeluar)).strftime('%d-%m-%y %H:%M')
   
            # ubah format data ke dictionary dan append ke list
            res = komenkeluar.ke_dictionary()
            
            if data["penindak"] in list_of_ka:
                cari = model.kepalaupt.atur.cari(data["penindak"])
                if len(cari) == 1 :
                    cari = cari[0] 

                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penindak_komentar'] = cari

            elif data["penindak"] in list_of_ad:
                cari = model.admin.atur.cari(data["penindak"])
                if len(cari) == 1 :
                    cari = cari[0] 
                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penindak_komentar'] = cari

            elif data["penindak"] in list_of_st:
                cari = model.staff.atur.cari(data["penindak"])
                if len(cari) == 1 :
                    cari = cari[0] 

                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penindak_komentar'] = cari
            
            data_komenkeluar.append(res)

        return data_komenkeluar
    
def update(id, data):

    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data suratmasuk berdasar property id
    key = client.key(KOMENKELUAR_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key)
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada suratkeluar dengan id: {id}.")

    try:
        if(data['tgl_komenkeluar'] != ""):
            data['tgl_komenkeluar'] = datetime.datetime.timestamp(datetime.datetime.strptime(data['tgl_komenkeluar'], '%d-%m-%y %H:%M'))

    except:
        pass

    # Simpan
    hasil.update(data)
    client.put(hasil)
    # kembalikan data suratkeluar
    return Komenkeluar(id=id)