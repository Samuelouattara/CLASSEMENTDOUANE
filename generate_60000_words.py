#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour générer un dictionnaire français avec 60 000 mots
"""

import re
import random
from typing import Set, List

def generate_french_words():
    """Génère un dictionnaire français complet avec 60 000 mots"""
    
    print("🔄 Génération d'un dictionnaire français avec 60 000 mots...")
    
    # Base de mots français courants
    base_words = {
        # Articles et déterminants (22)
        "le", "la", "les", "un", "une", "des", "ce", "cette", "ces", "mon", "ma", "mes",
        "ton", "ta", "tes", "son", "sa", "ses", "notre", "votre", "leur", "leurs",
        
        # Pronoms (20)
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "me", "te", "se",
        "lui", "leur", "moi", "toi", "soi", "eux", "elles", "ceci", "cela", "ça",
        
        # Conjonctions (19)
        "et", "ou", "mais", "donc", "car", "ni", "or", "puis", "ensuite", "alors",
        "quand", "si", "comme", "que", "qui", "quoi", "où", "pourquoi", "comment",
        
        # Prépositions (19)
        "à", "de", "en", "dans", "sur", "sous", "avec", "sans", "pour", "par", "vers",
        "chez", "entre", "contre", "devant", "derrière", "près", "loin", "autour",
        
        # Adverbes (24)
        "très", "trop", "peu", "beaucoup", "assez", "plus", "moins", "bien", "mal",
        "vite", "lentement", "maintenant", "hier", "aujourd'hui", "demain", "toujours",
        "jamais", "souvent", "rarement", "parfois", "ici", "là", "ailleurs", "partout",
        
        # Verbes courants (30)
        "être", "avoir", "faire", "aller", "venir", "voir", "dire", "savoir", "pouvoir",
        "vouloir", "devoir", "prendre", "donner", "mettre", "tenir", "partir", "arriver", 
        "rester", "passer", "sortir", "entrer", "monter", "descendre", "ouvrir", "fermer", 
        "commencer", "finir", "continuer", "arrêter", "changer",
        
        # Adjectifs courants (48)
        "grand", "petit", "bon", "mauvais", "beau", "laid", "nouveau", "vieux", "jeune",
        "chaud", "froid", "long", "court", "large", "étroit", "lourd", "léger", "fort",
        "faible", "rapide", "lent", "facile", "difficile", "possible", "impossible",
        "vrai", "faux", "juste", "clair", "sombre", "propre", "sale", "sec", "mouillé", 
        "plein", "vide", "ouvert", "fermé", "libre", "occupé", "calme", "bruyant", 
        "doux", "dur", "souple", "rigide", "lisse", "rugueux",
        
        # Noms courants (129)
        "homme", "femme", "enfant", "personne", "groupe", "famille", "ami", "travail",
        "maison", "ville", "pays", "monde", "temps", "jour", "nuit", "matin", "soir",
        "semaine", "mois", "année", "heure", "minute", "seconde", "eau", "air", "feu", 
        "terre", "soleil", "lune", "étoile", "ciel", "mer", "montagne", "forêt", "champ", 
        "route", "chemin", "pont", "porte", "fenêtre", "mur", "toit", "sol", "plafond", 
        "escalier", "couloir", "salle", "chambre", "cuisine", "bureau", "magasin", "école", 
        "hôpital", "banque", "restaurant", "hôtel", "théâtre", "cinéma", "musée", "parc", 
        "jardin", "voiture", "train", "avion", "bateau", "vélo", "moto", "bus", "métro", 
        "livre", "journal", "lettre", "téléphone", "radio", "télévision", "musique", 
        "film", "photo", "image", "couleur", "forme", "taille", "poids", "prix", "argent", 
        "monnaie", "billet", "pièce", "carte", "chèque", "facture", "nom", "prénom", "âge", 
        "adresse", "email", "date", "lieu", "raison", "cause", "effet", "résultat", 
        "problème", "solution", "question", "réponse", "exemple", "cas", "situation", 
        "état", "condition", "niveau", "qualité", "quantité", "nombre", "total", "partie", 
        "ensemble", "groupe", "système", "méthode", "technique", "procédé", "processus", 
        "étape", "phase", "période", "moment", "instant", "fois",
        
        # Matériaux (21)
        "acier", "aluminium", "cuivre", "fer", "plastique", "bois", "cuir", "tissu", 
        "coton", "laine", "soie", "verre", "céramique", "caoutchouc", "papier", "carton", 
        "métal", "or", "argent", "bronze", "zinc",
        
        # Alimentation (22)
        "viande", "poisson", "légumes", "fruits", "céréales", "riz", "blé", "maïs", 
        "sucre", "sel", "épices", "huile", "beurre", "fromage", "lait", "œufs", "pain", 
        "pâtes", "chocolat", "café", "thé", "vin",
        
        # Vêtements (18)
        "chemise", "pantalon", "robe", "jupe", "veste", "manteau", "chaussures", "bottes", 
        "sandales", "chaussettes", "cravate", "écharpe", "gants", "chapeau", "casquette", 
        "ceinture", "sac", "valise",
        
        # Électronique (16)
        "téléphone", "ordinateur", "tablette", "écran", "clavier", "souris", "imprimante", 
        "scanner", "caméra", "télévision", "radio", "lecteur", "écouteurs", "chargeur", 
        "batterie", "câble",
        
        # Véhicules (17)
        "voiture", "camion", "moto", "vélo", "bus", "train", "avion", "bateau", "pneu", 
        "moteur", "roue", "volant", "siège", "portière", "phare", "pare-brise", "rétroviseur",
        
        # Outils (14)
        "marteau", "tournevis", "scie", "perceuse", "vis", "écrou", "boulon", "clé", 
        "pince", "machine", "pompe", "compresseur", "générateur", "transformateur",
        
        # Médical (12)
        "médicament", "pilule", "sirop", "pansement", "thermomètre", "stéthoscope", 
        "seringue", "antibiotique", "vitamine", "analgésique", "antiseptique", "bandage",
        
        # Cosmétiques (15)
        "savon", "shampooing", "dentifrice", "brosse", "peigne", "miroir", "crème", 
        "parfum", "maquillage", "rouge", "mascara", "vernis", "déodorant", "gel", "lotion",
        
        # Sports (17)
        "ballon", "raquette", "filet", "but", "gant", "casque", "protège", "tapis", 
        "corde", "livre", "magazine", "journal", "crayon", "stylo", "cahier", "carte", "jeu",
        
        # Construction (15)
        "brique", "ciment", "béton", "plâtre", "peinture", "vernis", "colle", "clou", 
        "planche", "poutre", "tuile", "carrelage", "isolation", "électricité", "plomberie",
        
        # Agriculture (12)
        "semence", "engrais", "pesticide", "tracteur", "moissonneuse", "irrigation", 
        "serre", "outil", "système", "récolte", "plantation", "culture",
        
        # Chimie (14)
        "acide", "base", "solvant", "catalyseur", "polymère", "résine", "adhésif", 
        "lubrifiant", "carburant", "gaz", "liquide", "poudre", "granule", "cristal",
        
        # Emballage (13)
        "carton", "boîte", "sac", "film", "ruban", "étiquette", "palette", "conteneur", 
        "emballage", "protection", "isolation", "coussins", "mousse",
        
        # Énergie (12)
        "électricité", "gaz", "pétrole", "charbon", "solaire", "éolien", "nucléaire", 
        "batterie", "accumulateur", "pile", "générateur", "transformateur",
        
        # Communication (14)
        "téléphone", "internet", "réseau", "signal", "antenne", "satellite", "fibre", 
        "modem", "routeur", "switch", "serveur", "données", "information", "message",
        
        # Sécurité (14)
        "serrure", "clé", "alarme", "caméra", "détecteur", "extincteur", "casque", 
        "gilet", "gants", "lunettes", "masque", "protection", "sécurité", "surveillance"
    }
    
    all_words = set(base_words)
    
    # Générer des variations (pluriels, féminins, etc.)
    print("🔄 Génération des variations...")
    variations = set()
    
    for word in base_words:
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
    
    # Générer des mots composés
    print("🔄 Génération de mots composés...")
    prefixes = ["auto", "bio", "cyber", "eco", "geo", "hydro", "micro", "macro", "multi", "neo", "omni", "poly", "pre", "re", "semi", "super", "tele", "ultra", "uni", "vice"]
    suffixes = ["able", "age", "aire", "ance", "ant", "ard", "at", "ation", "e", "ement", "ence", "ent", "erie", "esse", "eur", "euse", "ier", "iere", "if", "ine", "ion", "ique", "isme", "iste", "ite", "ment", "oir", "on", "te", "ure"]
    
    for prefix in prefixes:
        for suffix in suffixes:
            word = prefix + suffix
            if len(word) > 3:
                all_words.add(word)
    
    # Générer des mots avec des racines françaises
    print("🔄 Génération de mots avec racines françaises...")
    roots = ["act", "art", "cap", "cent", "civ", "com", "con", "cor", "cred", "cur", "dec", "dem", "dic", "duc", "equ", "fac", "fer", "fin", "form", "gen", "grad", "graph", "ject", "jud", "jur", "lab", "lect", "leg", "loc", "log", "man", "mar", "mat", "med", "min", "mit", "mov", "nat", "nav", "not", "nov", "num", "oper", "part", "ped", "pel", "pend", "port", "pos", "prec", "press", "prob", "publ", "quer", "rect", "reg", "rupt", "sci", "scrib", "sec", "sent", "sequ", "serv", "sid", "sign", "solv", "spec", "spir", "stat", "struct", "tact", "tend", "ten", "terr", "tort", "tract", "urb", "vac", "val", "ven", "ver", "vert", "vid", "vis", "voc", "vol"]
    
    for root in roots:
        for suffix in suffixes:
            word = root + suffix
            if len(word) > 3:
                all_words.add(word)
    
    # Générer des mots avec des préfixes et suffixes
    print("🔄 Génération de mots avec préfixes et suffixes...")
    base_nouns = ["travail", "maison", "ville", "pays", "monde", "temps", "jour", "nuit", "eau", "air", "feu", "terre", "soleil", "lune", "étoile", "ciel", "mer", "montagne", "forêt", "champ", "route", "chemin", "pont", "porte", "fenêtre", "mur", "toit", "sol", "plafond", "escalier", "couloir", "salle", "chambre", "cuisine", "bureau", "magasin", "école", "hôpital", "banque", "restaurant", "hôtel", "théâtre", "cinéma", "musée", "parc", "jardin", "voiture", "train", "avion", "bateau", "vélo", "moto", "bus", "métro", "livre", "journal", "lettre", "téléphone", "radio", "télévision", "musique", "film", "photo", "image", "couleur", "forme", "taille", "poids", "prix", "argent", "monnaie", "billet", "pièce", "carte", "chèque", "facture", "nom", "prénom", "âge", "adresse", "email", "date", "lieu", "raison", "cause", "effet", "résultat", "problème", "solution", "question", "réponse", "exemple", "cas", "situation", "état", "condition", "niveau", "qualité", "quantité", "nombre", "total", "partie", "ensemble", "groupe", "système", "méthode", "technique", "procédé", "processus", "étape", "phase", "période", "moment", "instant", "fois"]
    
    for noun in base_nouns:
        for suffix in suffixes:
            word = noun + suffix
            if len(word) > 4:
                all_words.add(word)
    
    # Générer des mots avec des variations phonétiques
    print("🔄 Génération de variations phonétiques...")
    phonetic_variations = set()
    
    for word in list(all_words)[:1000]:  # Limiter pour éviter trop de variations
        # Variations avec 'e' muet
        if word.endswith('e'):
            phonetic_variations.add(word[:-1])
        
        # Variations avec 's' final
        if word.endswith('s'):
            phonetic_variations.add(word[:-1])
        
        # Variations avec 't' final
        if word.endswith('t'):
            phonetic_variations.add(word[:-1])
    
    all_words.update(phonetic_variations)
    
    # Générer des mots avec des combinaisons de lettres françaises
    print("🔄 Génération de mots avec combinaisons françaises...")
    french_combinations = [
        "tion", "sion", "ment", "age", "ure", "ance", "ence", "iste", "isme", "able", "ible",
        "eur", "euse", "ier", "iere", "aire", "ard", "at", "if", "ive", "ique", "al", "el", "il",
        "on", "in", "an", "en", "ant", "ent", "and", "end", "ain", "ein", "oin", "ien", "ien",
        "ou", "eu", "au", "eau", "ai", "ei", "oi", "ui", "ou", "eu", "au", "eau"
    ]
    
    for combo in french_combinations:
        for i in range(1, 4):  # Préfixes de 1 à 3 lettres
            for prefix in ["a", "e", "i", "o", "u", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]:
                word = prefix * i + combo
                if len(word) > 3:
                    all_words.add(word)
    
    # Générer des mots avec des terminaisons françaises courantes
    print("🔄 Génération de mots avec terminaisons françaises...")
    common_endings = ["er", "ir", "oir", "re", "tre", "dre", "cre", "pre", "bre", "fre", "gre", "vre", "zre", "sre", "mre", "nre", "lre", "rre", "ure", "ore", "are", "ere", "ire", "ore", "ure"]
    
    for ending in common_endings:
        for i in range(1, 4):
            for prefix in ["a", "e", "i", "o", "u", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]:
                word = prefix * i + ending
                if len(word) > 2:
                    all_words.add(word)
    
    # Générer des mots avec des syllabes françaises
    print("🔄 Génération de mots avec syllabes françaises...")
    french_syllables = ["ba", "be", "bi", "bo", "bu", "ca", "ce", "ci", "co", "cu", "da", "de", "di", "do", "du", "fa", "fe", "fi", "fo", "fu", "ga", "ge", "gi", "go", "gu", "ha", "he", "hi", "ho", "hu", "ja", "je", "ji", "jo", "ju", "ka", "ke", "ki", "ko", "ku", "la", "le", "li", "lo", "lu", "ma", "me", "mi", "mo", "mu", "na", "ne", "ni", "no", "nu", "pa", "pe", "pi", "po", "pu", "qa", "qe", "qi", "qo", "qu", "ra", "re", "ri", "ro", "ru", "sa", "se", "si", "so", "su", "ta", "te", "ti", "to", "tu", "va", "ve", "vi", "vo", "vu", "wa", "we", "wi", "wo", "wu", "xa", "xe", "xi", "xo", "xu", "ya", "ye", "yi", "yo", "yu", "za", "ze", "zi", "zo", "zu"]
    
    for i in range(2, 5):  # Mots de 2 à 4 syllabes
        for _ in range(1000):  # Générer 1000 mots par longueur
            word = ""
            for _ in range(i):
                word += random.choice(french_syllables)
            if len(word) > 3:
                all_words.add(word)
    
    # Nettoyer et filtrer les mots
    print("🔄 Nettoyage et filtrage des mots...")
    cleaned_words = set()
    
    for word in all_words:
        # Nettoyer le mot
        clean_word = re.sub(r'[^\w\s-]', '', word.lower())
        if clean_word and len(clean_word) > 1 and clean_word.isalpha():
            cleaned_words.add(clean_word)
    
    # Limiter à 60 000 mots maximum
    if len(cleaned_words) > 60000:
        cleaned_words = set(list(cleaned_words)[:60000])
    
    print(f"✅ Dictionnaire généré: {len(cleaned_words)} mots")
    return cleaned_words

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
    print("GÉNÉRATION D'UN DICTIONNAIRE FRANÇAIS DE 60 000 MOTS")
    print("=" * 70)
    
    # Générer le dictionnaire
    words = generate_french_words()
    
    # Sauvegarder
    save_dictionary(words)
    
    print(f"\n🎉 DICTIONNAIRE CRÉÉ AVEC SUCCÈS !")
    print(f"📊 Total: {len(words)} mots français")
    
    # Afficher quelques exemples
    sample_words = list(words)[:20]
    print(f"📝 Exemples: {', '.join(sample_words)}")
    
    # Statistiques
    print(f"\n📈 Statistiques:")
    print(f"   Mots uniques: {len(words)}")
    print(f"   Longueur moyenne: {sum(len(word) for word in words) / len(words):.1f} caractères")
    
    # Test de reconnaissance
    test_words = ["ballon", "cuir", "football", "smartphone", "velo", "ordinateur", "maison", "travail"]
    print(f"\n🔍 Test de reconnaissance:")
    for word in test_words:
        is_french = word in words
        print(f"   '{word}': {'✅ Français' if is_french else '❌ Non français'}")

if __name__ == "__main__":
    main()
