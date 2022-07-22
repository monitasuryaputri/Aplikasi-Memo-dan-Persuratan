from aplikasi import app, model

import datetime
from google.cloud import datastore

from tests.model.tindaklanjut import TINDAKLANJUT_KIND, Tindaklanjut

from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id, id_penugas, tugas, penanggungjawab, tenggatwaktu):
    #tambah tindaklanjut

    # cek parameter
    if tugas and penanggungjawab and tenggatwaktu is not None:
        # buat list 
        data_tindaklanjut = []
        # buat object yang mau disimpan
        tindaklanjut_baru = Tindaklanjut(
                suratmasuk=id,
                penugas=id_penugas,
                tugas=tugas,
                tgl_tugas=1643794758.564006,
                tgl_selesai="",
                followup="[]",
                penanggungjawab=penanggungjawab,
                tenggatwaktu=tenggatwaktu,
                check="0",
                notif="no"
                )
        # append atau add elemen ke list
        data_tindaklanjut.append(tindaklanjut_baru.ke_dictionary())
        # kembalikan tindaklanjut baru
        return data_tindaklanjut

def daftar():
    data_tindaklanjut = [{'id': 5644357755469824,
                            'suratmasuk': '5729017198018560', 
                            'penugas': 5652730257342464, 
                            'penanggungjawab': '5731076903272448', 
                            'tugas': 'sediakan ruangan', 
                            'tgl_tugas': 1643794758.564006,
                            'tgl_selesai': "",
                            'followup': "[]",
                            'tenggatwaktu': "2022-02-04",
                            'check': "0",
                            'notif': "no"
                            }]

    # ubah dalam format
    tindaklanjut = []

    # iterate data tindaklanjut, simpan ke list
    for satu_hasil in data_tindaklanjut:
        satu_tindaklanjut = Tindaklanjut(id=satu_hasil["id"],
                        suratmasuk=satu_hasil["suratmasuk"],
                        penugas=satu_hasil["penugas"],
                        tugas=satu_hasil["tugas"],
                        tgl_tugas=satu_hasil["tgl_tugas"],
                        tgl_selesai=satu_hasil["tgl_selesai"],
                        followup=satu_hasil["followup"],
                        penanggungjawab=satu_hasil["penanggungjawab"],
                        tenggatwaktu=satu_hasil["tenggatwaktu"],
                        check=satu_hasil["check"],
                        notif=satu_hasil["notif"]
                        )

        # append atau add elemen ke list
        tindaklanjut.append(satu_tindaklanjut)
    # buat list
    daftar_tindaklanjut = []
    # iterate data tindaklanjut, simpan ke list
    for satu_data in tindaklanjut:
        # append atau add elemen ke list
        daftar_tindaklanjut.append(satu_data.ke_dictionary())
    # kembalikan array daftar tindaklanjut
    return daftar_tindaklanjut


def cari(id):
    if id is not None:
        """ Mencari satu pengaduan berdasarkan id-nya. """

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        key_tindaklanjut = client.key(TINDAKLANJUT_KIND, id)
        #  ambil hasil carinya
        hasil = client.get(key_tindaklanjut)
        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise (f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_tindaklanjut = []

        # buat objek komen
        tindaklanjut = Tindaklanjut(id=hasil.id,
                        suratmasuk=hasil["suratmasuk"],
                        penugas=hasil["penugas"],
                        tugas=hasil["tugas"],
                        tgl_tugas=hasil["tgl_tugas"],
                        tgl_selesai=hasil["tgl_selesai"],
                        followup=hasil["followup"],
                        penanggungjawab=hasil["penanggungjawab"],
                        tenggatwaktu=hasil["tenggatwaktu"],
                        check=hasil["check"],
                        notif=hasil["notif"]
                        )

        if(tindaklanjut.tgl_tugas != ""):
            tindaklanjut.tgl_tugas = datetime.datetime.fromtimestamp(float(tindaklanjut.tgl_tugas)).strftime('%d-%m-%Y')

        if(tindaklanjut.tgl_selesai != ""):
            tindaklanjut.tgl_selesai = datetime.datetime.fromtimestamp(float(tindaklanjut.tgl_selesai)).strftime('%d-%m-%Y')
        
        # ubah format data ke dictionary dan append ke list
        data_tindaklanjut.append(tindaklanjut.ke_dictionary())
        return data_tindaklanjut

def caribysuratmasuk(id_suratmasuk):

    if id_suratmasuk is not None:
        """ Mencari satu surat berdasarkan id-nya. """

        daftar_tindaklanjut = [{'id': 5644357755469824,
                            'suratmasuk': '5729017198018560', 
                            'penugas': 5652730257342464, 
                            'penanggungjawab': '5731076903272448', 
                            'tugas': 'sediakan ruangan', 
                            'tgl_tugas': 1643794758.564006,
                            'tgl_selesai': "",
                            'followup': "[]",
                            'tenggatwaktu': "2022-02-04",
                            'check': "0",
                            'notif': "no"
                            }]

        # ubah dalam format
        data_tindaklanjut = []

        ad = list_ad()
        list_of_ad = [id for elem in ad
                        for id in elem.values()]
        ka = list_ka()
        list_of_ka = [id for elem in ka
                        for id in elem.values()]
        st = list_st()
        list_of_st = [id for elem in st
                        for id in elem.values()]

        penanggungjawab = model.jabatan.atur.daftar()
        penanggungjawab_nama = {}

        for data in penanggungjawab:
            penanggungjawab_nama[str(data.id)] = data.nama

        u = datetime.datetime.now()
        for data in daftar_tindaklanjut:   
            # buat objek komen
            tindaklanjut = Tindaklanjut(id=data["id"],
                            suratmasuk=data["suratmasuk"],
                            penugas=data["penugas"],
                            tugas=data["tugas"],
                            tgl_tugas=data["tgl_tugas"],
                            tgl_selesai=data["tgl_selesai"],
                            followup=data["followup"],
                            penanggungjawab=penanggungjawab_nama[data["penanggungjawab"]],
                            tenggatwaktu=data["tenggatwaktu"],
                            check=data["check"],
                            notif=data["notif"]
                            )

            if(tindaklanjut.tgl_tugas != ""):
                tindaklanjut.tgl_tugas = datetime.datetime.fromtimestamp(float(tindaklanjut.tgl_tugas)).strftime('%d-%m-%Y')
          
            if(tindaklanjut.tgl_selesai != ""):
                tindaklanjut.tgl_selesai = datetime.datetime.fromtimestamp(float(tindaklanjut.tgl_selesai)).strftime('%d-%m-%Y')
            
            x = datetime.datetime.strptime(tindaklanjut.tenggatwaktu, '%Y-%m-%d')
            res = tindaklanjut.ke_dictionary()


            if ( x - u <= datetime.timedelta(days=2) and tindaklanjut.check == "0"):
                tindaklanjut.notif = "yes"
                res["notif"] = tindaklanjut.notif

            if ( x - u <= datetime.timedelta(days=0) and tindaklanjut.check == "0"):
                tindaklanjut.notif = "lewat"
                res["notif"] = tindaklanjut.notif

            if data["penugas"]in list_of_ka:
                cari = model.kepalaupt.atur.cari(data["penugas"])
                if len(cari) == 1 :
                    cari = cari[0] 
                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penugas_tindaklanjut'] = cari

            elif data["penugas"]in list_of_st :
                cari = model.staff.atur.cari(data["penugas"])
                if len(cari) == 1 :
                    cari = cari[0] 

                jabatan = model.jabatan.atur.daftar()
                jabatan_nama = {}
                for data in jabatan:
                    jabatan_nama[str(data.id)] = data.nama

                cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

                res['penugas_tindaklanjut'] = cari

            data_tindaklanjut.append(res)
        return data_tindaklanjut

def update(id, data):

    # Buka koneksi ke datastore
    client = datastore.Client()

    # cari/filter data suratkeluar berdasar property id
    key = client.key(TINDAKLANJUT_KIND, id)
    #  ambil hasil carinya
    hasil = client.get(key)

    # Simpan
    hasil.update(data)
    data_tindaklanjut = []

    tindaklanjut_baru = Tindaklanjut(id=id,
                                suratmasuk=hasil["suratmasuk"],
                                penugas=hasil["penugas"],
                                tugas=hasil["tugas"],
                                tgl_tugas=hasil["tgl_tugas"],
                                tgl_selesai=hasil["tgl_selesai"],
                                followup=hasil["followup"],
                                penanggungjawab=hasil["penanggungjawab"],
                                tenggatwaktu=hasil["tenggatwaktu"],
                                check=hasil["check"],
                                notif=hasil["notif"]
                                )
    
    data_tindaklanjut.append(tindaklanjut_baru.ke_dictionary())
    # kembalikan data tindaklanjut
    return data_tindaklanjut