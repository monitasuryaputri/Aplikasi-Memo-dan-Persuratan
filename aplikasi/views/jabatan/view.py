from aplikasi import model, app
from flask import Blueprint, request, escape, jsonify

from aplikasi.model.jabatan import daftar, disposisi, tambah
from aplikasi.model.exception import EntityNotFoundException

jabatan = Blueprint("jabatan", __name__, url_prefix="/jabatan")

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

    hasil = daftar()

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

    hasil = disposisi()

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