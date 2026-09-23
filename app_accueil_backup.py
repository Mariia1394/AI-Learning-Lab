import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Learning Lab",
    page_icon="✦",
    layout="wide",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 92, 255, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(86, 180, 255, 0.08),
                transparent 30%
            ),
            #f8f9fa;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* --------------------------------------------------------
       HERO
    -------------------------------------------------------- */

    .hero {
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.96),
                rgba(247,245,255,0.96)
            );

        border: 1px solid rgba(125, 95, 255, 0.12);
        border-radius: 32px;

        padding: 4rem 4rem 3.5rem 4rem;

        box-shadow:
            0 20px 60px rgba(67, 56, 125, 0.08),
            0 4px 16px rgba(67, 56, 125, 0.04);

        margin-bottom: 2rem;
    }


    .badge {
        display: inline-block;

        padding: 0.45rem 0.9rem;

        border-radius: 999px;

        background: rgba(124, 92, 255, 0.10);

        color: #6950d9;

        font-size: 0.82rem;
        font-weight: 700;

        letter-spacing: 0.02em;

        margin-bottom: 1.2rem;
    }


    .hero-title {
        font-size: 3.4rem;
        line-height: 1.05;

        font-weight: 800;

        color: #242238;

        margin: 0 0 1rem 0;
    }


    .hero-title span {
        background:
            linear-gradient(
                90deg,
                #7057df,
                #5b9df5
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {
        font-size: 1.25rem;

        line-height: 1.65;

        color: #68677a;

        max-width: 720px;

        margin-bottom: 2rem;
    }


    .hero-description {
        font-size: 1rem;

        line-height: 1.7;

        color: #777689;

        max-width: 700px;
    }


    /* --------------------------------------------------------
       SECTION TITLES
    -------------------------------------------------------- */

    .section-title {
        font-size: 1.75rem;

        font-weight: 750;

        color: #29263d;

        margin-top: 2.5rem;
        margin-bottom: 0.4rem;
    }


    .section-subtitle {
        color: #777689;

        font-size: 1rem;

        margin-bottom: 1.5rem;
    }


    /* --------------------------------------------------------
       CARDS
    -------------------------------------------------------- */

    .card {
        background: rgba(255,255,255,0.94);

        border: 1px solid rgba(100, 90, 150, 0.09);

        border-radius: 24px;

        padding: 1.6rem;

        min-height: 190px;

        box-shadow:
            0 12px 35px rgba(60, 52, 100, 0.06);

        margin-bottom: 1rem;
    }


    .card-icon {
        width: 46px;
        height: 46px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 14px;

        background:
            linear-gradient(
                135deg,
                rgba(112,87,223,0.12),
                rgba(91,157,245,0.12)
            );

        font-size: 1.35rem;

        margin-bottom: 1rem;
    }


    .card-title {
        color: #302d46;

        font-size: 1.05rem;

        font-weight: 750;

        margin-bottom: 0.55rem;
    }


    .card-text {
        color: #777689;

        font-size: 0.93rem;

        line-height: 1.55;
    }


    /* --------------------------------------------------------
       MISSION
    -------------------------------------------------------- */

    .mission {
        background:
            linear-gradient(
                135deg,
                rgba(112,87,223,0.08),
                rgba(91,157,245,0.08)
            );

        border: 1px solid rgba(112,87,223,0.10);

        border-radius: 28px;

        padding: 2rem;

        margin-top: 1rem;
        margin-bottom: 1rem;
    }


    .mission-label {
        color: #7057df;

        font-size: 0.8rem;

        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 0.08em;

        margin-bottom: 0.6rem;
    }


    .mission-title {
        color: #29263d;

        font-size: 1.5rem;

        font-weight: 800;

        margin-bottom: 0.8rem;
    }


    .mission-text {
        color: #68677a;

        line-height: 1.65;

        margin-bottom: 0;
    }


    /* --------------------------------------------------------
       PARCOURS
    -------------------------------------------------------- */

    .step {
        display: flex;

        gap: 1rem;

        align-items: flex-start;

        margin-bottom: 1rem;
    }


    .step-number {
        min-width: 36px;
        height: 36px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background: rgba(112,87,223,0.10);

        color: #7057df;

        font-weight: 800;

        font-size: 0.9rem;
    }


    .step-content strong {
        color: #302d46;

        display: block;

        margin-bottom: 0.2rem;
    }


    .step-content span {
        color: #777689;

        font-size: 0.9rem;

        line-height: 1.5;
    }


    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        text-align: center;

        color: #9998a8;

        font-size: 0.8rem;

        margin-top: 3rem;
    }


    /* --------------------------------------------------------
       STREAMLIT BUTTON
    -------------------------------------------------------- */

    div.stButton > button {
        border: none;

        border-radius: 14px;

        padding: 0.75rem 1.5rem;

        font-weight: 700;

        background:
            linear-gradient(
                135deg,
                #7057df,
                #5b9df5
            );

        color: white;

        box-shadow:
            0 10px 25px rgba(112,87,223,0.20);

        transition: all 0.2s ease;
    }


    div.stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 14px 30px rgba(112,87,223,0.25);
    }


    /* --------------------------------------------------------
       RESPONSIVE
    -------------------------------------------------------- */

    @media (max-width: 900px) {

        .hero {
            padding: 2.5rem 2rem;
        }

        .hero-title {
            font-size: 2.5rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <section class="hero">

        <div class="badge">
            ✦ AI LEARNING LAB
        </div>

        <h1 class="hero-title">
            Apprendre en <span>pratiquant</span>
            avec l'IA
        </h1>

        <p class="hero-subtitle">
            Une expérience immersive de simulation conversationnelle
            pour développer ses compétences relationnelles face à
            une situation client difficile.
        </p>

        <p class="hero-description">
            Entrez dans la peau d'un conseiller clientèle et échangez
            avec un client simulé par une intelligence artificielle.
            Vos réponses influencent progressivement la dynamique
            de la conversation.
        </p>

    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Une expérience de formation augmentée par l'IA
    </div>

    <div class="section-subtitle">
        Ici, pas de scénario figé : vous apprenez en interagissant.
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">💬</div>

            <div class="card-title">
                Simulation conversationnelle
            </div>

            <div class="card-text">
                Échangez en langage naturel avec Alex, un client
                mécontent dont la commande n'a pas été livrée.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">🧠</div>

            <div class="card-title">
                Analyse comportementale
            </div>

            <div class="card-text">
                L'IA analyse vos réponses à travers plusieurs
                dimensions : empathie, reformulation, questions
                pertinentes et posture professionnelle.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">📈</div>

            <div class="card-title">
                Progression
            </div>

            <div class="card-text">
                La tension et la confiance évoluent au fil de
                vos réponses, afin de rendre visibles les effets
                de votre communication.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# OBJECTIF
# ============================================================

st.markdown(
    """
    <div class="section-title">
        L'objectif
    </div>

    <div class="section-subtitle">
        Désamorcer progressivement une situation client difficile.
    </div>

    <div class="mission">

        <div class="mission-label">
            Votre mission
        </div>

        <div class="mission-title">
            Transformer une interaction tendue en échange constructif.
        </div>

        <p class="mission-text">
            Votre objectif est de comprendre la situation d'Alex,
            reconnaître son insatisfaction, reformuler sa demande
            et rechercher une réponse adaptée tout en maintenant
            une posture professionnelle.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COMPÉTENCES
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Les compétences mobilisées
    </div>

    <div class="section-subtitle">
        Plusieurs compétences relationnelles sont observées pendant
        la simulation.
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">❤️</div>

            <div class="card-title">
                Empathie
            </div>

            <div class="card-text">
                Reconnaître l'émotion du client et montrer que
                sa situation est prise en considération.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="card">

            <div class="card-icon">🔎</div>

            <div class="card-title">
                Écoute et reformulation
            </div>

            <div class="card-text">
                Identifier le problème exprimé et le reformuler
                pour vérifier que la demande a bien été comprise.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">🗣️</div>

            <div class="card-title">
                Posture professionnelle
            </div>

            <div class="card-text">
                Maintenir une communication respectueuse,
                constructive et adaptée à une situation tendue.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="card">

            <div class="card-icon">🛠️</div>

            <div class="card-title">
                Orientation vers une solution
            </div>

            <div class="card-text">
                Passer de la compréhension du problème à la
                recherche d'une réponse concrète et adaptée.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PARCOURS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        Votre parcours
    </div>

    <div class="section-subtitle">
        Une expérience courte, interactive et réflexive.
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        <div class="card">

            <div class="step">

                <div class="step-number">
                    1
                </div>

                <div class="step-content">

                    <strong>
                        Plongez dans la situation
                    </strong>

                    <span>
                        Découvrez le contexte et prenez le rôle
                        du conseiller clientèle.
                    </span>

                </div>

            </div>


            <div class="step">

                <div class="step-number">
                    2
                </div>

                <div class="step-content">

                    <strong>
                        Échangez avec Alex
                    </strong>

                    <span>
                        Répondez librement et adaptez votre posture
                        aux réactions du client.
                    </span>

                </div>

            </div>


            <div class="step">

                <div class="step-number">
                    3
                </div>

                <div class="step-content">

                    <strong>
                        Observez la dynamique
                    </strong>

                    <span>
                        La tension, la confiance et le sentiment
                        d'écoute évoluent au fil de vos réponses.
                    </span>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="card">

            <div class="step">

                <div class="step-number">
                    4
                </div>

                <div class="step-content">

                    <strong>
                        Analysez votre performance
                    </strong>

                    <span>
                        Une analyse revient sur les comportements
                        mobilisés pendant la conversation.
                    </span>

                </div>

            </div>


            <div class="step">

                <div class="step-number">
                    5
                </div>

                <div class="step-content">

                    <strong>
                        Recevez un feedback
                    </strong>

                    <span>
                        Identifiez vos points forts et les axes
                        d'amélioration prioritaires.
                    </span>

                </div>

            </div>


            <div class="step">

                <div class="step-number">
                    6
                </div>

                <div class="step-content">

                    <strong>
                        Recommencez
                    </strong>

                    <span>
                        Mettez en pratique les conseils reçus
                        lors d'une nouvelle tentative.
                    </span>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CTA
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:3rem;
        margin-bottom:1rem;
    ">

        <div style="
            font-size:1.25rem;
            font-weight:750;
            color:#302d46;
            margin-bottom:0.5rem;
        ">
            Prête à relever le défi ?
        </div>

        <div style="
            color:#777689;
            margin-bottom:1.2rem;
        ">
            Une situation. Un client. Une conversation.
            À vous de jouer.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


col_left, col_center, col_right = st.columns([1, 2, 1])


with col_center:

    if st.button(
        "Commencer la simulation interactive →",
        key="btn_start_simulation",
        use_container_width=True,
    ):

        st.session_state["page"] = "simulation"

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Learning Lab · Simulation conversationnelle IA
        · Expérience de formation augmentée par l'IA
    </div>
    """,
    unsafe_allow_html=True,
)