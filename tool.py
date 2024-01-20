import aiohttp
import json
import re
import discord
from dotenv import load_dotenv
import os

load_dotenv()
discordlink = "https://discord.gg/fHfmjaCXtb"

class ToolError(Exception):
    pass 

class PSNTool:
    NPSSO = str(os.getenv("NPSSO"))

    @staticmethod
    async def add_to_cart(ctx, sku_id: str, token: str, selected_region: str) -> None:
        if sku_id.count("-") == 2:
            sku_get = await PSNTool.check_avatar(ctx, sku_id, token, selected_region, True)
            URL = "https://web.np.playstation.com/api/graphql/v1/op"
    
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
                async with session.post(URL, headers=psheaders, json=psdata) as response:
                    response.text = await response.text()

            if "subTotalPrice" in response.text:
                embed_success = discord.Embed(title="Success", description=f"{sku_id} has been added to your cart.", color=discord.Color.blue())
                embed_success.set_footer(text=f"Made by: hzh.\n{discordlink}")
                await ctx.respond(embed=embed_success, ephemeral=True)

            elif "Access denied! You need to be authorized to perform this action!" in response.text:
                raise ToolError("Are you sure that the token is invalid? Make sure your session is not expired.")

            elif "skuAlreadyInCart" in response.text:
                raise ToolError("SKU is already in the cart.")
            
            else:
                raise ToolError("Cannot add to cart.")
        else:
           raise ToolError("ID or token is invalid.")

    @staticmethod
    async def check_avatar(ctx, sku_id: str, token: str, selected_region: str, obtainonly: bool) -> str | None:
        if sku_id.count("-") == 2:
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
                raise ToolError("Can not obtain SkuID.")
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
            raise ToolError("ID or token is invalid.")
    
    @staticmethod
    async def obtain_skuid(ctx, url: str) -> str | None:
        pattern = r"\d+"
        match = re.search(pattern, url)

        if match:
            HEADERS = {"User-Agent": 
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            
            psprices_value = match.group()
            url = f"https://psprices.com/game/buy/{psprices_value}"

            async with aiohttp.ClientSession() as session:
                response = await session.get(url, allow_redirects=True, headers=HEADERS)

            url = response.url
            target_parameter = url.query

            # product_id = url.split("productId=")[1].split("&")[0]
            product_id = target_parameter.get("productId")
            embed_success2 = discord.Embed(title="Success", description=f"ProductID: {product_id}", color=discord.Color.blue())
            embed_success2.set_footer(text=f"Made by: hzh.\n{discordlink}")
            await ctx.respond(embed=embed_success2)
            return product_id

        else:
            raise ToolError("Could not obtain ID.")
