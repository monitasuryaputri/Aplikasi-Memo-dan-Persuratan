SURAT_KIND ="surat"

class Surat:
    def __init__(self, id=None,
                nomor= "Tidak Ada Informasi",
                asal= "Tidak Ada Informasi",
                tujuan= "Tidak Ada Informasi",
                tgl= "Tidak Ada Informasi",
                isi= "Tidak Ada Informasi",
                dokumen = "Tidak Ada Informasi" ):
        self.id=id
        self.nomor=nomor
        self.asal=asal
        self.tujuan=tujuan
        self.tgl=tgl
        self.isi=isi
        self.dokumen=dokumen

    def ke_dictionary(self):
        hasil = {}

        if self.id != None:
            hasil["id"] = self.id

        if self.nomor == None:
            hasil ["nomor"] = "Tidak Ada Informasi"
        else:
            hasil ["nomor"] = self.nomor

        if self.asal == None:
            hasil ["asal"] = "Tidak Ada Informasi"
        else:
            hasil ["asal"] = self.asal

        if self.tujuan == None:
            hasil ["tujuan"] = "Tidak Ada Informasi"
        else:
            hasil ["tujuan"] = self.tujuan

        if self.tgl == None:
            hasil ["tgl"] = "Tidak Ada Informasi"
        else:
            hasil ["tgl"] = self.tgl

        if self.isi == None:
            hasil ["isi"] = "Tidak Ada Informasi"
        else:
            hasil ["isi"] = self.isi

        if self.dokumen == None:
            hasil ["dokumen"] = "Tidak Ada Informasi"
        else:
            hasil ["dokumen"] = self.dokumen
        
        return hasil
