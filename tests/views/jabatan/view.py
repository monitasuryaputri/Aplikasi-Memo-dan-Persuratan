from flask import Blueprint, request, session, escape, redirect, flash, jsonify, render_template
from tests import model, app
from tests.model import jabatan, daftar, hapus, ubah, cari, tambah, JABATAN_KIND, Jabatan, cari_nama
from tests.model.exception import EntityIdException, EntityNotFoundException
from tests.model import admin, daftar, cari
from tests.model import kepalaupt, daftar, cari
from tests.model import staff, daftar, cari


jabatan = Blueprint("jabatan", __name__, url_prefix="/jabatan")

#Jabatan

# Endpoint untuk URL: /jabatan
#

# Tampilkan halaman jika sudah login

@jabatan.route("/tambah", methods=["POST"])
def jabatan_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        jabatan_baru = request.get_json()
    elif request.form:
        jabatan_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    # Periksa parameter sudah benar
    if jabatan_baru is None:
        return "Data Jabatan baru tidak ada!", 400        
    if "nama" not in jabatan_baru.keys():
        return "Salah data! Property nama tidak ada.", 400
    

    nama = escape(jabatan_baru["nama"]).strip()

    # Tambah jabatan baru
    try:
        hasil = tambah(nama)
    except EntityNotFoundException:
        return f"Gagal menambah jabatan baru", 400

    # Pastikan berhasil
    if (hasil is None):
        return "Gagal menambah data!", 500

    return "Berhasil", 200

@jabatan.route("/daftar", methods=["GET"])
def jabatan_daftar():

    # Minta data semua jabatan
    status = True

    hasil = model.jabatan.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar jabatan.", 400

    # Ubah class ke dictionary
    daftar_jabatan = []
    for satu_hasil in hasil:
        daftar_jabatan.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "status" : status, "data": daftar_jabatan }

    return jsonify(hasil), 200

@jabatan.route("/disposisi", methods=["GET"])
def jabatan_disposisi():

    # Minta data semua jabatan
    status = True

    hasil = model.jabatan.atur.disposisi()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar jabatan.", 400

    # Ubah class ke dictionary
    daftar_jabatan = []
    for satu_hasil in hasil:
        daftar_jabatan.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "status" : status, "data": daftar_jabatan }

    return jsonify(hasil), 200

@jabatan.route("/cari/nama", methods=["GET"])
def jabatan_cari_nama():
    nama = request.form.get("nama")

    try:
        hasil = cari_nama(nama)
    except:
        return f"Gagal mengambil nama '{nama}'", 400

        # Pastikan berhasil
    if hasil is None:
        return f"Gagal mengambil nama '{nama}'", 400

    # Buat wrapper dictionaty untuk dikembalikan
    hasil_json = []
    for satu_hasil in hasil:
        # kalau tidak diubah ke dictionary hasilnya error json not serializable(?)
        satu_hasil_json = satu_hasil.ke_dictionary()
        hasil_json.append(satu_hasil_json)            

    return jsonify(hasil_json), 200

@jabatan.route("/hapus/<int:id>", methods=["DELETE"])
def jabatan_hapus(id):
    # Panggil method hapus 
    try:
        hasil = hapus(id)
    except: 
        return f"Gagal menghapus jabatan dengan id: {id}.", 400

    return "Berhasil", 200


@jabatan.route("/ubah/<int:id>", methods=["PUT"])
def jabatan_ubah(id):
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        jabatan_baru = request.get_json()
    if request.form:
        jabatan_baru = request.form
    else:
        return "Hanya menerima request json dan form",400

    
    # Periksa parameter sudah benar
    if jabatan_baru is None:
        return "Data jabatan baru tidak ada!", 400        
    if "nama" not in jabatan_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    
    jabatan_baru = Jabatan(id=id, 
                            nama=jabatan["nama"]) 
                            
    try:
        hasil = ubah(id, jabatan_baru) 
    except EntityNotFoundException:
        return f"Tidak ada jabatan dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah jabatan dengan id: {id}.", 400
    
   # Pastikan berhasil
    if (hasil is None):
        return "Gagal menambah data!", 500

    return "Berhasil", 200

@jabatan.route("/cari/<int:id>", methods=["GET"])
def jabatan_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari jabatan dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari jabatan dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil), 200
