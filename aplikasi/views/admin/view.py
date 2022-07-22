from aplikasi import model, app

from aplikasi.model.konfigurasi.daftar_role import ADMIN_ROLE
from flask import Blueprint, request, session, escape, redirect, flash, render_template, url_for, jsonify

from aplikasi.model.admin import tambah as tambah_admin
from aplikasi.model.admin import hapus as hapus_admin
from aplikasi.model.admin import ubah as ubah_admin
from aplikasi.model.admin import Admin
from aplikasi.model.exception import EntityNotFoundException

from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st

admin = Blueprint("admin", __name__, url_prefix="/admin")

#Admin
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
    return redirect(url_for('superadmin.dashboardsuperadmin'))


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
    
    cari_admin = model.admin.atur.cari(id)

    if len(cari_admin) == 1:
        cari_admin = cari_admin[0]
        
        cari_admin["nama"] = admin_baru["nama"]
        cari_admin["no_hp"] = admin_baru["no_hp"]
        cari_admin["email"] = admin_baru["email"]
        cari_admin["jabatan"] = cari_admin["jabatan"]
        cari_admin["picture"] = cari_admin["picture"]

        del cari_admin["id"]
                            
    try:
        hasil = ubah_admin(id, cari_admin) 
    except EntityNotFoundException:
        return f"Tidak ada admin dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah admin dengan id: {id}.", 400
    
   # Pastikan berhasil
    if (hasil is None):

        # set flash message
        flash('Gagal mengubah data admin')
        # direct ke laman ubah admin
        return redirect('/superadmin/admin/ubah/'+id)

    # set flash message
    flash('Admin berhasil diubah')         
    #direct ke halaman dashboard superadmin
    return redirect(url_for('superadmin.dashboardsuperadmin'))

#halaman dashboard
@admin.route("/dashboardadmin", methods=["GET"])
def dashboardadmin():

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

    # Muat template
    return render_template("admin/dashboardadmin.j2", 
                            title="Dashboard")

#halaman surat Masuk
@admin.route("/suratmasuk", methods=["GET"])
def suratmasuk():

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    
    # Muat template
    return render_template("admin/suratmasuk.j2", 
                            title="Surat Masuk", 
                            breadcrumb="Home", 
                            breadcrumb_active="Surat Masuk", 
                            daftar_suratmasuk=suratmasuk)

#halaman tambah surat masuk
@admin.route("/tambahsuratmasuk", methods=["GET"])
def tambahsuratmasuk():

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

    jabatan = model.jabatan.atur.disposisi()
    
    # Muat template
    return render_template("admin/tambahsuratmasuk.j2", 
                            title="Tambah Surat Masuk",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Surat Masuk", 
                            breadcrumb_active="Tambah Surat Masuk", 
                            daftar_jabatan=jabatan)

#halaman detail surat masuk
@admin.route("/detailsuratmasuk/<int:id>", methods=['GET', 'POST'])
def detailsuratmasuk(id):

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

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
    
    # Muat template
    return render_template("admin/detailsuratmasuk.j2", 
                            title="Detail Surat Masuk",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Surat Masuk", 
                            breadcrumb_active="Detail Surat Masuk", 
                            data_suratmasuk=cari_suratmasuk)

#halaman draf surat
@admin.route("/drafsurat", methods=["GET"])
def drafsurat():

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

    suratkeluar = model.suratkeluar.atur.daftar()

    # Muat template
    return render_template("admin/drafsurat.j2", 
                            title="Draf Surat",
                            breadcrumb="Home", 
                            breadcrumb_active="Draf Surat", 
                            daftar_suratkeluar=suratkeluar)

#halaman tambah surat keluar
@admin.route("/tambahsuratkeluar", methods=["GET"])
def tambahsuratkeluar():

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

    jabatan = model.jabatan.atur.disposisi()
    
    # Muat template
    return render_template("admin/tambahsuratkeluar.j2", 
                            title="Tambah Surat Keluar",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Draf Surat", 
                            breadcrumb_active="Tambah Surat Keluar", 
                            daftar_jabatan=jabatan)

#halaman detail draf surat
@admin.route("/detaildrafsurat/<int:id>", methods=["GET"])
def detaildrafsurat(id):

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

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
    
    # Muat template
    return render_template("admin/detaildrafsurat.j2", 
                            title="Detail Draf Surat",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Draf Surat", 
                            breadcrumb_active="Detail Draf Surat", 
                            data_suratkeluar=cari_suratkeluar, 
                            daftar_jabatan=jabatan)

#halaman surat keluar
@admin.route("/suratkeluar", methods=["GET"])
def suratkeluar():

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

    suratkeluar = model.suratkeluar.atur.daftar()

    # Muat template
    return render_template("admin/suratkeluar.j2", 
                            title="Surat Keluar",
                            breadcrumb="Home", 
                            breadcrumb_active="Surat Keluar", 
                            daftar_suratkeluar=suratkeluar)

#halaman detail surat keluar
@admin.route("/detailsuratkeluar/<int:id>", methods=["GET"])
def detailsuratkeluar(id):

    if session['role'] != ADMIN_ROLE:
        return redirect('/')

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

    # Muat template
    return render_template("admin/detailsuratkeluar.j2", 
                            title="Detail Surat Keluar",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Surat Keluar", 
                            breadcrumb_active="Detail Surat Keluar", 
                            data_suratkeluar=cari_suratkeluar)








