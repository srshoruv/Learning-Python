import gspread
import requests
import time
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials


# === Connect to Google Sheet ===
def connect_to_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("codeforces-link-fetcher-152c6c219b6d.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1


# === Extract handle from URL ===
def get_handle(link):
    if isinstance(link, str) and "codeforces.com/profile/" in link:
        return link.strip().split("/")[-1]
    return None


# === Fetch total solved ===
def get_total_solved(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] != 'OK':
            return "Invalid Handle"
        solved = set()
        for sub in data['result']:
            if sub.get("verdict") == "OK":
                prob_id = f"{sub['problem']['contestId']}-{sub['problem']['index']}"
                solved.add(prob_id)
        return len(solved)
    except Exception as e:
        print(f"Error for {handle}: {e}")
        return "Error"


# === Fetch last online in GMT+6 ===
def get_last_online(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] != 'OK':
            return "Invalid Handle"
        last_online_unix = data['result'][0]['lastOnlineTimeSeconds']
        last_online_dt = datetime.utcfromtimestamp(last_online_unix) + timedelta(hours=6)
        now_dt = datetime.utcnow() + timedelta(hours=6)
        diff = now_dt - last_online_dt
        seconds = int(diff.total_seconds())
        if seconds < 60:
            return f"{seconds} seconds ago"
        elif seconds < 3600:
            return f"{seconds // 60} minutes ago"
        elif seconds < 86400:
            return f"{seconds // 3600} hours ago"
        else:
            return f"{seconds // 86400} days ago"
    except Exception as e:
        print(f"Error for {handle}: {e}")
        return "Error"


# === Solved in last 24 hours ===
def get_solved_last_24h(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] != 'OK':
            return "Invalid Handle"
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=24)
        solved_24h = set()
        for sub in data['result']:
            if sub.get("verdict") == "OK":
                created_at = datetime.utcfromtimestamp(sub['creationTimeSeconds'])
                if created_at >= cutoff:
                    prob_id = f"{sub['problem']['contestId']}-{sub['problem']['index']}"
                    solved_24h.add(prob_id)
        return len(solved_24h)
    except Exception as e:
        print(f"Error in 24h check for {handle}: {e}")
        return "Error"


# === Update only ===
def update_sheet(sheet):
    records = sheet.get_all_records()
    for i, row in enumerate(records, start=2):  # Skip header
        link = row.get("Codeforces Profile Link")
        handle = get_handle(link)

        if not handle:
            sheet.update_cell(i, 3, "Invalid Link")
            sheet.update_cell(i, 6, "")
            sheet.update_cell(i, 7, "")
            continue

        total = get_total_solved(handle)
        solved_24h = get_solved_last_24h(handle)
        last_online = get_last_online(handle)

        print(f"Row {i} | {handle}: Solved = {total}, Solved 24h = {solved_24h}, Last Online = {last_online}")

        sheet.update_cell(i, 3, total)         # Total Solved
        sheet.update_cell(i, 4, solved_24h)    # Solved in 24h
        sheet.update_cell(i, 5, last_online)   # Last Online
        sheet.update_cell(i, 6, handle)        # Handle

        time.sleep(1)  # Respect Codeforces API rate limit


# === Run ===
if __name__ == "__main__":
    sheet = connect_to_sheet("codeforces_students_updated")
    update_sheet(sheet)