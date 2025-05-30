import pandas as pd
import requests
import time

# Load Excel file
file_path = "codeforces_students.xlsx"  # Change to your file name
df = pd.read_excel(file_path)
print("Available columns:", df.columns.tolist())

if 'Codeforces Profile Link' not in df.columns:
    raise Exception("Missing 'Codeforces Profile Link' column.")

def get_handle(link):
    if isinstance(link, str) and "codeforces.com/profile/" in link:
        return link.strip().split("/")[-1]
    return None

def get_total_solved(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['status'] != 'OK':
            return "Invalid Handle"
        solved = set()
        for sub in data['result']:
            if sub.get("verdict") == "OK":
                prob_id = f"{sub['problem']['contestId']}-{sub['problem']['index']}"
                solved.add(prob_id)
        return len(solved)
    except:
        return "Error"

# Process each row
solved_counts = []
for index, row in df.iterrows():
    link = row['Codeforces Profile Link']
    handle = get_handle(link)
    if not handle:
        solved_counts.append("Invalid Link")
    else:
        total = get_total_solved(handle)
        print(f"{handle}: {total}")
        solved_counts.append(total)
        time.sleep(1)  # Respect rate limits

# Add to new column
df["Total Solved Problems"] = solved_counts

# Save updated Excel file
output_file = "codeforces_students.xlsx"
df.to_excel(output_file, index=False)
print(f"Updated file saved as {output_file}")