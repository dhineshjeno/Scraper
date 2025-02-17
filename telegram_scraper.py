from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
import tkinter as tk
from tkinter import scrolledtext

api_id = 19503222  # Ensure this is an integer
api_hash = 'c35294017da1c161cf62e9683a8b4f01'
session_name = 'my_session'

client = TelegramClient(session_name, api_id, api_hash)

keywords = ['MDMA', 'LSD', 'cocaine', 'buy drugs', 'drug sale', 'kolamaavu']

def start_scraping():
    channel_name = entry.get()
    text_area.insert(tk.END, f"Scraping started for {channel_name}\n")
    client.loop.run_until_complete(scrape_channel(channel_name))

async def scrape_channel(channel_name):
    await client.start()
    try:
        channel = await client.get_entity(channel_name)
        found = False
        async for message in client.iter_messages(channel):
            if message.text and any(keyword.lower() in message.text.lower() for keyword in keywords):
                text_area.insert(tk.END, f"Detected: {message.text} by user {message.sender_id}\n")
                found = True
        if not found:
            text_area.insert(tk.END, f"No drug-related keywords found in {channel_name}\n")
    except Exception as e:
        error_message = str(e)
        if "Cannot find any entity" in error_message:
            text_area.insert(tk.END, f"Cannot find any entity corresponding to '{channel_name}'\n")
        else:
            text_area.insert(tk.END, f"Error: {error_message}\n")

# Create GUI
root = tk.Tk()
root.title("Telegram Scraper")

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Enter Channel Name:")
label.pack(side=tk.LEFT)

entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, padx=5)

button = tk.Button(frame, text="Start", command=start_scraping)
button.pack(side=tk.LEFT)

text_area = scrolledtext.ScrolledText(root, width=80, height=20)
text_area.pack(pady=10)

root.mainloop()
