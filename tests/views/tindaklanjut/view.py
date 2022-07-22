from tests.model.tindaklanjut.model import Tindaklanjut
from flask import Blueprint, json, request, session, escape, redirect, flash, jsonify, render_template, url_for
from tests import model, app
from tests.model.tindaklanjut import tambah
from tests.model.tindaklanjut import daftar
from tests.model.tindaklanjut import cari
from tests.model.tindaklanjut import Tindaklanjut
from tests.model.tindaklanjut import TINDAKLANJUT_KIND
from datetime import datetime

from google.cloud import datastore

from tests.model.exception import EntityIdException, EntityNotFoundException
import tests.model.konfigurasi


app.config['UPLOAD_PATH'] = '/data_dir/file_komen '


tindaklanjut = Blueprint("tindaklanjut", __name__, url_prefix="/tindaklanjut")


#komen


@tindaklanjut.route("/tambah", methods=["POST"])
def tindaklanjut_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        tindaklanjut_baru = request.get_json()
    elif request.form:
        tindaklanjut_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400   

    # Periksa parameter sudah benar
    if tindaklanjut_baru is None:
        return "Data tindaklanjut baru tidak ada!", 400        
    if "tugas" not in tindaklanjut_baru.keys():
        return "Salah data! Property tugas tidak ada.", 400 
    if "penanggungjawab" not in tindaklanjut_baru.keys():
        return "Salah data! Property penanggungjawab tidak ada.", 400 
    if "tenggatwaktu" not in tindaklanjut_baru.keys():
        return "Salah data! Property tenggatwaktu tidak ada.", 400 
 
    id = str(escape(tindaklanjut_baru["id_suratmasuk"]).strip())
    tugas = str(escape(tindaklanjut_baru["tugas"]))
    penanggungjawab = escape(tindaklanjut_baru["penanggungjawab"]).strip()
    tenggatwaktu = str(escape(tindaklanjut_baru["tenggatwaktu"]))

    #  update array id surat komen
    cari_suratmasuk = model.suratmasuk.atur.cari(int(id))

    if len(cari_suratmasuk) == 1:
        cari_suratmasuk = cari_suratmasuk[0]

        # Tambah tindaklanjut
        try:
            hasil = tambah(session['id'], id, cari_suratmasuk['nomor_surat'], tugas, penanggungjawab, tenggatwaktu)
            
        except EntityNotFoundException:
            return f"Gagal menambah tindaklanjut baru", 400

        # json dumps
        cari_suratmasuk['tindaklanjut'] = json.loads(cari_suratmasuk['tindaklanjut'])
        cari_suratmasuk['tindaklanjut'] += [str(hasil.id)]
        cari_suratmasuk['tindaklanjut'] = json.dumps(cari_suratmasuk['tindaklanjut'])
        if cari_suratmasuk['status_tindaklanjut'] == "-":
            cari_suratmasuk['status_tindaklanjut'] = "proses"
        del cari_suratmasuk['id']

    try:
        hasil = model.suratmasuk.atur.update(int(id), cari_suratmasuk)

        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update suratmasuk dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update suratmasuk dengan id: {id}.", 400

   
    # Pastikan berhasil
    if (hasil is None):
        # set flash message
        # flash('Gagal menambah komen baru')
        # direct ke laman buat komen
        # return redirect("/penindaklanjut/buat-tindaklanjut/" + id)
        return "Gagal", 400
    # set flash message
    # flash('komentar berhasil ditambahkan')         
    # direct ke halaman beranda operator
    return redirect(request.referrer)
    # return "Berhasil", 200

@tindaklanjut.route("/daftar", methods=["GET"])
def tindaklanjut_daftar():

    # Minta data semua komen
    hasil = daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar komen.", 400

    # Ubah class ke dictionary
    daftar_tindaklanjut = []
    for satu_hasil in hasil:
        daftar_tindaklanjut.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil = { "daftar": daftar_tindaklanjut }

    return jsonify(hasil), 200

@tindaklanjut.route("/selesai/<int:id>", methods=["GET"])
def tindaklanjut_selesai(id):

    cari_suratmasuk = model.suratmasuk.atur.cari(int(id))

    if len(cari_suratmasuk) == 1:
        cari_suratmasuk = cari_suratmasuk[0]

        if cari_suratmasuk['status_tindaklanjut'] == "proses":
            cari_suratmasuk['status_tindaklanjut'] = "selesai"
        del cari_suratmasuk['id']

    try:
        hasil = model.suratmasuk.atur.update(int(id), cari_suratmasuk)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update pengaduan dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update pengaduan dengan id: {id}.", 400

   
    return redirect(url_for('kepalaupt.tindaklanjut'))

@tindaklanjut.route("/selesaistaff/<int:id>", methods=["GET"])
def tindaklanjut_selesaistaff(id):

    cari_suratmasuk = model.suratmasuk.atur.cari(int(id))

    if len(cari_suratmasuk) == 1:
        cari_suratmasuk = cari_suratmasuk[0]

        if cari_suratmasuk['status_tindaklanjut'] == "proses":
            cari_suratmasuk['status_tindaklanjut'] = "selesai"
        del cari_suratmasuk['id']

    try:
        hasil = model.suratmasuk.atur.update(int(id), cari_suratmasuk)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update pengaduan dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update pengaduan dengan id: {id}.", 400

   
    return redirect(url_for('staff.tindaklanjutstaff'))

@tindaklanjut.route("/kirim/<int:id>", methods=["GET"])
def tindaklanjut_kirim(id):
    
    cari_tindaklanjut = model.tindaklanjut.atur.cari(int(id))
    x = cari_tindaklanjut[0]["suratmasuk"]

    if len(cari_tindaklanjut) == 1:
        cari_tindaklanjut = cari_tindaklanjut[0]

        if cari_tindaklanjut['check'] == "0":
            cari_tindaklanjut['check'] = "1"
        del cari_tindaklanjut['id']

    if cari_tindaklanjut['tgl_selesai'] == "" :
        cari_tindaklanjut['tgl_selesai'] = datetime.now().timestamp()


    try:
        hasil = model.tindaklanjut.atur.update(int(id), cari_tindaklanjut)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update pengaduan dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update pengaduan dengan id: {id}.", 400

   
    return redirect("/staff/detailtindaklanjutstaff/" + x)

@tindaklanjut.route("/kirimka/<int:id>", methods=["GET"])
def tindaklanjut_kirimka(id):
    
    cari_tindaklanjut = model.tindaklanjut.atur.cari(int(id))
    x = cari_tindaklanjut[0]["suratmasuk"]

    if len(cari_tindaklanjut) == 1:
        cari_tindaklanjut = cari_tindaklanjut[0]

        if cari_tindaklanjut['check'] == "0":
            cari_tindaklanjut['check'] = "1"
        del cari_tindaklanjut['id']

    if cari_tindaklanjut['tgl_selesai'] == "" :
        cari_tindaklanjut['tgl_selesai'] = datetime.now().timestamp()


    try:
        hasil = model.tindaklanjut.atur.update(int(id), cari_tindaklanjut)
        status = True
        msg = "Success"
    except: 
        msg = f"Update Gagal update pengaduan dengan id: {id}.", 400
    else:
        msg = f"Len Gagal update pengaduan dengan id: {id}.", 400

   
    return redirect("/kepalaupt/detailtindaklanjut/" + x)

@tindaklanjut.route("/tindaklanjut/cari/<int:id>", methods=["GET"])
def tindaklanjut_cari(id):
    # Lakukan pencarian
    try:
        hasil = cari(id)
    except: 
        return f"Gagal mencari tindaklanjut dengan id: {id}.", 400
    
    # Pastikan berhasil
    if hasil is None:
        return f"Gagal mencari tindaklanjut dengan id: {id}.", 400
    # Kembalikan hasilnya dalam format JSON dan kode HTTP 200
    return jsonify(hasil.ke_dictionary()), 200
    


