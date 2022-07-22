"""
Model Untuk Surat Masuk

"""
# konstanta kind surat masuk, konstanta ini dipakai agar nama kind untuk surat masuk seragam
SURATMASUK_KIND = "suratmasuk"

#buat object class surat masuk
class Suratmasuk:
    def __init__(self, 
                id=None, 
                nomor_surat="TIDAK ADA INFORMASI", 
                tgl_surat="TIDAK ADA INFORMASI", 
                asal_surat="TIDAK ADA INFORMASI", 
                hal="TIDAK ADA INFORMASI", 
                isi_ringkas="TIDAK ADA INFORMASI",  
                dokumen="TIDAK ADA INFORMASI", 
                disposisi="TIDAK ADA INFORMASI", 
                komentar="TIDAK ADA INFORMASI",
                tindaklanjut="TIDAK ADA INFORMASI",
                dibaca="TIDAK ADA INFORMASI",
                tgl_disposisi="TIDAK ADA INFORMASI", 
                status_tindaklanjut="TIDAK ADA INFORMASI",
                reply="TIDAK ADA INFORMASI" 
                ):
        self.id = id
        self.nomor_surat = nomor_surat
        self.tgl_surat = tgl_surat
        self.asal_surat = asal_surat
        self.hal = hal
        self.isi_ringkas = isi_ringkas
        self.dokumen = dokumen
        self.disposisi = disposisi
        self.komentar = komentar
        self.tindaklanjut = tindaklanjut
        self.dibaca = dibaca
        self.tgl_disposisi = tgl_disposisi
        self.status_tindaklanjut = status_tindaklanjut
        self.reply = reply


    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id

        # Jika nomor_surat None jadikan "TIDAK ADA INFORMASI"
        if self.nomor_surat == None:
            hasil["nomor_surat"] = "TIDAK ADA INFORMASI"
        else:
            hasil["nomor_surat"] = self.nomor_surat

        # Jika tgl_surat None jadikan "TIDAK ADA INFORMASI"
        if self.tgl_surat == None:
            hasil["tgl_surat"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_surat"] = self.tgl_surat
        
        # Jika asal_surat None jadikan "TIDAK ADA INFORMASI"
        if self.asal_surat == None:
            hasil["asal_surat"] = "TIDAK ADA INFORMASI"
        else:
            hasil["asal_surat"] = self.asal_surat

        # Jika hal None jadikan "TIDAK ADA INFORMASI"
        if self.hal == None:
            hasil["hal"] = "TIDAK ADA INFORMASI"
        else:
            hasil["hal"] = self.hal

        # Jika isi_ringkas None jadikan "TIDAK ADA INFORMASI"
        if self.isi_ringkas == None:
            hasil["isi_ringkas"] = "TIDAK ADA INFORMASI"
        else:
            hasil["isi_ringkas"] = self.isi_ringkas

        # Jika dokumen None jadikan "TIDAK ADA INFORMASI"
        if self.dokumen == None:
            hasil["dokumen"] = "TIDAK ADA INFORMASI"
        else:
            hasil["dokumen"] = self.dokumen

        # Jika disposisi None jadikan "TIDAK ADA INFORMASI"
        if self.disposisi == None:
            hasil["disposisi"] = "TIDAK ADA INFORMASI"
        else:
            hasil["disposisi"] = self.disposisi

        # Jika komentar None jadikan "TIDAK ADA INFORMASI"
        if self.komentar == None:
            hasil["komentar"] = "TIDAK ADA INFORMASI"
        else:
            hasil["komentar"] = self.komentar

        # Jika tindaklanjut None jadikan "TIDAK ADA INFORMASI"
        if self.tindaklanjut == None:
            hasil["tindaklanjut"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tindaklanjut"] = self.tindaklanjut

        # Jika dibaca None jadikan "TIDAK ADA INFORMASI"
        if self.dibaca == None:
            hasil["dibaca"] = "TIDAK ADA INFORMASI"
        else:
            hasil["dibaca"] = self.dibaca
        
        # Jika tgl_disposisi None jadikan "TIDAK ADA INFORMASI"
        if self.tgl_disposisi == None:
            hasil["tgl_disposisi"] = "TIDAK ADA INFORMASI"
        else:
            hasil["tgl_disposisi"] = self.tgl_disposisi

        # Jika status_tindaklanjut None jadikan "TIDAK ADA INFORMASI"
        if self.status_tindaklanjut == None:
            hasil["status_tindaklanjut"] = "TIDAK ADA INFORMASI"
        else:
            hasil["status_tindaklanjut"] = self.status_tindaklanjut

        # Jika reply None jadikan "TIDAK ADA INFORMASI"
        if self.reply == None:
            hasil["reply"] = "TIDAK ADA INFORMASI"
        else:
            hasil["reply"] = self.reply

        return hasil
        