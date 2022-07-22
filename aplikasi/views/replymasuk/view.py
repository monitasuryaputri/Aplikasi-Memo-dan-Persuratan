from aplikasi import model, app

from flask import Blueprint, json, request, session, escape, redirect, flash
from aplikasi.model.replymasuk import tambah, Replymasuk, REPLYMASUK_KIND

from aplikasi.model.exception import EntityNotFoundException

replymasuk = Blueprint("replymasuk", __name__, url_prefix="/replymasuk")

@replymasuk.route("/tambah", methods=["POST"])
def replymasuk_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        replymasuk_baru = request.get_json()
    elif request.form:
        replymasuk_baru = request.form
        
    else:
        return "Hanya menerima request json dan form", 400  
    
    # Periksa parameter sudah benar
    if replymasuk_baru is None:
        return "Data reply baru tidak ada!", 400        
    if "isi_replymasuk" not in replymasuk_baru.keys():
        return "Salah data! Property isi_reply tidak ada.", 400

    isi_replymasuk = str(escape(replymasuk_baru["isi_replymasuk"]))
    id = str(escape(replymasuk_baru["komenmasuk"]).strip())
    suratmasuk = str(escape(replymasuk_baru["suratmasuk"]).strip())
    
    #  update array id surat komen
    cari_komenmasuk = model.komenmasuk.atur.caribykomenmasuk(int(suratmasuk), int(id))

    if len(cari_komenmasuk) == 1:
        cari_komenmasuk = cari_komenmasuk[0]

        # Tambah reply baru
        try:
            hasil = tambah(session['id'], id, suratmasuk, isi_replymasuk)
        except EntityNotFoundException:
            return f"Gagal menambah komen baru", 400

        cari_suratmasuk = model.suratmasuk.atur.cari(int(suratmasuk))

        if len(cari_suratmasuk) == 1:
            cari_suratmasuk = cari_suratmasuk[0]
            # json dumps
            cari_suratmasuk['reply'] = json.loads(cari_suratmasuk['reply'])
            cari_komenmasuk['reply'] = json.loads(cari_komenmasuk['reply'])
            cari_komenmasuk['reply'] += [str(hasil.id)]
            cari_suratmasuk['reply'] += [str(hasil.id)]
            cari_suratmasuk['reply'] = json.dumps(cari_suratmasuk['reply'])
            cari_komenmasuk['reply'] = json.dumps(cari_komenmasuk['reply'])
            
            del cari_suratmasuk['id']
            del cari_komenmasuk['id']
            
            try:
                hasil = model.suratmasuk.atur.update(int(suratmasuk), cari_suratmasuk)
                hasil = model.komenmasuk.atur.update(int(id), cari_komenmasuk)
                status = True
                msg = "Success"
            except: 
                msg = f"Update Gagal update suratmasuk dengan id: {id}.", 400
            else:
                msg = f"Len Gagal update suratmasuk dengan id: {id}.", 400

    return redirect(request.referrer)