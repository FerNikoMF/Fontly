import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from font_gui import FontInstallerUI


def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except:
            print("Failed to run the script as administrator.")

if __name__ == "__main__":
    run_as_admin()
    app = QApplication(sys.argv)
    window = FontInstallerUI()
    
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        window.start_progress(folder_path)
    
    window.show()
    sys.exit(app.exec())
