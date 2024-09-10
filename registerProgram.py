import sys
import sqlite3
from PyQt5 import QtWidgets

class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.baglanti_olustur() # Bağlantıyı oluştur
        self.init_ui()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("database.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS üyeler (kullanıcı_Adı TEXT, parola TEXT)")
        self.baglanti.commit()  # Bağlantıyı geçerli kılar

    def init_ui(self):
        # Arayüz öğeleri oluşturulur
        self.kullanici_adi = QtWidgets.QLineEdit()
        self.parola = QtWidgets.QLineEdit()
        self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.giris = QtWidgets.QPushButton("Giriş Yap")
        self.yazi_alani = QtWidgets.QLabel("")
        self.kayit_ol = QtWidgets.QPushButton("Kayıt ol")

        # Layout oluşturulur
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.kullanici_adi)
        v_box.addWidget(self.parola)
        v_box.addWidget(self.yazi_alani)
        v_box.addStretch()
        v_box.addWidget(self.giris)
        v_box.addWidget(self.kayit_ol)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)

        # Butonlar için sinyal-slot bağlantıları
        self.giris.clicked.connect(self.login)
        self.kayit_ol.clicked.connect(self.register)

        self.setWindowTitle("Kullanıcı Girişi")
        self.setGeometry(100, 100, 500, 500)
        self.show()

    def login(self):
        adi = self.kullanici_adi.text()
        par = self.parola.text()

        cursor = self.baglanti.cursor()
        cursor.execute("SELECT * FROM üyeler WHERE kullanıcı_Adı = ? AND parola = ?", (adi, par))

        data = cursor.fetchall()

        if len(data) == 0:
            self.yazi_alani.setText("Böyle bir kullanıcı yok\n Lütfen Tekrar Deneyin.")
        else:
            self.yazi_alani.setText("Hoşgeldiniz " + adi)

    def register(self):
        adi = self.kullanici_adi.text()
        par = self.parola.text()

        cursor = self.baglanti.cursor()
        cursor.execute("SELECT * FROM üyeler WHERE kullanıcı_Adı = ?", (adi,))
        data = cursor.fetchall()        

        if len(data) != 0:
            self.yazi_alani.setText("Bu kullanıcı adı zaten var. Lütfen farklı bir kullanıcı adı seçin.")
        else:
            cursor.execute("INSERT INTO üyeler (kullanıcı_Adı, parola) VALUES (?, ?)", (adi, par))
            self.yazi_alani.setText("Kayıt başarılı. Hoşgeldiniz " + adi)

        self.baglanti.commit()


app = QtWidgets.QApplication(sys.argv)
pencere = Pencere()
sys.exit(app.exec_())

