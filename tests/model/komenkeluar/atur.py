from aplikasi import app, model

from google.cloud import datastore, storage

from tests.model.komenkeluar import KOMENKELUAR_KIND, Komenkeluar
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id, id_penindak, isi_komenkeluar, file_komenkeluar):
    #tambah komenkeluar

    # cek parameter
    if isi_komenkeluar is not None:
        # buat list 
        data_komenkeluar = []
        # buat object yang mau disimpan
        komenkeluar_baru = Komenkeluar(
             suratkeluar=id,
             penindak=id_penindak,             
             isi_komenkeluar=isi_komenkeluar,
             tgl_komenkeluar=1643882750.899903,
             file_komenkeluar=file_komenkeluar,
             reply="[]"
             )
        # append atau add elemen ke list
        data_komenkeluar.append(komenkeluar_baru.ke_dictionary())
        # kembalikan komenkeluar baru
        return data_komenkeluar

def daftar():
    data_komenkeluar = [{'id': 5076466173739008, 
                         'suratkeluar': '5671441819238400', 
                         'penindak': 6548254560878592, 
                         'isi_komenkeluar': "komentar", 
                         'tgl_komenkeluar': 1643882750.899903, 
                         'file_komenkeluar': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}],
                         'reply': "[]"}]
    # buat list
    komenkeluar = []                
    # iterate data komenkeluar, simpan ke list
    for satu_hasil in data_komenkeluar:
        satu_komenkeluar = Komenkeluar(id=satu_hasil["id"],
                                       suratkeluar=satu_hasil["suratkeluar"],
                                       penindak=satu_hasil["penindak"],
                                       isi_komenkeluar=satu_hasil["isi_komenkeluar"],
                                       tgl_komenkeluar=satu_hasil["tgl_komenkeluar"],
                                       file_komenkeluar=satu_hasil["file_komenkeluar"],
                                       reply=satu_hasil["reply"]
                                        )
        # append atau add elemen ke list
        komenkeluar.append(satu_komenkeluar)
    # buat list
    daftar_komenkeluar = []
    # iterate data komenkeluar, simpan ke list
    for satu_data in komenkeluar:
        # append atau add elemen ke list
        daftar_komenkeluar.append(satu_data.ke_dictionary())
    # kembalikan array daftar komenkeluar
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
            raise (f"Tidak ada komen dengan id: {id}.")
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
            raise (f"Tidak ada komen dengan id: {id}.")
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
        
        data_komenkeluar.append(komenkeluar.ke_dictionary())

        return data_komenkeluar

def caribysuratkeluar(id_suratkeluar):

    if id_suratkeluar is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        daftarkomenkeluar = [{'id': 5076466173739008, 
                            'suratkeluar': '5671441819238400', 
                            'penindak': 6548254560878592, 
                            'isi_komenkeluar': "komentar", 
                            'tgl_komenkeluar': 1643882750.899903, 
                            'file_komenkeluar': [{"url":"https://storage.googleapis.com/surat-labter.appspot.com/Surat%20Keluar/16/FMIPA/122/ADM/85/","name":""}],
                            'reply': "[]"}]

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

        for data in daftarkomenkeluar:
            # buat objek komen
            komenkeluar = Komenkeluar(id=data["id"],
                            suratkeluar=data["suratkeluar"],
                            penindak=data["penindak"],
                            isi_komenkeluar=data["isi_komenkeluar"],
                            tgl_komenkeluar=data["tgl_komenkeluar"],
                            file_komenkeluar=data["file_komenkeluar"],
                            reply=data["reply"]
                            )
   
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
        raise (f"Tidak ada suratkeluar dengan id: {id}.")

    # Simpan
    hasil.update(data)
    data_komenkeluar = []

    komenkeluar_baru = Komenkeluar(id=id,
                                suratkeluar=hasil["suratkeluar"],
                                penindak=hasil["penindak"],
                                isi_komenkeluar=hasil["isi_komenkeluar"],
                                tgl_komenkeluar=hasil["tgl_komenkeluar"],
                                file_komenkeluar=hasil["file_komenkeluar"],
                                reply=hasil["reply"]
                                )
    
    data_komenkeluar.append(komenkeluar_baru.ke_dictionary())
    # kembalikan data komenkeluar
    return data_komenkeluar