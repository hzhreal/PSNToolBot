import aiohttp
import json
import re
import discord
from dotenv import load_dotenv
import os
load_dotenv()
discordlink = "https://discord.gg/fHfmjaCXtb"

class PSNTool:
    def __init__(self):
        pass

    NPSSO = str(os.getenv("NPSSO"))

    @staticmethod
    async def add_to_cart(ctx, sku_id: str, token: str, selected_region: str) -> None:
        if sku_id.count("-") == 2 and token != "" and len(selected_region) == 5:
            sku_get = await PSNTool.check_avatar(ctx, sku_id, token, selected_region, True)

            psheaders = {
                "Origin": "https://checkout.playstation.com",
                "content-type": "application/json",
                "Accept-Language": f"{selected_region}",
                "Cookie": f"AKA_A2=A; pdccws_p={token}; isSignedIn=true; userinfo={PSNTool.NPSSO}; p=0; gpdcTg=%5B1%5D"
            }

            psdata = {
                "operationName": "addToCart",
                "variables": {
                    "skus": [{"skuId": sku_get}]
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "93eb198753e06cba3a30ed3a6cd3abc1f1214c11031ffc5b0a5ca6d08c77061f"
                    }
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post("https://web.np.playstation.com/api/graphql/v1/op", headers=psheaders, json=psdata) as response:
                    response.text = await response.text()

            if "subTotalPrice" in response.text:
                embed_success = discord.Embed(title="Success", description=f"{sku_id} has been added to your cart.", color=discord.Color.blue())
                embed_success.set_footer(text=f"Made by: hzh.\n{discordlink}")
                await ctx.respond(embed=embed_success, ephemeral=True)
            else:
                embed_error = discord.Embed(title="Error", description="Can not add to cart.", color=discord.Color.red())
                embed_error.set_footer(text=f"Made by: hzh.\n{discordlink}")
                await ctx.respond(embed=embed_error, ephemeral=True)
                return
        else:
            embed_error1 = discord.Embed(title="Error", description="ID, token, or region is invalid.", color=discord.Color.red())
            embed_error1.set_footer(text=f"Made by: hzh.\n{discordlink}")
            await ctx.respond(embed=embed_error1, ephemeral=True)
            return

    @staticmethod
    async def check_avatar(ctx, sku_id: str, token: str, selected_region: str, obtainonly: bool) -> str | None:

        if sku_id.count("-") == 2 and token != "" and len(selected_region) == 5:

            regionURL = selected_region.replace("-", "/")

            psheaders = {
                "Origin": "https://checkout.playstation.com",
                "content-type": "application/json",
                "Accept-Language": f"{selected_region}",
                "Cookie": f"AKA_A2=A; pdccws_p={token}; isSignedIn=true; userinfo={PSNTool.NPSSO}; p=0; gpdcTg=%5B1%5D"
            }

            url = f"https://store.playstation.com/store/api/chihiro/00_09_000/container/{regionURL}/19/{sku_id}/"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=psheaders) as response:
                    response.text = await response.text()

            sku_info = json.loads(response.text)
            sku_get = sku_info.get("default_sku", {}).get("id")

            if sku_get is None:
                embed_error2 = discord.Embed(title="Error", description="Can not obtain SkuID.", color=discord.Color.red())
                embed_error2.set_footer(text=f"Made by: hzh.\n{discordlink}")
                await ctx.respond(embed=embed_error2, ephemeral=True)
                return
            else:
                if obtainonly:
                    return sku_get
                else:
                    picture_avatar = f"https://store.playstation.com/store/api/chihiro/00_09_000/container/{regionURL}/19/{sku_id}/image"
                    embed_success1 = discord.Embed(title="Success", description="Found your avatar.", color=discord.Color.blue())
                    embed_success1.set_footer(text=f"Made by: hzh.\n{discordlink}")
                    embed_success1.set_image(url=picture_avatar)
                    await ctx.respond(embed=embed_success1, ephemeral=True)
                    return picture_avatar
               
        else:
            embed_error3 = discord.Embed(title="Error", description="ID, token, or region is invalid.", color=discord.Color.red())
            embed_error3.set_footer(text=f"Made by: hzh.\n{discordlink}")
            await ctx.respond(embed=embed_error3, ephemeral=True)
            return
    
    @staticmethod
    async def obtain_skuid(ctx, url: str) -> str | None:
        
        pattern = r'\d+'
        match = re.search(pattern, url)

        if match:
            psprices_value = match.group()
            url = f"https://psprices.com/game/buy/{psprices_value}"

            async with aiohttp.ClientSession() as session:
                response = await session.get(url, allow_redirects=True)

            url = response.url
            target_parameter = url.query

            # product_id = url.split("productId=")[1].split("&")[0]
            product_id = target_parameter.get("productId")
            embed_success2 = discord.Embed(title="Success", description=f"ProductID: {product_id}", color=discord.Color.blue())
            embed_success2.set_footer(text=f"Made by: hzh.\n{discordlink}")
            await ctx.respond(embed=embed_success2, ephemeral=True)
            return product_id

        else:
            print("NO MATCH: Could not obtain ID")
            embed_error4 = discord.Embed(title="Error", description="Could not obtain ID.", color=discord.Color.red())
            embed_error4.set_footer(text=f"Made by: hzh.\n{discordlink}")
            await ctx.respond(embed=embed_error4, ephemeral=True)
            return