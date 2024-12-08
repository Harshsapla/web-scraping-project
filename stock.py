import time
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Initialize Chrome options
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode (without UI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_argument("--disable-software-rasterizer")
options.add_argument("--remote-debugging-port=9222")  # Set debugging port
options.add_argument("--disable-extensions")
options.add_argument("--disable-features=VizDisplayCompositor")  # Disable some GPU features

# Set up the Chrome driver with webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the stock URLs and their corresponding group
stock_groups = {
    1: [
        "https://alphasquare.co.kr/home/stock-information?code=041440",
        "https://alphasquare.co.kr/home/stock-information?code=000490"
    ],
    2: [
        "https://alphasquare.co.kr/home/stock-information?code=460930",
        "https://alphasquare.co.kr/home/stock-information?code=042660"
    ]
}

# Function to fetch stock price from the given URL
def fetch_stock_price(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#stock-nav__stock-info-container > div.main-stock-info.price-color > h2"))
        )
        price_element = driver.find_element(By.CSS_SELECTOR, "#stock-nav__stock-info-container > div.main-stock-info.price-color > h2")
        price = price_element.text.replace(',', '')  # Remove commas for calculation
        return float(price) if price.replace('.', '', 1).isdigit() else None
    except Exception as e:
        print(f"Error fetching stock price from {url}: {e}")
        return None

# Function to check if the market is open (9:00 AM to 3:30 PM Korean time)
def is_market_open():
    now = datetime.now()
    market_open = now.replace(hour=9, minute=0, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    return market_open <= now <= market_close

# Function to send email notifications
def send_email_notification(subject, body, recipient_email, sender_email, sender_password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function for text-to-speech notification
def tts_notification(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# Function to monitor prices during market hours
def monitor_prices(interval=10, price_change_threshold=2, group_avg_change_threshold=3):
    if not is_market_open():
        print("Market is currently closed. Please run the program during market hours (9:00 AM to 3:30 PM Korean time).")
        return

    print("Market is open. Starting price monitoring...")
    stock_data = []
    prev_prices = {group: [None] * len(urls) for group, urls in stock_groups.items()}
    prev_group_averages = {group: None for group in stock_groups}

    while is_market_open():
        print(f"\nFetching prices at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Fetch prices and calculate group averages
        for group, urls in stock_groups.items():
            print(f"Fetching prices for Group {group}:")
            prices = []
            for i, url in enumerate(urls):
                price = fetch_stock_price(url)
                if price:
                    print(f"  - Stock {i + 1} price: {price}")
                    prices.append(price)
                    last_price = prev_prices[group][i]
                    if last_price and abs(price - last_price) / last_price * 100 > price_change_threshold:
                        print(f"  [Alert] Significant price change for Group {group}, Stock {i + 1}: {price}")
                        send_email_notification(
                            f"Stock Price Alert: Group {group}, Stock {i + 1}",
                            f"Stock price changed significantly to {price}",
                            "recipient@example.com", "your_email@gmail.com", "your_password"
                        )
                        tts_notification(f"Significant price change for Group {group}, Stock {i + 1}")
                    prev_prices[group][i] = price

            if prices:
                avg_price = sum(prices) / len(prices)
                print(f"  - Group {group} Average Price: {avg_price}")
                if prev_group_averages[group] and abs(avg_price - prev_group_averages[group]) / prev_group_averages[group] * 100 > group_avg_change_threshold:
                    print(f"  [Alert] Significant group average price change for Group {group}: {avg_price}")
                    send_email_notification(
                        f"Group Average Price Alert: Group {group}",
                        f"Group average price changed significantly to {avg_price}",
                        "recipient@example.com", "your_email@gmail.com", "your_password"
                    )
                    tts_notification(f"Significant group average price change for Group {group}")
                prev_group_averages[group] = avg_price
                stock_data.append({
                    "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "Group": group,
                    "Average Price": avg_price
                })

        # Save to Excel
        df = pd.DataFrame(stock_data)
        df.to_excel("real_time_stock_prices.xlsx", index=False)

        time.sleep(interval)

    print("Market is closed. Monitoring stopped.")

# Start monitoring
monitor_prices(interval=10)

# Close the driver
driver.quit()
