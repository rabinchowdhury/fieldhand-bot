import os
import discord
import json
import datetime
import asyncio

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
                with open(FILE_NAME, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    questions = data.get("questions", [])[cite: 1]

                if questions:
                    # Picks a question based on day of the year
                    day_of_year = datetime.datetime.now().timetuple().tm_yday
                    question_index = day_of_year % len(questions)
                    selected_question = questions[question_index]["text"][cite: 1]

                    embed = discord.Embed(
                        title="Fieldhand's Daily Question",
                        description=selected_question,
                        color=discord.Color.green()
                    )
                    await channel.send(embed=embed)
                    print(f"Successfully posted: {selected_question}")
            except Exception as e:
                print(f"Error: {e}")
        
        await client.close()

    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(send_question())