import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from font_gui import FontInstallerUI

def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                sys.exit()  # Выходим, чтобы предотвратить запуск обычного экземпляра программы
        except Exception as e:
            print("Failed to run the script as administrator:", e)

if __name__ == "__main__":
    run_as_admin()  # Проверяем права администратора
    
    app = QApplication(sys.argv)
    window = FontInstallerUI()
    
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        window.start_progress(folder_path)
    
    window.show()
    sys.exit(app.exec())
