JABATAN_KIND="jabatan"

class Jabatan:
    def __init__(self, id=None, nama="TIDAK ADA INFORMASI"):
        self.id = id
        self.nama = nama

    def ke_dictionary(self):
        hasil = {}

        # Jika id None jangan buat key "id"
        if self.id != None:
            hasil["id"] = self.id
        if self.nama == None:
            hasil["nama"] = "TIDAK ADA INFORMASI"
        else:
            hasil["nama"] = self.nama
        return hasil
        