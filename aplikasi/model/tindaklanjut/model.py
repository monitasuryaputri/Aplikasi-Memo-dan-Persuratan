TINDAKLANJUT_KIND="tindaklanjut"

class Tindaklanjut:
    def __init__(self, id=None, 
                suratmasuk="TIDAK ADA INFORMASI",
                penugas="TIDAK ADA INFORMASI",
                penanggungjawab="TIDAK ADA INFORMASI", 
                tugas="TIDAK ADA INFORMASI", 
                tgl_tugas="TIDAK ADA INFORMASI",
                tgl_selesai="TIDAK ADA INFORMASI",
                followup="TIDAK ADA INFORMASI",
                tenggatwaktu="TIDAK ADA INFORMASI",
                check="TIDAK ADA INFORMASI",
                notif="TIDAK ADA INFORMASI"):

        self.id = id
        self.suratmasuk = suratmasuk
        self.penugas = penugas
        self.penanggungjawab = penanggungjawab
        self.tugas = tugas
        self.tgl_tugas = tgl_tugas
        self.tgl_selesai = tgl_selesai
        self.followup = followup
        self.tenggatwaktu = tenggatwaktu
        self.check = check
        self.notif = notif

    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id

        if self.suratmasuk == None:
            hasil["suratmasuk"] = "TIDAK ADA INFORMASI"
        else:
            hasil["suratmasuk"] = self.suratmasuk  

        if self.penugas == None:
            hasil["penugas"] = "TIDAK ADA INFORMASI"
        else:
            hasil["penugas"] = self.penugas

        if self.penanggungjawab == None:
            hasil["penanggungjawab"] = "TIDAK ADA INFORMASI"
        else:
            hasil["penanggungjawab"] = self.penanggungjawab

        if self.tugas == None:
            hasil["tugas"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tugas"] = self.tugas
        
        if self.tgl_tugas == None:
            hasil["tgl_tugas"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_tugas"] = self.tgl_tugas

        if self.tgl_selesai == None:
            hasil["tgl_selesai"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_selesai"] = self.tgl_selesai
            
        if self.followup == None:
            hasil["followup"] = "TIDAK ADA INFORMASI"
        else:
            hasil["followup"] = self.followup

        if self.tenggatwaktu == None:
            hasil["tenggatwaktu"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tenggatwaktu"] = self.tenggatwaktu

        if self.check == None:
            hasil["check"] = "TIDAK ADA INFORMASI"
        else:
            hasil["check"] = self.check

        if self.notif == None:
            hasil["notif"] = "TIDAK ADA INFORMASI"
        else:
            hasil["notif"] = self.notif

        return hasil
        