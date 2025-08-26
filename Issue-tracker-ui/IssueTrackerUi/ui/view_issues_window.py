from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class ViewIssuesWindow(QMainWindow):
    def __init__(self, api):
        super().__init__()
        self.setWindowTitle("View Issues")
        self.resize(600, 400)

        self.api = api

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Status"])
        layout.addWidget(self.table)

        self.load_issues()

    def load_issues(self):
        issues = self.api.get_issues()
        self.table.setRowCount(len(issues))

        for row, issue in enumerate(issues):
            self.table.setItem(row, 0, QTableWidgetItem(str(issue.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(issue.get("title", "")))
            self.table.setItem(row, 2, QTableWidgetItem(issue.get("status", "")))
