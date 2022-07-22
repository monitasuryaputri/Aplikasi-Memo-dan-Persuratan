REPLYMASUK_KIND="replymasuk"

class Replymasuk:
    def __init__(self, id=None,
                 komenmasuk="TIDAK ADA INFORMASI",
                 suratmasuk="TIDAK ADA INFORMASI",
                 penindak="TIDAK ADA INFORMASI", 
                 isi_replymasuk="TIDAK ADA INFORMASI", 
                 tgl_replymasuk="TIDAK ADA INFORMASI"):
        self.id = id
        self.komenmasuk = komenmasuk
        self.suratmasuk = suratmasuk
        self.penindak = penindak
        self.isi_replymasuk = isi_replymasuk
        self.tgl_replymasuk = tgl_replymasuk


    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id

        if self.komenmasuk == None:
            hasil["komenmasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["komenmasuk"] = self.komenmasuk  

        if self.suratmasuk == None:
            hasil["suratmasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["suratmasuk"] = self.suratmasuk

        if self.penindak == None:
            hasil["penindak"] = "TIDAK ADA INFORMASI"
        else:
            hasil["penindak"] = self.penindak 

        if self.isi_replymasuk == None:
            hasil["isi_replymasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["isi_replymasuk"] = self.isi_replymasuk
            
        if self.tgl_replymasuk == None:
            hasil["tgl_replymasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_replymasuk"] = self.tgl_replymasuk
            
        return hasil
        