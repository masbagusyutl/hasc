import requests
import time
import random
import json
import datetime

# Read account data from data.txt
def read_accounts(file_path):
    with open(file_path, 'r') as file:
        accounts = file.readlines()
    return [account.strip() for account in accounts]

# Get user info
def get_user_info(auth_token):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': auth_token
    }
    response = requests.get('https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users', headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Username: {data['user']['userName']}, Mined Coins: {data['minedCoins']}, Shard: {data['user']['shard']}")
        return data
    else:
        print(f"Failed to get user info: {response.status_code}")
        print(response.text)

# Start tapping task
def start_tapping(auth_token):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': auth_token,
        'Content-Type': 'application/json'
    }
    payload = {
        'dateStartMs': int(time.time() * 1000)
    }
    response = requests.post('https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/start-tapping', headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data['token']
    else:
        print(f"Failed to start tapping: {response.status_code}")
        print(response.text)

# Perform tap tap task
def perform_tap_tap(auth_token, token, tap_balance):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': auth_token,
        'Content-Type': 'application/json'
    }
    payload = {
        'tapBalance': tap_balance,
        'token': token
    }
    response = requests.post('https://hashcats-gateway-ffa6af9b026a.herokuapp.com/users/save-tap-balance', headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"Balance: {data['balance']}, Energy: {data['energy']}")
        return data
    else:
        print(f"Failed to perform tap tap: {response.status_code}")
        print(response.text)

# Main function
def main():
    accounts = read_accounts('data.txt')
    print(f"Total accounts: {len(accounts)}")

    for idx, auth_token in enumerate(accounts):
        print(f"Processing account {idx + 1} of {len(accounts)}")

        # Get user info
        user_info = get_user_info(auth_token)

        # Start tapping task
        token = start_tapping(auth_token)

        # Perform first tap tap task with random tapBalance between 2 and 10
        initial_tap_balance = random.randint(2, 10)
        tap_tap_data = perform_tap_tap(auth_token, token, initial_tap_balance)

        # Perform subsequent tap tap tasks based on the energy from the first tap tap
        remaining_energy = tap_tap_data['energy']
        while remaining_energy > 0:
            tap_balance = random.randint(5, min(200, remaining_energy))
            tap_tap_data = perform_tap_tap(auth_token, token, tap_balance)
            remaining_energy -= tap_balance

        # Delay before processing the next account
        time.sleep(5)

    # Countdown timer for 3.5 hours
    for remaining in range(3*60*60 + 30*60, 0, -1):
        print(f"Time remaining for next run: {datetime.timedelta(seconds=remaining)}", end='\r')
        time.sleep(1)

if __name__ == "__main__":
    main()
