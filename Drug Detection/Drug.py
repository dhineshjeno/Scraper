from telethon.sync import TelegramClient

# Replace these with your own values
api_id = '19503222'
api_hash = 'c35294017da1c161cf62e9683a8b4f01'
phone_number = '8838278976'

# Create a new Telegram client session
client = TelegramClient('Drugdetection', api_id, api_hash)

async def main():
    # Make sure you're authorized
    await client.start(phone=phone_number)

    # Specify the group or channel you want to monitor
    group_name = 'Gamer'

    async for message in client.iter_messages(group_name):
        if any(keyword in message.message for keyword in drug_keywords):
            sender = await message.get_sender()
            print(f"Drug-related message found: {message.message} by {sender.username}")
            save_message(message.message, sender.username)

with client:
    client.loop.run_until_complete(main())