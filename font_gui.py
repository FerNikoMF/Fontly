import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QMessageBox
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QMovie
from PyQt6.QtCore import QTimer, Qt

from font_installer import install_fonts_from_folder

class FontInstallerUI(QWidget):
    def __init__(self):
        super().__init__()

        # Установка темы приложения
        app_palette = QPalette()
        app_palette.setColor(QPalette.ColorRole.Window, QColor("#282828"))
        app_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        app_palette.setColor(QPalette.ColorRole.Button, QColor("#5C5C5C"))
        app_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        app_palette.setColor(QPalette.ColorRole.Highlight, QColor("#0674ff"))
        app_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

        self.setPalette(app_palette)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setWindowTitle("Установлено шрифтов Fontly")
        self.setWindowIcon(QIcon("resource/images/logo.png"))
        self.setFixedSize(350, 300)

        self.font_count = 0
        self.error_count = 0

        self.title_label = QLabel("Fontly")
        font = QFont("unbounded", 24, QFont.Weight.Bold)
        self.title_label.setFont(font)
        self.layout.addWidget(self.title_label)

        self.gif_label = QLabel(self)
        self.movie = QMovie("resource/images/red.gif")
        self.movie.setScaledSize(self.size())
        self.gif_label.setMovie(self.movie)
        self.layout.addWidget(self.gif_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 6px;
                background-color: #424242;
                text-align: center;
                width: 16px;
            }
            QProgressBar::chunk {
                background-color: #0674ff;
                border-radius: 6px;
                width: 16px;
            }
        """)
        self.progress_bar.setMinimumSize(0, 30)
        self.layout.addWidget(self.progress_bar)

        self.progress_counter = QLabel("0%")
        self.layout.addWidget(self.progress_counter, alignment=Qt.AlignmentFlag.AlignCenter)

        self.folder_label = QLabel("")
        self.layout.addWidget(self.folder_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.browse_button = QPushButton("Обзор...")
        self.browse_button.setMinimumWidth(170)
        self.browse_button.setFont(QFont("Segoe UI", 12))
        self.browse_button.setStyleSheet("background-color: #0070ff; color: white; border-radius: 5px;")
        self.browse_button.setMinimumSize(0, 30)
        self.browse_button.clicked.connect(self.browse_folder)
        self.layout.addWidget(self.browse_button, alignment=Qt.AlignmentFlag.AlignBottom)

        # Links layout
        links_layout = QHBoxLayout()

        # First link
        self.link1_label = QLabel("<a href='https://github.com/FerNikoMF/Fontly'>GitHub</a>")
        self.link1_label.setOpenExternalLinks(True)
        links_layout.addWidget(self.link1_label)

        # Add links layout to main layout
        self.layout.addLayout(links_layout)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку с шрифтами")
        if folder_path:
            folder_name = os.path.basename(folder_path)
            self.folder_label.setText(f"Устанавливаются шрифты из папки: {folder_name}")
            self.start_progress(folder_path)
            self.timer.start(100)  # Запускаем таймер для обновления прогресса

    def start_progress(self, folder_path):
        self.font_count = 0
        self.error_count = 0
        self.progress_bar.setValue(0)
        self.progress_counter.setText("0%")
        self.font_count = install_fonts_from_folder(folder_path)

    def update_progress(self):
        if self.progress_value <= 100:
            self.progress_value += 1
            self.progress_bar.setValue(self.progress_value)
            self.progress_counter.setText(f"{self.progress_value}%")
        else:
            self.timer.stop()
            self.progress_counter.setText(f"Установлено шрифтов: {self.font_count}")
            if self.error_count == 0:
                QMessageBox.information(self, "Успешно", "Шрифты успешно установлены!", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(self, "Ошибка", "В процессе установки шрифтов произошли ошибки.", QMessageBox.StandardButton.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FontInstallerUI()
    window.show()
    sys.exit(app.exec())
