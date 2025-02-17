from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Path to your ChromeDriver
driver_path = 'C:\Users\Raj Narayanan\Downloads\chromedriver-win64'  # Adjust this path

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Optional: Start Chrome maximized

# Initialize the Chrome driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://web.whatsapp.com')

# Wait for manual QR code scan
input("Press Enter after scanning QR code...")

# Define keywords related to drugs
keywords = ['MDMA', 'LSD', 'cocaine']

def scrape_chat():
    messages = driver.find_elements(By.CSS_SELECTOR, "span._1Gy50")
    for message in messages:
        text = message.text
        if any(keyword.lower() in text.lower() for keyword in keywords):
            print(f"Detected Message: {text}")

scrape_chat()
driver.quit()
