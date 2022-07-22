from aplikasi.model.admin.atur import daftarjabatan
from aplikasi.model.konfigurasi.daftar_role import MANAJEMEN_ROLE
from flask import Blueprint, request, session, redirect, flash, jsonify, render_template, escape
from aplikasi import model, app
from aplikasi.model import jabatan, tambah, ubah, MANAJEMEN_KIND, Manajemen
from aplikasi.model.exception import EntityIdException, EntityNotFoundException
# import aplikasi.model.konfigurasi
from aplikasi.model import admin, daftar, cari
from aplikasi.model import kepalaupt, daftar, cari
from aplikasi.model import staff, daftar, cari

from aplikasi.views.kepalaupt.view import kepalaupt_list as kepalaupt_list
from aplikasi.views.staff.view import staff_list as list_st

from flask_login import login_required

# from aplikasi.views.admin.view import suratmasuk  

manajemen = Blueprint("manajemen", __name__, url_prefix="/manajemen")

#Super Admin

# Endpoint untuk URL: /dashboardadmin
#

# Tampilkan halaman jika sudah login

@manajemen.route("/tambah", methods=["POST"])
def manajemen_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        manajemen_baru = request.get_json()
    elif request.form:
        manajemen_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    # # Periksa parameter sudah benar
    # if  manajemen_baru is None:
    #     return "Data Super Admin baru tidak ada!", 400        
    # if "email" not in  manajemen_baru.keys():
    #     return "Salah data! Property email tidak ada.", 400
    

    email_manajemen = escape(manajemen_baru["manajemen"]).strip()
    # app.logger.info(email)
    # app.logger.info(type(email))
    # Tambah admin baru
    try:
        hasil = model.manajemen.atur.tambah(email_manajemen)
    except EntityNotFoundException:
        return f"Gagal menambah admin baru", 400

    # # Pastikan berhasil
    # if (hasil is None):
    #     return "Gagal menambah data!", 500

    return "Berhasil", 200

@manajemen.route("/daftar", methods=["GET"])
def manajemen_daftar():

    # Minta data semua admin
    data = model.manajemen.atur.daftar()
    app.logger.info(data)
    app.logger.info(type(data))
    # app.logger.info("isi dalam data daftar manajemen di view")
    # app.logger.info(data)

    # Ubah class ke dictionary
    manajemen_list = []

    for x in data:
       
        manajemen_list.append(x.ke_dictionary())

    # Buat wrapper dictionary untuk dikembalikan
    
    return jsonify(manajemen_list), 200

@manajemen.route("/list", methods=["GET"])
def manajemen_list():

    # Minta data semua superadmin
    hasil = model.manajemen.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar admin.", 400

    # Ubah class ke dictionary
    daftar_manajemen = []
    for satu_hasil in hasil:
        daftar_manajemen.append(satu_hasil)

    # Buat wrapper dictionaty untuk dikembalikan
    hasil =  daftar_manajemen 
    return hasil

@manajemen.route("/cari/email", methods=["GET"])
def manajemen_cari_email():
    email = request.form.get("email")

    try:
        hasil = model.manajemen.atur.cari_email(email)
    except:
        return f"Gagal mengambil email '{email}'", 400

    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mengambil email '{email}'", 400

    # Buat wrapper dictionary untuk dikembalikan
    hasil_json = []
    for satu_hasil in hasil:
        # kalau tidak diubah ke dictionary hasilnya error json not serializable(?)
        satu_hasil_json = satu_hasil.ke_dictionary()
        hasil_json.append(satu_hasil_json)            

    return jsonify(hasil_json), 200

# @superadmin.route("/hapus/<int:id>", methods=["DELETE"])
# def superadmin_hapus(id):
#     # Panggil method hapus 
#     try:
#         hasil = hapus(id)
#     except: 
#         return f"Gagal menghapus superadmin dengan id: {id}.", 400

#     return "Berhasil", 200


@manajemen.route("/ubah/<int:id>", methods=["POST"])
def manajemen_ubah(id):
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        manajemen_baru = request.get_json()
    if request.form:
        manajemen_baru = request.form
    else:
        return "Hanya menerima request json dan form",400
    # Periksa parameter sudah benar
    if manajemen_baru is None:
        return "Data superadmin baru tidak ada!", 400        
    if "email" not in manajemen_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    
    cari_manajemen = model.manajemen.atur.cari(id)

    if len(cari_manajemen) == 1:
        cari_manajemen = cari_manajemen[0]
        
        cari_manajemen["email"] = manajemen_baru["email"]
                            
    try:
        hasil = ubah(id, cari_manajemen) 
    except EntityNotFoundException:
        return f"Tidak ada superadmin dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah superadmin dengan id: {id}.", 400
    
   # Pastikan berhasil
    if (hasil is None):
        return "Gagal menambah data!", 500

    return "Berhasil", 200

# @superadmin.route("/cari/<int:id>", methods=["GET"])
# def superadmin_cari(id):
#     # Lakukan pencarian
#     try:
#         hasil = cari(id)
#     except: 
#         return f"Gagal mencari superadmin dengan id: {id}.", 400
    
#     # Pastikan berhasil
#     if hasil is None:
#         return f"Gagal mencari superadmin dengan id: {id}.", 400
#     # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
#     return jsonify(hasil), 200

# #halaman dashboard
# @manajemen.route("/berandamanajemen", methods=["GET"])
# def berandamanajemen():
#     # periksa login user, jika sudah login ditandai dengan adanya session role
#     # periksa session role, jika bukan role MANAJEMEN maka direct ke landing page
    
        
#     admin = model.admin.atur.daftar() # == daftar (tipe list dari atur)

#     # Muat template
#     return render_template("manajemen/beranda-manajemen.j2", judul="Dashboard", daftar_admin=admin )

#halaman dashboard tes surat masuk
@manajemen.route("/berandamanajemen", methods=["GET"])
def berandamanajemen():
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role MANAJEMEN maka direct ke landing page
    
        
    staf = model.staff.atur.daftarjabatan() ## == daftar (tipe list dari atur dengan )


    # Muat template
    return render_template("manajemen/beranda-manajemen.j2", judul="Dashboard", daftar_staf=staf )

#halaman surat 
@manajemen.route("/surat", methods=["GET"])
def surat():

    surat = model.surat.atur.daftar()
    # Muat template
    return render_template("manajemen/surat-manajemen.j2", 
                            title="Surat", 
                            breadcrumb="Home", 
                            breadcrumb_active="Surat", 
                            daftar_surat=surat)

#halaman tambah surat
@manajemen.route("/tambahsurat", methods=["GET"])
def tambahsurat():

    jabatan = model.jabatan.atur.disposisi()
    
    # Muat template
    return render_template("manajemen/tambahsurat.j2", 
                            title="Surat", 
                            breadcrumb="Home", 
                            breadcrumb_active="Surat", 
                            daftar_jabatan=jabatan)

#halaman detail surat masuk
@manajemen.route("/detailsurat/<int:id>", methods=["GET"])
def detailsurat(id):

    # Lakukan pencarian surat masuk berdasar id
    cari_surat = model.surat.atur.detail(id)

    # Muat template
    return render_template("manajemen/detailsurat.j2", 
                            title="Detail Surat Masuk",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Surat Masuk", 
                            breadcrumb_active="Detail Surat Masuk",
                            data_surat=cari_surat
                            )

# #halaman ubah admin model superadmin
# @superadmin.route("/admin/ubah/<int:id>", methods=["GET"])
# def superadmin_admin_ubah(id):
#     # periksa login user, jika sudah login ditandai dengan adanya session role
#     # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
#     if session['role'] != SUPERADMIN_ROLE:
#         return redirect('/superadmin')
    
#     # lakukan pencarian admin berdasar id
#     try:
#         cari_admin = model.admin.atur.cari(id)
#     except:
#         return f"Gagal mencari admin dengan id: {id}.", 400

#     # pastikan berhasil
#     if cari_admin is None:
#         return f"Gagal mencari admin dengan id: {id}.", 400

#     # Load template
#     # parameter title dikirim untuk mengisi nilai variabel title di template
#     return render_template("superadmin/ubah-admin.j2",
#                             title="UPT Laboratorium Terpadu",
#                             judul="Ubah Admin",
#                             isi_breadcrumb="ubah admin",
#                             data_admin=cari_admin)

# #halaman ubah kepalaupt model superadmin
# @superadmin.route("/kepalaupt/ubah/<int:id>", methods=["GET"])
# def superadmin_kepala_ubah(id):
#     # periksa login user, jika sudah login ditandai dengan adanya session role
#     # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
#     if session['role'] != SUPERADMIN_ROLE:
#         return redirect('/superadmin')
    
#     # lakukan pencarian kepalaupt berdasar id
#     try:
#         cari_kepalaupt = model.kepalaupt.atur.cari(id)
#     except:
#         return f"Gagal mencari kepala upt dengan id: {id}.", 400

#     # pastikan berhasil
#     if cari_kepalaupt is None:
#         return f"Gagal mencari kepala upt dengan id: {id}.", 400

#     # Load template
#     # parameter title dikirim untuk mengisi nilai variabel title di template
#     return render_template("superadmin/ubah-kepalaupt.j2",
#                             title="UPT Laboratorium Terpadu",
#                             judul="Ubah Kepala UPT",
#                             isi_breadcrumb="ubah kepala upt",
#                             data_kepalaupt=cari_kepalaupt)

#                             #halaman ubah admin model superadmin
# @superadmin.route("/staff/ubah/<int:id>", methods=["GET"])
# def superadmin_staff_ubah(id):
#     # periksa login user, jika sudah login ditandai dengan adanya session role
#     # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
#     if session['role'] != SUPERADMIN_ROLE:
#         return redirect('/superadmin')
    
#     # lakukan pencarian staff berdasar id
#     try:
#         cari_staff = model.staff.atur.cari(id)
#     except:
#         return f"Gagal mencari staff dengan id: {id}.", 400

#     # pastikan berhasil
#     if cari_staff is None:
#         return f"Gagal mencari staff dengan id: {id}.", 400

#     # Load template
#     # parameter title dikirim untuk mengisi nilai variabel title di template
#     return render_template("superadmin/ubah-staff.j2",
#                             title="UPT Laboratorium Terpadu",
#                             judul="Ubah Staff",
#                             isi_breadcrumb="ubah staff",
#                             data_staff=cari_staff)

# #halaman tambah admin modul superadmin
# @superadmin.route("/admin/tambah", methods=["GET"])
# def superadmin_admin_tambah():
#     # periksa login user, jika sudah login ditandai dengan adanya session role
#     # periksa session role, jika bukan role SUPERADMIN_ROLE maka direct ke landing page
#     if session['role'] != SUPERADMIN_ROLE:
#         return redirect('/superadmin')
#     # Load template 
#     # parameter title dikirim untuk mengisi nilai variabel title di template
#     return render_template("superadmin/tambah-admin.j2", title="UPT Laboratorium Terpadu", judul="Tambah Admin", isi_breadcrumb="Tambah Admin")

# #halaman tambah kepalaupt modul superadmin
# @superadmin.route("/kepalaupt/tambah", methods=["GET"])
# def superadmin_kepalaupt_tambah():
#     # periksa login user, jika sudah login ditandai dengan adanya session role
#     # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
#     if session['role'] != SUPERADMIN_ROLE:
#         return redirect('/superadmin')
#     # Load template 
#     # parameter title dikirim untuk mengisi nilai variabel title di template
#     return render_template("superadmin/tambah-kepalaupt.j2", title="UPT Laboratorium Terpadu", judul="Tambah Kepala UPT", isi_breadcrumb="Tambah Kepala UPT")

# #halaman tambah staff modul superadmin
# @superadmin.route("/staff/tambah", methods=["GET"])
# def superadmin_staff_tambah():
#     # periksa login user, jika sudah login ditandai dengan adanya session role
#     # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
#     if session['role'] != SUPERADMIN_ROLE:
#         return redirect('/superadmin')
#     # Load template 
#     # parameter title dikirim untuk mengisi nilai variabel title di template
#     return render_template("superadmin/tambah-staff.j2", title="UPT Laboratorium Terpadu", judul="Tambah Staff", isi_breadcrumb="Tambah Staff")

#halaman tambah staff modul superadmin
@manajemen.route("/superadmin/tambah", methods=["GET"])
def manajemen_superadmin_tambah():
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # parameter title dikirim untuk mengisi nilai variabel title di template
    return render_template("manajemen/tambah-superadmin.j2", title="UPT Laboratorium Terpadu", judul="Tambah Superadmin", isi_breadcrumb="Tambah Superadmin")
