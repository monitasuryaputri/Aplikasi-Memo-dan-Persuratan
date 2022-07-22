FOLLOWUP_KIND="followup"

class Followup:
    def __init__(self, 
                id=None, 
                tindaklanjut="TIDAK ADA INFORMASI", 
                penanggungjawab="TIDAK ADA INFORMASI", 
                isi_followup="TIDAK ADA INFORMASI", 
                file_followup="TIDAK ADA INFORMASI", 
                tgl_followup="TIDAK ADA INFORMASI"):
        self.id = id
        self.tindaklanjut = tindaklanjut
        self.penanggungjawab = penanggungjawab
        self.isi_followup = isi_followup
        self.file_followup = file_followup
        self.tgl_followup = tgl_followup


    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id
        if self.tindaklanjut == None:
            hasil["tindaklanjut"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tindaklanjut"] = self.tindaklanjut  
        if self.penanggungjawab == None:
            hasil["penanggungjawab"] = "TIDAK ADA INFORMASI"
        else:
            hasil["penanggungjawab"] = self.penanggungjawab 

        if self.isi_followup == None:
            hasil["isi_followup"] = "TIDAK ADA INFORMASI"
        else:
            hasil["isi_followup"] = self.isi_followup

        if self.file_followup == None:
            hasil["file_followup"] = "TIDAK ADA INFORMASI"
        else:
            hasil["file_followup"] = self.file_followup
            
        if self.tgl_followup == None:
            hasil["tgl_followup"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_followup"] = self.tgl_followup
        return hasil
        