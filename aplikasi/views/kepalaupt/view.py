from aplikasi import model, app

from aplikasi.model.konfigurasi.daftar_role import KEPALAUPT_ROLE
from flask import Blueprint, json, request, session, escape, redirect, flash, render_template, url_for

from aplikasi.model.kepalaupt import tambah, hapus, ubah, Kepalaupt

from aplikasi.model.exception import EntityNotFoundException

from aplikasi.views.staff.view import staff_list as list_st

kepalaupt = Blueprint("kepalaupt", __name__, url_prefix="/kepalaupt")

#kepalaupt
@kepalaupt.route("/tambah", methods=["POST"])
def kepalaupt_tambah():
    #konversi request ke json
    if request.is_json:
        #ambil parameter
        kepalaupt_baru = request.get_json()
    elif request.form:
        kepalaupt_baru = request.form
    else:
        return "Hanya menerima request json dan form", 400

    #periksa parameter sudah benar
    if kepalaupt_baru is None:
        return "Data kepalaupt baru tidak ada!", 400
    if "nama" in kepalaupt_baru is None:
        return "Salah data! Properti nama tidak ada", 400
    if "email" in kepalaupt_baru is None:
        return "Salah data! Properti email tidak ada", 400
    if "no_hp" in kepalaupt_baru is None:
        return "Salah data! Properti no_hp tidak ada", 400
    # if "jabatan" in kepalaupt_baru is None:
    #     return "Salah data! Properti jabatan tidak ada", 400
    
    nama = escape(kepalaupt_baru["nama"]).strip()
    email = escape(kepalaupt_baru["email"]).strip()
    no_hp = escape(kepalaupt_baru["no_hp"]).strip()
    jabatan = escape(kepalaupt_baru["jabatan"]).strip()


    #tambah kepalaupt baru
    try:
        hasil = tambah(nama,email,no_hp, jabatan)
    except EntityNotFoundException:
        return f"Gagal menambah kepalaupt baru", 400
    
    #pastikan berhasil
    if (hasil is None):
        #set flash message
        flash('Gagal menambah kepalaupt baru')
        #direct ke halaman tambah kepalaupt
        return redirect(url_for('superadmin.superadmin_kepalaupt_tambah'))

    #set flash message
    flash('Kepala Uupt berhasil ditambahkan')
    #direct ke halaman daftar kepalaupt
    return redirect(url_for('superadmin.dashboardsuperadmin'))

@kepalaupt.route("/listka", methods=["GET"])
def kepalaupt_list():

    # Minta data semua kepalaupt
    hasil = model.kepalaupt.atur.daftar()

    # Pastikan berhasil
    if hasil is None:
        return "Gagal meminta daftar kepalaupt.", 400

    # Ubah class ke dictionary
    daftar_kepalaupt = []
    for satu_hasil in hasil:
        daftar_kepalaupt.append(satu_hasil.ke_dictionary())

    # Buat wrapper dictionaty untuk dikembalikan
    hasil =  daftar_kepalaupt 
    
    return hasil

@kepalaupt.route("/hapus/<int:id>")
def kepalaupt_hapus(id):

    # panggil method hapus
    try:
        hapus(id)
    except: 
        return f"Gagal menghapus kepala dengan id: {id}.", 400

    # set flash message
    flash('Kepalaupt berhasil dihapus')
    #direct ke halaman daftar Kepalaupt
    return redirect('/superadmin/dashboardsuperadmin')

@kepalaupt.route("/ubah/<int:id>", methods=["POST"])
def kepalaupt_ubah(id):
    # konversi request ke json
    if request.is_json:
        # Ambil parameter
        kepalaupt_baru = request.get_json()
    if request.form:
        kepalaupt_baru = request.form
    else:
        return "Hanya menerima request json dan form",400

    
    # Periksa parameter sudah benar
    if kepalaupt_baru is None:
        return "Data admin baru tidak ada!", 400        
    if "nama" not in kepalaupt_baru.keys():
        return "Salah data! Property nama tidak ada.", 400
    if "email" not in kepalaupt_baru.keys():
        return "Salah data! Property email tidak ada.", 400
    if "no_hp" not in kepalaupt_baru.keys():
        return "Salah data! Property no_hp tidak ada.", 400
    
    cari_kepalaupt = model.kepalaupt.atur.cari(id)

    if len(cari_kepalaupt) == 1:
        cari_kepalaupt = cari_kepalaupt[0]
        
        cari_kepalaupt["nama"] = kepalaupt_baru["nama"]
        cari_kepalaupt["no_hp"] = kepalaupt_baru["no_hp"]
        cari_kepalaupt["email"] = kepalaupt_baru["email"]
        cari_kepalaupt["jabatan"] = cari_kepalaupt["jabatan"]
        cari_kepalaupt["picture"] = cari_kepalaupt["picture"]

        del cari_kepalaupt["id"] 
                            
    try:
        hasil = ubah(id, cari_kepalaupt) 
    except EntityNotFoundException:
        return f"Tidak ada kepalaupt dengan id: {id}.", 400
    except: 
        return f"Gagal mengubah kepalaupt dengan id: {id}.", 400
    
   # Pastikan berhasil
    if (hasil is None):

        # set flash message
        flash('Gagal mengubah data kepalaupt')
        # direct ke laman ubah kepalaupt
        return redirect('/superadmin/kepalaupt/ubah/'+id)

    # set flash message
    flash('Kepala UPT berhasil diubah')         
    #direct ke halaman dashboard superadmin
    return redirect(url_for('superadmin.dashboardsuperadmin'))

@kepalaupt.route("/detailsuratmasukka/update/<int:id>", methods=["POST"])
def detailsuratmasukka_update(id):

    status = False
    msg = f"Gagal update pengaduan dengan id: {id}.", 400
    update_suratmasuk = model.suratmasuk.atur.cari(id)

    data = {
        "id": request.form.get("id"),
        "penerima": json.loads(request.form.get("penerima"))
    }

    if len(update_suratmasuk) == 1:
        cari_suratmasuk = update_suratmasuk[0]

        cari_suratmasuk['disposisi'] = (cari_suratmasuk['disposisi'])
        cari_suratmasuk['disposisi'] += [x.lower() for x in data['penerima']]

        del cari_suratmasuk['id']

        try:
            model.suratmasuk.atur.update(id, cari_suratmasuk)
            status = True
            msg = "Success"
        except: 
            msg = f"Update Gagal update surat masuk dengan id: {id}.", 400

    return {
        'status' : status,
        'msg' : msg
    }

@kepalaupt.route("/detaildrafsuratka/tugaskan/<int:id>", methods=["POST"])
def detaildrafsuratka_tugaskan(id):

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    status = False
    msg = f"Gagal update pengaduan dengan id: {id}.", 400
    update_suratkeluar = model.suratkeluar.atur.cari(id)

    data = {
        "id": request.form.get("id"),
        "penerima": json.loads(request.form.get("penerima"))
    }

    if len(update_suratkeluar) == 1:
        cari_suratkeluar = update_suratkeluar[0]

        cari_suratkeluar['disposisi'] = (cari_suratkeluar['disposisi'])
        cari_suratkeluar['disposisi'] += [x.lower() for x in data['penerima']]

        del cari_suratkeluar['id']

        try:
            model.suratkeluar.atur.update(id, cari_suratkeluar)
            status = True
            msg = "Success"
        except: 
            msg = f"Update Gagal update surat masuk dengan id: {id}.", 400

    return {
        'status' : status,
        'msg' : msg
    }

#halaman detail draf update
@kepalaupt.route("/detaildrafsuratka/update/<int:id>", methods=["POST"])
def detaildrafsuratka_update(id):

    status = False
    msg = f"Gagal update pengaduan dengan id: {id}.", 400
    update_suratkeluar = model.suratkeluar.atur.cari(id)

    data = {
        "id": request.form.get("id"),
        "lampiran": request.files.get("lampiran")
    }

    if len(update_suratkeluar) == 1:
        cari_suratkeluar = update_suratkeluar[0]

        cari_suratkeluar['dokumen'] = (cari_suratkeluar['dokumen'])
        cari_suratkeluar['dokumen'] = (data['lampiran'])

        del cari_suratkeluar['id']

        try:
            model.suratkeluar.atur.update(id, cari_suratkeluar)
            status = True
            msg = "Success"
        except: 
            msg = f"Update Gagal update surat masuk dengan id: {id}.", 400

    return {
        'status' : status,
        'msg' : msg
    }

@kepalaupt.route("/isi-tindaklanjutka/simpan/<int:id>", methods=["POST"])
def simpantindaklanjutkepala(id):

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)

    if len(cari_tindaklanjut) == 1:
        cari_tindaklanjut = cari_tindaklanjut[0]

        cari_tindaklanjut['tenggatwaktu'] = request.form.get("tenggatwaktu")

        del cari_tindaklanjut['id']

        model.tindaklanjut.atur.update(id, cari_tindaklanjut)
        
    return redirect('/kepalaupt/isi-tindaklanjutka/'+ str(id))

#halaman dashboard
@kepalaupt.route("/dashboardka", methods=["GET"])
def dashboardka():

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')
    
    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    # Muat template
    return render_template("kepalaupt/dashboardka.j2", 
                            title="Dashboard",
                            daftar_suratmasuk=suratmasuk,
                            daftar_suratkeluar=suratkeluar, 
                            sesi=sesi)

#halaman surat masuk
@kepalaupt.route("/suratmasukka", methods=["GET"])
def suratmasukka():

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()
    
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    # Muat template
    return render_template("kepalaupt/suratmasukka.j2", 
                            title="Surat Masuk",
                            breadcrumb="Home", 
                            breadcrumb_active="Surat Masuk",
                            daftar_suratmasuk=suratmasuk,
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

#halaman detail surat masuk
@kepalaupt.route("/detailsuratmasukka/<int:id>", methods=["GET"])
def detailsuratmasukka(id):

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])
    
    pembaca =  model.suratmasuk.atur.cari(id)
    
    ka = kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = list_st()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if session['id'] in list_of_ka:
        cari = model.kepalaupt.atur.cari(session['id'])
        cari = cari[0]['jabatan']
        
        pembaca[0]['dibaca'] = pembaca[0]['dibaca'] 
        if len(pembaca[0]['dibaca']) >= 1:
            if cari not in pembaca[0]['dibaca']:
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
            else:
                pembaca[0]['dibaca'].remove(cari)
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
        else:
            pembaca[0]['dibaca'] += [cari]
            del pembaca[0]['id']
            model.suratmasuk.atur.update(id, pembaca[0])   

    elif session['id'] in list_of_st:
        cari = model.staff.atur.cari(session['id'])
        cari = cari[0]['jabatan']

        pembaca[0]['dibaca'] = pembaca[0]['dibaca']
        if len(pembaca[0]['dibaca']) >= 1:
            if cari not in pembaca[0]['dibaca']:
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
            else:
                pembaca[0]['dibaca'].remove(cari)
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratmasuk.atur.update(id, pembaca[0])
        else:
            pembaca[0]['dibaca'] += [cari]
            del pembaca[0]['id']
            model.suratmasuk.atur.update(id, pembaca[0])

    # Lakukan pencarian surat masuk berdasar id
    try:
        cari_suratmasuk = model.suratmasuk.atur.detail(id)
        jabatan = model.jabatan.atur.disposisi()
    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400

    if cari_suratmasuk is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratmasuk[0]["data_komentar"] = model.komenmasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    cari_suratmasuk[0]["data_reply"] = model.replymasuk.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])

    # Muat template
    return render_template("kepalaupt/detailsuratmasukka.j2", 
                            title="Detail Surat Masuk",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Surat Masuk", 
                            breadcrumb_active="Detail Surat Masuk",
                            data_suratmasuk=cari_suratmasuk, 
                            daftar_jabatan=jabatan,                             
                            daftar_suratmasuk=suratmasuk,
                            daftar_suratkeluar=suratkeluar, 
                            sesi=sesi)

#halaman draf surat
@kepalaupt.route("/drafsuratka", methods=["GET"])
def drafsuratka():

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratkeluar = model.suratkeluar.atur.daftar()
    suratmasuk = model.suratmasuk.atur.daftar()
    
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    # Muat template
    return render_template("kepalaupt/drafsuratka.j2", 
                            title="Draf Surat",                             
                            breadcrumb="Home", 
                            breadcrumb_active="Draf Surat",
                            daftar_suratkeluar=suratkeluar,
                            daftar_suratmasuk=suratmasuk,
                            sesi=sesi)

#halaman detail draf surat
@kepalaupt.route("/detaildrafsuratka/<int:id>", methods=["GET"])
def detaildrafsuratka(id):

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    pembaca =  model.suratkeluar.atur.cari(id)

    ka = kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = list_st()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if session['id'] in list_of_ka:
        cari = model.kepalaupt.atur.cari(session['id'])
        cari = cari[0]['jabatan']
        
        pembaca[0]['dibaca'] = pembaca[0]['dibaca'] 
        if len(pembaca[0]['dibaca']) >= 1:
            if cari not in pembaca[0]['dibaca']:
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratkeluar.atur.update(id, pembaca[0])
            else:
                pembaca[0]['dibaca'].remove(cari)
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratkeluar.atur.update(id, pembaca[0])
        else:
            pembaca[0]['dibaca'] += [cari]
            del pembaca[0]['id']
            model.suratkeluar.atur.update(id, pembaca[0])   

    elif session['id'] in list_of_st:
        cari = model.staff.atur.cari(session['id'])
        cari = cari[0]['jabatan']

        pembaca[0]['dibaca'] = pembaca[0]['dibaca']
        if len(pembaca[0]['dibaca']) >= 1:
            if cari not in pembaca[0]['dibaca']:
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratkeluar.atur.update(id, pembaca[0])
            else:
                pembaca[0]['dibaca'].remove(cari)
                pembaca[0]['dibaca'] += [cari]
                del pembaca[0]['id']
                model.suratkeluar.atur.update(id, pembaca[0])
        else:
            pembaca[0]['dibaca'] += [cari]
            del pembaca[0]['id']
            model.suratkeluar.atur.update(id, pembaca[0])

    # Lakukan pencarian draf surat berdasar id
    try:
        cari_suratkeluar = model.suratkeluar.atur.detail(id)
        jabatan = model.jabatan.atur.disposisi()

    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratkeluar is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratkeluar[0]["data_komentar"] = model.komenkeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])
    cari_suratkeluar[0]["data_reply"] = model.replykeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])
    
    # Muat template
    return render_template("kepalaupt/detaildrafsuratka.j2", 
                            title="Detail Draf Surat",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Draf Surat", 
                            breadcrumb_active="Detail Draf Surat", 
                            data_suratkeluar=cari_suratkeluar, 
                            daftar_jabatan=jabatan,                            
                            daftar_suratmasuk=suratmasuk, 
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

#halaman surat keluar
@kepalaupt.route("/suratkeluarka", methods=["GET"])
def suratkeluarka():

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratkeluar = model.suratkeluar.atur.daftar()
    suratmasuk = model.suratmasuk.atur.daftar()
    
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    # Muat template
    return render_template("kepalaupt/suratkeluarka.j2", 
                            title="Surat Keluar",                             
                            breadcrumb="Home", 
                            breadcrumb_active="Surat Keluar",
                            daftar_suratkeluar=suratkeluar, 
                            daftar_suratmasuk=suratmasuk, 
                            sesi=sesi)

#halaman detail surat keluar
@kepalaupt.route("/detailsuratkeluar/<int:id>", methods=["GET"])
def detailsuratkeluarka(id):

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    # Lakukan pencarian draf surat berdasar id
    try:
        cari_suratkeluar = model.suratkeluar.atur.detail(id)
    except: 
        return f"Except Gagal mencari surat dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratkeluar is None:
        return f"Gagal mencari surat dengan id: {id}.", 400

    cari_suratkeluar[0]["data_komentar"] = model.komenkeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])
    cari_suratkeluar[0]["data_reply"] = model.replykeluar.atur.caribysuratkeluar(cari_suratkeluar[0]['id'])

    # Muat template
    return render_template("kepalaupt/detailsuratkeluar.j2", 
                            title="Detail Surat Keluar",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Surat Keluar", 
                            breadcrumb_active="Detail Surat Keluar", 
                            data_suratkeluar=cari_suratkeluar,
                            daftar_suratmasuk=suratmasuk,
                            daftar_suratkeluar=suratkeluar, 
                            sesi=sesi)

#halaman tindak lanjut surat
@kepalaupt.route("/tindaklanjut", methods=["GET"])
def tindaklanjut():

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    # Muat template
    return render_template("kepalaupt/tindaklanjut.j2", 
                            title="Tindak Lanjut",                             
                            breadcrumb="Home", 
                            breadcrumb_active="Tindak Lanjut",
                            daftar_suratmasuk=suratmasuk,
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

#halaman detail tindak lanjut surat
@kepalaupt.route("/detailtindaklanjut/<int:id>", methods=["GET"])
def detailtindaklanjut(id):

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()
    
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])
    try:
        cari_suratmasuk = model.suratmasuk.atur.cari(id)
    except: 
        return f"try Gagal mencari pengaduan dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratmasuk is None:
        return f"None Gagal mencari pengaduan dengan id: {id}.", 400

    cari_suratmasuk[0]["data_tindaklanjut"] = model.tindaklanjut.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    cari_suratmasuk[0]["data_disposisi"] = model.suratmasuk.atur.penanggung(id)
    cari_suratmasuk[0]["data_disposisi"] = cari_suratmasuk[0]["data_disposisi"][0]
    
    # Muat template
    return render_template("kepalaupt/detailtindaklanjut.j2", 
                            title="Detail Tindak Lanjut",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Tindak Lanjut", 
                            breadcrumb_active="Detail Tindak Lanjut",  
                            data_suratmasuk=cari_suratmasuk,
                            daftar_suratmasuk=suratmasuk, 
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

#halaman detail tindak lanjut surat
@kepalaupt.route("/detailtindaklanjutselesai/<int:id>", methods=["GET"])
def detailtindaklanjutselesai(id):

    if session['role'] != KEPALAUPT_ROLE:
        return redirect ('/')

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])
    try:
        cari_suratmasuk = model.suratmasuk.atur.cari(id)
    except: 
        return f"try Gagal mencari pengaduan dengan id: {id}.", 400
    
    # Pastikan berhasil
    if cari_suratmasuk is None:
        return f"None Gagal mencari pengaduan dengan id: {id}.", 400

    cari_suratmasuk[0]["data_tindaklanjut"] = model.tindaklanjut.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])

    # Muat template
    return render_template("kepalaupt/detailtindaklanjutselesai.j2", 
                            title="Detail Tindak Lanjut Selesai",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Tindak Lanjut", 
                            breadcrumb_active="Detail Tindak Lanjut Selesai", 
                            data_suratmasuk=cari_suratmasuk,
                            daftar_suratmasuk=suratmasuk, 
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

@kepalaupt.route("/isi-tindaklanjutka/<int:id>", methods=["GET"])
def isitindaklanjutka(id):

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
    x = cari_tindaklanjut[0]["penugas"]

    ka = kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = list_st()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if x in list_of_ka:
        cari = model.kepalaupt.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 
        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]
        x = cari

    elif x in list_of_st:
        cari = model.staff.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

        x = cari

    cari_tindaklanjut[0]["penugas"] = x['nama_jabatan']
    
    # Pastikan berhasil
    if cari_tindaklanjut is None:
        return f"Gagal mencari surat dengan id: {id}.", 400
    cari_tindaklanjut[0]["data_followup"] = model.followup.atur.caribytindaklanjut(cari_tindaklanjut[0]['id'])
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama
    cari_tindaklanjut[0]["penanggungjawab"] = jabatan_nama[cari_tindaklanjut[0]["penanggungjawab"]]
    cari_tindaklanjut[0]["data_pn"] = jabatan_nama[session['jabatan']]

    # Muat template
    return render_template("kepalaupt/isi-tindaklanjutka.j2", 
                            title="Tugas Tindak Lanjut",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Tindak Lanjut", 
                            breadcrumb_active="Detail Tindak Lanjut", 
                            breadcrumb_activated="Tugas Tindak Lanjut",
                            data_tindaklanjut=cari_tindaklanjut,
                            daftar_suratmasuk=suratmasuk, 
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

@kepalaupt.route("/isi-tindaklanjutka/edit/<int:id>", methods=["GET"])
def edittindaklanjutkepala(id):

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)

    # Muat template
    return render_template("kepalaupt/edittindaklanjutka.j2", 
                            title="Tugas Tindak Lanjut",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Tindak Lanjut", 
                            breadcrumb_active="Detail Tindak Lanjut", 
                            breadcrumb_activated="Tugas Tindak Lanjut",  
                            data_tindaklanjut=cari_tindaklanjut,                             
                            daftar_suratmasuk=suratmasuk, 
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

@kepalaupt.route("/followup/<int:id>", methods=["GET"])
def followup(id):

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    try:
        cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
        x = cari_tindaklanjut[0]["suratmasuk"]
        cari_suratmasuk = model.suratmasuk.atur.cari(int(x))
    except: 
        return f"try Gagal mencari pengaduan dengan id: {id}.", 400
    
    cari_suratmasuk[0]["data_tindaklanjut"] = model.tindaklanjut.atur.caribysuratmasuk(cari_suratmasuk[0]['id'])
    
    # Pastikan berhasil
    if cari_tindaklanjut is None:
        return f"None Gagal mencari pengaduan dengan id: {id}.", 400
    
    cari_tindaklanjut[0]["data_followup"] = model.followup.atur.caribytindaklanjut(cari_tindaklanjut[0]['id'])

    # Muat template
    return render_template("kepalaupt/followup.j2", 
                            title="Proses Tugas", 
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Surat Masuk", 
                            breadcrumb_active="Detail Tindak Lanjut", 
                            breadcrumb_activated="Tugas Tindak Lanjut", 
                            breadcrumb_aktif="Proses Tugas", 
                            data_tindaklanjut=cari_tindaklanjut, 
                            data_suratmasuk=cari_suratmasuk, 
                            daftar_suratmasuk=suratmasuk, 
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)

@kepalaupt.route("/historika/<int:id>", methods=["GET"])
def historitindaklanjutka(id):

    suratmasuk = model.suratmasuk.atur.daftar()
    suratkeluar = model.suratkeluar.atur.daftar()

    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.id
    sesi = str(jabatan_nama[session['jabatan']])

    cari_tindaklanjut = model.tindaklanjut.atur.cari(id)
    x = cari_tindaklanjut[0]["penugas"]

    
    ka = kepalaupt_list()
    list_of_ka = [id for elem in ka
                    for id in elem.values()]
    st = list_st()
    list_of_st = [id for elem in st
                    for id in elem.values()]

    if x in list_of_ka :
        cari = model.kepalaupt.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 
        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]
        x = cari

    elif x in list_of_st :
        cari = model.staff.atur.cari(x)
        if len(cari) == 1 :
            cari = cari[0] 

        jabatan = model.jabatan.atur.daftar()
        jabatan_nama = {}
        for data in jabatan:
            jabatan_nama[str(data.id)] = data.nama

        cari['nama_jabatan'] = jabatan_nama[cari["jabatan"]]

        x = cari

    cari_tindaklanjut[0]["penugas"] = x['nama_jabatan']
    
    # Pastikan berhasil
    if cari_tindaklanjut is None:
        return f"Gagal mencari surat dengan id: {id}.", 400
    cari_tindaklanjut[0]["data_followup"] = model.followup.atur.caribytindaklanjut(cari_tindaklanjut[0]['id'])
    jabatan = model.jabatan.atur.daftar()
    jabatan_nama = {}
    for data in jabatan:
        jabatan_nama[str(data.id)] = data.nama
    cari_tindaklanjut[0]["penanggungjawab"] = jabatan_nama[cari_tindaklanjut[0]["penanggungjawab"]]
    
    # Muat template
    return render_template("kepalaupt/status-followup.j2", 
                            title="Histori Tindak Lanjut",
                            breadcrumb="Home", 
                            breadcrumb_nonactive="Tindak Lanjut", 
                            breadcrumb_active="Detail Tindak Lanjut", 
                            breadcrumb_activated="Histori Tindak Lanjut", 
                            data_tindaklanjut=cari_tindaklanjut,
                            daftar_suratmasuk=suratmasuk, 
                            daftar_suratkeluar=suratkeluar,
                            sesi=sesi)





















