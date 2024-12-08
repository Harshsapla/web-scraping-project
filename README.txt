# Real-Time Stock Price Monitoring System

## Overview:
This Python script monitors real-time stock prices of multiple stocks during market hours (9:00 AM to 3:30 PM Korean time) by scraping data from a website. It sends notifications via email and text-to-speech (TTS) when there are significant changes in stock prices or group averages. The data is also saved to an Excel file for further analysis.

## Features:
- Scrapes stock prices from a list of URLs.
- Monitors stock prices during market hours.
- Sends email alerts for significant price changes.
- Provides TTS notifications for price changes.
- Saves stock price data to an Excel file.
- Headless browser mode for efficient scraping.

## Python Code Details:
1. **Libraries Used:**
   - `time`: For controlling the time intervals between price checks.
   - `pandas`: For saving the data to an Excel file.
   - `smtplib`: For sending email notifications.
   - `pyttsx3`: For text-to-speech notifications.
   - `selenium`: For web scraping the stock prices.
   - `webdriver_manager`: For automatically managing the ChromeDriver.
   - `datetime`: For time-based functions and managing market hours.

2. **Main Functionality:**
   - **Stock URL Groups:** The script monitors stock prices for different groups of stocks, where each group contains multiple stock URLs.
   - **Fetching Stock Prices:** The `fetch_stock_price` function uses Selenium to load the page and extract the stock price.
   - **Price Change Alerts:** If the stock price changes by a certain percentage compared to the previous value, an email and TTS notification are triggered.
   - **Market Hours Check:** The script only runs during Korean market hours (9:00 AM to 3:30 PM) using the `is_market_open` function.
   - **Email Notifications:** The `send_email_notification` function sends email alerts when stock prices or group averages change significantly.
   - **Text-to-Speech Notifications:** The `tts_notification` function uses pyttsx3 to announce price changes audibly.

3. **Steps in the Code:**
   - The script initializes the Chrome driver in headless mode.
   - It defines stock groups with their corresponding URLs.
   - The script continuously fetches stock prices during market hours and checks if the price change exceeds a threshold.
   - If a significant price change is detected, an email is sent, and a TTS message is played.
   - The stock price data is saved in an Excel file (`real_time_stock_prices.xlsx`).

4. **Important Functions:**
   - **fetch_stock_price(url):** Fetches the stock price from the given URL using Selenium.
   - **is_market_open():** Checks if the current time is within market hours.
   - **send_email_notification(subject, body, recipient_email, sender_email, sender_password):** Sends an email notification.
   - **tts_notification(message):** Plays a text-to-speech message.
   - **monitor_prices(interval=10, price_change_threshold=2, group_avg_change_threshold=3):** Monitors stock prices, detects significant changes, and saves data to an Excel file.

## Requirements:
Before running the script, make sure the following Python packages are installed:
- selenium
- pandas
- pyttsx3
- smtplib
- webdriver_manager

You can install the required packages using pip:

## Usage:
1. Replace `recipient@example.com`, `your_email@gmail.com`, and `your_password` in the code with your email details.
2. Run the script. It will start monitoring stock prices and send alerts when there are significant changes.
3. The script checks for stock prices every 10 seconds (you can adjust the interval by changing the `interval` parameter in the `monitor_prices` function).
4. The data will be saved in `real_time_stock_prices.xlsx`.

## How it Works:
1. **Fetching Stock Prices:**
   The script uses Selenium to scrape stock prices from the provided URLs. It waits until the price element is visible on the page.

2. **Price Change Detection:**
   The script calculates if there’s a significant price change (greater than the specified threshold) and sends email and TTS notifications.

3. **Market Hours Check:**
   The script runs only during market hours (9:00 AM to 3:30 PM Korean time) and stops when the market is closed.

4. **Saving Data:**
   The stock data is continuously saved to `real_time_stock_prices.xlsx`.
