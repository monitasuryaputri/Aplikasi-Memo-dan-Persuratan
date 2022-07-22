from aplikasi.model import manajemen
from aplikasi.model.konfigurasi.daftar_role import KEPALAUPT_ROLE, STAFF_ROLE, SUPERADMIN_ROLE, ADMIN_ROLE, MANAJEMEN_ROLE
from aplikasi import model, app

from aplikasi.model.exception import EntityNotFoundException
from aplikasi.views.admin.view import admin_list as list_ad
from aplikasi.views.kepalaupt.view import kepalaupt_list as list_ka
from aplikasi.views.staff.view import staff_list as list_st
from aplikasi.views.superadmin.view import superadmin_list as list_sa
# from aplikasi.views.manajemen.view import manajemen_list as list_ma

from flask import Blueprint, render_template, request, session, escape, redirect, url_for, flash

from flask_login import login_user, logout_user, login_required, LoginManager

from authlib.integrations.flask_client import OAuth

import os
import hashlib
import yaml

rahasia_yaml = open("aplikasi/model/konfigurasi/rahasia.yaml")
""" import file rahasia.yaml """
rahasia = yaml.load(rahasia_yaml, Loader=yaml.FullLoader)
"""parsed_yaml_file"""
app.secret_key = rahasia["SECRET_KEY"]
"""Secret key yang dipergunakan oleh FLASK untuk enkripsi.
    Nilainya diambil dari rahasia.yaml """

oauth           =OAuth(app)
"""Object OAuth untuk login ke Google."""

google                  =oauth.register(
    name                =rahasia["GOOGLE_OAUTH_NAME"],
    client_id           =rahasia["CLIENT_ID"],
    client_secret       =rahasia["CLIENT_SECRET"],
    access_token_url    =rahasia["ACCESS_TOKEN_URL"],
    access_token_params =rahasia["ACCESS_TOKEN_PARAMS"],
    authorize_url       =rahasia["AUTHORIZE_URL"],
    authorize_params    =rahasia["AUTHORIZE_PARAMS"],
    api_base_url        =rahasia["API_BASE_URL"],
    client_kwargs       =rahasia["CLIENT_KWARGS"],
    jwks_uri            =rahasia["JWKS_URI"]
)

# Buat blueprint login
login = Blueprint("login", __name__)

#Login

#halaman Landing
@login.route("/", methods=["GET"])
def halaman_landing():
    
    if request.method == 'POST':
        return redirect(url_for('login.halaman_login'))
        
    return render_template("login/login.j2", title="UPT Laboratorium Terpadu")

#halaman Login
@login.route('/login')
def halaman_login():
    """ 
        User mengklik link login pada halaman dashboard admin.
        Buat state token, simpan pada state session
        token ini akan divalidasi nanti
    """
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    session['state'] = state
    redirect_uri = url_for('login.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)
 

#halaman authentikasi
@login.route('/authorize')
def authorize():
    """Callback function oleh proses login Google.

        Callback function yang dipanggil oleh service google jika login si user berhasil.
        cek session state
        memastikan request berasal dari user bukan forgery
    """
    if "state" not in session:
        flash("State tidak valid")
        return render_template("login/login.j2")
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    
    email = user_info['email']

    sa = list_sa()
    list_of_sa = [email for elem in sa
                    for email in elem.values()]
    ad = list_ad()

    list_of_ad = [email for elem in ad
                    for email in elem.values()]
    ka = list_ka()
    list_of_ka = [email for elem in ka
                    for email in elem.values()]
    st = list_st()
    list_of_st = [email for elem in st
                    for email in elem.values()]
    # ma = list_ma()
    # list_of_ma = [email for elem in ma
    #                 for email in elem.values()]
    
    # app.logger.info("=====")
    # app.logger.info(list_of_ma)
    
    if email in list_of_sa:
        # cek apakah email superadmin telah terdaftar
        try:
            hasil = model.superadmin.atur.cari_email(email)
        except:
            return f'Gagal mencari email {email}',400
        hasil_json = []
        # iterate hasil untuk dirubah ke dictionary
        for satu_hasil in hasil:
            satu_hasil_json = satu_hasil.ke_dictionary()
            hasil_json.append(satu_hasil_json)

        if len(hasil_json) == 0:
            flash("Akun Belum Terdaftar")
            return render_template("login/login.j2")

        # email terdaftar, buat session untuk user tersebut
        session['email']    = user_info['email']
        session['name']     = user_info['name']
        session['picture']  = user_info['picture']
        session['role']     = SUPERADMIN_ROLE
        # print(session['role'])
        return redirect(url_for("superadmin.dashboardsuperadmin"))

    # elif email in list_of_ma:
    #     # cek apakah email manajemen telah terdaftar
    #     try:
    #         hasil = model.manajemen.atur.cari_email(email)
    #     except:
    #         return f'Gagal mencari email {email}',400
    #     hasil_json = []
    #     # iterate hasil untuk dirubah ke dictionary
    #     for satu_hasil in hasil:
    #         satu_hasil_json = satu_hasil.ke_dictionary()
    #         hasil_json.append(satu_hasil_json)

    #     if len(hasil_json) == 0:
    #         flash("Akun Belum Terdaftar")
    #         return render_template("login/login.j2")

    #     # email terdaftar, buat session untuk user tersebut
    #     session['email']    = user_info['email']
    #     session['name']     = user_info['name']
    #     session['picture']  = user_info['picture']
    #     session['role']     = MANAJEMEN_ROLE

    #     return redirect(url_for("manajemen.berandamanajemen"))
    
    elif email in list_of_ad:
        try:
            hasil = model.admin.atur.cari_email(email)
        except:
            return f'Gagal mencari email {email}',400
        hasil_json = []
        # iterate hasil untuk dirubah ke dictionary
        for satu_hasil in hasil:
            satu_hasil_json = satu_hasil
            hasil_json.append(satu_hasil_json)

        if len(hasil_json) == 0:
            flash("Akun Belum Terdaftar")

            return render_template("login/login.j2")

        # email terdaftar, buat session untuk user tersebut
        session['email']    = user_info['email']
        session['name']     = user_info['name']
        session['picture']  = user_info['picture']
        session['role']     = ADMIN_ROLE
        session['jabatan']  = hasil[0]['jabatan']
        session['id']       = hasil[0]['id']

        # TODO

        if len(hasil) == 1:
        
            hasil = hasil[0]

            hasil['picture'] = user_info['picture']
            id = hasil['id']
            del hasil['id']

            try:
                hasil = model.admin.atur.ubah(id, hasil)

            except EntityNotFoundException:
                return f"Gagal mengubah staff", 400

        return redirect(url_for("admin.dashboardadmin"))

    elif email in list_of_ka:
        try:
            hasil = model.kepalaupt.atur.cari_email(email)
        except:
            return f'Gagal mencari email {email}',400
        hasil_json = []
        # iterate hasil untuk dirubah ke dictionary
        for satu_hasil in hasil:
            satu_hasil_json = satu_hasil
            hasil_json.append(satu_hasil_json)

        if len(hasil_json) == 0:
            flash("Akun Belum Terdaftar")

            return render_template("login/login.j2")

        # email terdaftar, buat session untuk user tersebut
        session['email']    = user_info['email']
        session['name']     = user_info['name']
        session['picture']  = user_info['picture']
        session['role']     = KEPALAUPT_ROLE
        session['jabatan']  = hasil[0]['jabatan']
        session['id']       = hasil[0]['id']

        # TODO

        if len(hasil) == 1:
        
            hasil = hasil[0]

            hasil['picture'] = user_info['picture']
            id = hasil['id']
            del hasil['id']

            try:
                hasil = model.kepalaupt.atur.ubah(id, hasil)

            except EntityNotFoundException:
                return f"Gagal mengubah staff", 400
            
        print(session['role'])
        return redirect(url_for("kepalaupt.dashboardka"))

    elif email in list_of_st:
        try:
            hasil = model.staff.atur.cari_email(email)
        except:
            return f'Gagal mencari email {email}',400
        hasil_json = []
        # iterate hasil untuk dirubah ke dictionary
        for satu_hasil in hasil:
            satu_hasil_json = satu_hasil
            hasil_json.append(satu_hasil_json)

        if len(hasil_json) == 0:
            flash("Akun Belum Terdaftar")

            return render_template("login/login.j2")

        # email terdaftar, buat session untuk user tersebut
        session['email']    = user_info['email']
        session['name']     = user_info['name']
        session['picture']  = user_info['picture']
        session['role']     = STAFF_ROLE
        session['jabatan']  = hasil[0]['jabatan']
        session['id']       = hasil[0]['id']

        # TODO

        if len(hasil) == 1:
        
            hasil = hasil[0]

            hasil['picture'] = user_info['picture']
            id = hasil['id']
            del hasil['id']
            try:
                hasil = model.staff.atur.ubah(id, hasil)

            except EntityNotFoundException:
                return f"Gagal mengubah staff", 400

        return redirect(url_for("staff.dashboardstaff"))

    else:
        flash("Akun Belum Terdaftar")
        return render_template("login/login.j2")

@login.route('/logout')
def logout():
    """
        User menekan logout dari laman superadmin
        session dihapus
        diredirect ke landing page superadmin
    """
    for key in list(session.keys()):
        session.pop(key)
        # set flash message
        flash("Berhasil Logout")
        break
    return redirect(url_for("login.halaman_landing"))