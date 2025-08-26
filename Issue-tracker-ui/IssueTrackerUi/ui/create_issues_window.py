from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal


class CreateIssueWindow(QMainWindow):
    issue_created = Signal()
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("Create New Issue")
        self.resize(500, 400)

        self.api = api

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Title
        layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        # Description
        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        layout.addWidget(self.desc_input)

        # Status
        layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Open", "In Progress", "Resolved", "Closed"])
        layout.addWidget(self.status_combo)

        # Submit button
        self.btn_submit = QPushButton("✅ Create Issue")
        layout.addWidget(self.btn_submit)

        self.btn_submit.clicked.connect(self.create_issue)

    def create_issue(self):
        title = self.title_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        status = self.status_combo.currentText()

        if not title:
            QMessageBox.warning(self, "Validation Error", "Title cannot be empty!")
            return

        payload = {
            "title": title,
            "description": description,
            "status": status
        }

        try:
            response = self.api.create_issue(payload)
            if response:
                QMessageBox.information(self, "Success", "Issue created successfully!")
                self.issue_created.emit()  # 👉 kirim signal
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Failed to create issue.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"API error: {e}")
