import asyncio
import aiofiles
import sys


async def read_from_file(filename):
    async with aiofiles.open(filename, mode='r') as file:
        content = await file.read()
        print(f"Contenu du fichier {filename} : {content}")


async def read_from_stdin():
    loop = asyncio.get_running_loop()

    # Crée un futur pour attendre l'entrée de l'utilisateur
    future = loop.create_future()

    # Callback pour définir le résultat du futur lorsque l'entrée est disponible
    def stdin_callback():
        line = sys.stdin.readline()
        future.set_result(line)

    # Ajoute le callback au loop pour écouter l'entrée standard
    loop.add_reader(sys.stdin.fileno(), stdin_callback)

    # Attend que l'utilisateur entre du texte
    line = await future
    print(f"Entrée utilisateur : {line}")

    # Nettoie le callback
    loop.remove_reader(sys.stdin.fileno())


async def main():
    filename = "/tmp/foxdotcode.txt"

    # Planifie la lecture du fichier et de stdin simultanément
    await asyncio.gather(
        read_from_file(filename),
        read_from_stdin(),
    )


# Exécute la boucle d'événements
asyncio.run(main())
