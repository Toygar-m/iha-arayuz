import time
import subprocess
import os
from datetime import datetime
from colorama import Fore, Style, init
import argparse

init()

folders = './'

parser = argparse.ArgumentParser(description="UI dosyası izleme ve GUI yeniden başlatma sistemi")
parser.add_argument('-u', '--ui', type=str, default='gui.ui', help='İzlenecek UI dosyası (varsayılan: design.ui)')
parser.add_argument('-p', '--python', type=str, default='test.py', help='GUI uygulamasını çalıştıran Python dosyası (varsayılan: gui_app.py)')
args = parser.parse_args()

ui_file = args.ui
gui_file = args.python

file_mod_time = 0  # Başlangıç için eski mod zamanı 0

def get_file_mod_time(file_path):
    if os.path.isfile(file_path):
        return os.path.getmtime(file_path)
    return None

# Başlangıçta GUI çalıştır
process = subprocess.Popen(['python', gui_file])

try:
    file_mod_time = get_file_mod_time(ui_file)
    while True:
        time.sleep(0.5)
        current_mod_time = get_file_mod_time(ui_file)
        
        if current_mod_time and current_mod_time != file_mod_time:
            print(Fore.LIGHTRED_EX + datetime.now().strftime("%H:%M:%S") + Fore.WHITE + Style.DIM + 
                  " >>" + Style.RESET_ALL + f" '{ui_file}' dosyasında değişiklik tespit edildi, GUI yeniden başlatılıyor!")
            
            # .ui dosyasını .py'ye dönüştür
            subprocess.run(['python', '-m', 'PyQt5.uic.pyuic', '-x', ui_file, '-o', gui_file])
            
            # Mevcut süreci sonlandır ve yeniden başlat
            process.terminate()
            process.wait()
            process = subprocess.Popen(['python', gui_file])
            
            # Zaman damgasını güncelle
            file_mod_time = current_mod_time
except KeyboardInterrupt:
    print(Fore.LIGHTRED_EX + datetime.now().strftime("%H:%M:%S") + Fore.WHITE + Style.DIM + 
          " >>" + Style.RESET_ALL + " Sistem kapatılıyor! İzleme devre dışı.")
finally:
    process.terminate()
