from disnake.ext import commands
from disnake import Embed
import disnake


class HelperCog(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot


    @commands.slash_command(description="Show current bot ping")
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        latency = round(self.bot.latency * 1000)
        await inter.response.send_message(f"🏓 Ping: {latency} ms")


    @commands.slash_command(description="Lost?")
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        embed = Embed(
            title="Help Menu",
            description="Here are the commands you can use:",
            color=0xFFA500
        )
        embed.add_field(name="/ping 🏓", value="Show current bot ping", inline=False)
        embed.add_field(name="/help 👍", value="Show this help message", inline=False)
        embed.add_field(name="Create ... 🌄", value="Generate an image", inline=False)

        await inter.response.send_message(embed=embed)



def setup(bot: commands.InteractionBot):
    bot.add_cog(HelperCog(bot))
