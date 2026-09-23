from agents import Agent, Runner
from evaluation import behavior_analyzer, final_evaluator

import asyncio
import json


# ============================================================
# AGENT CLIENT : ALEX
# ============================================================

alex = Agent(
    name="Alex",

    instructions="""
Tu joues le rôle d'Alex, une personne cliente mécontente.

============================================================
CONTEXTE
============================================================

Alex a commandé un produit qui devait être livré lundi.

Nous sommes jeudi et la commande n'a toujours pas été reçue.

Alex a déjà contacté le service client une première fois,
mais estime que le problème n'a pas réellement été pris en charge.


============================================================
INFORMATIONS CONNUES PAR ALEX
============================================================

- Numéro de commande : CMD-458721
- Livraison prévue : lundi
- Nous sommes jeudi
- Alex a déjà contacté le service client.


============================================================
PERSONNALITÉ
============================================================

- Alex est agacé(e) et frustré(e).
- Alex souhaite obtenir une solution concrète.
- Alex n'est pas insultant(e).
- Alex ne doit pas être agressif(ve) gratuitement.
- Alex réagit naturellement à ce que dit le conseiller.


============================================================
INFORMATIONS À RÉVÉLER PROGRESSIVEMENT
============================================================

Alex ne donne pas forcément toutes les informations immédiatement.

Si le conseiller demande clairement le numéro de commande,
Alex fournit :

CMD-458721

Si le conseiller demande où trouver le numéro de commande,
Alex peut expliquer qu'il se trouve dans l'e-mail de confirmation.

Une fois le numéro de commande fourni :

- ne prétends jamais qu'il n'a pas été fourni ;
- n'invente jamais un autre numéro ;
- n'utilise jamais de placeholder comme "[numéro]".


============================================================
ÉVOLUTION DU COMPORTEMENT
============================================================

TENSION 8 À 10 :

Alex est très mécontent(e).

Alex demande des explications et souhaite une solution concrète.

TENSION 5 À 7 :

Alex est encore mécontent(e), mais accepte davantage le dialogue.

TENSION 2 À 4 :

Alex commence à être rassuré(e) et devient plus coopératif(ve).

TENSION 0 À 1 :

Alex est calme et coopératif(ve).


============================================================
RÈGLES DE RÉACTION
============================================================

Adapte toujours ta réaction au dernier message du conseiller.

Si le conseiller fait preuve d'empathie :
Alex peut légèrement se calmer.

Si le conseiller reformule correctement :
Alex peut confirmer que le problème a bien été compris.

Si le conseiller pose une question pertinente :
Alex répond naturellement.

Si le conseiller propose une solution concrète :
Alex réagit positivement si cette solution répond réellement
au problème.

Si le conseiller minimise le problème :
Alex peut devenir davantage frustré(e).

Si le conseiller rejette la faute :
Alex peut contester cette réponse.

Si le conseiller est agressif :
Alex peut devenir plus tendu(e).


============================================================
IMPORTANT
============================================================

Utilise uniquement les informations réellement disponibles.

N'invente jamais :

- un statut de livraison ;
- une date de livraison ;
- une heure de livraison ;
- une adresse ;
- un remboursement ;
- une compensation ;
- une information technique concernant la commande.

Si le conseiller affirme une information qui n'est pas connue
dans le scénario, Alex peut demander :

"Comment pouvez-vous en être sûr(e) ?"

ou :

"Vous avez cette information dans votre système ?"


Les réponses doivent rester naturelles et relativement courtes.

Ne révèle jamais que tu es une intelligence artificielle.

Reste toujours dans ton rôle de personne cliente.
"""
)


# ============================================================
# CALCUL DU SCORE
# ============================================================

def calculate_total(evaluation):

    return (
        evaluation.empathy_score
        + evaluation.reformulation_score
        + evaluation.professional_posture_score
        + evaluation.solution_score
        + evaluation.tension_management_score
    )


# ============================================================
# AFFICHAGE DE L'ÉVALUATION
# ============================================================

def display_evaluation(evaluation, numero_tentative):

    total = calculate_total(evaluation)

    print("\n")
    print("╔════════════════════════════════════╗")
    print("║          ÉVALUATION FINALE         ║")
    print("╚════════════════════════════════════╝")

    print(f"\nTentative {numero_tentative}")

    print("\n--- COMPÉTENCES ---")

    print(
        f"\nEmpathie : "
        f"{evaluation.empathy_score}/2"
    )
    print(evaluation.empathy_feedback)

    print(
        f"\nReformulation : "
        f"{evaluation.reformulation_score}/2"
    )
    print(evaluation.reformulation_feedback)

    print(
        f"\nPosture professionnelle : "
        f"{evaluation.professional_posture_score}/2"
    )
    print(evaluation.professional_posture_feedback)

    print(
        f"\nSolution : "
        f"{evaluation.solution_score}/2"
    )
    print(evaluation.solution_feedback)

    print(
        f"\nGestion de la tension : "
        f"{evaluation.tension_management_score}/2"
    )
    print(evaluation.tension_management_feedback)

    print("\n------------------------------------")
    print(f"SCORE DE LA TENTATIVE {numero_tentative} : {total}/10")
    print("------------------------------------")

    print("\n--- FEEDBACK GLOBAL ---")
    print(evaluation.overall_feedback)

    print("\n--- CONSEIL POUR PROGRESSER ---")
    print(evaluation.improvement_tip)


# ============================================================
# SIMULATION
# ============================================================

async def run_simulation(numero_tentative):

    print("\n")
    print("========================================")
    print(f"          TENTATIVE {numero_tentative}")
    print("========================================")

    print("\nVous êtes le conseiller ou la conseillère clientèle.")
    print("Tapez 'fin' pour terminer la simulation.\n")

    conversation = []

    # --------------------------------------------------------
    # ÉTAT INITIAL
    # --------------------------------------------------------

    tension = 8
    confiance = 2
    ecoute = 2

    initial_state = f"""
ÉTAT INITIAL :

- Tension : {tension}/10
- Confiance : {confiance}/10
- Sentiment d'être écouté : {ecoute}/10

C'est le début de la conversation.

Commence directement en tant qu'Alex.

Explique brièvement :

- la commande devait être livrée lundi ;
- nous sommes jeudi ;
- elle n'est toujours pas arrivée ;
- Alex a déjà contacté le service client ;
- Alex estime que le problème n'a pas été réellement pris en charge.

Exprime une frustration crédible correspondant à une tension de 8/10.

Ne donne pas spontanément le numéro de commande.

Reste naturel(le) et relativement court.
"""

    initial_result = await Runner.run(
        alex,
        initial_state
    )

    initial_response = initial_result.final_output

    print(f"\nAlex : {initial_response}\n")

    conversation.append(
        {
            "role": "assistant",
            "content": initial_response
        }
    )

    # ========================================================
    # BOUCLE DE CONVERSATION
    # ========================================================

    while True:

        message = input("Vous : ")

        # ----------------------------------------------------
        # FIN DE LA SIMULATION
        # ----------------------------------------------------

        if message.strip().lower() == "fin":

            print("\n--- FIN DE LA SIMULATION ---")

            print("\nAnalyse de votre conversation...")

            final_result = await Runner.run(
                final_evaluator,
                json.dumps(
                    conversation,
                    ensure_ascii=False,
                    indent=2
                )
            )

            evaluation = final_result.final_output

            display_evaluation(
                evaluation,
                numero_tentative
            )

            return evaluation

        # ----------------------------------------------------
        # ANALYSE DU COMPORTEMENT
        # ----------------------------------------------------

        analysis_result = await Runner.run(
            behavior_analyzer,
            message
        )

        analysis_text = analysis_result.final_output

        print("\nAnalyse :", analysis_text)

        try:

            analysis = json.loads(
                analysis_text
            )

        except json.JSONDecodeError:

            print(
                "\nAttention : l'analyse de l'IA "
                "n'est pas au format JSON attendu."
            )

            analysis = {}

        # ----------------------------------------------------
        # MISE À JOUR DE L'ÉTAT
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # LIMITES 0-10
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # AFFICHAGE DE L'ÉTAT
        # ----------------------------------------------------

        print("\n╔════════════════════════════╗")
        print("║     ÉTAT DE LA SIMULATION  ║")
        print("╠════════════════════════════╣")
        print(
            f"║ Tension       {tension:>2} / 10    ║"
        )
        print(
            f"║ Confiance     {confiance:>2} / 10    ║"
        )
        print(
            f"║ Écoute        {ecoute:>2} / 10    ║"
        )
        print("╚════════════════════════════╝")

        # ----------------------------------------------------
        # AJOUT DU MESSAGE DU CONSEILLER
        # ----------------------------------------------------

        conversation.append(
            {
                "role": "user",
                "content": message
            }
        )

        # ----------------------------------------------------
        # RÉACTION D'ALEX
        # ----------------------------------------------------

        state_message = f"""
ÉTAT ACTUEL :

- Tension : {tension}/10
- Confiance : {confiance}/10
- Sentiment d'être écouté : {ecoute}/10

Adapte ta réaction à cet état.

Réagis directement au dernier message du conseiller.

Ne répète pas inutilement les informations déjà données.
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

        print(f"\nAlex : {response}\n")

        conversation.append(
            {
                "role": "assistant",
                "content": response
            }
        )


# ============================================================
# COMPARAISON DES DEUX TENTATIVES
# ============================================================

def display_comparison(
    evaluation_1,
    evaluation_2
):

    total_1 = calculate_total(
        evaluation_1
    )

    total_2 = calculate_total(
        evaluation_2
    )

    progression = total_2 - total_1

    print("\n\n")
    print("╔══════════════════════════════════════════╗")
    print("║       COMPARAISON DES TENTATIVES        ║")
    print("╚══════════════════════════════════════════╝")

    # --------------------------------------------------------
    # SCORES GLOBAUX
    # --------------------------------------------------------

    print("\n--- SCORES GLOBAUX ---")

    print(
        f"\nTentative 1 : {total_1}/10"
    )

    print(
        f"Tentative 2 : {total_2}/10"
    )

    if progression > 0:

        print(
            f"\nProgression globale : "
            f"+{progression} point(s)"
        )

    elif progression < 0:

        print(
            f"\nÉvolution globale : "
            f"{progression} point(s)"
        )

    else:

        print(
            "\nProgression globale : "
            "0 point"
        )

    # --------------------------------------------------------
    # PROGRESSION PAR COMPÉTENCE
    # --------------------------------------------------------

    print(
        "\n--- PROGRESSION PAR COMPÉTENCE ---\n"
    )

    empathy = (
        evaluation_2.empathy_score
        - evaluation_1.empathy_score
    )

    reformulation = (
        evaluation_2.reformulation_score
        - evaluation_1.reformulation_score
    )

    posture = (
        evaluation_2.professional_posture_score
        - evaluation_1.professional_posture_score
    )

    solution = (
        evaluation_2.solution_score
        - evaluation_1.solution_score
    )

    tension = (
        evaluation_2.tension_management_score
        - evaluation_1.tension_management_score
    )

    print(
        f"Empathie                : "
        f"{evaluation_1.empathy_score}/2 → "
        f"{evaluation_2.empathy_score}/2 "
        f"({empathy:+d})"
    )

    print(
        f"Reformulation           : "
        f"{evaluation_1.reformulation_score}/2 → "
        f"{evaluation_2.reformulation_score}/2 "
        f"({reformulation:+d})"
    )

    print(
        f"Posture professionnelle : "
        f"{evaluation_1.professional_posture_score}/2 → "
        f"{evaluation_2.professional_posture_score}/2 "
        f"({posture:+d})"
    )

    print(
        f"Solution                : "
        f"{evaluation_1.solution_score}/2 → "
        f"{evaluation_2.solution_score}/2 "
        f"({solution:+d})"
    )

    print(
        f"Gestion de la tension   : "
        f"{evaluation_1.tension_management_score}/2 → "
        f"{evaluation_2.tension_management_score}/2 "
        f"({tension:+d})"
    )

    # --------------------------------------------------------
    # BILAN PÉDAGOGIQUE
    # --------------------------------------------------------

    print("\n--- BILAN PÉDAGOGIQUE ---\n")

    if progression > 0:

        print(
            "La deuxième tentative montre une "
            "progression du score global."
        )

        print(
            "Vous avez pu mettre en pratique les "
            "conseils issus de la première simulation."
        )

    elif progression < 0:

        print(
            "Le score global est inférieur lors "
            "de la deuxième tentative."
        )

        print(
            "Les résultats permettent d'identifier "
            "les compétences qui nécessitent encore "
            "un entraînement."
        )

    else:

        print(
            "Le score global reste stable entre "
            "les deux tentatives."
        )

        print(
            "Les résultats permettent d'identifier "
            "les compétences à retravailler."
        )

    # --------------------------------------------------------
    # FIN
    # --------------------------------------------------------

    print("\n")
    print("==========================================")
    print("             FIN DES TENTATIVES")
    print("==========================================")


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

async def main():

    print("\n")
    print("==========================================")
    print("          AI LEARNING LAB")
    print("==========================================")
    print("      Simulation : relation client")
    print("==========================================")

    # --------------------------------------------------------
    # TENTATIVE 1
    # --------------------------------------------------------

    evaluation_1 = await run_simulation(
        1
    )

    # --------------------------------------------------------
    # CHOIX DE L'UTILISATEUR
    # --------------------------------------------------------

    print("\n")
    print("==========================================")
    print("       QUE SOUHAITEZ-VOUS FAIRE ?")
    print("==========================================")
    print("1 - Refaire la simulation")
    print("2 - Quitter")
    print("==========================================")

    choix = input(
        "\nVotre choix : "
    )

    # --------------------------------------------------------
    # TENTATIVE 2
    # --------------------------------------------------------

    if choix == "1":

        print("\n")
        print("==========================================")
        print("          TENTATIVE 2")
        print("==========================================")

        print(
            "\nMettez en pratique les conseils "
            "reçus lors de la première tentative."
        )

        evaluation_2 = await run_simulation(
            2
        )

        # ----------------------------------------------------
        # COMPARAISON
        # ----------------------------------------------------

        display_comparison(
            evaluation_1,
            evaluation_2
        )

    else:

        print("\n")
        print("Fin du module. À bientôt !")


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )