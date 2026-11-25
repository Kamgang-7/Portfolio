import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from google import genai
import os

# Configuration de la page
st.set_page_config(page_title="Copilote Data & Risques IA", layout="wide")
st.title("🤖 Assistant Intelligent d'Analyse de Données (Text-to-SQL)")
st.markdown(
    "Posez une question métier en langage naturel sur le portefeuille de crédits."
)

# Récupération de la clé API (via secrets Streamlit en prod ou variable locale)
api_key = st.sidebar.text_input(
    "Clé API Gemini", type="password", value=os.getenv("GEMINI_API_KEY", "")
)

# Schéma de la base envoyé au LLM pour qu'il comprenne les tables
DB_SCHEMA = """
Tables disponibles dans SQLite :
1. clients (client_id, nom, region, segment, age, revenu_annuel)
2. credits (credit_id, client_id, type_credit, montant, taux_interet, statut_defaut, date_octroi)
Note : statut_defaut = 1 signifie que le crédit est en défaut de paiement, 0 signifie sain.
"""

# Exemples cliquables pour le recruteur
st.sidebar.subheader("💡 Exemples de questions à tester")
exemple = st.sidebar.radio(
    "Cliquez sur une question :",
    [
        "Quel est le montant total des crédits et le taux de défaut par région ?",
        "Top 5 des segments clients avec le revenu annuel moyen le plus élevé",
        "Répartition du montant total accordé par type de crédit",
        "Quels sont les 10 clients ayant les plus gros montants en défaut ?",
    ],
)

question = st.text_input("Votre question métier :", value=exemple)

if st.button("Analyser les données", type="primary"):
    if not api_key:
        st.error("Veuillez renseigner une clé API Gemini dans le menu à gauche.")
    else:
        with st.spinner("Traduction en SQL et analyse en cours..."):
            try:
                client = genai.Client(api_key=api_key)

                # 1. Génération de la requête SQL
                prompt_sql = f"""
                Tu es un expert Data Analyst SQL. Convertis la question suivante en une requête SQLite valide.
                Schéma : {DB_SCHEMA}
                Règles strictes :
                - Renvoie UNIQUEMENT le code SQL brut, sans balises markdown (```sql), sans explication.
                - Utilise uniquement des requêtes SELECT (lecture seule).
                Question : {question}
                """
                response_sql = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt_sql
                )
                sql_query = (
                    response_sql.text.strip()
                    .replace("```sql", "")
                    .replace("```", "")
                    .strip()
                )

                # Garde-fou de sécurité (très apprécié en entretien)
                if not sql_query.upper().startswith("SELECT"):
                    st.error(
                        "Action bloquée : seules les requêtes de lecture (SELECT) sont autorisées."
                    )
                    st.stop()

                # 2. Exécution sur SQLite
                conn = sqlite3.connect("data/banque_data.db")
                df = pd.read_sql_query(sql_query, conn)
                conn.close()

                # 3. Affichage des résultats
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader("📊 Résultats extraits")
                    st.dataframe(df, use_container_width=True)
                    with st.expander("🔍 Voir la requête SQL générée par l'IA"):
                        st.code(sql_query, language="sql")

                with col2:
                    st.subheader("📈 Visualisation automatique")
                    if len(df.columns) >= 2 and len(df) > 1:
                        fig = px.bar(
                            df, x=df.columns[0], y=df.columns[1], text_auto=True
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("KPI unique détecté : affichage sous forme de tableau.")

                # 4. Synthèse métier générée par l'IA
                prompt_analyse = f"""
                En tant que Consultant Business & Data Analyst, rédige une synthèse courte (3 phrases max) 
                et une recommandation métier à partir de ces données :
                Question : {question}
                Données : {df.to_string()}
                """
                synth = client.models.generate_content(
                    model="gemini-2.5-flash", contents=prompt_analyse
                )
                st.success(f"**💡 Analyse du Consultant IA :**\n\n{synth.text}")

            except Exception as e:
                st.error(f"Erreur lors de l'analyse : {e}")
