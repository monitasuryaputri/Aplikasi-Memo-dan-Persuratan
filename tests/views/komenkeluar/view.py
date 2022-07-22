from tests.views import komenkeluar
from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app
from tests.model.komenkeluar import tambah
from tests.model.komenkeluar import daftar
from tests.model.komenkeluar import cari
from tests.model.komenkeluar import Komenkeluar
from tests.model.komenkeluar import KOMENKELUAR_KIND
from datetime import datetime

from google.cloud import datastore

from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi


app.config['UPLOAD_PATH'] = '/data_dir/file_komen '


komenkeluar = Blueprint("komenkeluar", __name__, url_prefix="/komenkeluar")


#komen


@komenkeluar.route("/tambah", methods=["POST"])
def komenkeluar_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        komenkeluar_baru = request.get_json()
    elif request.form:
        komenkeluar_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400   

    # Periksa parameter sudah benar
    if komenkeluar_baru is None:
        return "Data komentar baru tidak ada!", 400        
    if "isi_komenkeluar" not in komenkeluar_baru.keys():
        return "Salah data! Property isi_komen tidak ada.", 400 
    
    file_komenkeluar = request.files.getlist("file_komenkeluar")
    isi_komenkeluar = str(escape(komenkeluar_baru["isi_komenkeluar"]))
    id = str(escape(komenkeluar_baru["id_suratkeluar"]).strip())

    #  update array id surat komen
    cari_suratkeluar = model.suratkeluar.atur.cari(int(id))

    if len(cari_suratkeluar) == 1:
        cari_suratkeluar = cari_suratkeluar[0]

        # Tambah komen baru
        try:
            hasil = tambah(session['id'], id, cari_suratkeluar['nomor_surat'], isi_komenkeluar, file_komenkeluar)
        except EntityNotFoundException:
            return f"Gagal menambah komen baru", 400
        # json dumps
        cari_suratkeluar['komentar'] = cari_suratkeluar['komentar']
        cari_suratkeluar['komentar'] += [str(hasil.id)]
        cari_suratkeluar['dokumen'] += hasil.file_komenkeluar

        del cari_suratkeluar['id']

    try:
        hasil = model.suratkeluar.atur.update(int(id), cari_suratkeluar)

        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update suratkeluar dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update suratkeluar dengan id: {id}.", 400

   
    # Pastikan berhasil
    if (hasil is None):
        # set flash message
        return "Gagal", 400
    return redirect(request.referrer)
    # return "Berhasil", 200

@komenkeluar.route("/daftar", methods=["GET"])
def komenkeluar_daftar():

    # Minta data semua komen
    hasil = daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar komen.", 400

    # Ubah class ke dictionary
    daftar_komenkeluar = []
    for satu_hasil in hasil:
        daftar_komenkeluar.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "daftar": daftar_komenkeluar }

    return jsonify(hasil), 200


@komenkeluar.route("/komenkeluar/cari/<int:id>", methods=["GET"])
def komenkeluar_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari komen dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari komen dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil.ke_dictionary()), 200
    


