from AmberAI.const import SberSecretKey, SberKey, MNNKey, MNNId
from aiohttp import FormData
import asyncio
import base64
import json


class Kandinsky:
    def __init__(self, session):
        self.session = session
        self.URL = "https://api-key.fusionbrain.ai/"
        self.AUTH_HEADERS = {
            "X-Key": f"Key {SberKey}",
            "X-Secret": f"Secret {SberSecretKey}",
        }

    async def get_model(self):
        async with self.session.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS) as response:
            data = await response.json()
            return data[0]['id']

    async def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = FormData()
        data.add_field('model_id',
                       str(model),
                       content_type='text/plain')
        data.add_field('params',
                       json.dumps(params),
                       content_type='application/json')

        async with self.session.post(
                self.URL + 'key/api/v1/text2image/run',
                headers=self.AUTH_HEADERS,
                data=data
        ) as response:
            data = await response.json()
            return data['uuid']

    async def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            async with self.session.get(
                    self.URL + 'key/api/v1/text2image/status/' + request_id,
                    headers=self.AUTH_HEADERS
            ) as response:
                data = await response.json()
                if data['status'] == 'DONE':
                    return data['images']

            attempts -= 1
            await asyncio.sleep(delay)


class MNN:
    def __init__(self, messages, model, session):
        self.messages = messages
        self.model = model
        self.session = session

    async def generate(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": MNNKey,
            "Platform": "pc",
            "Id": MNNId
        }

        payload = {
            "model": self.model,
            "messages": self.messages,
            "temperature": 0.5,
            "stream": False
        }
        async with self.session.post(f"https://api.mnnai.ru/v1/chat/completion", headers=headers, json=payload) as response:
            result = await response.text()
            result = json.loads(result)
            if result["data"][0]["choices"][0]["text"]:
                return result["data"][0]["choices"][0]["text"]


async def GenerateImage(session, prompt):
    try:
        api = Kandinsky(session=session)

        model_id = await api.get_model()
        uuid = await api.generate(prompt, model_id)
        images = await api.check_generation(uuid)

        with open(f'AmberAI/Images/user.png', 'wb') as f:
            f.write(base64.b64decode(images[0]))

        return 'Ok'

    except Exception as e:
        print(f"Error during image generation: {e}")
