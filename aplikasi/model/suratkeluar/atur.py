from aplikasi import model, app, CLOUD_STORAGE_BUCKET

from flask import json
from aplikasi.model import daftar, cari, suratkeluar

from google.cloud import datastore, storage
from aplikasi.model.exception import EntityNotFoundException
import datetime
from .model import SURATKELUAR_KIND, Suratkeluar

#tambah suratkeluar
def tambah(nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi):
    
    # cek parameter agar tidak kosong
    if nomor_surat and tgl_surat and tujuan_surat and hal and isi_ringkas and dokumen and disposisi is not None:
        
        # upload ke storage
        # Create a Cloud Storage client.
        gcs = storage.Client()
        
        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        # simpan file dengan format nomor surat/file
        url_list = []
        for dokumen_data in dokumen:
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
        

        #buat objek yang mau disimpan
        suratkeluar_baru = Suratkeluar(nomor_surat=nomor_surat,
                                    tgl_surat=tgl_surat,
                                    tujuan_surat=tujuan_surat,
                                    hal=hal,
                                    isi_ringkas=isi_ringkas,
                                    dokumen=json.dumps(url_list),
                                    disposisi=disposisi,
                                    komentar=[],
                                    tgl_disposisi=datetime.datetime.now().timestamp(),
                                    status="draf",
                                    reply="[]",
                                    dibaca=[]
                                    )
        
        #buka koneksi ke datastore
        client = datastore.Client()
        #minta dibuatkan key baru
        key_baru = client.key(SURATKELUAR_KIND)
        #buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        #isi data untuk entity baru
        entity_baru.update(suratkeluar_baru.ke_dictionary())
        #simpan perubahan data entity baru
        client.put(entity_baru)
        #kembalikan suratkeluar baru
        return Suratkeluar(id=entity_baru.id,
                        nomor_surat=entity_baru["nomor_surat"],
                        tgl_surat=entity_baru["tgl_surat"],
                        tujuan_surat=entity_baru["tujuan_surat"],
                        hal=entity_baru["hal"],
                        isi_ringkas=entity_baru["isi_ringkas"],
                        dokumen=entity_baru["dokumen"],
                        disposisi=entity_baru["disposisi"],
                        komentar=entity_baru["komentar"],
                        tgl_disposisi=entity_baru["tgl_disposisi"],
                        status=entity_baru["status"],
                        reply=entity_baru["reply"],
                        dibaca=entity_baru["dibaca"]
                        )

def daftar():
    # Ambil daftar suratkeluar yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk suratkeluar
    query = client.query(kind=SURATKELUAR_KIND)
    # query untuk ambil seluruh data suratkeluar, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_suratkeluar = []

    # iterate data suratkeluar, simpan ke list
    for satu_hasil in hasil:
        satu_suratkeluar = Suratkeluar( id=satu_hasil.id,
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            tujuan_surat=satu_hasil["tujuan_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status=satu_hasil["status"],
                            reply=satu_hasil["reply"],
                            dibaca=satu_hasil["dibaca"]
                            )
        
        try:
            satu_suratkeluar.dokumen = json.loads(satu_suratkeluar.dokumen)
        except:
            pass

        if(satu_suratkeluar.tgl_disposisi != ""):
            satu_suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
        res = satu_suratkeluar.ke_dictionary()
        tanggal_surat = datetime.datetime.strptime(satu_suratkeluar.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%Y/%m/%d %H:%M')
        res["tanggal_surat"] = tanggal_surat
        tanggal_disposisi = datetime.datetime.strptime(satu_suratkeluar.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%d/%m/%Y')
        res["tanggal"] = tanggal_disposisi
        #append atau add elemen ke list
        daftar_suratkeluar.append(res)
    # kembalikan list daftar suratkeluar
    return daftar_suratkeluar

# Ambil daftar suratkeluar yang telah di disposisi berdasarkan jabatan saja
def daftarbyjabatan(id_jabatan):
    # Ambil daftar suratkeluar yang telah terdaftar di datastore
    client = datastore.Client()
    # Buat query khusus untuk suratkeluar
    query = client.query(kind=SURATKELUAR_KIND).add_filter('disposisi', '=', id_jabatan)

    # query untuk ambil seluruh data surat keluar, hasilnya dalam iterator
    hasil = query.fetch()

    # buat list
    daftar_suratkeluar = []

    # iterate data suratkeluar, simpan ke list
    for satu_hasil in hasil:
        satu_suratkeluar = Suratkeluar( id=satu_hasil.id,
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            tujuan_surat=satu_hasil["tujuan_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status=satu_hasil["status"],
                            reply=satu_hasil["reply"],
                            dibaca=satu_hasil["dibaca"]
                            )
    
        if(satu_suratkeluar.tgl_disposisi != ""):
            satu_suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
        
        res = satu_suratkeluar.ke_dictionary()
        
        tanggal_surat = datetime.datetime.strptime(satu_suratkeluar.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%Y/%m/%d %H:%M')
        res["tanggal_surat"] = tanggal_surat
        tanggal_disposisi = datetime.datetime.strptime(satu_suratkeluar.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%d/%m/%Y')
        res["tanggal"] = tanggal_disposisi
        
        #append atau add elemen ke list
        daftar_suratkeluar.append(res)            
    # kembalikan list daftar surat masuk
    return daftar_suratkeluar

def cari(id):
    if id is not None:
        """ Mencari satu suratkeluar berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratkeluar = client.key(SURATKELUAR_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratkeluar)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada suratkeluar dengan id: {id}.")
        
        # buat list
        data_suratkeluar = []

        # buat objek suratkeluar
        suratkeluar = Suratkeluar(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        tujuan_surat=hasil["tujuan_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=hasil["disposisi"],
                        komentar=hasil["komentar"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status=hasil["status"],
                        reply=hasil["reply"],
                        dibaca=hasil["dibaca"]
                        )

       
        if(suratkeluar.tgl_disposisi != ""):
            suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
    
        try:
            suratkeluar.dokumen = json.loads(suratkeluar.dokumen)
        except:
            pass
    
        data_suratkeluar.append(suratkeluar.ke_dictionary())
        
        return data_suratkeluar

def detail(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratkeluar = client.key(SURATKELUAR_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratkeluar)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada suratmasuk dengan id: {id}.")
        
        # buat list
        data_suratkeluar = []

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        penerima = {}
        penerima["disposisi"]=hasil["disposisi"]
        for x in range(len(hasil["disposisi"])):
            penerima["disposisi"][x] = jabatan_nama[hasil["disposisi"][x]]
        
        pembaca = {}
        pembaca["dibaca"]=hasil["dibaca"]
        for x in range(len(hasil["dibaca"])):
            pembaca["dibaca"][x] = jabatan_nama[hasil["dibaca"][x]]

        # buat objek suratmasuk
        suratkeluar = Suratkeluar(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        tujuan_surat=hasil["tujuan_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=penerima["disposisi"],
                        komentar=hasil["komentar"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status=hasil["status"],
                        reply=hasil["reply"],
                        dibaca=pembaca["dibaca"]
                        )

        
        if(suratkeluar.tgl_disposisi != ""):
            suratkeluar.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratkeluar.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')

        try:
            suratkeluar.dokumen = json.loads(suratkeluar.dokumen)
        except:
            pass
        
        res = suratkeluar.ke_dictionary()
        
        tanggal_surat = datetime.datetime.strptime(suratkeluar.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%d-%m-%Y %H:%M')
        res["tanggal_surat"] = tanggal_surat

        data_suratkeluar.append(res)
        
        return data_suratkeluar

def update(id, data):

    # Buka koneksi ke datastore
    client = datastore.Client()
    # cari/filter data suratkeluar berdasar property id
    key = client.key(SURATKELUAR_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key)
    
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada suratkeluar dengan id: {id}.")
    try:
        if(data['tgl_disposisi'] != ""):
            data['tgl_disposisi'] = datetime.datetime.timestamp(datetime.datetime.strptime(data['tgl_disposisi'], '%d/%m/%Y %H:%M'))
    except:
        pass

    # Simpan
    hasil.update(data)

    client.put(hasil)
    # kembalikan data suratkeluar
    return Suratkeluar(id=id)
