from agents import Runner

from client_agent import (
    alex,
    behavior_analyzer,
    final_evaluator
)

import json


async def start_simulation():

    conversation = []

    tension = 8
    confiance = 2
    ecoute = 2

    initial_state = """
Tu es Alex, une personne cliente mécontente.

Ta commande devait être livrée lundi.
Nous sommes jeudi et elle n'est toujours pas arrivée.

Tu as déjà contacté le service client,
mais tu as le sentiment que ton problème
n'a pas réellement été pris en charge.

Commence directement la conversation.

Exprime une frustration crédible correspondant
à une tension de 8/10.

Ne donne pas spontanément ton numéro de commande.

Reste naturel(le), crédible et relativement court.
"""

    result = await Runner.run(
        alex,
        initial_state
    )

    response = result.final_output

    conversation.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    return {
        "conversation": conversation,
        "tension": tension,
        "confiance": confiance,
        "ecoute": ecoute
    }


async def send_message(
    message,
    conversation,
    tension,
    confiance,
    ecoute
):

    # --------------------------------------------------------
    # ANALYSE DU MESSAGE DU CONSEILLER
    # --------------------------------------------------------

    analysis_result = await Runner.run(
        behavior_analyzer,
        message
    )

    analysis_text = analysis_result.final_output

    try:

        analysis = json.loads(
            analysis_text
        )

    except json.JSONDecodeError:

        analysis = {}


    # --------------------------------------------------------
    # MISE À JOUR DE L'ÉTAT
    # --------------------------------------------------------

    if analysis.get("empathy"):

        tension -= 1
        confiance += 1
        ecoute += 1

    if analysis.get("reformulation"):

        tension -= 2
        confiance += 2
        ecoute += 2

    if analysis.get("relevant_question"):

        tension -= 1
        confiance += 1
        ecoute += 1

    if analysis.get("solution"):

        tension -= 2
        confiance += 2

    if analysis.get("minimization"):

        tension += 2
        confiance -= 2

    if analysis.get("blame"):

        tension += 2
        confiance -= 2

    if analysis.get("aggression"):

        tension += 3
        confiance -= 3


    # --------------------------------------------------------
    # LIMITES
    # --------------------------------------------------------

    tension = max(
        0,
        min(10, tension)
    )

    confiance = max(
        0,
        min(10, confiance)
    )

    ecoute = max(
        0,
        min(10, ecoute)
    )


    # --------------------------------------------------------
    # AJOUT DU MESSAGE DU CONSEILLER
    # --------------------------------------------------------

    conversation.append(
        {
            "role": "user",
            "content": message
        }
    )


    # --------------------------------------------------------
    # RÉACTION D'ALEX
    # --------------------------------------------------------

    state_message = f"""
ÉTAT ACTUEL :

Tension : {tension}/10
Confiance : {confiance}/10
Sentiment d'être écouté : {ecoute}/10

Adapte ta réaction à cet état.

Réagis directement au dernier message
du conseiller.

Ne répète pas inutilement les informations
déjà données.
"""

    result = await Runner.run(
        alex,
        state_message
        + "\n\nHISTORIQUE DE LA CONVERSATION :\n"
        + json.dumps(
            conversation,
            ensure_ascii=False,
            indent=2
        )
    )

    response = result.final_output


    conversation.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    return {
        "conversation": conversation,
        "tension": tension,
        "confiance": confiance,
        "ecoute": ecoute,
        "analysis": analysis
    }