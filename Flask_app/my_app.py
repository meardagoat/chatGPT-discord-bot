import discord
from discord.ext import commands
import asyncio
from flask import Flask

# Création de l'instance de l'application Flask
app = Flask(__name__)

# Création de l'instance du bot Discord avec un préfixe de commande
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)


# Définition de la route racine de l'application Flask
@app.route('/')
def index():
    # Fonction de la route racine qui retourne une chaîne "Hello, world!"
    return 'Hello, world!'


# Définition de la route pour envoyer un message au bot Discord
@app.route('/send_message/<int:channel_id>/<message>')
def send_message(channel_id, message):
    # Récupération du canal Discord spécifié par son identifiant
    channel = bot.get_channel(channel_id)

    # Envoi du message au canal Discord spécifié
    asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)

    # Retourne un message confirmant l'envoi du message au canal Discord
    return f'Message sent to channel {channel_id}: {message}'


# Fonction exécutée avant la première requête HTTP vers l'application Flask
def run_bot():
    # Démarrage du bot Discord en utilisant le token du bot
    asyncio.run(bot.start(''))


# Exécuter la fonction run_bot avant la première requête HTTP
app.before_first_request(run_bot)


# Fonction exécutée après chaque requête HTTP vers l'application Flask
@app.after_request
async def close_bot(response):
    # Arrêt du bot Discord
    await bot.close()
    return response


# Vérification si le script est exécuté en tant que programme principal
if __name__ == '__main__':
    # Lancement de l'application Flask en mode debug
    app.run(debug=True)




