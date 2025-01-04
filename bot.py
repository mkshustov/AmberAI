from AmberAI.const import Token, Activity
from disnake.ext import commands
import disnake


intents = disnake.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('The bot is running!')
    await bot.change_presence(status=disnake.Status.idle, activity=disnake.Game(Activity))


bot.load_extension('AmberAI.Cogs.AiCog')
bot.load_extension('AmberAI.Cogs.HelperCog')


if __name__ == '__main__':
    bot.run(Token)