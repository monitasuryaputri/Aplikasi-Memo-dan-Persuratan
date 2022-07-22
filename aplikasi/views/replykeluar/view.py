from aplikasi import model, app

from flask import Blueprint, json, request, session, escape, redirect, flash
from aplikasi.model.replykeluar import tambah, Replykeluar, REPLYKELUAR_KIND

from aplikasi.model.exception import EntityNotFoundException

replykeluar = Blueprint("replykeluar", __name__, url_prefix="/replykeluar")


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
