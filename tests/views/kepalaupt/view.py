from tests.model.konfigurasi.daftar_role import KEPALAUPT_ROLE
from tests.views.admin import view
from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app

from tests.model.kepalaupt import tambah
from tests.model.kepalaupt import daftar
from tests.model.kepalaupt import hapus
from tests.model.kepalaupt import ubah
from tests.model.kepalaupt import cari
from tests.model.kepalaupt import cari_email
from tests.model.kepalaupt import Kepalaupt
from tests.model.kepalaupt import KEPALAUPT_KIND

from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi
from google.cloud import datastore

from flask import Blueprint, request, session, escape, redirect, flash, jsonify, render_template

from tests.views.staff.view import staff_list as list_st

kepalaupt = Blueprint("kepalaupt", __name__, url_prefix="/kepalaupt")


#kepalaupt
@kepalaupt.route("/tambah", methods=["POST"])
def kepalaupt_tambah():
    #konversi request ke json
    if request.is_json:
        #ambil parameter
        kepalaupt_baru = request.get_json()
    elif request.form:
        kepalaupt_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    #periksa parameter sudah benar
    if kepalaupt_baru is None:
        return "Data kepalaupt baru tidak ada!", 400
    if "nama" in kepalaupt_baru is None:
        return "Salah data! Properti nama tidak ada", 400
    if "email" in kepalaupt_baru is None:
        return "Salah data! Properti email tidak ada", 400
    if "no_hp" in kepalaupt_baru is None:
        return "Salah data! Properti no_hp tidak ada", 400
    # if "jabatan" in kepalaupt_baru is None:
    #     return "Salah data! Properti jabatan tidak ada", 400
    
    nama = escape(kepalaupt_baru["nama"]).strip()
    email = escape(kepalaupt_baru["email"]).strip()
    no_hp = escape(kepalaupt_baru["no_hp"]).strip()
    jabatan = escape(kepalaupt_baru["jabatan"]).strip()


    #tambah kepalaupt baru
    try:
        hasil = tambah(nama,email,no_hp, jabatan)
    except EntityNotFoundException:
        return f"Gagal menambah kepalaupt baru", 400
    
    #pastikan berhasil
    if (hasil is None):
        #set flash message
        flash('Gagal menambah kepalaupt baru')
        #direct ke halaman tambah kepalaupt
        return redirect(url_for('superadmin.superadmin_kepalaupt_tambah'))

    #set flash message
    flash('Kepala Uupt berhasil ditambahkan')
    #direct ke halaman daftar kepalaupt
    return redirect(url_for('superadmin.dashboardsuperadmin'))

@kepalaupt.route("/daftar", methods=["GET"])
def kepalaupt_daftar():

    #minta data semua kepalaupt
    hasil = model.kepalaupt.atur.daftar()

    #pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar Kepalaupt", 400

    # ubah class ke dictionary
    daftar_kepalaupt = []
    for satu_hasil in hasil:
        daftar_kepalaupt.append(satu_hasil.ke_dictionary())
    
    # buat wrapper dictionary untuk dikembalikan
    hasil = { "daftar": daftar_kepalaupt }

    return jsonify(hasil), 200

@kepalaupt.route("/listka", methods=["GET"])
def kepalaupt_list():

    # Minta data semua kepalaupt
    hasil = model.kepalaupt.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar kepalaupt.", 400

    # Ubah class ke dictionary
    daftar_kepalaupt = []
    for satu_hasil in hasil:
        daftar_kepalaupt.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil =  daftar_kepalaupt 
    
    return hasil

@kepalaupt.route("/cari/email", methods=["GET"])
def kepalaupt_cari_email():
    email = request.form.get("email")

    try:
        hasil = cari_email(email)
    except:
        return f"Gagal mengambil email '{email}'", 400

    # pastikan berhasil
    if hasil is None:
        return f"Gagal mengambil email '{email}'", 400

    # buat wrapper dictionary untuk dikembalikan
    hasil_json = []
    for satu_hasil in hasil:
        # kalau tidak diubah ke dictionary hasilnya error json not serializable (?)
        satu_hasil_json = satu_hasil.ke_dictionary()
        hasil_json.append(satu_hasil_json)
    
    return jsonify(hasil_json), 200

@kepalaupt.route("/hapus/<int:id>")
def kepalaupt_hapus(id):

    # panggil method hapus
    try:
        hapus(id)
    except: 
        return f"Gagal menghapus kepala dengan id: {id}.", 400

    # set flash message
    flash('Kepalaupt berhasil dihapus')
    #direct ke halaman daftar Kepalaupt
    return redirect('/superadmin/dashboardsuperadmin')

@kepalaupt.route("/ubah/<int:id>", methods=["POST"])
def kepalaupt_ubah(id):
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        kepalaupt_baru = request.get_json()
    if request.form:
        kepalaupt_baru = request.form
    else:
        return "Hanya menerima request json dan form",400

    
    # Periksa parameter sudah benar
    if kepalaupt_baru is None:
        return "Data admin baru tidak ada!", 400        
    if "nama" not in kepalaupt_baru.keys():
        return "Salah data! Property nama tidak ada.", 400
    if "email" not in kepalaupt_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    if "no_hp" not in kepalaupt_baru.keys():
        return "Salah data! Property no_hp tidak ada.", 400
    
    kepalaupt_baru = Kepalaupt(id=id, 
                        nama=kepalaupt_baru["nama"],
                        email=kepalaupt_baru["email"],
                        no_hp=kepalaupt_baru["no_hp"],
                        jabatan=kepalaupt_baru["jabatan"]) 
                            
    try:
        hasil = ubah(id, kepalaupt_baru) 
    except EntityNotFoundException:
        return f"Tidak ada kepalaupt dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah kepalaupt dengan id: {id}.", 400
    
   # Pastikan berhasil
    if (hasil is None):

        # set flash message
        flash('Gagal mengubah data kepalau[pt')
        # direct ke laman tambah kepalaupt
        return redirect(url_for('superadmin.superadmin_kepalaupt_ubah'))

    # set flash message
    flash('Kepala UPT berhasil diubah')         
    #direct ke halaman daftar kepalaupt
    return redirect(url_for('superadmin.superadmin_kepalaupt_daftar'))

    
@kepalaupt.route("/kepalaupt/cari/<int:id>", methods=["GET"])
def kepalaupt_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari kepalaupt dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari kepalaupt dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil.ke_dictionary()), 200


#halaman dashboard
@kepalaupt.route("/dashboardka", methods=["GET"])
def dashboardka():
    return render_template("kepalaupt/dashboardka.j2", title="Dashboard")

#halaman detail draf surat
@kepalaupt.route("/detaildrafsuratka/<int:id>", methods=["GET"])
def detaildrafsuratka(id):

    # Lakukan pencarian draf surat berdasar id
    try:
        cari_suratkeluar = model.suratkeluar.atur.detail(id)
        jabatan = model.jabatan.atur.disposisi()

    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratkeluar is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratkeluar[0]["data_komentar"] = model.komenkeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])
    cari_suratkeluar[0]["data_reply"] = model.replykeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])

    return render_template("kepalaupt/detaildrafsuratka.j2", title="Detail Draf Surat", data_suratkeluar=cari_suratkeluar,  daftar_jabatan=jabatan, breadcrumb="Home", breadcrumb_nonactive="Draf Surat", breadcrumb_active="Detail Draf Surat")

@kepalaupt.route("/detaildrafsuratka/tugaskan/<int:id>", methods=["POST"])
def detaildrafsuratka_tugaskan(id):

    status = False
    msg = f"Gagal update pengaduan dengan id: {id}.", 400
    update_suratkeluar = model.suratkeluar.atur.cari(id)

    data = {
        "id": request.form.get("id"),
        "penerima": json.loads(request.form.get("penerima"))
    }

    if len(update_suratkeluar) == 1:
        cari_suratkeluar = update_suratkeluar[0]

        cari_suratkeluar['disposisi'] = (cari_suratkeluar['disposisi'])
        cari_suratkeluar['disposisi'] += [x.lower() for x in data['penerima']]

        del cari_suratkeluar['id']

        try:
            model.suratkeluar.atur.update(id, cari_suratkeluar)
            status = True
            msg = "Success"
        except: 
            msg = f"Update Gagal update surat masuk dengan id: {id}.", 400

    return {
        'status' : status,
        'msg' : msg
    }

#halaman detail draf update
@kepalaupt.route("/detaildrafsuratka/update/<int:id>", methods=["POST"])
def detaildrafsuratka_update(id):

    status = False
    msg = f"Gagal update pengaduan dengan id: {id}.", 400
    update_suratkeluar = model.suratkeluar.atur.cari(id)

    data = {
        "id": request.form.get("id"),
        "lampiran": request.files.get("lampiran")
    }

    if len(update_suratkeluar) == 1:
        cari_suratkeluar = update_suratkeluar[0]

        cari_suratkeluar['dokumen'] = (cari_suratkeluar['dokumen'])
        cari_suratkeluar['dokumen'] = (data['lampiran'])

        del cari_suratkeluar['id']

        try:
            model.suratkeluar.atur.update(id, cari_suratkeluar)
            status = True
            msg = "Success"
        except: 
            msg = f"Update Gagal update surat masuk dengan id: {id}.", 400

    return {
        'status' : status,
        'msg' : msg
    }

#halaman detail surat keluar
@kepalaupt.route("/detailsuratkeluar/<int:id>", methods=["GET"])
def detailsuratkeluarka(id):

    # Lakukan pencarian draf surat berdasar id
    try:
        cari_suratkeluar = model.suratkeluar.atur.detail(id)
    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratkeluar is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratkeluar[0]["data_komentar"] = model.komenkeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])
    cari_suratkeluar[0]["data_reply"] = model.replykeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])


    return render_template("kepalaupt/detailsuratkeluar.j2", title="Detail Surat Keluar", data_suratkeluar=cari_suratkeluar, breadcrumb="Home", breadcrumb_nonactive="Surat Keluar", breadcrumb_active="Detail Surat Keluar")

#halaman detail surat masuk
@kepalaupt.route("/detailsuratmasukka/<int:id>", methods=["GET"])
def detailsuratmasukka(id):

    pembaca =  model.suratmasuk.atur.cari(id)
    
    ka = kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = list_st()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if session['id'] in list_of_ka:
        cari = model.kepalaupt.atur.cari(session['id'])
        cari = cari[0]['jabatan']
        
        pembaca[0]['dibaca'] = pembaca[0]['dibaca'] 
        if len(pembaca[0]['dibaca']) >= 1:
            if cari not in pembaca[0]['dibaca']:
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
            else:
                pembaca[0]['dibaca'].remove(cari)
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
        else:
            pembaca[0]['dibaca'] += [cari]
            del pembaca[0]['id']
            model.suratmasuk.atur.update(id, pembaca[0])   

    elif session['id'] in list_of_st:
        cari = model.staff.atur.cari(session['id'])
        cari = cari[0]['jabatan']

        pembaca[0]['dibaca'] = pembaca[0]['dibaca']
        if len(pembaca[0]['dibaca']) >= 1:
            if cari not in pembaca[0]['dibaca']:
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
            else:
                pembaca[0]['dibaca'].remove(cari)
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
        else:
            pembaca[0]['dibaca'] += [cari]
            del pembaca[0]['id']
            model.suratmasuk.atur.update(id, pembaca[0])

    # Lakukan pencarian surat masuk berdasar id
    try:
        cari_suratmasuk = model.suratmasuk.atur.detail(id)
        jabatan = model.jabatan.atur.disposisi()
    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400

    if cari_suratmasuk is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratmasuk[0]["data_komentar"] = model.komenmasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    cari_suratmasuk[0]["data_reply"] = model.replymasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])

    return render_template("kepalaupt/detailsuratmasukka.j2", title="Detail Surat Masuk", data_suratmasuk=cari_suratmasuk, daftar_jabatan=jabatan, breadcrumb="Home", breadcrumb_nonactive="Surat Masuk", breadcrumb_active="Detail Surat Masuk")

#halaman detail surat masuk update
@kepalaupt.route("/detailsuratmasukka/update/<int:id>", methods=["POST"])
def detailsuratmasukka_update(id):

    status = False
    msg = f"Gagal update pengaduan dengan id: {id}.", 400
    update_suratmasuk = model.suratmasuk.atur.cari(id)

    data = {
        "id": request.form.get("id"),
        "penerima": json.loads(request.form.get("penerima"))
    }

    if len(update_suratmasuk) == 1:
        cari_suratmasuk = update_suratmasuk[0]

        cari_suratmasuk['disposisi'] = (cari_suratmasuk['disposisi'])
        cari_suratmasuk['disposisi'] += [x.lower() for x in data['penerima']]

        del cari_suratmasuk['id']

        try:
            model.suratmasuk.atur.update(id, cari_suratmasuk)
            status = True
            msg = "Success"
        except: 
            msg = f"Update Gagal update surat masuk dengan id: {id}.", 400

    return {
        'status' : status,
        'msg' : msg
    }

#halaman draf surat
@kepalaupt.route("/drafsuratka", methods=["GET"])
def drafsuratka():

    suratkeluar = model.suratkeluar.atur.daftar()

    return render_template("kepalaupt/drafsuratka.j2", title="Draf Surat", daftar_suratkeluar=suratkeluar,  breadcrumb="Home", breadcrumb_active="Draf Surat")

#halaman surat keluar
@kepalaupt.route("/suratkeluarka", methods=["GET"])
def suratkeluarka():

    suratkeluar = model.suratkeluar.atur.daftar()

    return render_template("kepalaupt/suratkeluarka.j2", title="Surat Keluar", daftar_suratkeluar=suratkeluar,  breadcrumb="Home", breadcrumb_active="Surat Keluar")

#halaman surat masuk
@kepalaupt.route("/suratmasukka", methods=["GET"])
def suratmasukka():

    suratmasuk = model.suratmasuk.atur.daftar()

    return render_template("kepalaupt/suratmasukka.j2", title="Surat Masuk", daftar_suratmasuk=suratmasuk, breadcrumb="Home", breadcrumb_active="Surat Masuk")

#halaman tindak lanjut surat
@kepalaupt.route("/tindaklanjut", methods=["GET"])
def tindaklanjut():

    suratmasuk = model.suratmasuk.atur.daftar()

    return render_template("kepalaupt/tindaklanjut.j2", title="Tindak Lanjut", daftar_suratmasuk=suratmasuk,  breadcrumb="Home", breadcrumb_active="Tindak Lanjut")

#halaman detail tindak lanjut surat
@kepalaupt.route("/detailtindaklanjut/<int:id>", methods=["GET"])
def detailtindaklanjut(id):

    try:
        cari_suratmasuk = model.suratmasuk.atur.cari(id)
    except: 
        return f"try Gagal mencari pengaduan dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratmasuk is None:
        return f"None Gagal mencari pengaduan dengan id: {id}.", 400

    cari_suratmasuk[0]["data_tindaklanjut"] = model.tindaklanjut.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    cari_suratmasuk[0]["data_disposisi"] = model.suratmasuk.atur.penanggung(id)
    cari_suratmasuk[0]["data_disposisi"] = cari_suratmasuk[0]["data_disposisi"][0]
    
    return render_template("kepalaupt/detailtindaklanjut.j2", title="Detail Tindak Lanjut", data_suratmasuk=cari_suratmasuk, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut")

#halaman detail tindak lanjut surat
@kepalaupt.route("/detailtindaklanjutselesai/<int:id>", methods=["GET"])
def detailtindaklanjutselesai(id):

    try:
        cari_suratmasuk = model.suratmasuk.atur.cari(id)
    except: 
        return f"try Gagal mencari pengaduan dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratmasuk is None:
        return f"None Gagal mencari pengaduan dengan id: {id}.", 400

    cari_suratmasuk[0]["data_tindaklanjut"] = model.tindaklanjut.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])

    return render_template("kepalaupt/detailtindaklanjutselesai.j2", title="Detail Tindak Lanjut Selesai", data_suratmasuk=cari_suratmasuk, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut Selesai")

@kepalaupt.route("/isi-tindaklanjutka/<int:id>", methods=["GET"])
def isitindaklanjutka(id):

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
    x = cari_tindaklanjut[0]["penugas"]

    ka = kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = list_st()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if x in list_of_ka:
        cari = model.kepalaupt.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 
        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]
        x = cari

    elif x in list_of_st:
        cari = model.staff.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

        x = cari

    cari_tindaklanjut[0]["penugas"] = x['nama_jabatan']
    
    # Pastikan berhasil
    if cari_tindaklanjut is None:
        return f"Gagal mencari surat dengan id: {id}.", 400
    cari_tindaklanjut[0]["data_followup"] = model.followup.atur.caribytindaklanjut(cari_tindaklanjut[0]['id'])
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama
    cari_tindaklanjut[0]["penanggungjawab"] = jabatan_nama[cari_tindaklanjut[0]["penanggungjawab"]]
    cari_tindaklanjut[0]["data_pn"] = jabatan_nama[session['jabatan']]

    return render_template("kepalaupt/isi-tindaklanjutka.j2", title="Tugas Tindak Lanjut", data_tindaklanjut=cari_tindaklanjut, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Tugas Tindak Lanjut")

@kepalaupt.route("/isi-tindaklanjutka/edit/<int:id>", methods=["GET"])
def edittindaklanjutkepala(id):

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)

    return render_template("kepalaupt/edittindaklanjutka.j2", title="Tugas Tindak Lanjut", data_tindaklanjut=cari_tindaklanjut, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Tugas Tindak Lanjut")

@kepalaupt.route("/isi-tindaklanjutka/simpan/<int:id>", methods=["POST"])
def simpantindaklanjutkepala(id):

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)

    if len(cari_tindaklanjut) == 1:
        cari_tindaklanjut = cari_tindaklanjut[0]

        cari_tindaklanjut['tenggatwaktu'] = request.form.get("tenggatwaktu")

        del cari_tindaklanjut['id']

        model.tindaklanjut.atur.update(id, cari_tindaklanjut)
        
    return redirect('/kepalaupt/isi-tindaklanjutka/'+ str(id))

@kepalaupt.route("/followup/<int:id>", methods=["GET"])
def followup(id):

    try:
        cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
        x = cari_tindaklanjut[0]["suratmasuk"]
        cari_suratmasuk = model.suratmasuk.atur.cari(int(x))
    except: 
        return f"try Gagal mencari pengaduan dengan id: {id}.", 400
    
    cari_suratmasuk[0]["data_tindaklanjut"] = model.tindaklanjut.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    
    # Pastikan berhasil
    if cari_tindaklanjut is None:
        return f"None Gagal mencari pengaduan dengan id: {id}.", 400
    
    cari_tindaklanjut[0]["data_followup"] = model.followup.atur.caribytindaklanjut(cari_tindaklanjut[0]['id'])

    # Muat template
    return render_template("kepalaupt/followup.j2", title="Proses Tugas" , breadcrumb="Home", breadcrumb_nonactive="Surat Masuk", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Tugas Tindak Lanjut", breadcrumb_aktif="Proses Tugas", data_tindaklanjut=cari_tindaklanjut, data_suratmasuk=cari_suratmasuk)

@kepalaupt.route("/historika/<int:id>", methods=["GET"])
def historitindaklanjutka(id):

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
    x = cari_tindaklanjut[0]["penugas"]

    
    ka = kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = list_st()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if x in list_of_ka :
        cari = model.kepalaupt.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 
        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]
        x = cari

    elif x in list_of_st :
        cari = model.staff.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

        x = cari

    cari_tindaklanjut[0]["penugas"] = x['nama_jabatan']
    
    # Pastikan berhasil
    if cari_tindaklanjut is None:
        return f"Gagal mencari surat dengan id: {id}.", 400
    cari_tindaklanjut[0]["data_followup"] = model.followup.atur.caribytindaklanjut(cari_tindaklanjut[0]['id'])
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama
    cari_tindaklanjut[0]["penanggungjawab"] = jabatan_nama[cari_tindaklanjut[0]["penanggungjawab"]]
    
    return render_template("kepalaupt/status-followup.j2", title="Histori Tindak Lanjut", data_tindaklanjut=cari_tindaklanjut, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Histori Tindak Lanjut")