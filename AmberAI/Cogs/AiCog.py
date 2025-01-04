from AmberAI.const import ImageCommands, TextModel
from AmberAI.Ai import GenerateImage, MNN
from collections import defaultdict
from disnake.ext import commands
from disnake import File
import aiohttp
import disnake
import time

users_being_served = {}
user_message_history = defaultdict(list)


async def process_image_request(session, inter, content):
    start_time = time.time()
    embed = disnake.Embed(title="Generating...", color=0x3498db)
    gen_msg = await inter.channel.send(embed=embed)

    image = await GenerateImage(session, content)

    generation_time = time.time() - start_time

    embed = disnake.Embed(title=f"Your request:", description=f"{content} \n \n **Time**: {generation_time:.2f} секунд",
                          color=0x3498db)

    if image:
        file = File("AmberAI/Images/user.png", filename="user.png")
        embed.set_image(url="attachment://user.png")
    else:
        file = File("AmberAI/Images/error.png", filename="error.png")
        embed.set_image(url="attachment://error.png")

    embed.set_footer(text="Made with AmberAi and Kandinsky 3.1")

    await inter.channel.send(embed=embed, file=file)
    await gen_msg.delete()


async def process_text_request(session, inter, content_message, message_history):
    try:
        chat_history = [
            {"role": "user", "content": msg["content"]}
            for msg in message_history
        ]
        chat_history.append({"role": "user", "content": content_message})

        async with inter.channel.typing():
            message = await MNN(session=session, model=TextModel, messages=chat_history).generate()
            message = message.replace('\\n', '\n')

            if len(message) <= 2000:
                await inter.channel.send(message)
            else:
                l = len(message) + 1
                part_1 = message[:l // 2]
                part_2 = message[l // 2:]
                await inter.channel.send(part_1)
                await inter.channel.send(part_2)

    except Exception as e:
        return f"Что-то сломалось: {e}"


class AiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands = ImageCommands
        self.session = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self.session:
            await self.session.close()

    @commands.Cog.listener()
    async def on_message(self, inter):
        if inter.author == self.bot.user:
            return

        if inter.author.id in users_being_served:
            return

        users_being_served[inter.author.id] = True

        content = inter.content.lower()
        bot_mention = f"<@{self.bot.user.id}>"

        try:
            if inter.author.id not in user_message_history:
                user_message_history[inter.author.id] = []

            user_message_history[inter.author.id].append({
                "content": content
            })
            user_message_history[inter.author.id] = user_message_history[inter.author.id][-5:]

            if inter.guild:
                content_message = content.replace(bot_mention, "").strip()
                if self.bot.user in inter.mentions and any(
                        content.startswith(f"{bot_mention} {cmd}") for cmd in self.commands):
                    await process_image_request(self.session, inter, content_message)
                else:
                    if content.startswith(bot_mention):
                        await process_text_request(
                            self.session,
                            inter,
                            content_message,
                            user_message_history[inter.author.id]
                        )
            else:
                if any(content.startswith(cmd) for cmd in self.commands):
                    await process_image_request(self.session, inter, content)
                else:
                    await process_text_request(
                        self.session,
                        inter,
                        content,
                        user_message_history[inter.author.id]
                    )
        finally:
            del users_being_served[inter.author.id]


        await self.bot.process_commands(inter)


def setup(bot):
    bot.add_cog(AiCog(bot))