# 🤖 Copilote Data & Risques IA — Assistant Text-to-SQL

> **Contexte (Étude de cas) :** Permettre aux équipes métiers (Direction des Risques et Direction Commerciale) d'interroger une base de données de crédits bancaires en langage naturel, sans compétence SQL et sans attendre le support de l'équipe BI.

## 🎯 Problématique & Valeur Métier
* **Problème :** Les demandes ad hoc de extraction de données mobilisent les Data Analysts sur des tâches répétitives et ralentissent la prise de décision.
* **Solution :** Une interface conversationnelle propulsée par un LLM (Gemini) capable de traduire une question métier en requête SQL sécurisée, d'exécuter l'extraction, de générer une visualisation interactive et de rédiger une synthèse exécutive.
* **Garde-fous intégrés :** Blocage strict de toute requête d'écriture/suppression (seul `SELECT` est autorisé) et affichage transparent du code SQL généré pour auditabilité.

## 🛠️ Architecture & Stack Technique
* **Base de données :** SQLite (modèle relationnel `clients` / `credits`)
* **IA Générative :** Google GenAI SDK (`gemini-2.5-flash`)
* **Backend & Frontend :** Python, Streamlit, Pandas, Plotly

## 🚀 Tester l'application en direct
👉 **[Accéder à la démo interactive en ligne]((https://portfolio-b4utwbmwhkrqs5uapgtpjx.streamlit.app/))**
