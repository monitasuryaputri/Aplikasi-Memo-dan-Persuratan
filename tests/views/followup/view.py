from tests.views import followup
from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app

from tests.model.followup import tambah
from tests.model.followup import daftar
from tests.model.followup import cari
from tests.model.followup import Followup
from tests.model.followup import FOLLOWUP_KIND
from datetime import datetime

from google.cloud import datastore

from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi


app.config['UPLOAD_PATH'] = '/data_dir/file_followup '


followup = Blueprint("followup", __name__, url_prefix="/followup")


#followup


@followup.route("/tambahstaff", methods=["POST"])
def followup_tambahstaff():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        followup_baru = request.get_json()
    elif request.form:
        followup_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400   

    # Periksa parameter sudah benar
    if followup_baru is None:
        return "Data Pengaduan baru tidak ada!", 400        
    if "isi_followup" not in followup_baru.keys():
        return "Salah data! Property isi_followup tidak ada.", 400 
    
    
    file_followup = request.files.getlist("file_followup")
    isi_followup = str(escape(followup_baru["isi_followup"]))
    id = str(escape(followup_baru["tindaklanjut"]).strip())


    #  update array id tindaklanjut followup
    cari_tindaklanjut = model.tindaklanjut.atur.cari(int(id))
    
    if len(cari_tindaklanjut) == 1:
        cari_tindaklanjut = cari_tindaklanjut[0]

        # Tambah followup baru
        try:
            hasil = tambah(session['id'], id, isi_followup, file_followup)
        except EntityNotFoundException:
            return f"Gagal menambah followup baru", 400

        # jsn dumps
        cari_tindaklanjut['followup'] = json.loads(cari_tindaklanjut['followup'])
        cari_tindaklanjut['followup'] += [str(hasil.id)]
        cari_tindaklanjut['followup'] = json.dumps(cari_tindaklanjut['followup'])

        del cari_tindaklanjut['id']

    try:
        hasil = model.tindaklanjut.atur.update(int(id), cari_tindaklanjut)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update tindaklanjut dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update tindaklanjut dengan id: {id}.", 400

    # set flash message
    # flash('Pengaduan berhasil ditambahkan')         
    # direct ke halaman beranda isi tindaklanjut
    return redirect("/staff/isi-tindaklanjutstaff/" + id)

@followup.route("/tambahka", methods=["POST"])
def followup_tambahka():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        followup_baru = request.get_json()
    elif request.form:
        followup_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400   

    # Periksa parameter sudah benar
    if followup_baru is None:
        return "Data Pengaduan baru tidak ada!", 400        
    if "isi_followup" not in followup_baru.keys():
        return "Salah data! Property isi_followup tidak ada.", 400 
    
    
    file_followup = request.files.getlist("file_followup")
    
    isi_followup = str(escape(followup_baru["isi_followup"]))
    id = str(escape(followup_baru["tindaklanjut"]).strip())


    #  update array id tindaklanjut followup
    cari_tindaklanjut = model.tindaklanjut.atur.cari(int(id))
    
    if len(cari_tindaklanjut) == 1:
        cari_tindaklanjut = cari_tindaklanjut[0]

        # Tambah followup baru
        try:
            hasil = tambah(session['id'], id, isi_followup, file_followup)
        except EntityNotFoundException:
            return f"Gagal menambah followup baru", 400

        # jsn dumps
        cari_tindaklanjut['followup'] = json.loads(cari_tindaklanjut['followup'])
        cari_tindaklanjut['followup'] += [str(hasil.id)]
        cari_tindaklanjut['followup'] = json.dumps(cari_tindaklanjut['followup'])

        del cari_tindaklanjut['id']

    try:
        hasil = model.tindaklanjut.atur.update(int(id), cari_tindaklanjut)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update tindaklanjut dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update tindaklanjut dengan id: {id}.", 400

   
    # Pastikan berhasil
    if (hasil is None):
    #     # set flash message
        flash('Gagal menambah followup baru')
    #     # direct ke laman buat followup
        return redirect("/penindaklanjut/buat-tindaklanjut/" + id)

    # set flash message
    flash('Follow up berhasil ditambahkan')         
    # # direct ke halaman beranda isi tindaklanjut
    return redirect("/kepalaupt/isi-tindaklanjutka/" + id)

@followup.route("/daftar", methods=["GET"])
def followup_daftar():

    # Minta data semua followup
    hasil = daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar followup.", 400

    # Ubah class ke dictionary
    daftar_followup = []
    for satu_hasil in hasil:
        daftar_followup.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "daftar": daftar_followup }

    return jsonify(hasil), 200


@followup.route("/followup/cari/<int:id>", methods=["GET"])
def followup_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari followup dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari followup dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil.ke_dictionary()), 200
    


