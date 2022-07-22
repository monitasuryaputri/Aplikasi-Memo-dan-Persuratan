from tests.model.konfigurasi.daftar_role import STAFF_ROLE
from tests.views.kepalaupt import view

from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app
from datetime import datetime

from tests.model.staff import tambah
from tests.model.staff import daftar
from tests.model.staff import hapus
from tests.model.staff import ubah
from tests.model.staff import cari
from tests.model.staff import cari_email
from tests.model.staff import Staff
from tests.model.staff import STAFF_KIND

from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi
from google.cloud import datastore

staff = Blueprint("staff", __name__, url_prefix="/staff")

#staff
@staff.route("/tambah", methods=["POST"])
def staff_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        staff_baru = request.get_json()
    elif request.form:
        staff_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    # Periksa parameter sudah benar
    if staff_baru is None:
        return "Data Staff baru tidak ada!", 400        
    if "nama" not in staff_baru.keys():
        return "Salah data! Property nama tidak ada.", 400
    if "no_hp" not in staff_baru.keys():
        return "Salah data! Property no_hp tidak ada.", 400
    if "email" not in staff_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    if "jabatan" not in staff_baru.keys():
        return "Salah data! Property jabatan tidak ada.", 400
   
    nama = escape(staff_baru["nama"]).strip()
    no_hp = escape(staff_baru["no_hp"]).strip()
    email = escape(staff_baru["email"]).strip()
    jabatan = escape(staff_baru["jabatan"]).strip()

    # Tambah staff baru
    try:
        hasil = tambah(nama, no_hp, email, jabatan)
    except EntityNotFoundException:
        return f"Gagal menambah staff baru", 400

    # # Pastikan berhasil
    if (hasil is None):
    #     return "Gagal menambah data!", 500

        # set flash message
        flash('Gagal menambah staff baru')
        # direct ke laman tambah staff
        return redirect(url_for('superadmin.superadmin_staff_tambah'))

    # set flash message
    flash('Staff berhasil ditambahkan')         
    #direct ke halaman daftar staff
    return redirect(url_for('superadmin.dashboardsuperadmin'))

@staff.route("/daftar", methods=["GET"])
def staff_daftar():

    # Minta data semua staff
    hasil = model.staff.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar staff.", 400

    # Ubah class ke dictionary
    daftar_staff = []
    for satu_hasil in hasil:
        daftar_staff.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "daftar": daftar_staff }

    return jsonify(hasil), 200

@staff.route("/listst", methods=["GET"])
def staff_list():

    # Minta data semua staff
    hasil = model.staff.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar staff.", 400

    # Ubah class ke dictionary
    daftar_staff = []
    for satu_hasil in hasil:
        daftar_staff.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil =  daftar_staff
    
    return hasil

@staff.route("/cari/email", methods=["GET"])
def staff_cari_email():
    email = request.form.get("email")

    try:
        hasil = cari_email(email)
    except:
        return f"Gagal mengambil email '{email}'", 400

        # Pastikan berhasil
    if hasil is None:
        return f"Gagal mengambil email '{email}'", 400

    # Buat wrapper dictionaty untuk dikembalikan
    hasil_json = []
    for satu_hasil in hasil:
        # kalau tidak diubah ke dictionary hasilnya error json not serializable(?)
        satu_hasil_json = satu_hasil.ke_dictionary()
        hasil_json.append(satu_hasil_json)            

    return jsonify(hasil_json), 200

@staff.route("/hapus/<int:id>")
def staff_hapus(id):

    # Panggil method hapus 
    try:
        hapus(id)
    except: 
        return f"Gagal menghapus staff dengan id: {id}.", 400

    # set flash message
    flash('Staff berhasil dihapus')         
    # direct ke halaman daftar staff
    return redirect(url_for('superadmin.dashboardsuperadmin'))

@staff.route("/ubah/<int:id>", methods=["POST"])
def staff_ubah(id):
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        staff_baru = request.get_json()
    elif request.form:
        staff_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    
    # Periksa parameter sudah benar
    if staff_baru is None:
        return "Data Staff baru tidak ada!", 400        
    if "nama" not in staff_baru.keys():
        return "Salah data! Property nama tidak ada.", 400
    if "no_hp" not in staff_baru.keys():
        return "Salah data! Property no_hp tidak ada.", 400
    if "email" not in staff_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    if "jabatan" not in staff_baru.keys():
        return "Salah data! Property jabatan tidak ada.", 400
    
    staff_baru = Staff(id=id, 
                        nama=staff_baru["nama"], 
                        no_hp=staff_baru["no_hp"],
                        email=staff_baru["email"],
                        jabatan=staff_baru["jabatan"]
                        )

    try:
        hasil = ubah(id, staff_baru) 
    except EntityNotFoundException:
        return f"Tidak ada staff dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah staff dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        # set flash message
        flash('Gagal mengubah data staff')
        # direct ke laman tambah staff
        return redirect('/superadmin/staff/ubah/'+id)

    # set flash message
    flash('Data staff berhasil diubah')         
    # direct ke halaman daftar staff
    return redirect(url_for('superadmin.dashboardsuperadmin'))

@staff.route("/staff/cari/<int:id>", methods=["GET"])
def staff_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari staff dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari staff dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil.ke_dictionary()), 200


# Endpoint untuk URL: /dashboardstaff
#

# Tampilkan halaman jika sudah login

#halaman dashboard
@staff.route("/dashboardstaff", methods=["GET"])
def dashboardstaff():



    if session['role'] != STAFF_ROLE:
        return redirect('/staff')

    return render_template("staff/dashboardstaff.j2", title="Dashboard")

#halaman Detail Draf Surat
@staff.route("/detaildrafsuratstaff/<int:id>", methods=["GET"])
def detaildrafsuratstaff(id):

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

    return render_template("staff/detaildrafsuratstaff.j2", title="Detail Draf Surat", data_suratkeluar=cari_suratkeluar, daftar_jabatan=jabatan, breadcrumb="Home", breadcrumb_nonactive="Draf Surat", breadcrumb_active="Detail Draf Surat")


@staff.route("/detaildrafsuratstaff/tugaskan/<int:id>", methods=["POST"])
def detaildrafsuratstaff_tugaskan(id):

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

#halaman Detail Surat Keluar
@staff.route("/detailsuratkeluar/<int:id>", methods=["GET"])
def detailsuratkeluarstaff(id):

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


    return render_template("staff/detailsuratkeluar.j2", title="Detail Surat Keluar", data_suratkeluar=cari_suratkeluar, breadcrumb="Home", breadcrumb_nonactive="Surat Keluar", breadcrumb_active="Detail Surat Keluar")

#halaman Detail Surat Masuk
@staff.route("/detailsuratmasukstaff/<int:id>", methods=["GET"])
def detailsuratmasukstaff(id):

    pembaca =  model.suratmasuk.atur.cari(id)

    
    ka = view.kepalaupt_list
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = staff_list()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if session['id'] in list_of_ka:
        cari = model.kepalaupt.atur.cari(session['id'])
        cari = cari[0]['jabatan']

        pembaca[0]['dibaca'] = pembaca[0]['dibaca']
        if len(pembaca[0]['dibaca']) >= 1:
            for x in pembaca[0]['dibaca']:
                if (x != cari):
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
    
    # Pastikan berhasil
    if cari_suratmasuk is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratmasuk[0]["data_komentar"] = model.komenmasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    cari_suratmasuk[0]["data_reply"] = model.replymasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])

    return render_template("staff/detailsuratmasukstaff.j2", title="Detail Surat Masuk", data_suratmasuk=cari_suratmasuk, daftar_jabatan=jabatan, breadcrumb="Home", breadcrumb_nonactive="Surat Masuk", breadcrumb_active="Detail Surat Masuk")

#halaman detail surat masuk update
@staff.route("/detailsuratmasukstaff/update/<int:id>", methods=["POST"])
def detailsuratmasukstaff_update(id):

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
    else:
        msg = f"Len Gagal update surat masuk dengan id: {id}.", 400


    return {
        'status' : status,
        'msg' : msg
    }


#halaman Detail Tindak Lanjut
@staff.route("/detailtindaklanjutstaff/<int:id>", methods=["GET"])
def detailtindaklanjutstaff(id):

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

    return render_template("staff/detailtindaklanjutstaff.j2", title="Detail Tindak Lanjut", data_suratmasuk=cari_suratmasuk,  breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut")

#halaman Detail Tindak Lanjut Selesai
@staff.route("/detailtindaklanjutselesaistaff/<int:id>", methods=["GET"])
def detailtindaklanjutselesaistaff(id):

    try:
        cari_suratmasuk = model.suratmasuk.atur.cari(id)
    except: 
        return f"try Gagal mencari pengaduan dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratmasuk is None:
        return f"None Gagal mencari pengaduan dengan id: {id}.", 400

    cari_suratmasuk[0]["data_tindaklanjut"] = model.tindaklanjut.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])


    return render_template("staff/detailtindaklanjutselesaistaff.j2", title="Detail Tindak Lanjut Selesai", data_suratmasuk=cari_suratmasuk,  breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut Selesai")

#halaman Draf Surat
@staff.route("/drafsuratstaff", methods=["GET"])
def drafsuratstaff():

    suratkeluar = model.suratkeluar.atur.daftarbyjabatan(session['jabatan'])


    return render_template("staff/drafsuratstaff.j2", title="Draf Surat", daftar_suratkeluar=suratkeluar, breadcrumb="Home", breadcrumb_active="Draf Surat")

#halaman Surat Keluar Staff
@staff.route("/suratkeluarstaff", methods=["GET"])
def suratkeluarstaff():

    suratkeluar = model.suratkeluar.atur.daftarbyjabatan(session['jabatan'])

    return render_template("staff/suratkeluarstaff.j2", title="Surat Keluar", daftar_suratkeluar=suratkeluar, breadcrumb="Home", breadcrumb_active="Surat Keluar")

#halaman Surat Masuk Staff
@staff.route("/suratmasukstaff", methods=["GET"])
def suratmasukstaff():

    suratmasuk = model.suratmasuk.atur.daftarbyjabatan(session['jabatan'])

    return render_template("staff/suratmasukstaff.j2", title="Surat Masuk", daftar_suratmasuk=suratmasuk, breadcrumb="Home", breadcrumb_active="Surat Masuk")

#halaman Tindak Lanjut Staff
@staff.route("/tindaklanjutstaff", methods=["GET"])
def tindaklanjutstaff():

    suratmasuk = model.suratmasuk.atur.daftarbyjabatan(session['jabatan'])

    return render_template("staff/tindaklanjutstaff.j2", title="Tindak Lanjut", daftar_suratmasuk=suratmasuk, breadcrumb="Home", breadcrumb_active="Tindak Lanjut")


@staff.route("/isi-tindaklanjutstaff/<int:id>", methods=["GET"])
def isitindaklanjutstaff(id):

    # try:
    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
    x = cari_tindaklanjut[0]["penugas"]

   
    ka = view.kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = staff_list()
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

    # except: 
        # return f"Except Gagal mencari surat dengan id: {id}.", 400
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

    return render_template("staff/isi-tindaklanjutstaff.j2", title="Tugas Tindak Lanjut", data_tindaklanjut=cari_tindaklanjut, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Tugas Tindak Lanjut")

@staff.route("/isi-tindaklanjutstaff/edit/<int:id>", methods=["GET"])
def edittindaklanjutstaff(id):

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)

    return render_template("staff/edittindaklanjutstaff.j2", title="Tugas Tindak Lanjut", data_tindaklanjut=cari_tindaklanjut, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Tugas Tindak Lanjut")

@staff.route("/isi-tindaklanjutstaff/simpan/<int:id>", methods=["POST"])
def simpantindaklanjutstaff(id):

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)

    if len(cari_tindaklanjut) == 1:
        cari_tindaklanjut = cari_tindaklanjut[0]

        cari_tindaklanjut['tenggatwaktu'] = request.form.get("tenggatwaktu")

        del cari_tindaklanjut['id']

        model.tindaklanjut.atur.update(id, cari_tindaklanjut)
        
    return redirect('/staff/isi-tindaklanjutstaff/'+ str(id))

@staff.route("/followup/<int:id>", methods=["GET"])
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
    return render_template("staff/followup.j2", title="Proses Tugas" , breadcrumb="Home", breadcrumb_nonactive="Surat Masuk", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Tugas Tindak Lanjut", breadcrumb_aktif="Proses Tugas", data_tindaklanjut=cari_tindaklanjut, data_suratmasuk=cari_suratmasuk)

@staff.route("/histori/<int:id>", methods=["GET"])
def historitindaklanjut(id):

    # try:
    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
    x = cari_tindaklanjut[0]["penugas"]

    ka = view.kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = staff_list()
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
    
    # except: 
    #     return f"Except Gagal mencari surat dengan id: {id}.", 400
    # Pastikan berhasil
    if cari_tindaklanjut is None:
        return f"Gagal mencari surat dengan id: {id}.", 400
    cari_tindaklanjut[0]["data_followup"] = model.followup.atur.caribytindaklanjut(cari_tindaklanjut[0]['id'])
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama
    cari_tindaklanjut[0]["penanggungjawab"] = jabatan_nama[cari_tindaklanjut[0]["penanggungjawab"]]

    return render_template("staff/status-followup.j2", title="Histori Tindak Lanjut", data_tindaklanjut=cari_tindaklanjut, breadcrumb="Home", breadcrumb_nonactive="Tindak Lanjut", breadcrumb_active="Detail Tindak Lanjut", breadcrumb_activated="Histori Tindak Lanjut")