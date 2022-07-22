from tests.model.konfigurasi.daftar_role import KEPALAUPT_ROLE, SUPERADMIN_ROLE, ADMIN_ROLE, STAFF_ROLE
from flask import Blueprint, request, session, escape, redirect, flash, jsonify, render_template
from tests import model, app
from tests.model import superadmin, daftar, hapus, ubah, cari, tambah, SUPERADMIN_KIND, Superadmin, cari_email
from tests.model.exception import EntityIdException, EntityNotFoundException
# import aplikasi.model.konfigurasi
from tests.model import admin, daftar, cari
from tests.model import kepalaupt, daftar, cari
from tests.model import staff, daftar, cari

from flask_login import login_required

superadmin = Blueprint("superadmin", __name__, url_prefix="/superadmin")

#Super Admin

# Endpoint untuk URL: /dashboardadmin
#

# Tampilkan halaman jika sudah login

@superadmin.route("/tambah", methods=["POST"])
def superadmin_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        superadmin_baru = request.get_json()
    elif request.form:
        superadmin_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    # Periksa parameter sudah benar
    if superadmin_baru is None:
        return "Data Super Admin baru tidak ada!", 400        
    if "email" not in superadmin_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    

    email = escape(superadmin_baru["email"]).strip()

    # Tambah admin baru
    try:
        hasil = tambah(email)
    except EntityNotFoundException:
        return f"Gagal menambah admin baru", 400

    # Pastikan berhasil
    if (hasil is None):
        return "Gagal menambah data!", 500

    return "Berhasil", 200

@superadmin.route("/daftar", methods=["GET"])
def superadmin_daftar():

    # Minta data semua admin
    hasil = model.superadmin.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar superadmin.", 400

    # Ubah class ke dictionary
    daftar_superadmin = []
    for satu_hasil in hasil:
        daftar_superadmin.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionary untuk dikembalikan
    hasil = { "daftar": daftar_superadmin }

    return jsonify(hasil), 200

@superadmin.route("/list", methods=["GET"])
def superadmin_list():

    # Minta data semua superadmin
    hasil = model.superadmin.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar admin.", 400

    # Ubah class ke dictionary
    daftar_superadmin = []
    for satu_hasil in hasil:
        daftar_superadmin.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil =  daftar_superadmin 
    
    return hasil

@superadmin.route("/cari/email", methods=["GET"])
def superadmin_cari_email():
    email = request.form.get("email")

    try:
        hasil = cari_email(email)
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

@superadmin.route("/hapus/<int:id>", methods=["DELETE"])
def superadmin_hapus(id):
    # Panggil method hapus 
    try:
        hasil = hapus(id)
    except: 
        return f"Gagal menghapus superadmin dengan id: {id}.", 400

    return "Berhasil", 200


@superadmin.route("/ubah/<int:id>", methods=["PUT"])
def superadmin_ubah(id):
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        superadmin_baru = request.get_json()
    if request.form:
        superadmin_baru = request.form
    else:
        return "Hanya menerima request json dan form",400

    
    # Periksa parameter sudah benar
    if superadmin_baru is None:
        return "Data superadmin baru tidak ada!", 400        
    if "email" not in superadmin_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    
    superadmin_baru = Superadmin(id=id, 
                                email=superadmin["email"]) 
                            
    try:
        hasil = ubah(id, superadmin_baru) 
    except EntityNotFoundException:
        return f"Tidak ada superadmin dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah superadmin dengan id: {id}.", 400
    
   # Pastikan berhasil
    if (hasil is None):
        return "Gagal menambah data!", 500

    return "Berhasil", 200

@superadmin.route("/cari/<int:id>", methods=["GET"])
def superadmin_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari superadmin dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari superadmin dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil), 200

#halaman dashboard
@superadmin.route("/dashboardsuperadmin", methods=["GET"])
def dashboardsuperadmin():
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role SUPERADMIN_ROLE maka direct ke landing page
    if session['role'] != SUPERADMIN_ROLE:
        return redirect('/superadmin')
    admin = model.admin.atur.daftarjabatan()
    kepalaupt = model.kepalaupt.atur.daftarjabatan()
    staff = model.staff.atur.daftarjabatan()
    # Muat template
    return render_template("superadmin/list-petugas.j2", title="Dashboard", daftar_admin=admin, daftar_kepalaupt=kepalaupt, daftar_staff=staff )


#halaman ubah admin model superadmin
@superadmin.route("/admin/ubah/<int:id>", methods=["GET"])
def superadmin_admin_ubah(id):
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
    if session['role'] != SUPERADMIN_ROLE:
        return redirect('/superadmin')
    
    # lakukan pencarian admin berdasar id
    try:
        cari_admin = model.admin.atur.cari(id)
    except:
        return f"Gagal mencari admin dengan id: {id}.", 400

    # pastikan berhasil
    if cari_admin is None:
        return f"Gagal mencari admin dengan id: {id}.", 400

    # Load template
    # parameter title dikirim untuk mengisi nilai variabel title di template
    return render_template("superadmin/ubah-admin.j2",
                            title="UPT Laboratorium Terpadu",
                            judul="Ubah Admin",
                            
                            isi_breadcrumb="ubah admin",
                            data_admin=cari_admin)

#halaman ubah kepalaupt model superadmin
@superadmin.route("/kepalaupt/ubah/<int:id>", methods=["GET"])
def superadmin_kepala_ubah(id):
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
    if session['role'] != SUPERADMIN_ROLE:
        return redirect('/superadmin')
    
    # lakukan pencarian kepalaupt berdasar id
    try:
        cari_kepalaupt = model.kepalaupt.atur.cari(id)
    except:
        return f"Gagal mencari kepala upt dengan id: {id}.", 400

    # pastikan berhasil
    if cari_kepalaupt is None:
        return f"Gagal mencari kepala upt dengan id: {id}.", 400

    # Load template
    # parameter title dikirim untuk mengisi nilai variabel title di template
    return render_template("superadmin/ubah-kepalaupt.j2",
                            title="UPT Laboratorium Terpadu",
                            judul="Ubah Kepala UPT",
                            
                            isi_breadcrumb="ubah kepala upt",
                            data_kepalaupt=cari_kepalaupt)

                            #halaman ubah admin model superadmin
@superadmin.route("/staff/ubah/<int:id>", methods=["GET"])
def superadmin_staff_ubah(id):
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
    if session['role'] != SUPERADMIN_ROLE:
        return redirect('/superadmin')
    
    # lakukan pencarian staff berdasar id
    try:
        cari_staff = model.staff.atur.cari(id)
    except:
        return f"Gagal mencari staff dengan id: {id}.", 400

    # pastikan berhasil
    if cari_staff is None:
        return f"Gagal mencari staff dengan id: {id}.", 400

    # Load template
    # parameter title dikirim untuk mengisi nilai variabel title di template
    return render_template("superadmin/ubah-staff.j2",
                            title="UPT Laboratorium Terpadu",
                            judul="Ubah Staff",
                            
                            isi_breadcrumb="ubah staff",
                            data_staff=cari_staff)

#halaman tambah admin modul superadmin
@superadmin.route("/admin/tambah", methods=["GET"])
def superadmin_admin_tambah():
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role SUPERADMIN_ROLE maka direct ke landing page
    if session['role'] != SUPERADMIN_ROLE:
        return redirect('/superadmin')
    # Load template 
    # parameter title dikirim untuk mengisi nilai variabel title di template
    return render_template("superadmin/tambah-admin.j2", title="UPT Laboratorium Terpadu", judul="Tambah Admin", isi_breadcrumb="Tambah Admin")

#halaman tambah kepalaupt modul superadmin
@superadmin.route("/kepalaupt/tambah", methods=["GET"])
def superadmin_kepalaupt_tambah():
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
    if session['role'] != SUPERADMIN_ROLE:
        return redirect('/superadmin')
    # Load template 
    # parameter title dikirim untuk mengisi nilai variabel title di template
    return render_template("superadmin/tambah-kepalaupt.j2", title="UPT Laboratorium Terpadu", judul="Tambah Kepala UPT", isi_breadcrumb="Tambah Kepala UPT")

#halaman tambah staff modul superadmin
@superadmin.route("/staff/tambah", methods=["GET"])
def superadmin_staff_tambah():
    # periksa login user, jika sudah login ditandai dengan adanya session role
    # periksa session role, jika bukan role ADMIN_ROLE maka direct ke landing page
    if session['role'] != SUPERADMIN_ROLE:
        return redirect('/superadmin')
    # Load template 
    # parameter title dikirim untuk mengisi nilai variabel title di template
    return render_template("superadmin/tambah-staff.j2", title="UPT Laboratorium Terpadu", judul="Tambah Staff", isi_breadcrumb="Tambah Staff")
