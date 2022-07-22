from flask import Flask
from flask_login import LoginManager
import requests
import os
import logging

# Buat object Flask
app = Flask(__name__, template_folder="templates", instance_relative_config=True)

CLOUD_STORAGE_BUCKET="surat-labter.appspot.com"

# Muat konfigurasi global
app.config.from_object('config')

# Muat konfigurasi instance
app.config.from_pyfile('config.py')

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')

# Set server untuk development
app.config["ENV"] = "development"
# Hidupkan debugger di server
app.config["DEBUG"] = True

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# Periksa apakah ada didefisinikan mode dimana kode dijalankan
if "MODE_LINGKUNGAN" in app.config:
    if app.config["MODE_LINGKUNGAN"] == "DEV":
        # Kode dijalankan dalam lingkungan pengembangan
        app.config["ENV"] = "development"
        app.config["DEBUG"] = True
    elif app.config["MODE_LINGKUNGAN"] == "PROD":
        # Kode dijalankan dalam lingkungan produksi
        app.config["ENV"] = "production"
        app.config["DEBUG"] = False
    elif app.config["MODE_LINGKUNGAN"] == "TEST":
        # Kode dijalankan dalam lingkungan pengembangan
        app.config["ENV"] = "development"
        app.config["DEBUG"] = True

# Jadikan template bisa auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Buat session
app.secret_key = app.config["SESSION_SECRET_KEY"]

#
# Daftarkan semua blueprint
#

# Blueprint untuk login
from .views import login
app.register_blueprint(login)

# Blueprint untuk admin
from .views import admin, admin_list
app.register_blueprint(admin)

# Blueprint untuk kepalaupt
from .views import kepalaupt
app.register_blueprint(kepalaupt)

# Blueprint untuk staff
from .views import staff
app.register_blueprint(staff)

# Blueprint untuk jabatan
from .views import jabatan
app.register_blueprint(jabatan)

# Blueprint untuk surat masuk
from .views import suratmasuk
app.register_blueprint(suratmasuk)

# Blueprint untuk surat keluar
from .views import suratkeluar
app.register_blueprint(suratkeluar)

# Blueprint untuk komen masuk
from .views import komenmasuk
app.register_blueprint(komenmasuk)

# Blueprint untuk replymasuk
from .views import replymasuk
app.register_blueprint(replymasuk)

# Blueprint untuk replykeluar
from .views import replykeluar
app.register_blueprint(replykeluar)

# Blueprint untuk komen keluar
from .views import komenkeluar
app.register_blueprint(komenkeluar)

# Blueprint untuk tindaklanjut
from .views import tindaklanjut
app.register_blueprint(tindaklanjut)

# Blueprint untuk followup
from .views import followup
app.register_blueprint(followup)

# Blueprint untuk superadmin
from .views import superadmin
app.register_blueprint(superadmin)

# Blueprint untuk manajemen
from .views import manajemen
app.register_blueprint(manajemen)

#Blueprint untuk Surat
from .views import surat
app.register_blueprint(surat)