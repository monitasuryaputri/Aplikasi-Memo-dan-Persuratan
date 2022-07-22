from aplikasi import app, model

import datetime
from google.cloud import datastore
from aplikasi.model.exception import EntityNotFoundException

from .model import TINDAKLANJUT_KIND, Tindaklanjut

from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

def tambah(id_penugas, id, nomor_surat, tugas, penanggungjawab, tenggatwaktu):
    #tambah komen

    # cek parameter
    if tugas and penanggungjawab and tenggatwaktu is not None:

        # buat object yang mau disimpan
        tindaklanjut_baru = Tindaklanjut(
                suratmasuk=id,
                penugas=id_penugas,
                tugas=tugas,
                tgl_tugas=datetime.datetime.now().timestamp(),
                tgl_selesai="",
                followup="[]",
                penanggungjawab=penanggungjawab,
                tenggatwaktu=tenggatwaktu,
                check="0",
                notif="no"
                )
        
        #Buka koneksi ke datastore
        client = datastore.Client()
        # Minta dibuatkan key baru
        key_baru = client.key(TINDAKLANJUT_KIND)
        # Buat entity baru memakai key yang baru dibuat
        entity_baru = datastore.Entity(key=key_baru)
        # Isi data untuk entity baru
        entity_baru.update(tindaklanjut_baru.ke_dictionary())
        # Simpan perubahan data entity baru
        client.put(entity_baru)
        # kembalikan pengaduan baru
        return Tindaklanjut(id=entity_baru.id,
                    suratmasuk=id,
                    penugas=id_penugas,
                    tugas=entity_baru["tugas"],
                    tgl_tugas=entity_baru["tgl_tugas"],
                    tgl_selesai=entity_baru["tgl_selesai"],
                    followup=entity_baru["followup"],
                    penanggungjawab=entity_baru["penanggungjawab"],
                    tenggatwaktu=entity_baru["tenggatwaktu"],
                    check=entity_baru["check"],
                    notif=entity_baru["notif"]
                    )

def daftar():
    # Ambil daftar komen yang telah terdaftar di datastore
    client = datastore.Client()

    # Buat query khusus untuk komen
    query = client.query(kind=TINDAKLANJUT_KIND)
    # query untuk ambil seluruh data komen, hasilnya dalam iterator
    hasil = query.fetch()

    # ubah dalam format
    daftar_tindaklanjut = []
    for satu_hasil in hasil:
        satu_tindaklanjut = Tindaklanjut(id=satu_hasil.id,
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
        daftar_tindaklanjut.append(satu_tindaklanjut)
    # kembalikan array daftar komen
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
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id}.")
        # buat list
        data_tindaklanjut = []

        u = datetime.datetime.now()

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

        # Buka koneksi ke datastore
        client = datastore.Client()

        # Cari
        query = client.query(kind=TINDAKLANJUT_KIND).add_filter("suratmasuk", "=", str(id_suratmasuk))
        hasil = query.fetch()

        # jika tidak ditemukan, bangkitkan exception
        if hasil is None:
            raise EntityNotFoundException(f"Tidak ada komen dengan id: {id_suratmasuk}.")
        # buat list
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
        for data in hasil:   
            # buat objek komen
            tindaklanjut = Tindaklanjut(id=data.id,
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
    # jika tidak ditemukan, bangkitkan exception
    if hasil is None:
        raise EntityNotFoundException(f"Tidak ada  id: {id}.")

    try:

        if(data['tgl_tugas'] != ""):
            data['tgl_tugas'] = datetime.datetime.timestamp(datetime.datetime.strptime(data['tgl_tugas'], '%d-%m-%Y'))

        if(data['tgl_selesai'] != ""):
            data['tgl_selesai'] = datetime.datetime.timestamp(datetime.datetime.strptime(data['tgl_selesai'], '%d-%m-%Y'))

    except:
        pass

    # Simpan
    hasil.update(data)
    client.put(hasil)
    # kembalikan data suratkeluar
    return Tindaklanjut(id=id)