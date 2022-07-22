from aplikasi import model

from flask import json
from google.cloud import datastore

from tests.model.followup import FOLLOWUP_KIND, Followup
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id, id_penanggungjawab, isi_followup, file_followup):
    #tambah followup

    # cek parameter
    if isi_followup is not None:
        # buat list 
        data_followup = []
        # buat object yang mau disimpan
        followup_baru = Followup(
             penanggungjawab=id_penanggungjawab,
             tindaklanjut=id,
             isi_followup=isi_followup,
             file_followup=file_followup,
             tgl_followup=1649753736.719793
             )
        
        # append atau add elemen ke list
        data_followup.append(followup_baru.ke_dictionary())
        # kembalikan followup baru
        return data_followup

def daftar():
    data_followup = [{"id" : 4824222207574016,                            
                    "tindaklanjut" : "5656080600268800",
                    "penanggungjawab" : 5105697184284672,
                    "isi_followup" : "sudah didata",
                    "file_followup" : '[{"name": "Metodologi Penelitian Hukum.pptx", "url": "https://storage.googleapis.com/surat-labter.appspot.com/followup/Metodologi%20Penelitian%20Hukum.pptx"}]',
                    "tgl_followup" : 1649753736.719793
                    }]

    # buat list
    followup = []                
    # iterate data komen, simpan ke list
    for satu_hasil in data_followup:
        satu_followup = Followup(id=satu_hasil["id"],
                        tindaklanjut=satu_hasil["tindaklanjut"],
                        penanggungjawab=satu_hasil["penanggungjawab"],
                        isi_followup=satu_hasil["isi_followup"],
                        file_followup=satu_hasil["file_followup"],
                        tgl_followup=satu_hasil["tgl_followup"]
                        )
        # append atau add elemen ke list
        followup.append(satu_followup)
    # buat list
    daftar_followup = []
    # iterate data followup, simpan ke list
    for satu_data in followup:
        # append atau add elemen ke list
        daftar_followup.append(satu_data.ke_dictionary())
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
            raise (f"Tidak ada followup dengan id: {id}.")
        # buat list
        data_followup = []
        # buat objek followup
        followup = Followup(id=hasil.id,
                        tindaklanjut=hasil["tindaklanjut"],
                        penanggungjawab=hasil["penanggungjawab"],
                        isi_followup=hasil["isi_followup"],
                        file_followup=hasil["file_followup"],
                        tgl_followup=hasil["tgl_followup"]
                        )
        
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
            raise (f"Tidak ada followup dengan id: {id_tindaklanjut}.")
        # buat list
        data_followup = []

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
        