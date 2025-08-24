from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel)

class MainWindow(QMainWindow):
    def __init__(self, token, role):
        super().__init__()
        self.token = token
        self.role = role
        self.setWindowTitle("Issue Tracker")
        self.resize(400, 300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Logged in as {role}"))

        if role == "Admin":
            layout.addWidget(QPushButton("Create Issue"))
            layout.addWidget(QPushButton("View Issues"))
            layout.addWidget(QPushButton("Modify Issues"))
        elif role == "User":
            layout.addWidget(QPushButton("Submit Issue"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)