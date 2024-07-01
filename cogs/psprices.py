import discord
from discord import Option
from discord.ext import commands
from api.common import APIError
from api.psprices import PSPrices

class PSPricesCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    ps_prices_group = discord.SlashCommandGroup("psprices")

    @ps_prices_group.command(description="Grabs the product ID from a PSPrices URL.")
    async def product_id(
              self,
              ctx: discord.ApplicationContext, 
              url: Option(str, description="Link to psnprices avatar") # type: ignore
            ) -> None:
        
        await ctx.defer()

        try:
            api = PSPrices(url)
            product_id = await api.obtain_skuid()
        except APIError as e:
            embed_error = discord.Embed(
                title="Error", 
                description=e, 
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed_error)
            return

        embed_success = discord.Embed(
            title="Success",
            description=product_id,
            color=discord.Color.blue()
        )  
        await ctx.respond(embed=embed_success)
       

def setup(bot: commands.Bot) -> None:
    bot.add_cog(PSPricesCog(bot))