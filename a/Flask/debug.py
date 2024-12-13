import time, subprocess, os
from datetime import datetime, timezone
from colorama import Fore, Style, init
import argparse

init()

folders = './'

# Argümanları al
parser = argparse.ArgumentParser(description="Dosya izleme ve yeniden başlatma sistemi")
parser.add_argument('-f', '--file', type=str, default='test.py', help='Çalıştırılacak Python dosyası (varsayılan: main.py)')
args = parser.parse_args()

main = args.file

file_mod_times = {}

def get_file_mod_times():
    return {f: os.path.getmtime(os.path.join(folders, f)) 
            for f in os.listdir(folders) 
            if os.path.isfile(os.path.join(folders, f))}

# main.py'yi başlat
process = subprocess.Popen(['python', main])

try:
    file_mod_times = get_file_mod_times()
    while True:
        time.sleep(0.5)
        current_mod_times = get_file_mod_times()
        
        if current_mod_times != file_mod_times:
            print(Fore.LIGHTRED_EX + datetime.now().strftime("%H:%M:%S") + Fore.WHITE + Style.DIM + " >>" + Style.RESET_ALL + f" Değişiklik tespit edildi sistem yeniden başlatılıyor!")
            process.terminate()
            process.wait()
            process = subprocess.Popen(['python', main])
            file_mod_times = current_mod_times
except KeyboardInterrupt: print(Fore.LIGHTRED_EX + datetime.now().strftime("%H:%M:%S") + Fore.WHITE + Style.DIM + " >>" + Style.RESET_ALL + f" Sistem kapatılıyor! İzleme devre dışı.")
finally: process.terminate()
