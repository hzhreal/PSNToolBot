import discord
from discord.ext import commands

tutorialstring = (
    "**1**. First go to playstation.com\n"
    "**2**. When you have loaded check the link and you will see your region\n"
    "**3**. Now login to your account\n"
    "**4**. Go to inspect element and click '>>' at the top\n"
    "**5**. Click on the 'Application' option\n"
    "**6**. Navigate to cookies for playstation.com and look for the 'pdccws_p' cookie. That cookie is your token\n"
    "**7**. You will find the avatar id by using /obtain_id with the url to the avatar page on psprices\n"
)
tutorialemb = discord.Embed(
    title="**TUTORIAL**", 
    description=tutorialstring, 
    color=discord.Color.blue()
)

class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @discord.slash_command(description="Pings the bot.")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        latency = self.bot.latency * 1000
        await ctx.respond(f"Pong! {latency: .2f}ms")

    @discord.slash_command(description="Shows how to use the bot.")
    async def tutorial(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(embed=tutorialemb, ephemeral=True)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Misc(bot))