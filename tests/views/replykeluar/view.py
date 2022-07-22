from tests.views import replykeluar
from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app
from tests.model.replykeluar import tambah
from tests.model.replykeluar import daftar
from tests.model.replykeluar import cari
from tests.model.replykeluar import Replykeluar
from tests.model.replykeluar import REPLYKELUAR_KIND
from datetime import datetime
from tests.views.admin.view import suratkeluar

from google.cloud import datastore

from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi


app.config['UPLOAD_PATH'] = '/data_dir/file_komen '


replykeluar = Blueprint("replykeluar", __name__, url_prefix="/replykeluar")


#reply


@replykeluar.route("/tambah", methods=["POST"])
def replykeluar_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        replykeluar_baru = request.get_json()
    elif request.form:
        replykeluar_baru = request.form
        
    else:
        return "Hanya menerima request json dan form", 400  
    
    # Periksa parameter sudah benar
    if replykeluar_baru is None:
        return "Data reply baru tidak ada!", 400        
    if "isi_replykeluar" not in replykeluar_baru.keys():
        return "Salah data! Property isi_reply tidak ada.", 400
    isi_replykeluar = str(escape(replykeluar_baru["isi_replykeluar"]))
    id = str(escape(replykeluar_baru["komenkeluar"]).strip())
    suratkeluar = str(escape(replykeluar_baru["suratkeluar"]).strip())
    
    #  update array id surat komen
    cari_komenkeluar = model.komenkeluar.atur.caribykomenkeluar(int(suratkeluar), int(id))

    if len(cari_komenkeluar) == 1:
        cari_komenkeluar = cari_komenkeluar[0]

        # Tambah reply baru
        try:
            hasil = tambah(session['id'], id, suratkeluar, isi_replykeluar)
        except EntityNotFoundException:
            return f"Gagal menambah komen baru", 400

        cari_suratkeluar = model.suratkeluar.atur.cari(int(suratkeluar))

        if len(cari_suratkeluar) == 1:
            cari_suratkeluar = cari_suratkeluar[0]
            # json dumps
            cari_suratkeluar['reply'] = json.loads(cari_suratkeluar['reply'])
            cari_komenkeluar['reply'] = json.loads(cari_komenkeluar['reply'])
            cari_komenkeluar['reply'] += [str(hasil.id)]
            cari_suratkeluar['reply'] += [str(hasil.id)]
            cari_suratkeluar['reply'] = json.dumps(cari_suratkeluar['reply'])
            cari_komenkeluar['reply'] = json.dumps(cari_komenkeluar['reply'])
            
            del cari_suratkeluar['id']
            del cari_komenkeluar['id']
            
            try:
                hasil = model.suratkeluar.atur.update(int(suratkeluar), cari_suratkeluar)
                hasil = model.komenkeluar.atur.update(int(id), cari_komenkeluar)
                status = True
                msg = "Success"
            except: 
                msg = f"Update Gagal update suratkeluar dengan id: {id}.", 400
            else:
                msg = f"Len Gagal update suratkeluar dengan id: {id}.", 400
            
    return redirect(request.referrer)

@replykeluar.route("/daftar", methods=["GET"])
def replykeluar_daftar():

    # Minta data semua komen
    hasil = daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar komen.", 400

    # Ubah class ke dictionary
    daftar_replykeluar = []
    for satu_hasil in hasil:
        daftar_replykeluar.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "daftar": daftar_replykeluar }

    return jsonify(hasil), 200

@replykeluar.route("/cari/<int:id>", methods=["GET"])
def replykeluar_cari(id):
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
    


