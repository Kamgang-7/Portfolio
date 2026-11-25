import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("data/banque_data.db")
cursor = conn.cursor()

# Création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY,
    nom TEXT,
    region TEXT,
    segment TEXT,
    age INTEGER,
    revenu_annuel REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS credits (
    credit_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    type_credit TEXT,
    montant REAL,
    taux_interet REAL,
    statut_defaut INTEGER, -- 0 = Sain, 1 = En défaut
    date_octroi DATE,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
)
""")

# Génération de données réalistes
regions = ["Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France"]
segments = ["Particulier", "Professionnel", "Patrimonial"]
types_credit = ["Immobilier", "Consommation", "Auto", "Trésorerie Pro"]

for i in range(1, 501):
    cursor.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?)", (
        i,
        f"Client_{i}",
        random.choice(regions),
        random.choice(segments),
        random.randint(22, 70),
        round(random.uniform(25000, 150000), 2)
    ))

for j in range(1, 801):
    client_id = random.randint(1, 500)
    t_credit = random.choice(types_credit)
    montant = round(random.uniform(5000, 350000), 2) if t_credit == "Immobilier" else round(random.uniform(2000, 45000), 2)
    taux = round(random.uniform(2.5, 6.8), 2)
    # Simulation d'un risque plus élevé sur certains montants/taux
    defaut = 1 if random.random() < 0.14 else 0
    date_octroi = (datetime.now() - timedelta(days=random.randint(1, 730))).strftime("%Y-%m-%d")
    
    cursor.execute("INSERT INTO credits VALUES (?, ?, ?, ?, ?, ?, ?)", (
        j, client_id, t_credit, montant, taux, defaut, date_octroi
    ))

conn.commit()
conn.close()
print("Base de données banque_data.db générée avec succès !")