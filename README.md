# 🏛️ IA Classificateur CEDEAO

Une intelligence artificielle avancée pour la classification douanière selon le Système Harmonisé de la CEDEAO (Communauté Économique des États de l'Afrique de l'Ouest).

## 🎯 Objectif

Cette application permet de classifier automatiquement les produits selon le Tarif Extérieur Commun (TEC) de la CEDEAO en utilisant :

- **Analyse sémantique avancée** avec des modèles de traitement du langage naturel
- **Règles Générales d'Interprétation (RGI)** du Système Harmonisé
- **Base de données complète** du tarif douanier CEDEAO
- **Interface utilisateur moderne** et intuitive

## ✨ Fonctionnalités

### 🤖 IA Avancée
- **Analyse sémantique** : Compréhension du contexte et du sens des descriptions
- **Extraction de caractéristiques** : Matériaux, fonctions, spécifications techniques
- **Application des RGI** : Règles Générales d'Interprétation automatiques
- **Score de confiance** : Évaluation de la précision de la classification

### 📊 Classification Intelligente
- **Recherche multi-niveaux** : Sections, chapitres, sous-positions
- **Matching intelligent** : Correspondance basée sur la similarité sémantique
- **Suggestions d'amélioration** : Recommandations pour optimiser les descriptions
- **Explications détaillées** : Justification des classifications proposées

### 🎨 Interface Moderne
- **Design responsive** : Adaptation à tous les écrans
- **Visualisations claires** : Résultats présentés de manière intuitive
- **Options configurables** : Choix entre IA avancée et classification de base
- **Analyse détaillée** : Mode expert avec explications complètes

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd ICAN
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Télécharger les modèles spaCy (optionnel mais recommandé)**
```bash
python -m spacy download fr_core_news_sm
```

4. **Lancer l'application**
```bash
streamlit run app.py
```

## 📁 Structure du Projet

```
ICAN/
├── app.py                          # Application principale Streamlit
├── ai_classifier.py                # Module d'IA avancée
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation
├── MON-TEC-CEDEAO-SH-2022-FREN-09-04-2024.txt  # Base de données CEDEAO
├── RGI1.jpg                        # Règles Générales d'Interprétation
├── RGI2.jpg
├── RGI3.jpg
├── RGI4.jpg
└── RGI5.jpg
```

## 🔧 Utilisation

### Interface Utilisateur

1. **Description du produit** : Entrez une description détaillée du produit à classifier
2. **Options de classification** :
   - 🤖 **IA avancée** : Active l'analyse sémantique et les règles RGI
   - 📊 **Afficher les détails** : Affiche l'analyse détaillée et les explications
3. **Classification** : Cliquez sur "Classifier le Produit"
4. **Résultats** : Consultez la classification proposée avec le taux d'imposition

### Exemples d'utilisation

#### Ordinateur portable
```
Description : "Ordinateur portable Dell avec processeur Intel i7, 16GB RAM, 512GB SSD, écran 15 pouces"
Résultat attendu : Chapitre 84 - Machines et appareils mécaniques
```

#### Vêtement en coton
```
Description : "T-shirt en coton 100%, manches courtes, col rond, taille M"
Résultat attendu : Chapitre 61 - Vêtements en bonneterie
```

#### Produit chimique
```
Description : "Médicament antibiotique en comprimés, boîte de 20 unités"
Résultat attendu : Chapitre 30 - Produits pharmaceutiques
```

## 🧠 Architecture Technique

### Composants Principaux

1. **CEDEAOClassifier** (`app.py`)
   - Chargement et parsing de la base de données
   - Interface utilisateur Streamlit
   - Orchestration des classificateurs

2. **AdvancedCEDEAOClassifier** (`ai_classifier.py`)
   - Modèle de traitement du langage naturel
   - Analyse sémantique avec SentenceTransformers
   - Application des règles RGI
   - Extraction de caractéristiques

### Technologies Utilisées

- **Streamlit** : Interface utilisateur web
- **SentenceTransformers** : Modèles de similarité sémantique
- **spaCy** : Traitement du langage naturel
- **NLTK** : Outils de traitement de texte
- **scikit-learn** : Calculs de similarité
- **NumPy/Pandas** : Manipulation de données

## 📋 Règles Générales d'Interprétation (RGI)

L'IA applique automatiquement les 6 règles RGI du Système Harmonisé :

1. **RGI 1** : Les titres n'ont qu'une valeur indicative
2. **RGI 2** : Marchandises incomplètes classées comme complètes
3. **RGI 3** : Mélange/assemblage selon la matière prépondérante
4. **RGI 4** : Classification par analogie
5. **RGI 5** : Emballages classés avec les marchandises
6. **RGI 6** : Sous-positions spécifiques prioritaires

## 🎯 Amélioration de la Précision

### Conseils pour de meilleurs résultats

1. **Descriptions détaillées** : Plus d'informations = meilleure classification
2. **Matériaux précis** : Spécifiez les matériaux principaux
3. **Fonction claire** : Décrivez l'usage principal du produit
4. **Spécifications techniques** : Incluez les caractéristiques importantes
5. **Marques et modèles** : Mentionnez les informations de marque si pertinentes

### Exemple de description optimale
```
"Ordinateur portable Dell Latitude 5520, processeur Intel Core i7-1165G7 2.8GHz, 
16GB RAM DDR4, disque SSD 512GB, écran LCD 15.6 pouces 1920x1080, 
carte graphique Intel UHD Graphics, WiFi 6, Bluetooth 5.0, 
batterie lithium-ion 68Wh, poids 1.8kg, couleur noir"
```

## 🔍 Fonctionnalités Avancées

### Analyse Détaillée
- **Extraction de caractéristiques** : Matériaux, fonctions, dimensions
- **Détection de marques** : Identification automatique des marques
- **Spécifications techniques** : Reconnaissance des caractéristiques techniques
- **Recommandations** : Suggestions d'amélioration de la description

### Score de Confiance
- **Évaluation de la précision** : Score de 0% à 100%
- **Facteurs d'évaluation** :
  - Similarité sémantique
  - Application des règles RGI
  - Spécificité de la classification
  - Qualité de la description

## 🛠️ Développement

### Ajout de nouvelles fonctionnalités

1. **Nouveaux modèles d'IA** : Modifiez `ai_classifier.py`
2. **Interface utilisateur** : Éditez `app.py`
3. **Base de données** : Mettez à jour le fichier CEDEAO
4. **Tests** : Ajoutez des tests unitaires

### Structure des données

```python
# Format des résultats de classification
{
    'type': 'subheading',           # Type de classification
    'code': '84.71.90',            # Code SH
    'description': '...',           # Description
    'rate': '5%',                  # Taux d'imposition
    'similarity': 0.85,            # Score de similarité
    'rgi_score': 0.3,              # Score RGI
    'final_score': 0.75            # Score final combiné
}
```

## 📞 Support

Pour toute question ou suggestion d'amélioration :

- **Issues GitHub** : Signalez les bugs ou demandez des fonctionnalités
- **Documentation** : Consultez ce README et les commentaires dans le code
- **Exemples** : Testez avec les exemples fournis

## 📄 Licence

Ce projet est développé pour l'usage institutionnel de la CEDEAO et de ses États membres.

---

**🏛️ IA Classificateur CEDEAO** - Classification douanière intelligente pour l'Afrique de l'Ouest

