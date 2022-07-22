from aplikasi import model, app

from flask import Blueprint, request, session, escape, redirect, flash

from aplikasi.model.komenkeluar import tambah

from aplikasi.model.exception import EntityNotFoundException


komenkeluar = Blueprint("komenkeluar", __name__, url_prefix="/komenkeluar")


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
    