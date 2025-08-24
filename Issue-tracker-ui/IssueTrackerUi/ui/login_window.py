import sys
import json
import requests
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import QFile
from PySide6.QtGui import QFont
from ui_main import MainWindow

class LoginWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Login - Issue Tracker")
        self.resize(300, 200)

        # Apply external QSS style
        with open("styles/style.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        title = QLabel("Login to Issue Tracker")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)

        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def login(self):
        with open("config.json") as f:
            config = json.load(f)
        url = f"{config['api_url']}/auth/login"

        payload = {
            "username": self.user_input.text(),
            "password": self.pass_input.text()
        }

        try:
            r = requests.post(url, json=payload)
            if r.status_code == 200:
                data = r.json()
                token = data['token']
                role = data['role']

                self.main_window = MainWindow(token, role)
                self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid login")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))