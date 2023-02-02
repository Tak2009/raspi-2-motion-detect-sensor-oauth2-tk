import aiohttp
import asyncio
import json
import datetime
import credentials as cred

async def main():

    async with aiohttp.ClientSession() as session:
        
        url = 'https://tak2009.pythonanywhere.com/api/v1/auth/login/'
        payload = {"username": cred.USER, "password": cred.PW}
        headers = {'Content-Type': 'application/json'}

        async with session.post(url, data=json.dumps(payload), headers=headers) as resp: ## don't forget to convert the payload into json
            json_data = await resp.json()
            print(json_data)
            
            pic_post_headers={'Content-Type': 'application/json',
                     "Authorization": "Token " + json_data['token']}
            pics_url = 'https://tak2009.pythonanywhere.com/api/v1/pics/pics/'
            payload = {"title": 'Motion Detected at ' + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '!! Evidence pic is under review',
                       "created_by": 15
                       }
            async with session.post(pics_url, data=json.dumps(payload), headers=pic_post_headers) as resp: ## don't forget to convert the payload into json
                pic = await resp.json()
                print(pic)
                
                # 
                # pic_post_headers={#'Content-Type': 'image/jpg',
                #                     'Content-Type': 'application/json',
                #                     "Authorization": "Token " + json_data['token']}
                # pic_url = 'https://tak2009.pythonanywhere.com/api/v1/pics/pics/' + str(pic['id']) + '/'
                # print(pic_url)
                # payload = {'pic': open('/home/pi/Python/raspi-2-motion-detect-sensor-oauth2-tk/static/photo/img_2022-12-06_09-43-40.jpg', 'rb')}
                # async with session.patch(pic_url, data=payload, headers=pic_post_headers) as resp: ## don't do json.dumps
                #     pic = await resp.json()
                #     print(pic)

## reference

## https://docs.aiohttp.org/en/stable/client_advanced.html
## https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession
## https://programtalk.com/python-examples/aiohttp.ClientSession/
