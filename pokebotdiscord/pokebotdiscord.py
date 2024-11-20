import discord

from discord.ext import commands
import requests
from . import secretos

def buscar_pokemon(pokemon_buscado):
    result = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_buscado}")

    if result.text == "Not Found":
        return None
    else:
        return result.json()['sprites']['front_default']

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.command()
    async def test(ctx, *args):
        """
        manda al listado del chat de discord lo ingresado en el campo de ingreso
        si ingreso: $test hola que tal
        va a salir: hola que tal
        """
        respuesta = " ".join(args)
        await ctx.send(respuesta)
    
    @bot.command()
    async def poke(ctx, arg):
        """
        se ingresa, por ejemplo: $poke Pikachu
        devuelve la imagen de sprit del pokemon, pikachu en este caso
        """
        try:
            pokemon_buscado = arg.split(" ", 1)[0].lower()
            pokemon = buscar_pokemon(pokemon_buscado)
            await ctx.send("Pokemon no Encontrado" if pokemon is None else pokemon)
        except Exception as e:
            print("Error: ", e)

    @poke.error
    async def error_type(ctx, error):
        """
        si solo escribo $poke se muestra este mensaje
        """
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Tienes que pasarme un Pokemon")
    
    @bot.command()
    async def limpiar(ctx):
        """
        limpia el chat
        """
        await ctx.channel.purge()
        await ctx.send("Mensajes eliminados", delete_after=3)
    
    @bot.event
    async def on_ready():
        """
        para saber si se conecto a discord correctamente
        """
        print(f"Estamos dentro! {bot.user}")
    
    bot.run(secretos.TOKEN)