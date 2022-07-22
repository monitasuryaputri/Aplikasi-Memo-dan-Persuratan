from flask import Blueprint, request, redirect, flash, url_for
from aplikasi.model.surat import tambah

from aplikasi.model.exception import EntityNotFoundException

surat = Blueprint("surat", __name__, url_prefix="/surat")

"""
Rute Untuk Surat

"""

# rute untuk menambah surat masuk 
@surat.route("/tambah", methods=["POST"])
def surat_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        surat_baru = request.get_json()
    elif request.form:
        surat_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400


    # Periksa parameter sudah benar
    if surat_baru is None:
        return "Data Surat baru tidak ada!", 400        
    if "nomor" not in surat_baru.keys():
        return "Salah data! Property nomor tidak ada.", 400
    if "tujuan" not in surat_baru.keys():
        return "Salah data! Property tujuan tidak ada.", 400
    if "isi" not in surat_baru.keys():
        return "Salah data! Property isi tidak ada.", 400

    nomor = str(surat_baru.get("nomor"))
    tujuan = str(surat_baru.get("tujuan"))
    isi = str(surat_baru.get("isi"))
    dokumen = request.files.getlist("dokumen[]")

    # Tambah surat masuk baru
    try:
        hasil = tambah(nomor, tujuan, isi, dokumen)
    except EntityNotFoundException:
        return f"Gagal menambah surat baru", 400

    # Pastikan berhasil
    if (hasil is None):
        # set flash message
        flash('Gagal menambah surat baru')
        # direct ke laman tambah suratmasuk
        return redirect(url_for('manajemen.tambahsurat'))

    # set flash message
    flash('Surat berhasil ditambahkan')         
    #direct ke halaman surat masuk
    return redirect(url_for('manajemen.surat'))