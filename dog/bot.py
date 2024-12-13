import requests
import time
import re
import urllib.parse
import json

# URL API untuk daily login dan open day
DAILY_LOGIN_URL = "https://api.onetime.dog/advent/calendar/check"
OPEN_DAY_URL = "https://api.onetime.dog/advent/calendar/open-day"

# File yang berisi query/token dan user_id
COMBINED_FILE = "combined.txt"
DATA_FILE = "data.txt"
LOG_FILE = "log.txt"

# Fungsi untuk mencatat hasil ke log
def write_log(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")

# Fungsi untuk mengekstrak user_id dari query atau token dan menyimpan ke data.txt
def extract_user_ids():
    try:
        with open(COMBINED_FILE, "r") as file:
            content = file.read().strip()
    except FileNotFoundError:
        print(f"\033[35mFile {COMBINED_FILE} tidak ditemukan.\033[0m")
        return []

    parsed_content = urllib.parse.parse_qs(content)
    
    user_ids = []
    if 'user' in parsed_content:
        for user_data in parsed_content['user']:
            user_dict = json.loads(user_data.replace("'", '"'))
            user_id = user_dict.get('id', None)
            if user_id is not None:
                user_ids.append(user_id)

    if user_ids:
        with open(DATA_FILE, "w") as file:
            for user_id in user_ids:
                file.write(f"{user_id}\n")
        print(f"\033[35m{len(user_ids)} User ID berhasil disimpan ke {DATA_FILE}\033[0m")
    else:
        print("\033[35mTidak menemukan user_id dalam content dari combined.txt.\033[0m")
    return user_ids

# Fungsi untuk membaca user_id dari data.txt
def read_user_ids():
    try:
        with open(DATA_FILE, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"\033[35mFile {DATA_FILE} tidak ditemukan.\033[0m")
        return []

# Fungsi untuk mengirim permintaan ke API daily login
def send_daily_login(user_id, day):
    try:
        response = requests.post(f"{DAILY_LOGIN_URL}?user_id={user_id}&day={day}")
        result = response.json()
        if result.get("ok") is not False or result.get("error") == "already checked":
            print(f"\033[35mUSER_ID {user_id}, DAY {day}: Success\033[0m")
            write_log(f"USER_ID {user_id}, DAY {day}: Success")
            return "Success"
        else:
            error_message = result.get('error', 'Unknown error')
            print(f"\033[35mUSER_ID {user_id}, DAY {day}: Failed - {error_message}\033[0m")
            write_log(f"USER_ID {user_id}, DAY {day}: Failed - {error_message}")
            return f"Failed - {error_message}"
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP Error - {http_err}"
        print(f"\033[35mUSER_ID {user_id}, DAY {day}: {error_message}\033[0m")
        write_log(f"USER_ID {user_id}, DAY {day}: {error_message}")
        return error_message
    except ValueError:
        error_message = f"Error - Invalid JSON. Response: {response.text}"
        print(f"\033[35mUSER_ID {user_id}, DAY {day}: {error_message}\033[0m")
        write_log(f"USER_ID {user_id}, DAY {day}: {error_message}")
        return error_message
    except Exception as e:
        error_message = f"Error - {str(e)}"
        print(f"\033[35mUSER_ID {user_id}, DAY {day}: {error_message}\033[0m")
        write_log(f"USER_ID {user_id}, DAY {day}: {error_message}")
        return error_message

# Fungsi untuk membuka hari dalam kalender
def open_day(user_id):
    try:
        response = requests.post(f"{OPEN_DAY_URL}?user_id={user_id}")
        result = response.json()
        if result.get("ok") is not False:
            print(f"\033[35mUSER_ID {user_id}: Day opened successfully\033[0m")
            write_log(f"USER_ID {user_id}: Day opened successfully")
            return "Day opened successfully"
        else:
            error_message = result.get('error', 'Unknown error')
            print(f"\033[35mUSER_ID {user_id}: Failed to open day - {error_message}\033[0m")
            write_log(f"USER_ID {user_id}: Failed to open day - {error_message}")
            return f"Failed to open day - {error_message}"
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP Error opening day - {http_err}"
        print(f"\033[35mUSER_ID {user_id}: {error_message}\033[0m")
        write_log(f"USER_ID {user_id}: {error_message}")
        return error_message
    except ValueError:
        error_message = f"Error - Invalid JSON on open day. Response: {response.text}"
        print(f"\033[35mUSER_ID {user_id}: {error_message}\033[0m")
        write_log(f"USER_ID {user_id}: {error_message}")
        return error_message
    except Exception as e:
        error_message = f"Error opening day - {str(e)}"
        print(f"\033[35mUSER_ID {user_id}: {error_message}\033[0m")
        write_log(f"USER_ID {user_id}: {error_message}")
        return error_message

# Fungsi untuk menampilkan logo dan watermark
def display_logo():
    print("\033[35m DDDD  \033[0m   \033[35m OOO  \033[0m   \033[35m GGGG  \033[0m  \033[35m SSSSS  \033[0m")
    print("\033[35m D   D \033[0m  \033[35m O   O \033[0m  \033[35m G     \033[0m  \033[35m S     \033[0m")
    print("\033[35m D   D \033[0m  \033[35m O   O \033[0m  \033[35m G  GG \033[0m   \033[35m SSSSS \033[0m")
    print("\033[35m D   D \033[0m  \033[35m O   O \033[0m  \033[35m G   G \033[0m        \033[35m S     \033[0m")
    print("\033[35m DDDD  \033[0m   \033[35m OOO  \033[0m   \033[35m GGGG  \033[0m  \033[35m SSSSS  \033[0m")

    
    print("\033[38;5;206mby: pras & goodbye\033[0m")

# Menu utama
while True:
    display_logo()  # Menampilkan logo dan watermark
    print("\033[38;5;206mPilih opsi:\033[0m")
    print("1. Ekstrak Query/Token menjadi User ID dan simpan ke data.txt")
    print("2. Daily Login untuk semua User ID")
    print("3. Open Day untuk semua User ID")
    print("4. Keluar")
    
    choice = input("\033[38;5;206mPilih menu (1/2/3/4): \033[0m")

    if choice == '1':
        extract_user_ids()
    elif choice == '2':
        user_ids = read_user_ids()
        if user_ids:
            day = input("\033[38;5;206mMasukkan day keberapa: \033[0m")
            for user_id in user_ids:
                # Hanya satu percobaan untuk setiap user_id
                result = send_daily_login(user_id, day)
        else:
            print("\033[35mTidak ada user_id yang ditemukan di data.txt.\033[0m")
    elif choice == '3':
        user_ids = read_user_ids()
        if user_ids:
            for user_id in user_ids:
                result = open_day(user_id)
                print(result)
        else:
            print("\033[35mTidak ada user_id yang ditemukan di data.txt.\033[0m")
    elif choice == '4':
        print("\033[35mKeluar dari program.\033[0m")
        break
    else:
        print("\033[35mPilihan tidak valid. Silakan coba lagi.\033[0m")

    # Jeda antar opsi untuk memberi kesempatan untuk membaca hasil
    time.sleep(1)