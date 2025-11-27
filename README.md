# Flight Price Watcher

A small Python script that watches flight prices for multiple routes defined in a Google Sheet (via Sheety), updates the sheet with the best price and booking link, and sends an email notification when a new lowest price is found.

## Features

- Reads routes and dates from a Google Sheet: `From`, `To`, `Date`, `Best price`, `Link`.
- Uses the Travelpayouts Aviasales API to fetch the cheapest ticket for each route and date.
- Writes the current best price and deeplink back into the sheet via Sheety.
- Sends an email via Gmail SMTP when a new best price is detected.

## Requirements

- Python 3.10+
- A Travelpayouts API token
- A Sheety API endpoint for your Google Sheet
- A Gmail account with an **App Password** enabled (2FA required)

## Setup

1. **Clone the repo**


2. **Create and activate a virtual environment (optional but recommended)**


3. **Install dependencies**


4. **Create a `.env` file**

Create a `.env` file in the project root (same folder as `main.py`):


The `.env` file is **not** committed to git (see `.gitignore`).

5. **Configure Google Sheet / Sheety**

Your sheet should have columns like:

| From | To  | Date       | Best price | Link |
|------|-----|-----------|-----------|------|
| BER  | LHR | 2025-12-15 |           |      |

Point your Sheety project to this sheet and use the `/flightRadar/radar` endpoint in `sht_api`.

## Usage

Run the watcher:

