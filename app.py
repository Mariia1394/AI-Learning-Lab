import asyncio
import base64
import time
import streamlit as st

from agents import Runner
from simulation import send_message, start_simulation
from evaluation import final_evaluator

# ============================================================
# CONFIGURATION STREAMLIT
# ============================================================

st.set_page_config(page_title="AI Learning Lab", page_icon="✦", layout="wide")

# ============================================================
# GESTION DE LA NAVIGATION
# ============================================================

if "page" not in st.session_state:
    st.session_state["page"] = "accueil"
if "pending_transition" not in st.session_state:
    st.session_state["pending_transition"] = None

# ============================================================
# STYLE GLOBAL HAUT DE GAMME & SYMÉTRIQUE
# ============================================================

def inject_global_styles():
    st.markdown(
        """
        <style>
        header { visibility: hidden !important; }
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }

        /* Fond général immaculé et suppression des transparences */
        .stApp {
            background-color: #f8fafc !important;
            opacity: 1 !important;
        }

        /* Animation d'apparition fluide et élégante */
        @keyframes solidFadeIn {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .block-container {
            max-width: 1240px;
            padding-top: 2.5rem;
            padding-bottom: 6rem;
            animation: solidFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            background-color: #f8fafc;
        }

        /* Boutons globaux dynamiques avec dégradé sophistiqué */
        div.stButton > button {
            background: linear-gradient(135deg, #f43f5e 0%, #fb923c 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 16px 30px;
            font-weight: 700;
            font-size: 15px;
            box-shadow: 0 10px 25px rgba(244, 63, 94, 0.25);
            width: 100%;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }
        div.stButton > button:hover {
            opacity: 0.95;
            box-shadow: 0 14px 32px rgba(244, 63, 94, 0.38);
            transform: translateY(-2px);
        }
        div.stButton > button:active {
            transform: translateY(0px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_global_styles()

# ============================================================
# ÉCRAN DE TRANSITION PLEIN ÉCRAN
# ============================================================

def show_loading_overlay(title, subtitle="", emoji="✦"):
    subtitle_html = f'<div class="loading-subtitle">{subtitle}</div>' if subtitle else ""
    html = f"""
    <style>
    @keyframes overlayFadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    @keyframes floatBounce {{
        0%, 100% {{ transform: translateY(0) scale(1); }}
        50% {{ transform: translateY(-14px) scale(1.06); }}
    }}
    @keyframes spinGrad {{
        to {{ transform: rotate(360deg); }}
    }}
    @keyframes pulseDot {{
        0%, 80%, 100% {{ transform: scale(0.6); opacity: .35; }}
        40% {{ transform: scale(1); opacity: 1; }}
    }}
    .app-loading-overlay {{
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        z-index: 999999;
        background: radial-gradient(circle at 50% 35%, #fff7ed 0%, #f8fafc 68%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        animation: overlayFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .loading-orb-wrap {{
        position: relative;
        width: 130px;
        height: 130px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 26px;
    }}
    .loading-ring {{
        position: absolute;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        border: 3px solid rgba(244, 63, 94, 0.12);
        border-top-color: #f43f5e;
        border-right-color: #fb923c;
        animation: spinGrad 1s linear infinite;
    }}
    .loading-logo {{
        width: 78px;
        height: 78px;
        border-radius: 24px;
        background: linear-gradient(135deg, #f43f5e 0%, #fb923c 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 34px;
        color: white;
        box-shadow: 0 18px 40px rgba(244, 63, 94, 0.35);
        animation: floatBounce 1.7s ease-in-out infinite;
    }}
    .loading-title {{
        font-size: 19px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.01em;
        text-align: center;
    }}
    .loading-subtitle {{
        font-size: 14px;
        color: #64748b;
        margin-top: 10px;
        max-width: 360px;
        text-align: center;
        line-height: 1.55;
    }}
    .loading-dots {{ margin-top: 18px; }}
    .loading-dots span {{
        display: inline-block;
        width: 7px;
        height: 7px;
        margin: 0 3px;
        border-radius: 50%;
        background: #f43f5e;
        animation: pulseDot 1.3s infinite ease-in-out;
    }}
    .loading-dots span:nth-child(2) {{ animation-delay: .15s; background: #fb923c; }}
    .loading-dots span:nth-child(3) {{ animation-delay: .3s; background: #f97316; }}
    </style>
    <div class="app-loading-overlay">
    <div class="loading-orb-wrap">
    <div class="loading-ring"></div>
    <div class="loading-logo">{emoji}</div>
    </div>
    <div class="loading-title">{title}</div>
    {subtitle_html}
    <div class="loading-dots"><span></span><span></span><span></span></div>
    </div>
    """
    flattened = "\n".join(
        line.strip() for line in html.strip().splitlines() if line.strip()
    )
    st.markdown(flattened, unsafe_allow_html=True)


def go_to_page(target_page, title, subtitle="", emoji="✦", pause=0.45, clear_keys=None, task=None):
    if clear_keys:
        for key in clear_keys:
            st.session_state.pop(key, None)
    st.session_state["pending_transition"] = {
        "target": target_page,
        "title": title,
        "subtitle": subtitle,
        "emoji": emoji,
        "pause": pause,
        "task": task,
    }
    st.session_state["page"] = "loading"
    st.rerun()


# ============================================================
# FONCTION : PAGE DE DÉBRIEF / FIN DE SIMULATION
# ============================================================

def show_debrief_page():
  st.markdown(
      """
      <style>
      .debrief-header { text-align: center; margin-bottom: 40px; }
      .score-card-wahou {
          background: #ffffff;
          border: 1px solid #fed7aa;
          padding: 45px;
          border-radius: 28px;
          text-align: center;
          margin-bottom: 40px;
          box-shadow: 0 20px 45px rgba(244, 63, 94, 0.07);
          position: relative;
          overflow: hidden;
      }
      .score-card-wahou::before {
          content: '';
          position: absolute;
          top: 0; left: 0; right: 0; height: 6px;
          background: linear-gradient(90deg, #f43f5e, #fb923c);
      }
      .score-title { font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 2.5px; color: #64748b; }
      .score-value {
          font-size: 64px;
          font-weight: 900;
          background: linear-gradient(90deg, #f43f5e, #fb923c);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          margin: 12px 0;
          letter-spacing: -0.03em;
      }
      .criterion-card-wahou {
          background: #ffffff;
          border: 1px solid #e2e8f0;
          padding: 26px;
          border-radius: 22px;
          margin-bottom: 22px;
          box-shadow: 0 6px 20px rgba(15, 23, 42, 0.02);
          height: 100%;
          transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      }
      .criterion-card-wahou:hover {
          transform: translateY(-4px);
          box-shadow: 0 14px 30px rgba(244, 63, 94, 0.08);
          border-color: #f43f5e;
      }
      .criterion-title { font-size: 15px; font-weight: 800; color: #0f172a; }
      .criterion-score { font-size: 13px; font-weight: 700; color: #f43f5e; margin-top: 4px; }
      .criterion-feedback { font-size: 13.5px; color: #475569; line-height: 1.65; margin-top: 12px; }
      .global-feedback-box {
          background: #ffffff;
          border: 1px solid #e2e8f0;
          border-left: 5px solid #0284c7;
          padding: 30px;
          border-radius: 22px;
          margin-top: 25px;
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.02);
          height: 100%;
      }
      .tip-card-box {
          background: #ffffff;
          border: 1px solid #e2e8f0;
          border-left: 5px solid #f97316;
          padding: 30px;
          border-radius: 22px;
          margin-top: 25px;
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.02);
          height: 100%;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  conversation = st.session_state.get("conversation_finale", [])

  st.markdown(
      """
      <div class="debrief-header">
          <span style="background: linear-gradient(90deg, #f43f5e, #fb923c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 12px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;">✦ Bilan de Session ✦</span>
          <h1 style="font-weight: 900; color: #0f172a; font-size: 36px; margin-top: 6px; letter-spacing: -0.02em;">Analyse & Débriefing d'Expert</h1>
          <p style="color:#64748b; font-size:15.5px; margin-top: 8px;">
              Découvrez l'évaluation détaillée de votre posture et de votre communication face à Alex.
          </p>
      </div>
      """,
      unsafe_allow_html=True,
  )

  conversation_text = ""
  for message in conversation:
    role = "CONSEILLER" if message["role"] == "user" else "ALEX"
    conversation_text += f"{role} : {message['content']}\n\n"

  if conversation:
    cached_evaluation = st.session_state.get("evaluation_result")
    if cached_evaluation is not None:
      evaluation = cached_evaluation
    else:
      loading_slot = st.empty()
      with loading_slot.container():
        show_loading_overlay(
            "Analyse approfondie de votre performance...",
            emoji="📊",
        )
      evaluation_result = asyncio.run(
          Runner.run(final_evaluator, conversation_text)
      )
      loading_slot.empty()
      evaluation = evaluation_result.final_output
      st.session_state["evaluation_result"] = evaluation

    total_score = (
        evaluation.empathy_score
        + evaluation.reformulation_score
        + evaluation.professional_posture_score
        + evaluation.solution_score
        + evaluation.tension_management_score
    )

    st.markdown(
        f"""
        <div class="score-card-wahou">
            <div class="score-title">🏆 Score Global de Performance</div>
            <div class="score-value">{total_score} <span style="font-size: 30px; color: #94a3b8; font-weight: 600;">/ 10</span></div>
            <div style="color:#64748b; font-size: 14.5px; font-weight: 500;">
                Évaluation multicritère basée sur l'excellence relationnelle et la résolution de crise.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h3 style='font-size: 20px; font-weight: 800; color: #0f172a; margin-bottom: 22px; letter-spacing: -0.01em;'>📊 Détail par Critère Clé</h3>",
        unsafe_allow_html=True,
    )

    criteria = [
        ("💖 Empathie", evaluation.empathy_score, evaluation.empathy_feedback),
        ("🔄 Reformulation", evaluation.reformulation_score, evaluation.reformulation_feedback),
        ("🛡️ Posture professionnelle", evaluation.professional_posture_score, evaluation.professional_posture_feedback),
        ("💡 Recherche de solution", evaluation.solution_score, evaluation.solution_feedback),
        ("⚖️ Gestion de la tension", evaluation.tension_management_score, evaluation.tension_management_feedback),
    ]

    col1, col2 = st.columns(2, gap="large")

    for index, (title, score, feedback) in enumerate(criteria):
      column = col1 if index % 2 == 0 else col2
      with column:
        st.markdown(
            f"""
            <div class="criterion-card-wahou">
                <div class="criterion-title">{title}</div>
                <div class="criterion-score">Score : {score} / 2</div>
                <div class="criterion-feedback">
                    {feedback}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col_fb1, col_fb2 = st.columns(2, gap="large")

    with col_fb1:
      st.markdown(
          f"""
          <div class="global-feedback-box">
              <h4 style="color:#0284c7; margin-top:0; font-weight: 800; font-size: 16px;">
                  💬 Synthèse du Débrief
              </h4>
              <p style="color:#334155; line-height:1.7; font-size: 14.5px; margin-bottom: 0;">
                  {evaluation.overall_feedback}
              </p>
          </div>
          """,
          unsafe_allow_html=True,
      )

    with col_fb2:
      st.markdown(
          f"""
          <div class="tip-card-box">
              <h4 style="color:#c2410c; margin-top:0; font-weight: 800; font-size: 16px;">
                  🚀 Priorité pour la Prochaine Tentative
              </h4>
              <p style="color:#334155; line-height:1.7; font-size: 14.5px; margin-bottom: 0;">
                  {evaluation.improvement_tip}
              </p>
          </div>
          """,
          unsafe_allow_html=True,
      )

  else:
    st.warning("⚠️ Aucune conversation n'a été enregistrée pour cette simulation.")

  st.markdown("<br><br>", unsafe_allow_html=True)

  col1, col2 = st.columns(2, gap="large")
  with col1:
    if st.button("🔄 Recommencer une simulation", key="restart_sim", use_container_width=True):
      go_to_page(
          "simulation",
          "Préparation de votre simulation",
          emoji="🔄",
          clear_keys=["simulation", "conversation_finale", "evaluation_result"],
          task="start_simulation",
      )

  with col2:
    if st.button("🏠 Retour à l'accueil", key="back_home_from_debrief", use_container_width=True):
      go_to_page(
          "accueil",
          "Retour à l'accueil",
          emoji="🏠",
          clear_keys=["simulation", "conversation_finale", "evaluation_result"],
      )


# ============================================================
# FONCTION : PAGE SIMULATION
# ============================================================

def show_simulation_page():
  st.markdown(
      """
    <style>
    .sim-header-card-wahou {
        background: #ffffff;
        border: 1px solid #fed7aa;
        padding: 32px;
        border-radius: 26px;
        box-shadow: 0 12px 35px rgba(244, 63, 94, 0.05);
        margin-bottom: 25px;
    }
    .metric-card-wahou {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.02);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .metric-card-wahou:hover {
        transform: translateY(-3px);
        border-color: #fb923c;
        box-shadow: 0 10px 25px rgba(251, 146, 60, 0.08);
    }
    .metric-title {
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 6px;
    }
    .metric-value { font-size: 26px; font-weight: 900; letter-spacing: -0.02em; }
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        background: #ffffff;
        padding: 12px 18px;
        border-radius: 18px;
        border-bottom-left-radius: 4px;
        margin-bottom: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.03);
        border: 1px solid #f1f5f9;
    }
    .typing-dot {
        height: 7px;
        width: 7px;
        margin: 0 2.5px;
        background-color: #cbd5e1;
        border-radius: 50%;
        display: inline-block;
        animation: wave 1.3s infinite ease-in-out;
    }
    .typing-dot:nth-child(2) { animation-delay: -1.1s; }
    .typing-dot:nth-child(3) { animation-delay: -0.9s; }

    @keyframes wave {
        0%, 60%, 100% { transform: translateY(0); background-color: #cbd5e1; }
        30% { transform: translateY(-5px); background-color: #f97316; }
    }

    div.stButton > button[kind="secondary"] {
        background: #ffffff;
        color: #475569;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        font-weight: 600;
        padding: 12px 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #f8fafc;
        color: #f43f5e;
        border-color: #f43f5e;
        transform: translateY(-1px);
    }
    </style>
    """,
      unsafe_allow_html=True,
  )

  col_back, _ = st.columns([1, 5])
  with col_back:
    if st.button("← Retour", key="back_home", type="secondary"):
      go_to_page(
          "accueil",
          "Retour à l'accueil",
          emoji="🏠",
          clear_keys=["simulation"],
      )

  st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

  st.markdown(
      """
    <div class="sim-header-card-wahou">
        <span style="background: linear-gradient(90deg, #f43f5e, #fb923c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 11.5px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase;">⚡ LIVE SIMULATION ⚡</span>
        <h1 style="font-size: 30px; font-weight: 900; color: #0f172a; margin-top: 6px; margin-bottom: 10px; letter-spacing: -0.02em;">En ligne avec Alex 👤</h1>
        <p style="color: #475569; font-size: 15px; margin: 0; line-height: 1.65;">
            Alex est un client trés agacé suite à un retard de livraison. Gardez votre sang-froid et désamorcez la crise avec brio ! 🛡️
            <br><span style="color: #ea580c; font-weight: 700; font-size: 13.5px;">💡Tapez le mot <b>"terminer"</b> dans votre message pour clôturer la simulation et accéder au débrief.</span>
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  if "simulation" not in st.session_state:
    loading_slot = st.empty()
    with loading_slot.container():
      show_loading_overlay(
          "Préparation de votre simulation",
          emoji="👤",
      )
    st.session_state["simulation"] = asyncio.run(start_simulation())
    loading_slot.empty()

  simulation = st.session_state["simulation"]

  col1, col2, col3 = st.columns(3, gap="medium")

  with col1:
    st.markdown(
        f"""
        <div class="metric-card-wahou">
            <div class="metric-title">🔥 Niveau de Tension</div>
            <div class="metric-value" style="color: {'#ef4444' if int(simulation['tension']) > 5 else '#10b981'};">{simulation['tension']} <span style="font-size: 16px; color: #94a3b8;">/10</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col2:
    st.markdown(
        f"""
        <div class="metric-card-wahou">
            <div class="metric-title">🤝 Indice de Confiance</div>
            <div class="metric-value" style="color: #3b82f6;">{simulation['confiance']} <span style="font-size: 16px; color: #94a3b8;">/10</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col3:
    st.markdown(
        f"""
        <div class="metric-card-wahou">
            <div class="metric-title">🎧 Qualité d'Écoute</div>
            <div class="metric-value" style="color: #8b5cf6;">{simulation['ecoute']} <span style="font-size: 16px; color: #94a3b8;">/10</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

  st.subheader("💬 Fil de Discussion")

  chat_container = st.container()
  with chat_container:
    for message in simulation["conversation"]:
      if message["role"] == "assistant":
        with st.chat_message("assistant", avatar="👤"):
          st.markdown(
              f"<div style='background: #ffffff; padding: 16px 20px; border-radius: 18px; border: 1px solid #e2e8f0; color: #1e293b; box-shadow: 0 4px 14px rgba(0,0,0,0.02); line-height: 1.6;'><b>Alex :</b> {message['content']}</div>",
              unsafe_allow_html=True,
          )
      else:
        with st.chat_message("user", avatar="🧑‍💼"):
          st.markdown(
              f"<div style='background: #fff7ed; padding: 16px 20px; border-radius: 18px; border: 1px solid #fed7aa; color: #9a3412; box-shadow: 0 4px 14px rgba(0,0,0,0.02); line-height: 1.6;'><b>Vous :</b> {message['content']}</div>",
              unsafe_allow_html=True,
          )

  st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
  prompt = st.chat_input("Écrivez votre réponse à Alex ici... ✍️")

  if prompt:
    if prompt.strip().lower() == "terminer":
      st.session_state["conversation_finale"] = simulation["conversation"]
      go_to_page(
          "debrief",
          "Préparation de votre bilan",
          emoji="🏆",
          task="run_evaluator",
      )

    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-top: 12px;">
            <div style="background: #e2e8f0; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px;">👤</div>
            <div class="typing-indicator">
                <span style="font-size: 13px; color: #64748b; font-weight: 600; margin-right: 8px;">Alex est en train de rédiger sa réponse</span>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    result = asyncio.run(
        send_message(
            prompt,
            simulation["conversation"],
            simulation["tension"],
            simulation["confiance"],
            simulation["ecoute"],
        )
    )

    typing_placeholder.empty()

    st.session_state["simulation"] = result
    st.rerun()


# ============================================================
# ROUTEUR DE PAGES PRINCIPAL
# ============================================================

if st.session_state["page"] == "loading":
  transition = st.session_state.get("pending_transition") or {}
  show_loading_overlay(
      transition.get("title", "Chargement..."),
      transition.get("subtitle", ""),
      emoji=transition.get("emoji", "✦"),
  )
  task = transition.get("task")
  if task == "start_simulation":
    st.session_state["simulation"] = asyncio.run(start_simulation())
  elif task == "run_evaluator":
    conversation = st.session_state.get("conversation_finale", [])
    conversation_text = ""
    for message in conversation:
      role = "CONSEILLER" if message["role"] == "user" else "ALEX"
      conversation_text += f"{role} : {message['content']}\n\n"
    if conversation:
      evaluation_result = asyncio.run(Runner.run(final_evaluator, conversation_text))
      st.session_state["evaluation_result"] = evaluation_result.final_output
    else:
      st.session_state["evaluation_result"] = None
  else:
    time.sleep(transition.get("pause", 0.45))
  st.session_state["page"] = transition.get("target", "accueil")
  st.session_state["pending_transition"] = None
  st.rerun()
elif st.session_state["page"] == "simulation":
  show_simulation_page()
  st.stop()
elif st.session_state["page"] == "debrief":
  show_debrief_page()
  st.stop()


# ============================================================
# PAGE D'ACCUEIL
# ============================================================

def get_image_base64(path):
  try:
    with open(path, "rb") as img_file:
      return base64.b64encode(img_file.read()).decode("utf-8")
  except Exception:
    return ""


    """
    <style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px 40px 0px;
    }
    .brand-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 900;
        font-size: 17px;
        color: #1e1b4b;
        letter-spacing: -0.02em;
    }
    .brand-dot {
        background: linear-gradient(135deg, #fb7185, #f43f5e);
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        color: white;
        box-shadow: 0 10px 22px rgba(244, 63, 94, 0.35);
    }
    .meta-container {
        display: flex;
        gap: 12px;
        margin-top: 25px;
        margin-bottom: 35px;
        flex-wrap: wrap;
    }
    .meta-badge {
        background: #ffffff;
        border: 1px solid #fed7aa;
        padding: 9px 18px;
        border-radius: 30px;
        font-size: 13.5px;
        font-weight: 700;
        color: #475569;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.04);
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .meta-badge span { color: #f43f5e; }
    .hero-title {
        font-size: 50px;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.08;
        letter-spacing: -0.035em;
        margin-bottom: 22px;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #475569;
        line-height: 1.65;
        margin-bottom: 18px;
    }
    .eyebrow {
        background: linear-gradient(90deg, #f43f5e, #fb923c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 14px;
        display: block;
    }
    .dashboard-card-wahou {
        background: #ffffff;
        border: 1px solid #fed7aa;
        padding: 35px;
        border-radius: 28px;
        box-shadow: 0 22px 50px rgba(244, 63, 94, 0.07);
        position: relative;
        overflow: hidden;
    }
    .tab-content-item {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        font-size: 15px;
        color: #334155;
        line-height: 1.6;
        background: #f8fafc;
        padding: 18px 22px;
        border-radius: 18px;
        border: 1px solid #f1f5f9;
        margin-bottom: 14px;
        transition: transform 0.2s ease;
    }
    .tab-content-item:hover {
        transform: translateX(4px);
        background: #ffffff;
        border-color: #fed7aa;
    }
    </style>
    """,
    unsafe_allow_html=True,


st.markdown(
    """
    <div class="navbar">
        <div class="brand-logo">
            <div class="brand-dot">✦</div>
            LE LABO IA
        </div>
        <div style="font-size: 13.5px; font-weight: 800; color: #f43f5e; background: #fff1f2; padding: 8px 18px; border-radius: 22px; border: 1px solid #fecdd3; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.06);">
            Expérience Interactive
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_hero_left, col_hero_right = st.columns([1.1, 1.3], gap="large")

with col_hero_left:
  st.markdown(
      """
        <span class="eyebrow">Simulation Conversationnelle</span>
        <div class="hero-title">Gérer une situation client difficile</div>
        <div class="hero-subtitle">
        Plongez dans une situation client réaliste. Mettez en pratique l'écoute active, la négociation et la gestion des conflits pour trouver une solution et préserver la relation client.
        </div>
        """,
      unsafe_allow_html=True,
  )

  st.markdown(
      """
        <div class="meta-container">
            <div class="meta-badge">⏱️ <span>Durée :</span> 10–15 min</div>
            <div class="meta-badge">💬 <span>Format :</span> Chat immersif</div>
        </div>
        """,
      unsafe_allow_html=True,
  )

with col_hero_right:
  st.markdown('<div class="dashboard-card-wahou">', unsafe_allow_html=True)
  tab_obj, tab_comp = st.tabs(
      ["🎯 Objectifs Pédagogiques", "⚡ Compétences Clés"]
  )

  with tab_obj:
    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
            <div class="tab-content-item"><span style="color:#f43f5e; font-weight:900;">■</span> Identifier les besoins et les attentes du client lors d’une réclamation.</div>
            <div class="tab-content-item"><span style="color:#f43f5e; font-weight:900;">■</span> Utiliser l’écoute active et la reformulation pour clarifier la situation.</div>
            <div class="tab-content-item"><span style="color:#f43f5e; font-weight:900;">■</span> Proposer des solutions adaptées tout en préservant la relation commerciale.</div>
        """,
        unsafe_allow_html=True,
    )

  with tab_comp:
    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
            <div class="tab-content-item"><span style="color:#f43f5e; font-weight:900;">■</span> Gestion du stress et des situations conflictuelles.</div>
            <div class="tab-content-item"><span style="color:#f43f5e; font-weight:900;">■</span> Recherche de compromis orientés satisfaction client.</div>
            <div class="tab-content-item"><span style="color:#f43f5e; font-weight:900;">■</span> Maîtrise de la posture assertive et empathique.</div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Bouton de démarrage bien centré sous la section des objectifs et compétences
col_spacer1, col_btn, col_spacer2 = st.columns([1, 1.2, 1])
with col_btn:
  if st.button("🚀 Commencer la simulation", use_container_width=True):
    go_to_page(
        "simulation",
        "Préparation de votre simulation",
        emoji="🚀",
        clear_keys=["simulation", "conversation_finale", "evaluation_result"],
        task="start_simulation",
    )