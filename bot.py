import discord
from discord.ext import commands
import requests
from io import BytesIO

# Informações fornecidas pelo usuário
DISCORD_TOKEN = 'token'
RIOT_API_KEY = 'token'
CHANNEL_ID = coloqueoid  # Substitua pelo ID do canal onde a mensagem será enviada
 
# Configurações do cliente do Discord
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler o conteúdo das mensagens

bot = commands.Bot(command_prefix=".", intents=intents)

# Mapeamento de regiões para o endpoint correto da API da Riot
region_to_endpoint = {
    'na1': 'americas',
    'br1': 'americas',
    'euw1': 'europe',
    'eun1': 'europe',
    'jp1': 'asia',
    'kr': 'asia',
    'oc1': 'americas',
    'ru': 'europe',
    'tr1': 'europe',
    'la1': 'americas',
    'la2': 'americas'
}

# Função para obter PUUID a partir do Riot ID
def get_puuid(game_name, tag_line, endpoint):
    url = f'https://{endpoint}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
    headers = {
        'X-Riot-Token': RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['puuid']
    else:
        print(f'Error fetching PUUID: {response.status_code} - {response.text}')
        return None

# Função para verificar a conta de LoL usando PUUID
def check_lol_account(puuid, region):
    url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'
    headers = {
        'X-Riot-Token': RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f'Debug: Response data - {data}')  # Adiciona a resposta completa para depuração
        return data
    else:
        print(f'Error fetching data from Riot API: {response.status_code} - {response.text}')
        return None

# Função para obter as classificações do jogador
def get_ranked_stats(summoner_id, region):
    url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
    headers = {
        'X-Riot-Token': RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error fetching ranked stats: {response.status_code} - {response.text}')
        return None

# Função para obter os campeões mais jogados
def get_top_champions(puuid, region):
    url = f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}'
    headers = {
        'X-Riot-Token': RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[:3]  # Retorna os 3 campeões mais jogados
    else:
        print(f'Error fetching top champions: {response.status_code} - {response.text}')
        return None

# Função para carregar os dados dos campeões do Data Dragon
def load_champion_data():
    url = 'https://ddragon.leagueoflegends.com/cdn/14.12.1/data/en_US/champion.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {int(champion['key']): champion['name'] for champion in data['data'].values()}
    else:
        print(f'Error fetching champion data: {response.status_code} - {response.text}')
        return {}

# Função para baixar a imagem
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print(f'Error fetching image: {response.status_code} - {response.text}')
        return None

# Evento quando o bot está pronto
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send('Bot has started!')

# Evento de erro
@bot.event
async def on_command_error(ctx, error):
    print(f'Error: {error}')

# Comando para verificar a conta de LoL usando Riot ID
@bot.command(name='check')
async def check(ctx, *, name_tag_region: str):
    try:
        game_name, tag_line, region = name_tag_region.rsplit(' ', 2)
    except ValueError:
        await ctx.send("Formato inválido. Use: `<nome> <tag> <região>`")
        return

    endpoint = region_to_endpoint.get(region.lower())
    if not endpoint:
        await ctx.send(f'Região inválida: {region}')
        return

    puuid = get_puuid(game_name, tag_line, endpoint)
    if puuid:
        account_info = check_lol_account(puuid, region)
        if account_info:
            game_name_correct = account_info.get('name', game_name)
            profile_icon_id = account_info.get('profileIconId', 'N/A')
            summoner_level = account_info.get('summonerLevel', 'N/A')
            summoner_id = account_info.get('id', 'N/A')
            profile_icon_url = f'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{profile_icon_id}.jpg'
            profile_icon_image = download_image(profile_icon_url)

            # Carregar dados dos campeões
            champion_data = load_champion_data()

            # Obter as classificações do jogador
            ranked_stats = get_ranked_stats(summoner_id, region)
            solo_duo_rank = "Unranked"
            flex_rank = "Unranked"
            if ranked_stats:
                for queue in ranked_stats:
                    if queue['queueType'] == 'RANKED_SOLO_5x5':
                        solo_duo_rank = f"{queue['tier']} {queue['rank']} ({queue['leaguePoints']} LP)"
                    elif queue['queueType'] == 'RANKED_FLEX_SR':
                        flex_rank = f"{queue['tier']} {queue['rank']} ({queue['leaguePoints']} LP)"

            # Obter os campeões mais jogados
            top_champions = get_top_champions(puuid, region)
            top_champions_names = []
            if top_champions:
                for champion in top_champions:
                    champion_id = champion['championId']
                    champion_points = champion['championPoints']
                    champion_name = champion_data.get(champion_id, "Unknown")
                    top_champions_names.append(f"{champion_name} ({champion_points} points)")

            embed = discord.Embed(
                title=f"{game_name_correct}#{tag_line}",
                description=f"Summoner Level: {summoner_level}\n",
                color=discord.Color.blue()
            )

            files = []

            if profile_icon_image:
                profile_icon_file = discord.File(profile_icon_image, filename="profile_icon.jpg")
                embed.set_thumbnail(url="attachment://profile_icon.jpg")
                files.append(profile_icon_file)

            embed.add_field(name="Solo/Duo Rank", value=solo_duo_rank, inline=True)
            embed.add_field(name="Flex Rank", value=flex_rank, inline=True)

            if top_champions_names:
                champions_value = "\n".join(top_champions_names)
                embed.add_field(name="Top Champions", value=champions_value, inline=False)

            await ctx.send(files=files, embed=embed)
        else:
            await ctx.send("Account not found or an error occurred.")
    else:
        await ctx.send("Error fetching PUUID.")

# Inicia o bot
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    print(f'Error starting bot: {e}')
