import pandas as pd
import base64
from datetime import datetime, timedelta

# Fungsi untuk decode base64 ke hex
def base64_to_hex(b64_str):
    decoded_bytes = base64.b64decode(b64_str)
    return decoded_bytes.hex()

# Fungsi untuk mengkonversi hex ke timestamp UTC+7
def hex_to_timestamp(hex_str, start_index):
    try:
        # Mengambil karakter hex dari start_index hingga start_index+8
        hex_timestamp = hex_str[start_index:start_index+8]
        if len(hex_timestamp) < 8:
            raise ValueError("Hex string too short")
        # Mengkonversi hex ke integer
        timestamp_int = int(hex_timestamp, 16)
        # Membuat datetime dari epoch
        timestamp_utc = datetime.utcfromtimestamp(timestamp_int)
        # Menyesuaikan ke UTC+7
        timestamp_utc7 = timestamp_utc + timedelta(hours=7)
        return timestamp_utc7
    except (ValueError, TypeError) as e:
        print(f"Error converting hex to timestamp: {e}")
        return None

# Membaca file CSV
df = pd.read_csv('messages.csv')

# Menambahkan kolom 'data_hex'
df['data_hex'] = df.iloc[:, 6].apply(base64_to_hex)

for i in range(8): # ganti jumlah frames
    df['timestamp' + str(i+1)] = df['data_hex'].apply(lambda x: hex_to_timestamp(x, ((i * 20) + 12)))

# Menyimpan kembali ke file CSV
df.to_csv('output\output_messages.csv', index=False)

print("Proses selesai. Data telah disimpan dalam 'output_file.csv'.")