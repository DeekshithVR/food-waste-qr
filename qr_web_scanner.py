import streamlit as st
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import csv
import os
import numpy as np

st.title("📦 Food Inventory QR Scanner")
st.write("Upload a food item QR code and log it to your inventory.")

uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

def parse_qr_data(data):
    info = {}
    lines = data.strip().split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            info[key.strip()] = value.strip()
    return info

def save_to_csv(info, filename="inventory.csv"):
    fieldnames = ["Name", "Expiry", "Quantity", "Purchased"]
    file_exists = os.path.exists(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(info)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    codes = decode(img_cv)

    if codes:
        qr_data = codes[0].data.decode('utf-8')
        st.success("QR Code Scanned Successfully!")
        st.code(qr_data)

        parsed = parse_qr_data(qr_data)
        save_to_csv(parsed)

        st.success("📁 Data saved to inventory.csv")
        st.write("**Logged Info:**")
        st.json(parsed)
    else:
        st.error("Could not detect QR code. Try another image.")
