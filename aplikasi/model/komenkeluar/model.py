""" Model untuk Komen Keluar

Deskripsi method:
+ id                : int
+ suratkeluar       : string
+ penindak          : string
+ isi_komenkeluar   : string
+ tgl_komenkeluar   : st
+ file_komenkeluar  :
+ reply             :
"""

KOMENKELUAR_KIND="komenkeluar"

class Komenkeluar:
    def __init__(self, id=None, 
                 suratkeluar="TIDAK ADA INFORMASI", 
                 penindak="TIDAK ADA INFORMASI", 
                 isi_komenkeluar="TIDAK ADA INFORMASI", 
                 tgl_komenkeluar="TIDAK ADA INFORMASI",
                 file_komenkeluar="TIDAK ADA INFORMASI",
                 reply="TIDAK ADA INFORMASI"
                 ):
        self.id = id
        self.suratkeluar = suratkeluar
        self.penindak = penindak
        self.isi_komenkeluar = isi_komenkeluar
        self.tgl_komenkeluar = tgl_komenkeluar
        self.file_komenkeluar = file_komenkeluar
        self.reply = reply


    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id

        if self.suratkeluar == None:
            hasil["suratkeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["suratkeluar"] = self.suratkeluar  

        if self.penindak == None:
            hasil["penindak"] = "TIDAK ADA INFORMASI"
        else:
            hasil["penindak"] = self.penindak 

        if self.isi_komenkeluar == None:
            hasil["isi_komenkeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["isi_komenkeluar"] = self.isi_komenkeluar
            
        if self.tgl_komenkeluar == None:
            hasil["tgl_komenkeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_komenkeluar"] = self.tgl_komenkeluar
        
        if self.file_komenkeluar == None:
            hasil["file_komenkeluar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["file_komenkeluar"] = self.file_komenkeluar

        if self.reply == None:
            hasil["reply"] = "TIDAK ADA INFORMASI"
        else:
            hasil["reply"] = self.reply
            
        return hasil
        