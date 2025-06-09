from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

from removals_system.views.authentication import AuthenticationView

import sys
import os


def load_fonts_from_folder(folder_path: str) -> None:
    loaded_families: list[str] = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".ttf", ".otf")):
            font_path = os.path.join(folder_path, filename)
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                print(f"Loaded font: {font_path!r}")
                families = QFontDatabase.applicationFontFamilies(font_id)
                loaded_families.extend(families)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_fonts_from_folder(os.path.join("removals_system", "assets", "fonts"))
    window = AuthenticationView()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())