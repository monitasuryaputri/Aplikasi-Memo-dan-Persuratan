REPLYKELUAR_KIND="replykeluar"

class Replykeluar:
    def __init__(self, id=None,
                 komenkeluar="TIDAK ADA INFORMASI",
                 suratkeluar="TIDAK ADA INFORMASI",
                 penindak="TIDAK ADA INFORMASI", 
                 isi_replykeluar="TIDAK ADA INFORMASI", 
                 tgl_replykeluar="TIDAK ADA INFORMASI"):
        self.id = id
        self.komenkeluar = komenkeluar
        self.suratkeluar = suratkeluar
        self.penindak = penindak
        self.isi_replykeluar = isi_replykeluar
        self.tgl_replykeluar = tgl_replykeluar


    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id

        if self.komenkeluar == None:
            hasil["komenkeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["komenkeluar"] = self.komenkeluar  

        if self.suratkeluar == None:
            hasil["suratkeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["suratkeluar"] = self.suratkeluar

        if self.penindak == None:
            hasil["penindak"] = "TIDAK ADA INFORMASI"
        else:
            hasil["penindak"] = self.penindak 

        if self.isi_replykeluar == None:
            hasil["isi_replykeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["isi_replykeluar"] = self.isi_replykeluar
            
        if self.tgl_replykeluar == None:
            hasil["tgl_replykeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_replykeluar"] = self.tgl_replykeluar
            
        return hasil
        