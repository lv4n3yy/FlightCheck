import os
import time
import requests
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

my_email = os.getenv("my_email")
password = os.getenv("password")
def send_email(subject, body, my_email, password):
    smtp_server = "smtp.gmail.com"
    port = 587

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = my_email
    msg["To"] = my_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(my_email, password)
        server.sendmail(my_email, [my_email], msg.as_string())


load_dotenv(dotenv_path="./.env")

api = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
token = os.environ.get("token")
sht_api = os.environ.get("sht_api")

response = requests.get(sht_api)
radar_rows = response.json()["radar"]

cities_from = []
cities_to = []
dates = []
best_offer = []
current_link = []
all_params = []

for row in radar_rows:
    origin = row["from"]        # col A
    destination = row["to"]     # col B
    date = row["date"]          # col C (e.g. 2025-12-15)

    cities_from.append(origin)
    cities_to.append(destination)
    dates.append(date)

    best_price = row.get("bestPrice")
    best_offer.append(int(best_price) if best_price else 1_000_000)
    current_link.append(row.get("link", ""))

    all_params.append(
        {
            "origin": origin,
            "destination": destination,
            "departure_at": date,   # use date from sheet
            "token": token,
            "limit": "1",
            "currency": "eur",
        }
    )

print("Routes loaded from sheet:")
for o, d, dt in zip(cities_from, cities_to, dates):
    print(f"{o} -> {d} at {dt}")

while True:
    for i in range(len(all_params)):
        params = all_params[i]
        avia_response = requests.get(api, params=params)
        data = avia_response.json().get("data", [])

        if data:
            price = int(data[0]["price"])
            link = data[0]["link"]

            if price < best_offer[i]:
                best_offer[i] = price
                current_link[i] = link

                row_id = i + 2  # header is row 1

                price_payload = {"radar": {"bestPrice": best_offer[i]}}
                link_payload = {"radar": {"link": current_link[i]}}

                requests.put(f"{sht_api}/{row_id}", json=price_payload)
                requests.put(f"{sht_api}/{row_id}", json=link_payload)

                print(f"New best price {cities_from[i]} -> {cities_to[i]} {dates[i]}: {price} ({link})")
                subject = f"New best price {cities_from[i]} → {cities_to[i]} {dates[i]}"
                body = (
                    f"New price found:\n\n"
                    f"Route: {cities_from[i]} → {cities_to[i]}\n"
                    f"Date: {dates[i]}\n"
                    f"Price: {best_offer[i]} EUR\n"
                    f"Link: https://aviasales.ru{current_link[i]}"
                )
                send_email(subject, body, my_email, password)

        else:
            print(f"No flights found for {cities_from[i]} -> {cities_to[i]} {dates[i]}: {params}")

        time.sleep(1)

    print("Waiting 5 minutes before next check...")
    time.sleep(300)
