from flask_login import UserMixin

class User(UserMixin):
    # Class untuk User yang login
    # 
    # Property
    #   * id : ID dari user -> prasyarat Flask-Login
    #   * nama_lengkap: Nama lengkap User
    #   * email: Email user
    #   * url_gambar_profil: URL untuk gambar profil di Google

    def __init__(self, unique_id, nama_lengkap, email, url_gambar_profil):
        # Default constructor
        #
        # Inisialisasi semua property dari object
        #
        # Parameter
        #   * unique_id : ID dari user -> prasyarat Flask-Login
        #   * nama_lengkap: Nama lengkap User
        #   * email: Email user
        #   * url_gambar_profil: URL untuk gambar profil di Google

        self.id = unique_id
        self.nama_lengkap = nama_lengkap
        self.email = email
        self.url_gambar_profil = url_gambar_profil
