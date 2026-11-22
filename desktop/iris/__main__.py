"""IRIS desktop application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from iris.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("IRIS")
    app.setOrganizationName("IRIS")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
