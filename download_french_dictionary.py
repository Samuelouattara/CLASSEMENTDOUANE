#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour télécharger un dictionnaire français complet
"""

import requests
import re
import time
from typing import Set, List
import os

def download_from_github():
    """Télécharge un dictionnaire français depuis GitHub"""
    
    # Sources de dictionnaires français sur GitHub
    sources = [
        "https://raw.githubusercontent.com/words/an-array-of-french-words/master/words.txt",
        "https://raw.githubusercontent.com/words/fr-wordlist/main/words.txt",
        "https://raw.githubusercontent.com/words/french-words/master/words.txt",
        "https://raw.githubusercontent.com/words/french-wordlist/main/words.txt",
        "https://raw.githubusercontent.com/words/french-dictionary/master/words.txt"
    ]
    
    all_words = set()
    
    for i, source in enumerate(sources, 1):
        try:
            print(f"🔍 Tentative {i}/{len(sources)}: {source}")
            response = requests.get(source, timeout=15)
            
            if response.status_code == 200:
                content = response.text
                words = set()
                
                for line in content.split('\n'):
                    word = line.strip().lower()
                    if word and len(word) > 1 and word.isalpha():
                        words.add(word)
                
                if words:
                    all_words.update(words)
                    print(f"   ✅ {len(words)} mots récupérés")
                    break  # On s'arrête au premier succès
                else:
                    print(f"   ⚠️ Aucun mot valide trouvé")
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        time.sleep(1)  # Pause entre les tentatives
    
    return all_words

def download_from_wiktionary():
    """Télécharge des mots français depuis Wiktionary"""
    
    print("🔍 Téléchargement depuis Wiktionary...")
    
    # URL de la liste des mots français sur Wiktionary
    url = "https://fr.wiktionary.org/wiki/Catégorie:Mots_en_français"
    
    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            # Chercher les liens vers les mots
            pattern = r'href="/wiki/([^"]*)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, response.text)
            
            words = set()
            for link, word in matches:
                word = word.strip().lower()
                if word and len(word) > 1 and word.isalpha():
                    words.add(word)
            
            print(f"✅ {len(words)} mots récupérés depuis Wiktionary")
            return words
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur Wiktionary: {e}")
    
    return set()

def create_comprehensive_dictionary():
    """Crée un dictionnaire français complet avec des mots courants"""
    
    print("🔄 Création d'un dictionnaire français complet...")
    
    # Mots français courants par catégorie
    categories = {
        "articles": {"le", "la", "les", "un", "une", "des", "ce", "cette", "ces", "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses", "notre", "votre", "leur", "leurs"},
        "pronoms": {"je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "me", "te", "se", "lui", "leur", "moi", "toi", "soi", "eux", "elles", "ceci", "cela", "ça"},
        "conjonctions": {"et", "ou", "mais", "donc", "car", "ni", "or", "puis", "ensuite", "alors", "quand", "si", "comme", "que", "qui", "quoi", "où", "pourquoi", "comment"},
        "prepositions": {"à", "de", "en", "dans", "sur", "sous", "avec", "sans", "pour", "par", "vers", "chez", "entre", "contre", "devant", "derrière", "près", "loin", "autour"},
        "adverbes": {"très", "trop", "peu", "beaucoup", "assez", "plus", "moins", "bien", "mal", "vite", "lentement", "maintenant", "hier", "aujourd'hui", "demain", "toujours", "jamais", "souvent", "rarement", "parfois", "ici", "là", "ailleurs", "partout"},
        "verbes": {"être", "avoir", "faire", "aller", "venir", "voir", "dire", "savoir", "pouvoir", "vouloir", "devoir", "prendre", "donner", "mettre", "tenir", "partir", "arriver", "rester", "passer", "sortir", "entrer", "monter", "descendre", "ouvrir", "fermer", "commencer", "finir", "continuer", "arrêter", "changer"},
        "adjectifs": {"grand", "petit", "bon", "mauvais", "beau", "laid", "nouveau", "vieux", "jeune", "chaud", "froid", "long", "court", "large", "étroit", "lourd", "léger", "fort", "faible", "rapide", "lent", "facile", "difficile", "possible", "impossible", "vrai", "faux", "juste", "clair", "sombre", "propre", "sale", "sec", "mouillé", "plein", "vide", "ouvert", "fermé", "libre", "occupé", "calme", "bruyant", "doux", "dur", "souple", "rigide", "lisse", "rugueux"},
        "noms": {"homme", "femme", "enfant", "personne", "groupe", "famille", "ami", "travail", "maison", "ville", "pays", "monde", "temps", "jour", "nuit", "matin", "soir", "semaine", "mois", "année", "heure", "minute", "seconde", "eau", "air", "feu", "terre", "soleil", "lune", "étoile", "ciel", "mer", "montagne", "forêt", "champ", "route", "chemin", "pont", "porte", "fenêtre", "mur", "toit", "sol", "plafond", "escalier", "couloir", "salle", "chambre", "cuisine", "bureau", "magasin", "école", "hôpital", "banque", "restaurant", "hôtel", "théâtre", "cinéma", "musée", "parc", "jardin", "voiture", "train", "avion", "bateau", "vélo", "moto", "bus", "métro", "livre", "journal", "lettre", "téléphone", "radio", "télévision", "musique", "film", "photo", "image", "couleur", "forme", "taille", "poids", "prix", "argent", "monnaie", "billet", "pièce", "carte", "chèque", "facture", "nom", "prénom", "âge", "adresse", "email", "date", "lieu", "raison", "cause", "effet", "résultat", "problème", "solution", "question", "réponse", "exemple", "cas", "situation", "état", "condition", "niveau", "qualité", "quantité", "nombre", "total", "partie", "ensemble", "groupe", "système", "méthode", "technique", "procédé", "processus", "étape", "phase", "période", "moment", "instant", "fois"},
        "materiaux": {"acier", "aluminium", "cuivre", "fer", "plastique", "bois", "cuir", "tissu", "coton", "laine", "soie", "verre", "céramique", "caoutchouc", "papier", "carton", "métal", "or", "argent", "bronze", "zinc"},
        "alimentation": {"viande", "poisson", "légumes", "fruits", "céréales", "riz", "blé", "maïs", "sucre", "sel", "épices", "huile", "beurre", "fromage", "lait", "œufs", "pain", "pâtes", "chocolat", "café", "thé", "vin"},
        "vetements": {"chemise", "pantalon", "robe", "jupe", "veste", "manteau", "chaussures", "bottes", "sandales", "chaussettes", "cravate", "écharpe", "gants", "chapeau", "casquette", "ceinture", "sac", "valise"},
        "electronique": {"téléphone", "ordinateur", "tablette", "écran", "clavier", "souris", "imprimante", "scanner", "caméra", "télévision", "radio", "lecteur", "écouteurs", "chargeur", "batterie", "câble"},
        "vehicules": {"voiture", "camion", "moto", "vélo", "bus", "train", "avion", "bateau", "pneu", "moteur", "roue", "volant", "siège", "portière", "phare", "pare-brise", "rétroviseur"},
        "outils": {"marteau", "tournevis", "scie", "perceuse", "vis", "écrou", "boulon", "clé", "pince", "machine", "pompe", "compresseur", "générateur", "transformateur"},
        "medical": {"médicament", "pilule", "sirop", "pansement", "thermomètre", "stéthoscope", "seringue", "antibiotique", "vitamine", "analgésique", "antiseptique", "bandage"},
        "cosmetiques": {"savon", "shampooing", "dentifrice", "brosse", "peigne", "miroir", "crème", "parfum", "maquillage", "rouge", "mascara", "vernis", "déodorant", "gel", "lotion"},
        "sports": {"ballon", "raquette", "filet", "but", "gant", "casque", "protège", "tapis", "corde", "livre", "magazine", "journal", "crayon", "stylo", "cahier", "carte", "jeu"},
        "construction": {"brique", "ciment", "béton", "plâtre", "peinture", "vernis", "colle", "clou", "planche", "poutre", "tuile", "carrelage", "isolation", "électricité", "plomberie"},
        "agriculture": {"semence", "engrais", "pesticide", "tracteur", "moissonneuse", "irrigation", "serre", "outil", "système", "récolte", "plantation", "culture"},
        "chimie": {"acide", "base", "solvant", "catalyseur", "polymère", "résine", "adhésif", "lubrifiant", "carburant", "gaz", "liquide", "poudre", "granule", "cristal"},
        "emballage": {"carton", "boîte", "sac", "film", "ruban", "étiquette", "palette", "conteneur", "emballage", "protection", "isolation", "coussins", "mousse"},
        "energie": {"électricité", "gaz", "pétrole", "charbon", "solaire", "éolien", "nucléaire", "batterie", "accumulateur", "pile", "générateur", "transformateur"},
        "communication": {"téléphone", "internet", "réseau", "signal", "antenne", "satellite", "fibre", "modem", "routeur", "switch", "serveur", "données", "information", "message"},
        "securite": {"serrure", "clé", "alarme", "caméra", "détecteur", "extincteur", "casque", "gilet", "gants", "lunettes", "masque", "protection", "sécurité", "surveillance"}
    }
    
    all_words = set()
    
    for category, words in categories.items():
        all_words.update(words)
        print(f"   {category}: {len(words)} mots")
    
    # Ajouter des variations (pluriels, féminins, etc.)
    variations = set()
    for word in all_words:
        # Pluriels
        if word.endswith('al'):
            variations.add(word[:-2] + 'aux')
        elif word.endswith('au'):
            variations.add(word + 'x')
        elif word.endswith('eu'):
            variations.add(word + 'x')
        elif not word.endswith('s'):
            variations.add(word + 's')
        
        # Féminins pour les adjectifs
        if word.endswith('eux'):
            variations.add(word[:-3] + 'euse')
        elif word.endswith('er'):
            variations.add(word[:-2] + 'ère')
        elif word.endswith('f'):
            variations.add(word[:-1] + 've')
        elif word.endswith('x'):
            variations.add(word[:-1] + 'se')
    
    all_words.update(variations)
    
    print(f"✅ Dictionnaire créé: {len(all_words)} mots")
    return all_words

def save_dictionary(words: Set[str], filename: str = "dictionnaire_francais.txt"):
    """Sauvegarde le dictionnaire dans un fichier"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for word in sorted(words):
                f.write(word + '\n')
        
        print(f"✅ Dictionnaire sauvegardé dans {filename}")
        print(f"   {len(words)} mots écrits")
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")

def main():
    """Fonction principale"""
    
    print("=" * 70)
    print("TÉLÉCHARGEMENT DU DICTIONNAIRE FRANÇAIS")
    print("=" * 70)
    
    print("\nOptions disponibles:")
    print("1. Télécharger depuis GitHub (rapide)")
    print("2. Télécharger depuis Wiktionary (moyen)")
    print("3. Créer un dictionnaire complet (rapide)")
    print("4. Combiner toutes les sources (complet)")
    
    choice = input("\nVotre choix (1-4): ").strip()
    
    all_words = set()
    
    if choice == "1":
        print("\n🔄 Téléchargement depuis GitHub...")
        words = download_from_github()
        all_words.update(words)
        
    elif choice == "2":
        print("\n🔄 Téléchargement depuis Wiktionary...")
        words = download_from_wiktionary()
        all_words.update(words)
        
    elif choice == "3":
        print("\n🔄 Création d'un dictionnaire complet...")
        words = create_comprehensive_dictionary()
        all_words.update(words)
        
    elif choice == "4":
        print("\n🔄 Combinaison de toutes les sources...")
        
        # GitHub
        print("   📥 GitHub...")
        github_words = download_from_github()
        all_words.update(github_words)
        
        # Wiktionary
        print("   📥 Wiktionary...")
        wiktionary_words = download_from_wiktionary()
        all_words.update(wiktionary_words)
        
        # Dictionnaire complet
        print("   📥 Dictionnaire complet...")
        complete_words = create_comprehensive_dictionary()
        all_words.update(complete_words)
        
    else:
        print("❌ Choix invalide")
        return
    
    # Sauvegarder le dictionnaire final
    if all_words:
        save_dictionary(all_words)
        
        print(f"\n🎉 DICTIONNAIRE CRÉÉ AVEC SUCCÈS !")
        print(f"📊 Total: {len(all_words)} mots français")
        
        # Afficher quelques exemples
        sample_words = list(all_words)[:20]
        print(f"📝 Exemples: {', '.join(sample_words)}")
        
        # Statistiques
        print(f"\n📈 Statistiques:")
        print(f"   Mots uniques: {len(all_words)}")
        print(f"   Longueur moyenne: {sum(len(word) for word in all_words) / len(all_words):.1f} caractères")
        
    else:
        print("❌ Aucun mot récupéré")

if __name__ == "__main__":
    main()
