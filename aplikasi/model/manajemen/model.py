MANAJEMEN_KIND ="manajemen"

class Manajemen:
    def __init__(self, id=None, email="TIDAK ADA INFORMASI"):
        self.id = id
        self.email = email

    def ke_dictionary(self):
        hasil = {}

        if self.id != None:
            hasil["id"] = self.id
        if self.email == None:
            hasil["email"] = "TIDAK ADA INFORMASI"
        else:
            hasil["email"] = self.email

        return hasil