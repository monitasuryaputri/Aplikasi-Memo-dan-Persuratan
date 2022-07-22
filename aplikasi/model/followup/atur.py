""" Controller untuk model follow up

Deklarasi method:

tambah              : untuk membuat entitas baru 
daftar              : untuk select semua entitas yang terdaftar pada datastore
cari                : untuk mencari entitas tindak lanjut berdasarkan id
caribytindaklanjut  : untuk mencari entitas berdasarkan tindaklanjut

"""


from aplikasi import app, model, CLOUD_STORAGE_BUCKET

from flask import json
import datetime
from google.cloud import datastore, storage
from aplikasi.model.exception import EntityNotFoundException

from .model import FOLLOWUP_KIND, Followup
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id_penanggungjawab, id, isi_followup, file_followup):
    #tambah followup

    # cek parameter
    if isi_followup is not None:


        # upload ke storage
        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        url_list = []
        for file_followup_data in file_followup:
            file_followup_data_blob  =bucket.blob('followup/' +file_followup_data.filename)

            file_followup_data_blob.upload_from_string(
                file_followup_data.read(),
                content_type=file_followup_data.content_type
            )

            url_list += [{
                "name" : file_followup_data.filename,
                "url" : file_followup_data_blob.public_url
            }]

        # buat object yang mau disimpan
        followup_baru = Followup(
             penanggungjawab=id_penanggungjawab,
             tindaklanjut=id,
             isi_followup=isi_followup,
             file_followup=json.dumps(url_list),
             tgl_followup=datetime.datetime.now().timestamp()
             )
        
        #Buka koneksi ke datastore
        client = datastore.Client()
        # Minta dibuatkan key baru
        key_baru = client.key(FOLLOWUP_KIND)
        # Buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        # Isi data untuk entity baru
        entity_baru.update(followup_baru.ke_dictionary())
        # Simpan perubahan data entity baru
        client.put(entity_baru)
        # kembalikan tindaklanjut baru
        return Followup(id=entity_baru.id,
                    penanggungjawab=id_penanggungjawab,
                    tindaklanjut=id,
                    isi_followup=entity_baru["isi_followup"],
                    file_followup=entity_baru["file_followup"],
                    tgl_followup=entity_baru["tgl_followup"]
                    )

def daftar():
    # Ambil daftar followup yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk followup
    query = client.query(kind=FOLLOWUP_KIND)
    # query untuk ambil seluruh data followup, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_followup = []
    for satu_hasil in hasil:
        satu_followup = Followup(id=satu_hasil.id,
                        isi_followup=satu_hasil["isi_followup"],
                        file_followup=satu_hasil["file_followup"],
                        tgl_followup=satu_hasil["tgl_followup"]
                        )

        # append atau add elemen ke list
        daftar_followup.append(satu_followup)
    # kembalikan array daftar followup
    return daftar_followup


def cari(id):
    if id is not None:
        """ Mencari satu tindaklanjut berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_followup = client.key(FOLLOWUP_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_followup)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada followup dengan id: {id}.")
        # buat list
        data_followup = []
        # buat objek followup
        followup = Followup(id=hasil.id,
                        isi_followup=hasil["isi_followup"],
                        file_followup=hasil["file_followup"],
                        tgl_followup=hasil["tgl_followup"]
                        )

        if(followup.tgl_followup != ""):
            followup.tgl_followup = datetime.datetime.fromtimestamp(float(followup.tgl_followup)).strftime('%d-%m-%y %H:%M')


        try:
            followup.file_followup = json.loads(followup.file_followup)
        except:
            pass
        
        # ubah format data ke dictionary dan append ke list
        data_followup.append(followup.ke_dictionary())
        return data_followup

def caribytindaklanjut(id_tindaklanjut):

    if id_tindaklanjut is not None:
        """ Mencari satu tindaklanjut berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        query = client.query(kind=FOLLOWUP_KIND).add_filter("tindaklanjut", "=", str(id_tindaklanjut))
        hasil = query.fetch()

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada followup dengan id: {id_tindaklanjut}.")
        # buat list
        data_followup = []

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
           
            # buat objek followup
            followup = Followup(id=data.id,
                            tindaklanjut=data["tindaklanjut"],
                            penanggungjawab=data["penanggungjawab"],
                            isi_followup=data["isi_followup"],
                            file_followup=data["file_followup"],
                            tgl_followup=data["tgl_followup"]
                            )

            if(followup.tgl_followup != ""):
                followup.tgl_followup = datetime.datetime.fromtimestamp(float(followup.tgl_followup)).strftime('%d-%m-%y %H:%M')

            try:
                followup.file_followup = json.loads(followup.file_followup)
            except:
                pass
            
            # ubah format data ke dictionary dan append ke list
            res = followup.ke_dictionary()
            
            if data["penanggungjawab"] in list_of_ka:
                cari = model.kepalaupt.atur.cari(data["penanggungjawab"])
                if len(cari) == 1 :
                    cari = cari[0] 
                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penanggungjawab_tindaklanjut'] = cari

            elif data["penanggungjawab"] in list_of_st:
                cari = model.staff.atur.cari(data["penanggungjawab"])
                if len(cari) == 1 :
                    cari = cari[0] 

                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penanggungjawab_tindaklanjut'] = cari

            data_followup.append(res)

        return data_followup