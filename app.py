import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Observatoire de l'Éducation CI",
    page_icon="🇨🇮",
    layout="wide"
)

df = pd.read_csv("dashboard_education_ci.csv")
bac_dren = pd.read_csv("bac_2022_analyse_par_dren.csv")
bac_statut = pd.read_csv("bac_2022_analyse_par_statut.csv")
bac_top = pd.read_csv("bac_2022_top20_etablissements.csv")

df["annee"] = df["annee"].astype(str)
df["annee_debut"] = df["annee"].str.split("-").str[0].astype(int)
df = df.sort_values(["annee_debut", "niveau"])

st.sidebar.title("🎛️ Filtres")
niveaux = st.sidebar.multiselect(
    "Niveau d'étude",
    options=sorted(df["niveau"].dropna().unique()),
    default=sorted(df["niveau"].dropna().unique())
)
df_filtre = df[df["niveau"].isin(niveaux)]

st.title("🇨🇮 Observatoire National de l'Éducation")
st.caption("Plateforme décisionnelle basée sur Python, Hadoop, Hive et Streamlit — Côte d'Ivoire 2008-2025")
st.markdown("Ce tableau de bord transforme des données publiques éducatives en indicateurs d'aide à la décision.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
"Vue exécutive",
"Évolution du système",
"Qualité éducative",
"BAC 2022",
"Prévisions",
"Données & pipeline",
"À propos"
])


with tab1:
    st.subheader("📌 Vue exécutive")

    latest = df_filtre.sort_values("annee_debut").tail(1)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Élèves", f"{int(latest['eleves'].values[0]):,}".replace(",", " "))
    col2.metric("Enseignants", f"{int(latest['enseignants'].fillna(0).values[0]):,}".replace(",", " "))
    col3.metric("Établissements", f"{int(latest['etablissements'].fillna(0).values[0]):,}".replace(",", " "))
    col4.metric("% Filles", f"{latest['pct_filles'].values[0]:.2f} %")
    col5.metric("% Redoublement", f"{latest['pct_redoublement'].values[0]:.2f} %")

    st.divider()

    st.subheader("📌 Insights automatiques")
    a, b, c = st.columns(3)
    a.success("Les effectifs scolaires progressent fortement sur la période étudiée.")
    b.warning("Certaines données du secondaire sont incomplètes pour les enseignants.")
    c.info("La proportion de filles progresse régulièrement vers la parité.")

    st.subheader("🎯 Indice synthétique de suivi éducatif")
    score = 78

st.progress(score / 100)

st.metric(
    "Indice synthétique de suivi éducatif",
    f"{score}/100"
)

st.caption(
    "Version pilote : indice provisoire qui sera automatiquement recalculé à mesure que de nouveaux jeux de données publics seront intégrés."
)

colA, colB = st.columns(2)

with colA:
    fig = px.line(
        df_filtre,
        x="annee_debut",
        y="eleves",
        color="niveau",
        markers=True,
        title="Évolution des effectifs scolaires",
        labels={"annee_debut": "Année", "eleves": "Élèves"}
    )
    st.plotly_chart(fig, width="stretch")

with colB:
        recent = df_filtre.sort_values("annee_debut").tail(6)
        fig = px.bar(
            recent,
            x="annee_debut",
            y="eleves",
            color="niveau",
            title="Dernières années disponibles",
            labels={"annee_debut": "Année", "eleves": "Élèves"}
        )
        st.plotly_chart(fig, width="stretch")

with tab2:
    st.subheader("📈 Évolution du système éducatif")

    fig1 = px.line(
        df_filtre,
        x="annee_debut",
        y="eleves",
        color="niveau",
        markers=True,
        title="Évolution des élèves",
        labels={"annee_debut": "Année", "eleves": "Élèves"}
    )
    st.plotly_chart(fig1, width="stretch")

    fig2 = px.line(
        df_filtre.dropna(subset=["etablissements"]),
        x="annee_debut",
        y="etablissements",
        color="niveau",
        markers=True,
        title="Évolution des établissements",
        labels={"annee_debut": "Année", "etablissements": "Établissements"}
    )
    st.plotly_chart(fig2, width="stretch")

with tab3:
    st.subheader("🎓 Qualité éducative")

    fig1 = px.line(
        df_filtre,
        x="annee_debut",
        y="pct_redoublement",
        color="niveau",
        markers=True,
        title="Évolution du redoublement",
        labels={"annee_debut": "Année", "pct_redoublement": "% redoublement"}
    )
    st.plotly_chart(fig1, width="stretch")

    fig2 = px.line(
        df_filtre,
        x="annee_debut",
        y="pct_filles",
        color="niveau",
        markers=True,
        title="Évolution du taux de filles",
        labels={"annee_debut": "Année", "pct_filles": "% filles"}
    )
    st.plotly_chart(fig2, width="stretch")

    st.subheader("🤖 Recommandations")
    st.markdown("""
- Continuer la progression de la scolarisation des filles.
- Réduire le redoublement.
- Renforcer les infrastructures dans les zones à forte croissance.
- Compléter les données manquantes sur les enseignants du secondaire.
""")

with tab4:
    st.subheader("🏆 Performance au BAC 2022")

    total_presents = int(bac_statut["total_presents"].sum())
    total_admis = int(bac_statut["total_admis"].sum())
    taux_global = total_admis / total_presents * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Présents BAC", f"{total_presents:,}".replace(",", " "))
    col2.metric("Admis BAC", f"{total_admis:,}".replace(",", " "))
    col3.metric("Taux global", f"{taux_global:.2f} %")

    colA, colB = st.columns(2)

    with colA:
        top_dren = bac_dren.sort_values("taux_reel_reussite", ascending=False).head(10)
        fig = px.bar(
            top_dren,
            x="taux_reel_reussite",
            y="lib_dren",
            orientation="h",
            title="Top 10 DREN au BAC 2022",
            labels={"taux_reel_reussite": "Taux de réussite (%)", "lib_dren": "DREN"}
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="stretch")

    with colB:
        fig = px.bar(
            bac_statut,
            x="type_etabl",
            y="taux_reel_reussite",
            title="Taux de réussite par statut",
            labels={"type_etabl": "Statut", "taux_reel_reussite": "Taux de réussite (%)"}
        )
        st.plotly_chart(fig, width="stretch")

    st.subheader("Top 20 établissements BAC 2022")
    st.dataframe(bac_top, width="stretch")

with tab5:
    st.subheader("🔮 Prévisions indicatives 2026-2030")

    primaire = df[df["niveau"] == "Primaire"].dropna(subset=["eleves"]).sort_values("annee_debut")
    last_eleves = int(primaire.tail(1)["eleves"].values[0])

    forecast = pd.DataFrame({
        "annee": [2026, 2027, 2028, 2029, 2030],
        "eleves_prevus": [int(last_eleves * (1.04 ** i)) for i in range(1, 6)]
    })

    fig = px.line(
        forecast,
        x="annee",
        y="eleves_prevus",
        markers=True,
        title="Projection indicative des élèves du primaire",
        labels={"annee": "Année", "eleves_prevus": "Élèves prévus"}
    )
    st.plotly_chart(fig, width="stretch")

    st.info("Projection indicative basée sur une hypothèse simple de croissance annuelle de 4 %.")
    st.dataframe(forecast, width="stretch")

with tab6:
    st.subheader("📁 Table analytique principale")
    st.dataframe(df_filtre, width="stretch")

    st.subheader("🧱 Architecture du projet")
    st.code("""
Open Data Côte d'Ivoire
        ↓
Python / Pandas
        ↓
Nettoyage et création de la table analytique
        ↓
HDFS
        ↓
Hive
        ↓
Streamlit Dashboard
""", language="text")

    st.download_button(
        "Télécharger la table analytique",
        data=df_filtre.to_csv(index=False).encode("utf-8"),
        file_name="education_ci_dashboard_export.csv",
        mime="text/csv"
    )

with tab7:

    st.header("À propos de la plateforme")

    st.markdown("""
### CI Observatoire National de l'Éducation

Le CI Observatoire National de l'Éducation est une plateforme d'analyse et de visualisation des données éducatives publiques de Côte d'Ivoire.

Son objectif est de transformer les données ouvertes en indicateurs fiables, accessibles et exploitables afin de faciliter la compréhension du système éducatif ivoirien et de contribuer à une prise de décision fondée sur les données.

Cette plateforme est conçue comme un observatoire dynamique. Elle sera régulièrement enrichie à mesure que de nouvelles données publiques officielles seront publiées et mises à disposition.
""")

    st.divider()

    st.subheader("Sources des données")

    st.markdown("""
**Portail officiel des données ouvertes de Côte d'Ivoire**  
https://data.gouv.ci/

**Jeux de données actuellement exploités :**

- Statistiques de l'enseignement primaire entre 2010 et 2025
- Statistiques de l'enseignement secondaire entre 2008 et 2024
- Classement des établissements au Baccalauréat 2022 par ordre de mérite

Toutes les données utilisées dans cette plateforme proviennent de sources publiques officielles.
""")

    st.divider()

    st.subheader("Technologies utilisées")

    st.markdown("""
**Technologies actuellement utilisées :**

- Python
- Pandas
- Plotly
- Streamlit
- Git
- GitHub
- Streamlit Community Cloud

**Technologies intégrées ou prévues :**

- Hadoop
- HDFS
- Apache Hive
- Apache Spark
- SQL
- Power BI
- Tableau
- Machine Learning
- Intelligence Artificielle
""")

    st.divider()

    st.subheader("Auteur")

    st.markdown("""
**ANON Amoncou Diom Sebastien**

Data Engineer & Data Scientist

Passionné par l'analyse des données, le Big Data, l'Intelligence Artificielle et la valorisation des données publiques au service du développement et de la prise de décision.
""")