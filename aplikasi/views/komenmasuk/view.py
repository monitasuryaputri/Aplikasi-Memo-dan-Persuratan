from aplikasi import model, app

from flask import Blueprint, json, request, session, escape, redirect, flash
from aplikasi.model.komenmasuk import tambah

from aplikasi.model.exception import EntityNotFoundException

komenmasuk = Blueprint("komenmasuk", __name__, url_prefix="/komenmasuk")

#komen
@komenmasuk.route("/tambah", methods=["POST"])
def komenmasuk_tambah():
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        komenmasuk_baru = request.get_json()
    elif request.form:
        komenmasuk_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400   

    # Periksa parameter sudah benar
    if komenmasuk_baru is None:
        return "Data komentar baru tidak ada!", 400        
    if "isi_komenmasuk" not in komenmasuk_baru.keys():
        return "Salah data! Property isi_komen tidak ada.", 400 
    
    
    isi_komenmasuk = str(escape(komenmasuk_baru["isi_komenmasuk"]))
    id = str(escape(komenmasuk_baru["id_suratmasuk"]).strip())

    #  update array id surat komen

    cari_suratmasuk = model.suratmasuk.atur.cari(int(id))

    if len(cari_suratmasuk) == 1:
        cari_suratmasuk = cari_suratmasuk[0]

        # Tambah komen baru
        try:
            hasil = tambah(session['id'], id, cari_suratmasuk['nomor_surat'], isi_komenmasuk)
        except EntityNotFoundException:
            return f"Gagal menambah komen baru", 400

        # json dumps
        cari_suratmasuk['komentar'] = json.loads(cari_suratmasuk['komentar'])
        cari_suratmasuk['komentar'] += [str(hasil.id)]
        cari_suratmasuk['komentar'] = json.dumps(cari_suratmasuk['komentar'])

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
