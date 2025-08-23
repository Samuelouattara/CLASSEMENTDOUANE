# 🚀 Guide d'Utilisation - Version Avancée IA CEDEAO

## 📋 Vue d'ensemble

La **Version Avancée** de l'IA Classificateur CEDEAO est une application sophistiquée qui utilise l'intelligence artificielle pour classifier automatiquement les produits selon le Système Harmonisé de la CEDEAO.

## 🎯 Fonctionnalités Avancées

### 🤖 Intelligence Artificielle
- **NLP avancé** avec spaCy pour l'analyse linguistique
- **Analyse sémantique** TF-IDF pour la similarité de texte
- **Extraction automatique** de caractéristiques (matériaux, fonctions, marques)
- **Règles RGI** appliquées automatiquement

### 🔍 Analyse Automatique
- **Détection de matériaux** : coton, métal, plastique, verre, etc.
- **Identification de fonctions** : traitement, transport, médical, etc.
- **Reconnaissance de marques** : Dell, Apple, Nike, etc.
- **Extraction de dimensions** : pouces, cm, GB, MHz, etc.
- **Spécifications techniques** : Intel, WiFi, Bluetooth, etc.

## 🚀 Lancement de l'Application

### Option 1 : Interface Web (Recommandée)
```bash
python -m streamlit run app_advanced.py --server.headless true --server.port 8503
```

### Option 2 : Interface Interactive
```bash
python -m streamlit run app_advanced.py
```

### Accès à l'Application
- **URL locale** : http://localhost:8503
- **URL réseau** : http://192.168.1.190:8503
- **URL externe** : http://196.47.128.184:8503

## 📝 Utilisation de l'Interface

### 1. Saisie de Description
- Entrez une description **détaillée** du produit
- Plus la description est précise, meilleure sera la classification
- Incluez les matériaux, marques, dimensions, spécifications techniques

### 2. Options Avancées
- ✅ **Afficher l'analyse détaillée** : Voir l'extraction automatique des caractéristiques
- ✅ **Appliquer les règles RGI** : Utiliser les règles d'interprétation générales

### 3. Classification
- Cliquez sur **"Classifier avec IA Avancée"**
- L'IA analyse automatiquement le texte
- Les résultats s'affichent avec un score de confiance

## 🎯 Exemples d'Utilisation Avancée

### 💻 Ordinateur Portable Détaillé
```
Ordinateur portable Dell Latitude 5520, processeur Intel Core i7-1165G7 2.8GHz, 16GB RAM DDR4, disque SSD 512GB, écran LCD 15.6 pouces 1920x1080, carte graphique Intel UHD Graphics, WiFi 6, Bluetooth 5.0, batterie lithium-ion 68Wh, poids 1.8kg, couleur noir
```

**Résultat attendu :**
- Code SH : 84.71
- Section : XVI (Machines et appareils)
- Taux : 5%
- Confiance : ~85-95%

### 👕 T-shirt avec Spécifications
```
T-shirt en coton 100% bio, manches courtes, col rond, taille M, couleur bleue marine, marque Nike, fabriqué au Bangladesh, poids 180g
```

**Résultat attendu :**
- Code SH : 61.09
- Section : XI (Matières textiles)
- Taux : 20%
- Confiance : ~80-90%

### 💊 Médicament avec Détails
```
Médicament antibiotique Amoxicilline 500mg, comprimés pelliculés, boîte de 20 unités, prescription médicale obligatoire, fabricant Pfizer, date d'expiration 2025
```

**Résultat attendu :**
- Code SH : 30.04
- Section : VI (Produits chimiques)
- Taux : 5%
- Confiance : ~85-95%

### 🚗 Voiture avec Caractéristiques
```
Voiture automobile Toyota Corolla, moteur essence 1.8L 4 cylindres, 4 portes, transmission automatique CVT, année 2023, couleur blanche, équipements: climatisation, GPS, caméra de recul
```

**Résultat attendu :**
- Code SH : 87.03
- Section : XVII (Matériel de transport)
- Taux : 10%
- Confiance : ~90-95%

## 🔬 Analyse Détaillée

### Caractéristiques Extraites
L'IA extrait automatiquement :
- **Matériaux** : coton, métal, plastique, verre, etc.
- **Fonctions** : traitement, transport, médical, alimentaire, etc.
- **Marques** : Dell, Apple, Nike, Toyota, etc.
- **Dimensions** : 15.6 pouces, 512GB, 2.8GHz, etc.
- **Spécifications techniques** : Intel, WiFi, Bluetooth, SSD, etc.

### Explication de Classification
L'IA génère une explication détaillée :
- Code SH attribué et justification
- Caractéristiques détectées
- Règles RGI appliquées
- Score de confiance

### Alternatives Proposées
L'IA propose jusqu'à 5 alternatives de classification avec leurs scores de confiance.

## ⚖️ Règles RGI Appliquées

### RGI 1 : Titres indicatifs seulement
Les titres des sections et chapitres n'ont qu'une valeur indicative.

### RGI 2 : Marchandises incomplètes
Les marchandises incomplètes sont classées comme complètes.

### RGI 3 : Mélange selon matière prépondérante
Les mélanges sont classés selon la matière prépondérante.

### RGI 4 : Classification par analogie
Classification par analogie avec des produits similaires.

### RGI 5 : Emballages avec marchandises
Les emballages sont classés avec les marchandises qu'ils contiennent.

### RGI 6 : Sous-positions spécifiques prioritaires
Les sous-positions spécifiques ont priorité sur les générales.

## 💡 Conseils pour une Meilleure Classification

### 1. Description Détaillée
- Incluez les **matériaux** principaux
- Précisez la **fonction** principale
- Mentionnez la **marque** si applicable
- Ajoutez les **spécifications techniques**
- Indiquez les **dimensions** importantes

### 2. Mots-clés Efficaces
- **Matériaux** : coton, métal, plastique, verre, bois, cuir
- **Fonctions** : traitement, transport, médical, alimentaire, textile
- **Marques** : Dell, Apple, Nike, Toyota, Pfizer
- **Spécifications** : Intel, WiFi, Bluetooth, SSD, RAM

### 3. Évitez les Ambiguïtés
- Utilisez des termes précis
- Évitez les abréviations non standard
- Précisez le contexte d'utilisation

## 🔧 Dépannage

### Problème : Aucune classification trouvée
**Solution :**
- Vérifiez que la description contient des mots-clés reconnaissables
- Ajoutez plus de détails sur les matériaux et fonctions
- Essayez avec une description plus détaillée

### Problème : Score de confiance faible
**Solution :**
- Améliorez la description avec plus de spécifications
- Incluez les marques et modèles
- Ajoutez les dimensions et caractéristiques techniques

### Problème : Classification incorrecte
**Solution :**
- Vérifiez que la description est claire et précise
- Utilisez les suggestions d'amélioration fournies
- Consultez les alternatives proposées

## 📊 Statistiques Système

L'application affiche en temps réel :
- **Sections** : Nombre de sections du SH chargées
- **Chapitres** : Nombre de chapitres disponibles
- **Sous-positions** : Nombre de sous-positions avec taux
- **Produits en base** : Nombre de produits dans la base de données

## 🎉 Avantages de la Version Avancée

### Comparaison avec la Version Simple
| Fonctionnalité | Version Simple | Version Avancée |
|----------------|----------------|-----------------|
| Classification de base | ✅ | ✅ |
| Score de pertinence | ✅ | ✅ |
| Analyse sémantique | ❌ | ✅ |
| Extraction automatique | ❌ | ✅ |
| Règles RGI | ❌ | ✅ |
| Interface moderne | ❌ | ✅ |
| Explications détaillées | ❌ | ✅ |
| Suggestions d'amélioration | ❌ | ✅ |

### Bénéfices
1. **Précision accrue** grâce à l'analyse sémantique
2. **Automatisation complète** de l'extraction des caractéristiques
3. **Application intelligente** des règles RGI
4. **Interface utilisateur moderne** et intuitive
5. **Explications détaillées** pour chaque classification
6. **Suggestions d'amélioration** pour optimiser les descriptions

## 🚀 Prochaines Étapes

1. **Testez** l'application avec différents types de produits
2. **Améliorez** vos descriptions en suivant les suggestions
3. **Explorez** l'analyse détaillée pour comprendre les classifications
4. **Utilisez** les alternatives proposées pour des cas complexes

---

**🎯 Objectif :** Classification douanière précise et automatisée avec intelligence artificielle avancée.

**🔧 Support :** L'application est conçue pour être intuitive et fournir des explications détaillées pour chaque classification.

