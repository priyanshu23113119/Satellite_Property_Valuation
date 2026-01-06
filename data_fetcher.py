# download train images 
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

import pandas as pd
import os
from time import sleep

# ================= CONFIG =================
MAPBOX_TOKEN = "pk.eyJ1IjoiYW1hbi1zZHMiLCJhIjoiY21qYjRmZGJ1MDZiMDNlcXU5MHBtcm5ldSJ9.mQwuKyjiomJFuHAi-vmk4g"   # <-- apna token yahin daalo
ZOOM = 18
IMG_SIZE = "256x256"
STYLE = "mapbox/satellite-v9"

DATA_PATH = "/Users/prashantmaurya/Desktop/Satellite_Property_Valuation/data/clean_train.csv"
SAVE_DIR = "data/images/train"

# =========================================

# folder ensure
os.makedirs(SAVE_DIR, exist_ok=True)

# data load
df = pd.read_csv(DATA_PATH)

print("Total properties:", len(df))

for i, row in df.iterrows():
    lat = row["lat"]
    lon = row["long"]
    pid = row["id"]

    img_path = f"{SAVE_DIR}/{pid}.jpg"

    # agar image pehle se hai, skip
    if os.path.exists(img_path):
        continue

    url = (
        f"https://api.mapbox.com/styles/v1/{STYLE}/static/"
        f"{lon},{lat},{ZOOM}/{IMG_SIZE}"
        f"?access_token={MAPBOX_TOKEN}"
    )

    try:
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content))
        img.save(img_path)

        if i % 100 == 0:
            print(f"{i} images downloaded...")

        sleep(0.15)  # rate-limit safe

    except Exception as e:
        print(f"Failed for ID {pid}")

print("✅ All images downloaded")

# just check all images are properly download or not


df = pd.read_csv("/Users/prashantmaurya/Desktop/Satellite_Property_Valuation/data/clean_train.csv")

img_dir = "data/images/train"

available_ids = set(
    int(fname.split(".")[0])
    for fname in os.listdir(img_dir)
    if fname.endswith(".jpg")
)

df_img = df[df["id"].isin(available_ids)]

print("Total rows in dataset :", len(df))
print("Rows with images     :", len(df_img))
