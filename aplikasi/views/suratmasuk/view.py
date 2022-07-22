from flask import Blueprint, request, redirect, flash, url_for
from aplikasi.model.suratmasuk import tambah


from aplikasi.model.exception import EntityNotFoundException

suratmasuk = Blueprint("suratmasuk", __name__, url_prefix="/suratmasuk")

"""
Rute Untuk Surat Masuk

"""

# rute untuk menambah surat masuk 
@suratmasuk.route("/tambah", methods=["POST"])
def suratmasuk_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        suratmasuk_baru = request.get_json()
    elif request.form:
        suratmasuk_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400


    # Periksa parameter sudah benar
    if suratmasuk_baru is None:
        return "Data Surat Masuk baru tidak ada!", 400        
    if "nomor_surat" not in suratmasuk_baru.keys():
        return "Salah data! Property nomor_surat tidak ada.", 400
    if "tgl_surat" not in suratmasuk_baru.keys():
        return "Salah data! Property tgl_surat tidak ada.", 400
    if "asal_surat" not in suratmasuk_baru.keys():
        return "Salah data! Property asal_surat tidak ada.", 400
    if "hal" not in suratmasuk_baru.keys():
        return "Salah data! Property hal tidak ada.", 400
    if "isi_ringkas" not in suratmasuk_baru.keys():
        return "Salah data! Property isi_ringkas tidak ada.", 400
    
    dokumen = request.files.getlist("dokumen[]")
    nomor_surat = str(request.form.get("nomor_surat"))
    tgl_surat = str(request.form.get("tgl_surat"))
    asal_surat = str(request.form.get("asal_surat"))
    hal = str(request.form.get("hal"))
    isi_ringkas = str(request.form.get("isi_ringkas"))
    disposisi = request.form.getlist("disposisi")

    # Tambah surat masuk baru
    try:
        hasil = tambah(nomor_surat, tgl_surat, asal_surat, hal, isi_ringkas, dokumen, disposisi)
    except EntityNotFoundException:
        return f"Gagal menambah surat masuk baru", 400

    # Pastikan berhasil
    if (hasil is None):
        # set flash message
        flash('Gagal menambah surat masuk baru')
        # direct ke laman tambah suratmasuk
        return redirect(url_for('admin.tambahsuratmasuk'))

    # set flash message
    flash('Surat berhasil ditambahkan')         
    #direct ke halaman surat masuk
    return redirect(url_for('admin.suratmasuk'))