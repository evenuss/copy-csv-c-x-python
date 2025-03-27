import json
import csv
import random
import string
from datetime import datetime, timedelta

# Jumlah data yang ingin dibuat
NUM_ROWS = 1_000_000  # Ubah sesuai kebutuhan

# Nama file output
JSON_FILE = "dummy_data.json"
CSV_FILE = "dummy_data.csv"

# Fungsi membuat string random
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Fungsi membuat email acak
def random_email():
    return random_string(7) + "@example.com"

# Fungsi membuat tanggal acak
def random_date(start_date="2020-01-01", end_date="2025-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return start + timedelta(days=random.randint(0, (end - start).days))

# Fungsi membuat data dummy
def generate_data(num_rows):
    data = []
    for _ in range(num_rows):
        row = {
            "id": _ + 1,
            "name": random_string(12),
            "email": random_email(),
            "created_at": random_date().strftime("%Y-%m-%d %H:%M:%S"),
            "price": round(random.uniform(10, 1000), 2),
            "status": random.choice(["active", "inactive", "pending"]),
            "description": random_string(50)
        }
        data.append(row)
    return data

# Generate data
dummy_data = generate_data(NUM_ROWS)

# Simpan ke JSON
with open(JSON_FILE, "w") as f:
    json.dump(dummy_data, f, indent=2)

# Simpan ke CSV
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=dummy_data[0].keys())
    writer.writeheader()
    writer.writerows(dummy_data)

print(f"✅ Data berhasil dibuat! {NUM_ROWS} rows -> {JSON_FILE}, {CSV_FILE}")
