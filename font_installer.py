import os
import winreg

def count_fonts(folder_path):
    total_fonts = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".ttf", ".otf")):
                total_fonts += 1
    return total_fonts

def install_fonts_from_folder(folder_path, progress_callback=None):
    total_fonts = count_fonts(folder_path)
    fonts_installed = 0

    def install_callback(fonts_installed, total_fonts):
        if progress_callback:
            progress_callback(fonts_installed, total_fonts)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".ttf", ".otf")):
                font_file_path = os.path.join(root, file)
                font_file_name = os.path.basename(font_file_path)
                
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts", 0, winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(key, font_file_name, 0, winreg.REG_SZ, font_file_path)
                    winreg.CloseKey(key)
                    fonts_installed += 1
                    install_callback(fonts_installed, total_fonts)
                except Exception as e:
                    print(f"Ошибка установки шрифта '{font_file_name}': {e}")

    return fonts_installed
