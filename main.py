import discord
from discord.ext import commands
from tool import PSNTool, ToolError
import aiohttp
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()

NPSSO = os.getenv("NPSSO")

if NPSSO is not None:
    from psnawp_api import PSNAWP
    NPSSO = str(os.getenv("NPSSO"))
    psnawp = PSNAWP(NPSSO)
    print("psnawp initialized")

valid_regions = ["ar-AE", "ar-BH", "ar-KW", "ar-LB", "ar-OM", "ar-QA", "ar-SA", "ch-HK", "ch-TW", "cs-CZ",
                 "da-DK", "de-AT", "de-CH", "de-DE", "de-LU", "el-GR", "en-AE", "en-AR", "en-AU", "en-BG", 
                 "en-BH", "en-BR", "en-CA", "en-CL", "en-CO", "en-CR", "en-CY", "en-CZ", "en-DK", "en-EC", 
                 "en-ES", "en-FI", "en-GB", "en-GR", "en-HK", "en-HR", "en-HU", "en-ID", "en-IL", "en-IN", 
                 "en-IS", "en-KW", "en-LB", "en-MT", "en-MX", "en-MY", "en-NO", "en-NZ", "en-OM", "en-PA", 
                 "en-PE", "en-PL", "en-QA", "en-RO", "en-SA", "en-SE", "en-SG", "en-SI", "en-SK", "en-TH", 
                 "en-TR", "en-TW", "en-US", "en-ZA", "es-AR", "es-BR", "es-CL", "es-CO", "es-CR", "es-EC", 
                 "es-ES", "es-GT", "es-HN", "es-MX", "es-PA", "es-PE", "es-PY", "es-SV", "fi-FI", "fr-BE", 
                 "fr-CA", "fr-CH", "fr-FR", "fr-LU", "hu-HU", "id-ID", "it-CH", "it-IT", "ja-JP", "ko-KR", 
                 "nl-BE", "nl-NL", "no-NO", "pl-PL", "pt-BR", "pt-PT", "ro-RO", "ru-RU", "ru-UA", "sv-SE", 
                 "th-TH", "tr-TR", "vi-VN", "zh-CN", "zh-HK", "zh-TW"]

valid_regionsShow = [valid_regions[i:i + 5] for i in range(0, len(valid_regions), 10)]
valid_regionsShow = '\n'.join([", ".join(sublist) for sublist in valid_regionsShow])

discordlink = "https://discord.gg/fHfmjaCXtb"

activity = discord.Activity(type=discord.ActivityType.watching, name="Avatars")

invalid_region = discord.Embed(title="Error", description=f"Invalid region, make sure you have the last two letters in uppercase. Here are all valid regions:\n{valid_regionsShow}", color=discord.Color.red())
invalid_region.set_footer(text=f"Made by: hzh.\n{discordlink}")

bot = commands.Bot(command_prefix="!", activity=activity)
@bot.event
async def on_ready() -> None:
    print(
        f"Bot is ready, invite link: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot"
    )

@bot.slash_command(description="Adds the avatar you input in your cart.")
async def add(ctx, token: str, id: str, region: str) -> None:
    await ctx.respond("Adding...", ephemeral=True)

    if region not in valid_regions:
        await ctx.respond(embed=invalid_region, ephemeral=True)
        return

    try:
        await PSNTool.add_to_cart(ctx, id, token, region)
    except ToolError as e:
        embed_error = discord.Embed(title="Error", description=e, color=discord.Color.red())
        embed_error.set_footer(text=f"Made by: hzh.\n{discordlink}")
        await ctx.respond(embed=embed_error, ephemeral=True)

@bot.slash_command(description="Checks an avatar for you.")
async def check(ctx, token: str, id: str, region: str) -> None:
    await ctx.respond("Checking...", ephemeral=True)

    if region not in valid_regions:
        await ctx.respond(embed=invalid_region, ephemeral=True)
        return
    
    try:
        await PSNTool.check_avatar(ctx, id, token, region, False)
    except ToolError as e:
        embed_error = discord.Embed(title="Error", description=e, color=discord.Color.red())
        embed_error.set_footer(text=f"Made by: hzh.\n{discordlink}")
        await ctx.respond(embed=embed_error, ephemeral=True)

@bot.slash_command(description="Grabs the product ID from a psprices url.")
async def obtain_id(ctx, url: str) -> None:
    await ctx.defer()

    try:
        await PSNTool.obtain_skuid(ctx, url)
    except ToolError as e:
        embed_error = discord.Embed(title="Error", description=e, color=discord.Color.red())
        embed_error.set_footer(text=f"Made by: hzh.\n{discordlink}")
        await ctx.respond(embed=embed_error)


@bot.slash_command(description="Pings the bot.")
async def ping(ctx) -> None:
    latency = bot.latency * 1000
    await ctx.respond(f"Pong! {latency: .2f}ms")

@bot.slash_command(description="Gets the account id from a psn username.")
async def obtain_accid(ctx, username: str) -> None:
    await ctx.defer()

    limit = 0
    usernamePattern = r"^[a-zA-Z0-9_-]+$"

    embnv1 = discord.Embed(title="Error: PS username not valid",
                      description="This PS username is not in a valid format.",
                      colour=0x854bf7)
    embnv1.set_thumbnail(url="https://cdn.discordapp.com/avatars/248104046924267531/743790a3f380feaf0b41dd8544255085.png?size=1024")
    embnv1.set_footer(text="Made with expertise by HTOP")

    if len(username) < 3 or len(username) > 16:
        await ctx.edit(embed=embnv1)
        return
    elif not bool(re.match(usernamePattern, username)):
        await ctx.edit(embed=embnv1)
        return
    
    if NPSSO is not None:
        try:
            user = psnawp.user(online_id=username)
            user_id = user.account_id
            user_id = hex(int(user_id)) # convert decimal to hex
            user_id = user_id[2:] # remove 0x
            user_id = user_id.zfill(16) # pad to 16 length with zeros
            embed_id = discord.Embed(title=username, description=f"ACCOUNT ID: **{user_id}**", color=discord.Color.blue())
            embed_id.set_footer(text=f"Made by: hzh.\n{discordlink}")
            await ctx.respond(embed=embed_id)
        except:
            iderror = discord.Embed(title="Error", 
                                        description=f"Can not obtain account id from {username}, do you have on the right privacy settings so that you can be found?",
                                        color=discord.Color.red())
            iderror.set_footer(text=f"Made by: hzh.\n{discordlink}")
            await ctx.respond(embed=iderror)
    
    else:
        while True:
        
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://psn.flipscreen.games/search.php?username={username}") as response:
                    response.text = await response.text()

            if response.status == 200 and limit != 20:
                data = json.loads(response.text)
                obtainedUsername = data["online_id"]
                if obtainedUsername.lower() == username.lower():
                    user_id = data["user_id"]
                    user_id = hex(int(user_id)) # convert decimal to hex
                    user_id = user_id[2:] # remove 0x
                    user_id = user_id.zfill(16) # pad to 16 length with zeros
                    embed_id = discord.Embed(title=username, description=f"ACCOUNT ID: **{user_id}**", color=discord.Color.blue())
                    embed_id.set_footer(text=f"Made by: hzh.\n{discordlink}")
                    await ctx.respond(embed=embed_id)
                    break
                else: 
                    limit += 1
            else:
                if limit == 20:
                    iderror1 = discord.Embed(title="Error", 
                                        description=f"Can not obtain account id from {username}, website does not give the right value back.",
                                        color=discord.Color.red())
                    iderror1.set_footer(text=f"Made by: hzh.\n{discordlink}")
                    await ctx.respond(embed=iderror1)
                    break

                else:
                    iderror = discord.Embed(title="Error", 
                                            description=f"Can not obtain account id from {username}, do you have on the right privacy settings so that you can be found?",
                                            color=discord.Color.red())
                    iderror.set_footer(text=f"Made by: hzh.\n{discordlink}")
                    await ctx.respond(embed=iderror)
                    break

bot.run(str(os.getenv("TOKEN"))) # token
