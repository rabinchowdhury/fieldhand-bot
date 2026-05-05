import os
import discord
import json
import datetime
import asyncio
import random

# --- CONFIGURATION ---
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
FILE_NAME = "discord_questions.json"

async def send_question():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            try:
                # Open the JSON file containing your 262 questions
                with open(FILE_NAME, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get("questions", [])

                if questions:
                    # 1. Get the current date as a string (e.g., "2026-05-05")
                    # Using UTC ensures consistency regardless of where GitHub's servers are
                    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
                    
                    # 2. Use that date string as a "seed"[cite: 2]
                    # This trick ensures that 'random.choice' picks the SAME question 
                    # every time it runs today, but a DIFFERENT one tomorrow[cite: 2]
                    random.seed(today_str)
                    selected_item = random.choice(questions)
                    selected_question = selected_item["text"]

                    embed = discord.Embed(
                        title="Fieldhand's Daily Question",
                        description=selected_question,
                        color=discord.Color.green()
                    )
                    await channel.send(embed=embed)
                    print(f"Successfully posted for {today_str}: {selected_question}")
            except Exception as e:
                print(f"Error: {e}")
        
        await client.close()

    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(send_question())