import requests
import time
import json
from datetime import datetime, timedelta

# Fungsi untuk membaca Authorization dari data.txt
def get_authorizations():
    with open('data.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

# Fungsi untuk menampilkan hitung mundur dengan tampilan waktu yang bergerak
def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        timer = f'{hours:02d}:{mins:02d}:{secs:02d}'
        print(f"\rCountdown: {timer}", end="")
        time.sleep(1)
        seconds -= 1
    print("\nCountdown complete. Restarting...")

# Fungsi untuk melakukan klaim
def claim_reward(auth):
    url = "https://crypto-landing-cat-062fa2faee4e.herokuapp.com/users/claim"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Authorization": auth,
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "2",
        "Content-Type": "application/json",
        "Host": "crypto-landing-cat-062fa2faee4e.herokuapp.com",
        "Origin": "https://steady-alfajores-6f6a13.netlify.app",
        "Pragma": "no-cache",
        "Referer": "https://steady-alfajores-6f6a13.netlify.app/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    
    response = requests.post(url, headers=headers, json={})
    return response.status_code

# Fungsi utama untuk menjalankan proses klaim
def main():
    authorizations = get_authorizations()
    total_accounts = len(authorizations)
    print(f"Total accounts: {total_accounts}")

    while True:
        for i, auth in enumerate(authorizations):
            print(f"\nProcessing account {i+1}/{total_accounts}")
            status = claim_reward(auth)
            if status == 200:
                print(f"Account {i+1} claim successful!")
            else:
                print(f"Account {i+1} claim failed with status code: {status}")
            time.sleep(5)  # Jeda 5 detik sebelum beralih ke akun berikutnya

        print("\nAll accounts processed. Starting countdown for 3.5 hours.")
        countdown_timer(3 * 3600 + 1800)  # Hitung mundur 3.5 jam (3 jam + 1800 detik)

if __name__ == "__main__":
    main()
