from aplikasi import model, app, CLOUD_STORAGE_BUCKET

from flask import json
from aplikasi.model import daftar, cari, suratmasuk

from google.cloud import datastore, storage
from aplikasi.model.exception import EntityNotFoundException
import datetime
from .model import SURATMASUK_KIND, Suratmasuk


"""
Controller Untuk Surat Masuk

"""
#tambah surat masuk
def tambah(nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi):
    

    # cek parameter agar tidak kosong
    if nomor_surat and tgl_surat and asal_surat and hal and isi_ringkas and dokumen and disposisi is not None:
        
        # upload ke storage
        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        # simpan file dengan format nomor surat/file
        url_list = []
        for dokumen_data in dokumen:
            dokumen_data_blob  =bucket.blob('Surat Masuk/' + nomor_surat+'/'+dokumen_data.filename)

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
        suratmasuk_baru = Suratmasuk(nomor_surat=nomor_surat,
                                    tgl_surat=tgl_surat,
                                    asal_surat=asal_surat,
                                    hal=hal,
                                    isi_ringkas=isi_ringkas,
                                    dokumen=json.dumps(url_list),
                                    disposisi=disposisi,
                                    komentar="[]",
                                    tindaklanjut="[]",
                                    dibaca=[],
                                    tgl_disposisi=datetime.datetime.now().timestamp(),
                                    status_tindaklanjut="-",
                                    reply="[]"
                                    )

        #buka koneksi ke datastore
        client = datastore.Client()
        #minta dibuatkan key baru
        key_baru = client.key(SURATMASUK_KIND)
        #buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        #isi data untuk entity baru
        entity_baru.update(suratmasuk_baru.ke_dictionary())
        #simpan perubahan data entity baru
        client.put(entity_baru)
        #kembalikan suratmasuk baru
        return Suratmasuk(id=entity_baru.id,
                        nomor_surat=entity_baru["nomor_surat"],
                        tgl_surat=entity_baru["tgl_surat"],
                        asal_surat=entity_baru["asal_surat"],
                        hal=entity_baru["hal"],
                        isi_ringkas=entity_baru["isi_ringkas"],
                        dokumen=entity_baru["dokumen"],
                        disposisi=entity_baru["disposisi"],
                        komentar=entity_baru["komentar"],
                        tindaklanjut=entity_baru["tindaklanjut"],
                        dibaca=entity_baru["dibaca"],
                        tgl_disposisi=entity_baru["tgl_disposisi"],
                        status_tindaklanjut=entity_baru["status_tindaklanjut"],
                        reply=entity_baru["reply"]
                        )

def daftar():
    # Ambil daftar suratmasuk yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk suratmasuk
    query = client.query(kind=SURATMASUK_KIND)
    # query untuk ambil seluruh data suratmasuk, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_suratmasuk = []

    # iterate data suratmasuk, simpan ke list
    for satu_hasil in hasil:
        satu_suratmasuk = Suratmasuk( id=satu_hasil.id,
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            asal_surat=satu_hasil["asal_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tindaklanjut=satu_hasil["tindaklanjut"],
                            dibaca=satu_hasil["dibaca"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status_tindaklanjut=satu_hasil["status_tindaklanjut"],
                            reply=satu_hasil["reply"]
                            )
        
        if(satu_suratmasuk.tgl_disposisi != ""):
            satu_suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
        
        res = satu_suratmasuk.ke_dictionary()
        tanggal_surat = datetime.datetime.strptime(satu_suratmasuk.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%Y/%m/%d %H:%M')
        res["tanggal_surat"] = tanggal_surat
        tanggal_disposisi = datetime.datetime.strptime(satu_suratmasuk.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%d/%m/%Y')
        res["tanggal"] = tanggal_disposisi
        #append atau add elemen ke list
        daftar_suratmasuk.append(res)
    # kembalikan list daftar suratmasuk
    return daftar_suratmasuk

# Ambil daftar suratmasuk yang telah di disposisi berdasarkan jabatan saja
def daftarbyjabatan(id_jabatan):
    # Ambil daftar suratmasuk yang telah terdaftar di datastore
    client = datastore.Client()
    # Buat query khusus untuk suratmasuk
    query = client.query(kind=SURATMASUK_KIND).add_filter('disposisi', '=', id_jabatan)

    # query untuk ambil seluruh data surat masuk, hasilnya dalam iterator
    hasil = query.fetch()

    # buat list
    daftar_suratmasuk = []

    # iterate data suratmasuk, simpan ke list
    for satu_hasil in hasil:
        satu_suratmasuk = Suratmasuk( id=satu_hasil.id,
                            nomor_surat=satu_hasil["nomor_surat"],
                            tgl_surat=satu_hasil["tgl_surat"],
                            asal_surat=satu_hasil["asal_surat"],
                            hal=satu_hasil["hal"],
                            isi_ringkas=satu_hasil["isi_ringkas"],
                            dokumen=satu_hasil["dokumen"],
                            disposisi=satu_hasil["disposisi"],
                            komentar=satu_hasil["komentar"],
                            tindaklanjut=satu_hasil["tindaklanjut"],
                            dibaca=satu_hasil["dibaca"],
                            tgl_disposisi=satu_hasil["tgl_disposisi"],
                            status_tindaklanjut=satu_hasil["status_tindaklanjut"],
                            reply=satu_hasil["reply"]
                            )
        
        if(satu_suratmasuk.tgl_disposisi != ""):
            satu_suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(satu_suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
        
        res = satu_suratmasuk.ke_dictionary()
        tanggal_surat = datetime.datetime.strptime(satu_suratmasuk.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%Y/%m/%d %H:%M')
        res["tanggal_surat"] = tanggal_surat
        tanggal_disposisi = datetime.datetime.strptime(satu_suratmasuk.tgl_disposisi, "%d/%m/%Y %H:%M").strftime('%d/%m/%Y')
        res["tanggal"] = tanggal_disposisi
        #append atau add elemen ke list
        daftar_suratmasuk.append(res)
    # kembalikan list daftar surat masuk
    return daftar_suratmasuk

def cari(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratmasuk = client.key(SURATMASUK_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratmasuk)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada suratmasuk dengan id: {id}.")
        
        # buat list
        data_suratmasuk = []

        # buat objek suratmasuk
        suratmasuk = Suratmasuk(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        asal_surat=hasil["asal_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=hasil["disposisi"],
                        komentar=hasil["komentar"],
                        tindaklanjut=hasil["tindaklanjut"],
                        dibaca=hasil["dibaca"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status_tindaklanjut=hasil["status_tindaklanjut"],
                        reply=hasil["reply"]
                        )

       
        if(suratmasuk.tgl_disposisi != ""):
            suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
 
        try:
            suratmasuk.dokumen = json.loads(suratmasuk.dokumen)
        except:
            pass

        data_suratmasuk.append(suratmasuk.ke_dictionary())
        
        return data_suratmasuk


def detail(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_suratmasuk = client.key(SURATMASUK_KIND, id)

        #  ambil hasil carinya
        hasil = client.get(key_suratmasuk)

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada suratmasuk dengan id: {id}.")
        
        # buat list
        data_suratmasuk = []

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
        suratmasuk = Suratmasuk(id=hasil.id,
                        nomor_surat=hasil["nomor_surat"],
                        tgl_surat=hasil["tgl_surat"],
                        asal_surat=hasil["asal_surat"],
                        hal=hasil["hal"],
                        isi_ringkas=hasil["isi_ringkas"],
                        dokumen=hasil["dokumen"],
                        disposisi=penerima["disposisi"],
                        komentar=hasil["komentar"],
                        tindaklanjut=hasil["tindaklanjut"],
                        dibaca=pembaca["dibaca"],
                        tgl_disposisi=hasil["tgl_disposisi"],
                        status_tindaklanjut=hasil["status_tindaklanjut"],
                        reply=hasil["reply"]
                        )

        
        if(suratmasuk.tgl_disposisi != ""):
            suratmasuk.tgl_disposisi = datetime.datetime.fromtimestamp(float(suratmasuk.tgl_disposisi)).strftime('%d/%m/%Y %H:%M')
        
        try:
            suratmasuk.dokumen = json.loads(suratmasuk.dokumen)
        except:
            pass
        data_suratmasuk.append(suratmasuk.ke_dictionary())
        
        return data_suratmasuk

def penanggung(id):
    if id is not None:
        """ Mencari satu suratmasuk berdasarkan id-nya. """
        # Buka koneksi ke datastore
        client = datastore.Client()
        # Cari
        key_suratmasuk = client.key(SURATMASUK_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_suratmasuk)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada suratmasuk dengan id: {id}.")
        # buat list
        data_disposisi = []

        # buat objek suratmasuk
        suratmasuk = Suratmasuk(id=hasil.id,
                        disposisi=hasil["disposisi"]
                        )

        # ubah format data ke dictionary dan append ke list
        res  = suratmasuk.ke_dictionary()
        

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        penerima = {}
        penerima=hasil["disposisi"]
        for x in range(len(hasil["disposisi"])):
            penerima[x] = jabatan_nama[hasil["disposisi"][x]]
        res = penerima
        
        data_disposisi.append(res)
        return data_disposisi

def update(id, data):
    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data suratmasuk berdasar property id
    key = client.key(SURATMASUK_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key)

    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada suratmasuk dengan id: {id}.")

    try:
        if(data['tgl_disposisi'] != ""):
            data['tgl_disposisi'] = datetime.datetime.timestamp(datetime.datetime.strptime(data['tgl_disposisi'], '%d/%m/%Y %H:%M'))

    except:
        pass

    # Simpan
    hasil.update(data)
    client.put(hasil)
    # kembalikan data suratmasuk
    return Suratmasuk(id=id)