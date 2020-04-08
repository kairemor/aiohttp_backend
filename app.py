from aiohttp import web
from covid import Covid
import aiohttp_cors
import os

covid = Covid()


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def get_data(request):
    data = covid.get_data()
    return web.json_response(data)


async def get_country(request):
    id = request.match_info.get('id', 147)
    country = covid.get_status_by_country_id(id)
    return web.json_response(country)


async def get_country_by_name(request):
    name = request.match_info.get('name', 'senegal')
    country = covid.get_status_by_country_name(name)
    country['recovery_rate'] = country['recovered'] / country['confirmed']
    country['death_rate'] = country['deaths'] / country['confirmed']
    # print(country)
    return web.json_response(country)


async def get_all_data(request):
    active = covid.get_total_active_cases()
    confirmed = covid.get_total_confirmed_cases()
    recovered = covid.get_total_recovered()
    deaths = covid.get_total_deaths()
    data = {'confirmed': str(confirmed),
            'death': str(deaths),
            'recovery': str(recovered),
            'active': str(active),
            'recovery_rate': str(recovered/confirmed),
            'death_rate': str(deaths/confirmed),
            }
    return web.json_response(data)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/country_data/all', get_data),
                web.get('/data/all', get_all_data),
                web.get('/country_data/country', get_country),
                web.get('/country_data/country/{id}', get_country),
                web.get('/country_data/country_name/', get_country_by_name),
                web.get(
                    '/country_data/country_name/{name}', get_country_by_name)
                ])
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

for route in list(app.router.routes()):
    cors.add(route)

if __name__ == '__main__':
    # web.run_app(app)
    web.run_app(app, port=os.getenv('PORT'))
