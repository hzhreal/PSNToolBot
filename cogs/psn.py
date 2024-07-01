import discord
import os
from discord.ext import commands
from discord import Option
from api.common import APIError
from api.psn import PSN, PSNRequest

valid_regions = [
    "ar-AE", "ar-BH", "ar-KW", "ar-LB", "ar-OM", "ar-QA", "ar-SA", "ch-HK", "ch-TW", "cs-CZ",
    "da-DK", "de-AT", "de-CH", "de-DE", "de-LU", "el-GR", "en-AE", "en-AR", "en-AU", "en-BG", 
    "en-BH", "en-BR", "en-CA", "en-CL", "en-CO", "en-CR", "en-CY", "en-CZ", "en-DK", "en-EC", 
    "en-ES", "en-FI", "en-GB", "en-GR", "en-HK", "en-HR", "en-HU", "en-ID", "en-IL", "en-IN", 
    "en-IS", "en-KW", "en-LB", "en-MT", "en-MX", "en-MY", "en-NO", "en-NZ", "en-OM", "en-PA", 
    "en-PE", "en-PL", "en-QA", "en-RO", "en-SA", "en-SE", "en-SG", "en-SI", "en-SK", "en-TH", 
    "en-TR", "en-TW", "en-US", "en-ZA", "es-AR", "es-BR", "es-CL", "es-CO", "es-CR", "es-EC", 
    "es-ES", "es-GT", "es-HN", "es-MX", "es-PA", "es-PE", "es-PY", "es-SV", "fi-FI", "fr-BE", 
    "fr-CA", "fr-CH", "fr-FR", "fr-LU", "hu-HU", "id-ID", "it-CH", "it-IT", "ja-JP", "ko-KR", 
    "nl-BE", "nl-NL", "no-NO", "pl-PL", "pt-BR", "pt-PT", "ro-RO", "ru-RU", "ru-UA", "sv-SE", 
    "th-TH", "tr-TR", "vi-VN", "zh-CN", "zh-HK", "zh-TW"
]
valid_regionsShow = [valid_regions[i:i + 5] for i in range(0, len(valid_regions), 10)]
valid_regionsShow = "\n".join([", ".join(sublist) for sublist in valid_regionsShow])
invalid_region = discord.Embed(
    title="Error", 
    description=f"Invalid region, make sure you have the last two letters in uppercase. Here are all valid regions:\n```{valid_regionsShow}```", 
    color=discord.Color.red()
)

token_desc = "pdccws_p cookie"
id_desc = "ID from psprices product_id command"
region_desc = "For example 'en-US', check 'playstation.com'"

class PSNCog(commands.Cog):
    def __init__(self, secret: str, bot: commands.Bot) -> None:
        self.bot = bot
        self.api = PSN(secret)

    psn_group = discord.SlashCommandGroup("psn")

    @psn_group.command(description="Checks an avatar for you.")
    async def check_avatar(
              self, 
              ctx: discord.ApplicationContext, 
              pdccws_p: Option(str, description=token_desc), # type: ignore
              product_id: Option(str, description=id_desc), # type: ignore
              region: Option(str, description=region_desc) # type: ignore
            ) -> None:
        
        await ctx.respond("Checking...", ephemeral=True)

        if region not in valid_regions:
            await ctx.respond(embed=invalid_region, ephemeral=True)
            return

        request = PSNRequest(
            pdccws_p=pdccws_p,
            region=region,
            product_id=product_id
        )

        try:
            avatar_url = await self.api.check_avatar(request)
        except APIError as e:
            embed_error = discord.Embed(
                title="Error", 
                description=e, 
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed_error, ephemeral=True)
            return

        embed_success = discord.Embed(
            title="Success",
            description="Found your avatar.",
            color=discord.Color.blue()
        )
        embed_success.set_image(url=avatar_url)
        await ctx.respond(embed=embed_success, ephemeral=True)

    @psn_group.command(description="Adds the avatar you input into your cart.")
    async def add_avatar(
              self, 
              ctx: discord.ApplicationContext, 
              pdccws_p: Option(str, description=token_desc), # type: ignore
              product_id: Option(str, description=id_desc), # type: ignore
              region: Option(str, description=region_desc) # type: ignore
            ) -> None:
        
        await ctx.respond("Adding...", ephemeral=True)

        if region not in valid_regions:
            await ctx.respond(embed=invalid_region, ephemeral=True)
            return
        
        request = PSNRequest(
            pdccws_p=pdccws_p,
            region=region,
            product_id=product_id
        )
        
        try:
            await self.api.add_to_cart(request)
        except APIError as e:
            embed_error = discord.Embed(
                title="Error", 
                description=e, 
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed_error, ephemeral=True)
            return

        embed_success = discord.Embed(
            title="Success",
            description=f"{product_id} added to cart.",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed_success, ephemeral=True)

    @psn_group.command(description="Removes the avatar you input from your cart.")
    async def remove_avatar(
              self, 
              ctx: discord.ApplicationContext, 
              pdccws_p: Option(str, description=token_desc), # type: ignore
              product_id: Option(str, description=id_desc), # type: ignore
              region: Option(str, description=region_desc) # type: ignore
            ) -> None:
        
        await ctx.respond("Removing...", ephemeral=True)

        if region not in valid_regions:
            await ctx.respond(embed=invalid_region, ephemeral=True)
            return
        
        request = PSNRequest(
            pdccws_p=pdccws_p,
            region=region,
            product_id=product_id
        )
        
        try:
            await self.api.remove_from_cart(request)
        except APIError as e:
            embed_error = discord.Embed(
                title="Error", 
                description=e, 
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed_error, ephemeral=True)
            return

        embed_success = discord.Embed(
            title="Success",
            description=f"{product_id} removed from cart.",
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed_success, ephemeral=True)

    @psn_group.command(description="Gets the account ID from a PSN username.")
    async def account_id(self, ctx: discord.ApplicationContext, username: str) -> None:
        await ctx.defer()
        
        try:
            accid = await self.api.obtain_account_id(username)
        except APIError as e:
            embed_error = discord.Embed(
                title="Error", 
                description=e, 
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed_error)
            return

        embed_success = discord.Embed(
            title=username,
            description=f"**{accid}**",
            color=discord.Color.blue()
        )  
        await ctx.respond(embed=embed_success)
    
def setup(bot: commands.Bot) -> None:
    bot.add_cog(PSNCog(os.getenv("NPSSO"), bot))