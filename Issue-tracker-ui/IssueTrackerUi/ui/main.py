import sys
from PySide6.QtWidgets import QApplication
from login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load global stylesheet
    with open("styles/style.qss", "r") as f:
        app.setStyleSheet(f.read())

    login = LoginWindow(app)
    login.show()
    sys.exit(app.exec())