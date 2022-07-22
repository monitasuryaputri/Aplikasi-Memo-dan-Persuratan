from aplikasi import model, app

from flask import Blueprint, json, request, session, escape, redirect, flash
from aplikasi.model.followup import tambah, Followup, FOLLOWUP_KIND

from aplikasi.model.exception import EntityNotFoundException

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
    # flash('followup berhasil ditambahkan')         
    # direct ke halaman isi tindaklanjut
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
    


