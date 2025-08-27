#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer un dictionnaire français complet
"""

import os
import requests
from pathlib import Path

def download_french_dictionary():
    """Télécharge un dictionnaire français depuis plusieurs sources"""
    
    # Sources de dictionnaires français
    sources = [
        "https://raw.githubusercontent.com/words/an-array-of-french-words/master/words.txt",
        "https://raw.githubusercontent.com/words/fr-wordlist/main/words.txt",
        "https://raw.githubusercontent.com/words/french-words/master/words.txt"
    ]
    
    words = set()
    
    for source in sources:
        try:
            print(f"Tentative de téléchargement depuis: {source}")
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                content = response.text
                # Nettoyer et ajouter les mots
                for line in content.split('\n'):
                    word = line.strip().lower()
                    if word and len(word) > 1:
                        words.add(word)
                print(f"✓ {len(words)} mots récupérés depuis {source}")
                break
        except Exception as e:
            print(f"✗ Erreur avec {source}: {e}")
            continue
    
    return words

def create_comprehensive_dictionary():
    """Crée un dictionnaire français complet avec des mots courants"""
    
    # Mots français courants pour le classement douanier
    mots_douane = {
        # Matériaux
        "acier", "aluminium", "cuivre", "fer", "plastique", "bois", "cuir", "tissu", "coton", "laine", "soie",
        "verre", "céramique", "caoutchouc", "papier", "carton", "métal", "or", "argent", "bronze", "zinc",
        
        # Produits alimentaires
        "viande", "poisson", "légumes", "fruits", "céréales", "riz", "blé", "maïs", "sucre", "sel", "épices",
        "huile", "beurre", "fromage", "lait", "œufs", "pain", "pâtes", "chocolat", "café", "thé", "vin",
        
        # Vêtements et textiles
        "chemise", "pantalon", "robe", "jupe", "veste", "manteau", "chaussures", "bottes", "sandales",
        "chaussettes", "cravate", "écharpe", "gants", "chapeau", "casquette", "ceinture", "sac", "valise",
        
        # Électronique
        "téléphone", "ordinateur", "tablette", "écran", "clavier", "souris", "imprimante", "scanner",
        "caméra", "télévision", "radio", "lecteur", "écouteurs", "chargeur", "batterie", "câble",
        
        # Véhicules et transport
        "voiture", "camion", "moto", "vélo", "bus", "train", "avion", "bateau", "pneu", "moteur",
        "roue", "volant", "siège", "portière", "phare", "pare-brise", "rétroviseur",
        
        # Outils et machines
        "marteau", "tournevis", "scie", "perceuse", "vis", "écrou", "boulon", "clé", "pince",
        "machine", "moteur", "pompe", "compresseur", "générateur", "transformateur",
        
        # Médical et pharmaceutique
        "médicament", "pilule", "sirop", "pansement", "thermomètre", "stéthoscope", "seringue",
        "antibiotique", "vitamine", "analgésique", "antiseptique", "bandage",
        
        # Cosmétiques et hygiène
        "savon", "shampooing", "dentifrice", "brosse", "peigne", "miroir", "crème", "parfum",
        "maquillage", "rouge", "mascara", "vernis", "déodorant", "gel", "lotion",
        
        # Sports et loisirs
        "ballon", "raquette", "filet", "but", "gant", "casque", "protège", "tapis", "corde",
        "livre", "magazine", "journal", "crayon", "stylo", "cahier", "carte", "jeu",
        
        # Construction et bricolage
        "brique", "ciment", "béton", "plâtre", "peinture", "vernis", "colle", "clou",
        "planche", "poutre", "tuile", "carrelage", "isolation", "électricité", "plomberie",
        
        # Agriculture
        "semence", "engrais", "pesticide", "tracteur", "moissonneuse", "irrigation",
        "serre", "outil", "système", "récolte", "plantation", "culture",
        
        # Chimie et industrie
        "acide", "base", "solvant", "catalyseur", "polymère", "résine", "adhésif",
        "lubrifiant", "carburant", "gaz", "liquide", "poudre", "granule", "cristal",
        
        # Emballage et logistique
        "carton", "boîte", "sac", "film", "ruban", "étiquette", "palette", "conteneur",
        "emballage", "protection", "isolation", "coussins", "mousse", "papier",
        
        # Énergie
        "électricité", "gaz", "pétrole", "charbon", "solaire", "éolien", "nucléaire",
        "batterie", "accumulateur", "pile", "générateur", "transformateur", "câble",
        
        # Communication
        "téléphone", "internet", "réseau", "signal", "antenne", "satellite", "fibre",
        "modem", "routeur", "switch", "serveur", "données", "information", "message",
        
        # Sécurité
        "serrure", "clé", "alarme", "caméra", "détecteur", "extincteur", "casque",
        "gilet", "gants", "lunettes", "masque", "protection", "sécurité", "surveillance"
    }
    
    # Mots généraux français courants
    mots_generaux = {
        # Articles et déterminants
        "le", "la", "les", "un", "une", "des", "ce", "cette", "ces", "mon", "ma", "mes",
        "ton", "ta", "tes", "son", "sa", "ses", "notre", "votre", "leur", "leurs",
        
        # Pronoms
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "me", "te", "se",
        "lui", "leur", "moi", "toi", "soi", "eux", "elles", "ceci", "cela", "ça",
        
        # Conjonctions
        "et", "ou", "mais", "donc", "car", "ni", "or", "puis", "ensuite", "alors",
        "quand", "si", "comme", "que", "qui", "quoi", "où", "pourquoi", "comment",
        
        # Prépositions
        "à", "de", "en", "dans", "sur", "sous", "avec", "sans", "pour", "par", "vers",
        "chez", "entre", "contre", "devant", "derrière", "près", "loin", "autour",
        
        # Adverbes
        "très", "trop", "peu", "beaucoup", "assez", "plus", "moins", "bien", "mal",
        "vite", "lentement", "maintenant", "hier", "aujourd'hui", "demain", "toujours",
        "jamais", "souvent", "rarement", "parfois", "ici", "là", "ailleurs", "partout",
        
        # Verbes courants
        "être", "avoir", "faire", "aller", "venir", "voir", "dire", "savoir", "pouvoir",
        "vouloir", "devoir", "prendre", "donner", "mettre", "tenir", "venir", "partir",
        "arriver", "rester", "passer", "sortir", "entrer", "monter", "descendre",
        "ouvrir", "fermer", "commencer", "finir", "continuer", "arrêter", "changer",
        
        # Adjectifs courants
        "grand", "petit", "bon", "mauvais", "beau", "laid", "nouveau", "vieux", "jeune",
        "chaud", "froid", "long", "court", "large", "étroit", "lourd", "léger", "fort",
        "faible", "rapide", "lent", "facile", "difficile", "possible", "impossible",
        "vrai", "faux", "juste", "faux", "clair", "sombre", "propre", "sale", "sec",
        "mouillé", "plein", "vide", "ouvert", "fermé", "libre", "occupé", "calme",
        "bruyant", "doux", "dur", "souple", "rigide", "lisse", "rugueux", "lisse",
        
        # Noms courants
        "homme", "femme", "enfant", "personne", "groupe", "famille", "ami", "travail",
        "maison", "ville", "pays", "monde", "temps", "jour", "nuit", "matin", "soir",
        "semaine", "mois", "année", "heure", "minute", "seconde", "maintenant",
        "eau", "air", "feu", "terre", "soleil", "lune", "étoile", "ciel", "mer",
        "montagne", "forêt", "champ", "route", "chemin", "pont", "porte", "fenêtre",
        "mur", "toit", "sol", "plafond", "escalier", "couloir", "salle", "chambre",
        "cuisine", "salle", "bureau", "magasin", "école", "hôpital", "banque",
        "restaurant", "hôtel", "théâtre", "cinéma", "musée", "parc", "jardin",
        "voiture", "train", "avion", "bateau", "vélo", "moto", "bus", "métro",
        "livre", "journal", "lettre", "téléphone", "radio", "télévision", "musique",
        "film", "photo", "image", "couleur", "forme", "taille", "poids", "prix",
        "argent", "monnaie", "billet", "pièce", "carte", "chèque", "facture",
        "nom", "prénom", "âge", "adresse", "téléphone", "email", "date", "lieu",
        "raison", "cause", "effet", "résultat", "problème", "solution", "question",
        "réponse", "exemple", "cas", "situation", "état", "condition", "niveau",
        "qualité", "quantité", "nombre", "total", "partie", "ensemble", "groupe",
        "système", "méthode", "technique", "procédé", "processus", "étape", "phase",
        "période", "moment", "instant", "fois", "fois", "fois", "fois", "fois"
    }
    
    # Combiner tous les mots
    tous_mots = mots_douane.union(mots_generaux)
    
    # Ajouter des variations (pluriels, féminins, etc.)
    variations = set()
    for mot in tous_mots:
        # Pluriels
        if mot.endswith('al'):
            variations.add(mot[:-2] + 'aux')
        elif mot.endswith('au'):
            variations.add(mot + 'x')
        elif mot.endswith('eu'):
            variations.add(mot + 'x')
        elif not mot.endswith('s'):
            variations.add(mot + 's')
        
        # Féminins pour les adjectifs
        if mot.endswith('eux'):
            variations.add(mot[:-3] + 'euse')
        elif mot.endswith('er'):
            variations.add(mot[:-2] + 'ère')
        elif mot.endswith('f'):
            variations.add(mot[:-1] + 've')
        elif mot.endswith('x'):
            variations.add(mot[:-1] + 'se')
    
    # Combiner tout
    dictionnaire_complet = tous_mots.union(variations)
    
    return sorted(dictionnaire_complet)

def save_dictionary(words, filename="dictionnaire_francais.txt"):
    """Sauvegarde le dictionnaire dans un fichier"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')
    
    print(f"✓ Dictionnaire sauvegardé dans {filename}")
    print(f"✓ {len(words)} mots français ajoutés")

def main():
    """Fonction principale"""
    
    print("Génération du dictionnaire français complet...")
    
    # Essayer de télécharger d'abord
    words = download_french_dictionary()
    
    # Si le téléchargement échoue, créer un dictionnaire local
    if not words:
        print("Téléchargement échoué, création d'un dictionnaire local...")
        words = create_comprehensive_dictionary()
    
    # Sauvegarder le dictionnaire
    save_dictionary(words)
    
    print("✓ Dictionnaire français prêt !")

if __name__ == "__main__":
    main()
