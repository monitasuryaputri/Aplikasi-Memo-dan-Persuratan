from google.cloud import datastore, storage
from aplikasi.model import surat
from aplikasi.model.exception import EntityNotFoundException, EntityIdException
from aplikasi import model, CLOUD_STORAGE_BUCKET, app
from .model import SURAT_KIND, Surat
import datetime
import json

def tambah(nomor, tujuan, isi, dokumen):
    #tambah surat
    
    # cek parameter agar tidak kosong
    if nomor and tujuan and isi is not None:
        # upload ke storage
        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        # simpan file dengan format nomor surat/file
        url_list = []

        for dokumen_data in dokumen:
            dokumen_data_blob  =bucket.blob('Surat/' + nomor+'/'+dokumen_data.filename)

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
        #buat objek yang mau disimpan
        surat_baru = Surat( nomor=nomor,
                            asal= "monitasurya@gmail.com",
                            tujuan=tujuan,
                            tgl= datetime.datetime.now().timestamp(),
                            isi=isi,
                            dokumen= json.dumps(url_list)
                            )
        #buka koneksi ke datastore
        client = datastore.Client()
        #minta dibuatkan key baru
        key_baru = client.key(SURAT_KIND)
        #buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        #isi data untuk entity baru
        entity_baru.update(surat_baru.ke_dictionary())
        #simpan perubahan data entity baru
        """ 
        Menyimpan dictionary surat baru ke dalam datastore
        
        """
        client.put(entity_baru)
        #kembalikan admin baru
        return Surat(   id=entity_baru.id,
                        nomor=entity_baru["nomor"],
                        asal=entity_baru["asal"],
                        tujuan=entity_baru["tujuan"],
                        tgl=entity_baru["tgl"],
                        isi=entity_baru["isi"],
                        dokumen=entity_baru["dokumen"])

def daftar():
    # Ambil daftar suratmasuk yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk surat
    query = client.query(kind=SURAT_KIND)
    # query untuk ambil seluruh data suratmasuk, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_surat = []

    # iterate data suratmasuk, simpan ke list
    for satu_hasil in hasil:
        satu_surat = Surat( id= satu_hasil.id,
                            nomor= satu_hasil["nomor"],
                            asal= satu_hasil["asal"],
                            tujuan=satu_hasil["tujuan"],
                            tgl= satu_hasil["tgl"],
                            isi=satu_hasil["isi"],
                            dokumen=satu_hasil["dokumen"]
                            )
        
        if(satu_surat.tgl != ""):
            satu_surat.tgl = datetime.datetime.fromtimestamp(float(satu_surat.tgl)).strftime('%d/%m/%Y')
        
        dictionary_baru = satu_surat.ke_dictionary()

        tanggal_surat = datetime.datetime.strptime(satu_surat.tgl, "%d/%m/%Y").strftime('%Y/%m/%d')

        dictionary_baru["tgl"] = tanggal_surat

        #append atau add elemen ke list
        daftar_surat.append(dictionary_baru)
        
    # kembalikan list daftar suratmasuk
    return daftar_surat

def detail(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_surat = client.key(SURAT_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_surat)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada surat dengan id: {id}.")
        
        # buat list
        data_surat = []

        # buat objek suratmasuk
        surat = Surat( id=hasil.id,
                        nomor=hasil["nomor"],
                        asal=hasil["asal"],
                        tujuan=hasil["tujuan"],
                        tgl=hasil["tgl"],
                        isi=hasil["isi"],
                        dokumen=hasil["dokumen"]
                        )
        
        if(surat.tgl != ""):
            surat.tgl = datetime.datetime.fromtimestamp(float(surat.tgl)).strftime('%d/%m/%Y')
        
        surat.dokumen = json.loads(surat.dokumen)
        
        data_surat.append(surat.ke_dictionary())
        
        return data_surat