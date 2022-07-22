KOMENMASUK_KIND="komenmasuk"

class Komenmasuk:
    def __init__(self, id=None, 
                 suratmasuk="TIDAK ADA INFORMASI", 
                 penindak="TIDAK ADA INFORMASI", 
                 isi_komenmasuk="TIDAK ADA INFORMASI", 
                 tgl_komenmasuk="TIDAK ADA INFORMASI",
                 reply="TIDAK ADA INFORMASI"
                 ):
        self.id = id
        self.suratmasuk = suratmasuk
        self.penindak = penindak
        self.isi_komenmasuk = isi_komenmasuk
        self.tgl_komenmasuk = tgl_komenmasuk
        self.reply = reply


    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id

        if self.suratmasuk == None:
            hasil["suratmasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["suratmasuk"] = self.suratmasuk  

        if self.penindak == None:
            hasil["penindak"] = "TIDAK ADA INFORMASI"
        else:
            hasil["penindak"] = self.penindak 

        if self.isi_komenmasuk == None:
            hasil["isi_komenmasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["isi_komenmasuk"] = self.isi_komenmasuk
            
        if self.tgl_komenmasuk == None:
            hasil["tgl_komenmasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_komenmasuk"] = self.tgl_komenmasuk
            
        if self.reply == None:
            hasil["reply"] = "TIDAK ADA INFORMASI"
        else:
            hasil["reply"] = self.reply

        return hasil
        