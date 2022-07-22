from tests.model.konfigurasi.daftar_role import ADMIN_ROLE
from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app

from tests.model.suratkeluar import SURATKELUAR_KIND

from tests.model.admin import tambah as tambah_admin
from tests.model.admin import hapus as hapus_admin
from tests.model.admin import ubah as ubah_admin
from tests.model.admin import cari as cari_admin
from tests.model.admin import cari_email as cari_email_admin
from tests.model.admin import Admin
from tests.model.admin import ADMIN_KIND
from datetime import datetime
from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi
from google.cloud import datastore

from tests.views.kepalaupt.view import kepalaupt_list as list_ka
from tests.views.staff.view import staff_list as list_st

admin = Blueprint("admin", __name__, url_prefix="/admin")

#Admin

# Endpoint untuk URL: /dashboardadmin
#

# Tampilkan halaman jika sudah login

@admin.route("/tambah", methods=["POST"])
def admin_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        admin_baru = request.get_json()
    elif request.form:
        admin_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    # Periksa parameter sudah benar
    if admin_baru is None:
        return "Data Admin baru tidak ada!", 400        
    if "nama" not in admin_baru.keys():
        return "Salah data! Property nama tidak ada.", 400
    if "email" not in admin_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    if "no_hp" not in admin_baru.keys():
        return "Salah data! Property no_hp tidak ada.", 400

    nama = escape(admin_baru["nama"]).strip()
    email = escape(admin_baru["email"]).strip()
    no_hp = escape(admin_baru["no_hp"]).strip()
    jabatan = escape(admin_baru["jabatan"]).strip()

    # Tambah admin baru
    try:
        hasil = tambah_admin(nama,email,no_hp,jabatan)
    except EntityNotFoundException:
        return f"Gagal menambah admin baru", 400

    # Pastikan berhasil
    if (hasil is None):
    #     return "Gagal menambah data!", 500

        # set flash message
        flash('Gagal menambah admin baru')
        # direct ke laman tambah admin
        return redirect(url_for('superadmin.superadmin_admin_tambah'))

    # set flash message
    flash('Admin berhasil ditambahkan')         
    #direct ke halaman daftar admin
    return redirect(url_for('superadmin.dashboardsuperadmin'))


@admin.route("/daftar", methods=["GET"])
def admin_daftar():

    # Minta data semua admin
    hasil = model.admin.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar admin.", 400

    # Ubah class ke dictionary
    daftar_admin = []
    for satu_hasil in hasil:
        daftar_admin.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "daftar": daftar_admin }

    return jsonify(hasil), 200

@admin.route("/listad", methods=["GET"])
def admin_list():

    # Minta data semua admin
    hasil = model.admin.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar admin.", 400

    # Ubah class ke dictionary
    daftar_admin = []
    for satu_hasil in hasil:
        daftar_admin.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil =  daftar_admin 
    
    return hasil

@admin.route("/cari/email", methods=["GET"])
def admin_cari_email():
    email = request.form.get("email")

    try:
        hasil = cari_email_admin(email)
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

@admin.route("/hapus/<int:id>")
def admin_hapus(id):
    
    # panggil method hapus
    try:
        hapus_admin(id)
    except: 
        return f"Gagal menghapus admin dengan id: {id}.", 400

    # set flash message
    flash('Admin berhasil dihapus')
    #direct ke halaman daftar Staff
    return redirect('/superadmin/dashboardsuperadmin')


@admin.route("/ubah/<int:id>", methods=["POST"])
def admin_ubah(id):
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        admin_baru = request.get_json()
    if request.form:
        admin_baru = request.form
    else:
        return "Hanya menerima request json dan form",400

    
    # Periksa parameter sudah benar
    if admin_baru is None:
        return "Data admin baru tidak ada!", 400        
    if "nama" not in admin_baru.keys():
        return "Salah data! Property nama tidak ada.", 400
    if "email" not in admin_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    if "no_hp" not in admin_baru.keys():
        return "Salah data! Property no_hp tidak ada.", 400
    
    admin_baru = Admin(id=id, 
                        nama=admin_baru["nama"],
                        email=admin_baru["email"],
                        no_hp=admin_baru["no_hp"]) 
                            
    try:
        hasil = ubah_admin(id, admin_baru) 
    except EntityNotFoundException:
        return f"Tidak ada admin dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah admin dengan id: {id}.", 400
    
   # Pastikan berhasil
    if (hasil is None):

        # set flash message
        flash('Gagal mengubah data admin')
        # direct ke laman tambah admin
        return redirect(url_for('superadmin.superadmin_admin_ubah'))

    # set flash message
    flash('Admin berhasil diubah')         
    #direct ke halaman daftar admin
    return redirect(url_for('superadmin.superadmin_admin_daftar'))


@admin.route("admin/cari/<int:id>", methods=["GET"])
def admin_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari_admin(id)
    except: 
        return f"Gagal mencari admin dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari admin dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil), 200

#halaman dashboard
@admin.route("/dashboardadmin", methods=["GET"])
def dashboardadmin():

    if session['role'] != ADMIN_ROLE:
        return redirect('/admin')

    return render_template("admin/dashboardadmin.j2", title="Dashboard")


#halaman detail surat masuk
@admin.route("/detailsuratmasuk/<int:id>", methods=['GET', 'POST'])
def detailsuratmasuk(id):

    pembaca =  model.suratmasuk.atur.cari(id)
    ad = admin_list()
    list_of_ad = [id for elem in ad
                    for id in elem.values()]
    ka = list_ka()
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

    elif session['id'] in list_of_ad:
        cari = model.admin.atur.cari(session['id'])
        cari = cari[0]['jabatan']

        pembaca[0]['dibaca'] = pembaca[0]['dibaca'] 
        if len(pembaca[0]['dibaca']) >= 1:
            if cari not in pembaca[0]['dibaca']:
                pembaca[0]['dibaca'] += [cari]
            else:
                pembaca[0]['dibaca'].remove(cari)
                pembaca[0]['dibaca'] += [cari]
        else:
            pembaca[0]['dibaca'] += [cari]

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
    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratmasuk is None:
        return f"Gagal mencari surat dengan id: {id}.", 400
    
    cari_suratmasuk[0]["data_komentar"] = model.komenmasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    cari_suratmasuk[0]["data_reply"] = model.replymasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])

    return render_template("admin/detailsuratmasuk.j2", title="Detail Surat Masuk", data_suratmasuk=cari_suratmasuk, breadcrumb="Home", breadcrumb_nonactive="Surat Masuk", breadcrumb_active="Detail Surat Masuk")

#halaman detail draf surat
@admin.route("/detaildrafsurat/<int:id>", methods=["GET"])
def detaildrafsurat(id):

    # Lakukan pencarian draf surat berdasar id
    try:
        cari_suratkeluar = model.suratkeluar.atur.detail(id)
        jabatan = model.jabatan.daftar()
    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratkeluar is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratkeluar[0]["data_komentar"] = model.komenkeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])
    cari_suratkeluar[0]["data_reply"] = model.replykeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])
    return render_template("admin/detaildrafsurat.j2", title="Detail Draf Surat", data_suratkeluar=cari_suratkeluar, daftar_jabatan=jabatan, breadcrumb="Home", breadcrumb_nonactive="Draf Surat", breadcrumb_active="Detail Draf Surat")

#halaman detail surat keluar
@admin.route("/detailsuratkeluar/<int:id>", methods=["GET"])
def detailsuratkeluar(id):

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

    return render_template("admin/detailsuratkeluar.j2", title="Detail Surat Keluar", data_suratkeluar=cari_suratkeluar, breadcrumb="Home", breadcrumb_nonactive="Surat Keluar", breadcrumb_active="Detail Surat Keluar")

#halaman draf surat
@admin.route("/drafsurat", methods=["GET"])
def drafsurat():

    suratkeluar = model.suratkeluar.atur.daftar()

    return render_template("admin/drafsurat.j2", title="Draf Surat",  daftar_suratkeluar=suratkeluar, breadcrumb="Home", breadcrumb_active="Draf Surat")

#halaman surat keluar
@admin.route("/suratkeluar", methods=["GET"])
def suratkeluar():

    suratkeluar = model.suratkeluar.atur.daftar()

    return render_template("admin/suratkeluar.j2", title="Surat Keluar", daftar_suratkeluar=suratkeluar, breadcrumb="Home", breadcrumb_active="Surat Keluar")

#halaman surat Masuk
@admin.route("/suratmasuk", methods=["GET"])
def suratmasuk():

    suratmasuk = model.suratmasuk.atur.daftar()

    return render_template("admin/suratmasuk.j2", title="Surat Masuk", breadcrumb="Home", breadcrumb_active="Surat Masuk",  daftar_suratmasuk=suratmasuk)

#halaman tambah surat masuk
@admin.route("/tambahsuratmasuk", methods=["GET"])
def tambahsuratmasuk():

    jabatan = model.jabatan.atur.disposisi()
    
    return render_template("admin/tambahsuratmasuk.j2", title="Tambah Surat Masuk",  daftar_jabatan=jabatan, breadcrumb="Home", breadcrumb_nonactive="Surat Masuk", breadcrumb_active="Tambah Surat Masuk")


#halaman tambah surat keluar
@admin.route("/tambahsuratkeluar", methods=["GET"])
def tambahsuratkeluar():

    jabatan = model.jabatan.atur.disposisi()

    return render_template("admin/tambahsuratkeluar.j2", title="Tambah Surat Keluar", daftar_jabatan=jabatan, breadcrumb="Home", breadcrumb_nonactive="Draf Surat", breadcrumb_active="Tambah Surat Keluar")
