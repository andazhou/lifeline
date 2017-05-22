from pyicloud import *
import os, os.path
from photoimport import *
from PyQt5.QtWidgets import *



class App(QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        id_label = QLabel("Apple ID:")
        self.id = QLineEdit()

        pwd_label = QLabel("Password")
        self.pwd = QLineEdit()
        self.pwd.setEchoMode(QLineEdit.Password)

        self.submitButton = QPushButton("Submit")

        login_layout = QVBoxLayout()
        login_layout.addWidget(id_label)
        login_layout.addWidget(self.id)
        login_layout.addWidget(pwd_label)
        login_layout.addWidget(self.pwd)
        login_layout.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.submit_form)
        form_widget = QWidget(self)
        form_layout = QGridLayout()

        self.iphotos = QWidget()
        self.album_dropdown = QComboBox(self.iphotos)

        form_layout.addLayout(login_layout, 0, 1)

        form_widget.setLayout(form_layout)
        self.setCentralWidget(form_widget)
        self.setWindowTitle("Please Login to iCloud")

    def submit_form(self):
        id_field = self.id.text()
        pwd_field = self.pwd.text()

        self.login(id_field, pwd_field)


    def login(self, username, password):

        self.api = PyiCloudService(username, password)
        if self.api:
            pass
        else:
            errorMessage("Incorrect login information.")

        if self.api.requires_2fa:
            devices_label = QLabel("Two-factor authentication required. Your trusted devices are:")
            tf_widget = QWidget(self)
            tf_form = QVBoxLayout()
            tf_form.addWidget(devices_label)
            tf_widget.setLayout(tf_form)
            self.setCentralWidget(tf_widget)

            devices = self.api.trusted_devices
            twof_widget = QWidget(self)
            twof_form = QVBoxLayout()
            for i, device in enumerate(devices):
                device_string = ("  %s: %s" % (i, device.get('deviceName',
                                                      "SMS to %s" % device.get('phoneNumber'))))
                twof_label = QLabel(device_string)
                twof_form.addWidget(twof_label)



            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not self.api.send_verification_code(device):
                errorMessage("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not self.api.validate_verification_code(device, code):
                errorMessage("Failed to verify verification code")
                sys.exit(1)

            self.photoImport(self.api.photos.albums)
        else:
            self.photoImport(self.api.photos.albums)
        #self.close()

    def album_selected(self, i):
        text_name = self.album_dropdown.currentText()
        photo_album = list(self.api.photos.albums[text_name])
        for i in range(1,len(photo_album)):
            pdownload = photo_album[i].download()
            with open(os.path.join('./client/photos/', photo_album[i].filename), 'wb') as opened_file:
                try:
                    opened_file.write(pdownload.raw.read())
                except:
                    continue

            tdownload = photo_album[i].download('thumb')
            with open(os.path.join('./client/thumbnails/', photo_album[i].filename), 'wb') as thumb_file:
                try:
                    thumb_file.write(tdownload.raw.read())
                except:
                    continue

    def photoImport(self, albums):

        album_names = list(albums.keys())
        #for name in album_names:
        self.album_dropdown.addItems(album_names)

        self.setCentralWidget(self.iphotos)
        self.album_dropdown.currentIndexChanged.connect(self.album_selected)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    login = App()
    download = iCloud()

    login.show()

    sys.exit(app.exec_())