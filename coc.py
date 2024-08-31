import asyncio
import coc

from dotenv import load_dotenv
import os

from main import playerTag

load_dotenv()

cocToken = (os.getenv('cocBotToken'))

'''
async def main():
    async with coc.Client() as coc_client:
        try:
            await coc_client.login("email", "password")
        except coc.InvalidCredentials as error:
            exit(error)

        player = await coc_client.get_player("tag")
        print(f"{player.name} has {player.trophies} trophies!")

        clans = await coc_client.search_clans(name="best clan ever", limit=5)
        for clan in clans:
            print(f"{clan.name} ({clan.tag}) has {clan.member_count} members")

        try:
            war = await coc_client.get_current_war("#clantag")
            print(f"{war.clan_tag} is currently in {war.state} state.")
        except coc.privatewarlog:
            print("uh oh, they have a private war log!")
'''

async def main():
    async with coc.Client() as coc_client:
        try:
            await coc_client.login_with_tokens(cocToken)
        except coc.InvalidCredentials as error:
            exit(error)
        
        player = await coc_client.get_player(playerTag)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass