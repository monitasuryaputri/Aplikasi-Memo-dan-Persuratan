from tests.model.konfigurasi.daftar_role import KEPALAUPT_ROLE, STAFF_ROLE, SUPERADMIN_ROLE, ADMIN_ROLE
from tests.model import konfigurasi
from tests import model, app

from tests.model.exception import EntityNotFoundException
from tests.model.exception import EntityIdException
from tests.views.admin.view import admin_list as list_ad
from tests.views.kepalaupt.view import kepalaupt_list as list_ka
from tests.views.staff.view import staff_list as list_st
from tests.views.superadmin.view import superadmin_list as list_sa


from flask import Blueprint, render_template, request, session, escape, redirect, url_for, flash, make_response, json
import tests

from flask_login import login_user, logout_user, login_required, LoginManager

# from oauthlib.oauth2 import WebApplicationClient
from authlib.integrations.flask_client import OAuth

import os
import hashlib
import yaml

rahasia_yaml = open("rahasia.yaml")
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
)
"""Object OAuth Google. """


# Buat blueprint login
login = Blueprint("login", __name__)

#Login

#test Landing
@login.route("/", methods=["GET"])
def test_halaman_landing():
    with app.test_request_context():
        from flask import request, render_template, redirect, url_for

        if request.method == 'POST':
            return redirect(url_for('login.test_halaman_login'))
            
        return render_template("login/login.j2", title="UPT Laboratorium Terpadu")

#test Login
@login.route('/login')
def test_halaman_login():
    with app.test_request_context():
        from flask import session
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        session['state'] = state
        redirect_uri = url_for('login.test_authorize', _external=True)
        return google.authorize_redirect(redirect_uri)
 

#test authentikasi
@login.route('/authorize')
def test_authorize():
    with app.test_request_context():
        from flask import session, render_template
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
            print(session['role'])
            return redirect(url_for("superadmin.dashboardsuperadmin"))
        
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

            print(session['role'])
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


# @login.route('/logout')
# def logout():
#     """
#         User menekan logout dari laman superadmin
#         session dihapus
#         diredirect ke landing page superadmin
#     """
#     for key in list(session.keys()):
#         session.pop(key)
#         # set flash message
#         flash("Berhasil Logout")
#         break
#     return redirect(url_for("login.halaman_landing"))

# # Dipakai oleh Flask-Login untuk memeriksa seorang user
# #
# # Parameter:
# # * user_id : ID dari user yang hendak diperiksa
# #
# # Return: Object user yang diminta
# @login_manager.user_loader
# def load_user(user_id):
#     # Kita tidak ada database, ambil dari session
#     if "user_google" not in session:
#         return None

#     # Ambil object user dari session
#     user_json = json.loads(session["user_google"])

#     # Buat dan kembalikan object user 
#     return User(unique_id=user_json["id"], 
#                 nama_lengkap=user_json["nama_lengkap"], 
#                 email=user_json["email"], 
#                 url_gambar_profil=user_json["url_gambar_profil"])