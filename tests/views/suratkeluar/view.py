from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app
from tests.model.suratkeluar import tambah
from tests.model.suratkeluar import daftar
from tests.model.suratkeluar import cari
from tests.model.suratkeluar import Suratkeluar
from tests.model.suratkeluar import SURATKELUAR_KIND

from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi

suratkeluar = Blueprint("suratkeluar", __name__, url_prefix="/suratkeluar")

#Suratkeluar


@suratkeluar.route("/tambah", methods=["POST"])
def suratkeluar_tambah():

    nomor_surat = str(escape(request.form.get("nomor_surat")).strip())
    tgl_surat = str(escape(request.form.get("tgl_surat")).strip())
    tujuan_surat = str(escape(request.form.get("tujuan_surat")).strip())
    hal = str(escape(request.form.get("hal")).strip()  ) 
    isi_ringkas = str(escape(request.form.get("isi_ringkas")).strip())
    dokumen = request.files.getlist("dokumen")

    disposisi = request.form.getlist("disposisi")
    
    
    # Tambah surat keluar baru
    try:
        hasil = tambah(nomor_surat, tgl_surat, tujuan_surat, hal, isi_ringkas, dokumen, disposisi)
    except EntityNotFoundException:
        return f"Gagal menambah surat baru", 400

    # Pastikan berhasil
    if (hasil is None):
        # return "Gagal menambah data!", 500

        # set flash message
        flash('Gagal menambah admin baru')
        # direct ke laman tambah suratkeluar
        return redirect(url_for('admin.tambahsuratkeluar'))

    # set flash message
    flash('Surat berhasil ditambahkan')         
    #direct ke halaman surat masuk
    return redirect(url_for('admin.drafsurat'))


@suratkeluar.route("/daftar", methods=["GET"])
def suratkeluar_daftar():

    # Minta data semua suratkeluar
    hasil = model.suratkeluar.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar surat masuk.", 400

    # Ubah class ke dictionary
    daftar_suratkeluar = []
    for satu_hasil in hasil:
        daftar_suratkeluar.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "daftar": daftar_suratkeluar }

    return jsonify(hasil), 200

@suratkeluar.route("/cari/<int:id>", methods=["GET"])
def suratkeluar_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari surat masuk dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari surat masuk dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil), 200

# Submit draf surat menjadi surat keluar
@suratkeluar.route("/kirim/<int:id>", methods=["GET"])
def suratkeluar_kirim(id):
    
    cari_suratkeluar = model.suratkeluar.atur.cari(int(id))

    if len(cari_suratkeluar) == 1:
        cari_suratkeluar = cari_suratkeluar[0]

        if cari_suratkeluar['status'] == "draf":
            cari_suratkeluar['status'] = "submit"
        del cari_suratkeluar['id']


    try:
        hasil = model.suratkeluar.atur.update(int(id), cari_suratkeluar)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update suratkeluar dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update suratkeluar dengan id: {id}.", 400

   
    return redirect(url_for('kepalaupt.suratkeluarka'))

# Submit draf surat menjadi surat keluar
@suratkeluar.route("/keluar/<int:id>", methods=["GET"])
def suratkeluar_keluar(id):
    
    cari_suratkeluar = model.suratkeluar.atur.cari(int(id))

    if len(cari_suratkeluar) == 1:
        cari_suratkeluar = cari_suratkeluar[0]

        if cari_suratkeluar['status'] == "draf":
            cari_suratkeluar['status'] = "submit"
        del cari_suratkeluar['id']


    try:
        hasil = model.suratkeluar.atur.update(int(id), cari_suratkeluar)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update suratkeluar dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update suratkeluar dengan id: {id}.", 400

   
    return redirect(url_for('staff.suratkeluarstaff'))


# Submit draf surat menjadi surat keluar
@suratkeluar.route("/submit/<int:id>", methods=["GET"])
def suratkeluar_submit(id):
    
    cari_suratkeluar = model.suratkeluar.atur.cari(int(id))

    if len(cari_suratkeluar) == 1:
        cari_suratkeluar = cari_suratkeluar[0]

        if cari_suratkeluar['status'] == "draf":
            cari_suratkeluar['status'] = "submit"
        del cari_suratkeluar['id']


    try:
        hasil = model.suratkeluar.atur.update(int(id), cari_suratkeluar)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update suratkeluar dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update suratkeluar dengan id: {id}.", 400

   
    return redirect(url_for('admin.suratkeluar'))
