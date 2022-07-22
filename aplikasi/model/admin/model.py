"""
Model Untuk Admin

Property Admin:
+ id : integer
+ nama : string
+ email : string
+ no_hp : string
+ jabatan : string
+ picture : string

"""
# konstanta kind admin, konstanta ini dipakai agar nama kind untuk admin seragam
ADMIN_KIND="admin"

class Admin:
    """ 
    Membuat instance baru pada class Admin
    
    Methods: 
            + __init__ : inisialisasi pembuatan object dari class
            + ke_dictionary : menampung kumpulan object dari class Admin dalam bentuk dictionary
    
    """
    def __init__(self, id=None, 
                nama="TIDAK ADA INFORMASI", 
                email="TIDAK ADA INFORMASI", 
                no_hp="TIDAK ADA INFORMASI",
                jabatan="TIDAK ADA INFORMASI",
                picture="TIDAK ADA INFORMASI"):
        self.id = id
        self.nama = nama
        self.email = email
        self.no_hp = no_hp
        self.jabatan = jabatan
        self.picture = picture

    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id

        #jika nama none jadikan "tidak ada informasi"    
        if self.nama == None:
            hasil["nama"] = "TIDAK ADA INFORMASI"
        else:
            hasil["nama"] = self.nama

        #jika email none jadikan "tidak ada informasi"
        if self.email == None:
            hasil["email"] = "TIDAK ADA INFORMASI"
        else:
            hasil["email"] = self.email

        #jika nomor hp none jadikan "tidak ada informasi"
        if self.no_hp == None:
            hasil["no_hp"] = "TIDAK ADA INFORMASI"
        else:
            hasil["no_hp"] = self.no_hp

        #jika jabatan none jadikan "tidak ada informasi"
        if self.jabatan == None:
            hasil["jabatan"] = "TIDAK ADA INFORMASI"
        else:
            hasil["jabatan"] = self.jabatan

        #jika picture none jadikan "tidak ada informasi"
        if self.picture == None:
            hasil["picture"] = "TIDAK ADA INFORMASI"
        else:
            hasil["picture"] = self.picture

        return hasil
        