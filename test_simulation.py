import asyncio

from simulation import start_simulation


async def main():

    result = await start_simulation()

    print("\n==============================")
    print("RÉPONSE D'ALEX")
    print("==============================")

    print(result["conversation"][0]["content"])

    print("\n==============================")
    print("ÉTAT INITIAL")
    print("==============================")

    print("Tension :", result["tension"])
    print("Confiance :", result["confiance"])
    print("Écoute :", result["ecoute"])


asyncio.run(main())