from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx

app = FastAPI()
API_KEY = '8bb9a681086c0e812e7c88e81a449b40'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

templates = Jinja2Templates(directory='templates')





@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/weather",  response_class=HTMLResponse)
async def get_weather_data(city:str, request: Request):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'country': data['sys']['country'],
                'city': data['name'],
                'temp': data['main']['temp'],
                'temp_max': data['main']['temp_max'],
                'temp_min': data['main']['temp_min'],
                'icon': data['weather'][0]['icon'],
                'description': data['weather'][0]['description'],
            }

            return templates.TemplateResponse('main.html', {'request': request, 'weather_data': weather_data})
        else:
            raise HTTPException(status_code=response.status_code, detail='City not found')
