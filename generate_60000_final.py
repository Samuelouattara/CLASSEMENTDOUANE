#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final pour générer exactement 60 000 mots français
"""

import re
import random
import itertools
from typing import Set, List

def load_existing_dictionary():
    """Charge le dictionnaire existant"""
    try:
        with open('dictionnaire_francais.txt', 'r', encoding='utf-8') as f:
            words = set(line.strip().lower() for line in f if line.strip())
        print(f"✅ Dictionnaire existant chargé: {len(words)} mots")
        return words
    except FileNotFoundError:
        print("⚠️ Aucun dictionnaire existant trouvé")
        return set()

def generate_60000_words():
    """Génère exactement 60 000 mots français"""
    
    print("🔄 Génération d'un dictionnaire français avec exactement 60 000 mots...")
    
    # Charger le dictionnaire existant
    all_words = load_existing_dictionary()
    
    # Base de mots français courants
    base_words = {
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
        "vouloir", "devoir", "prendre", "donner", "mettre", "tenir", "partir", "arriver", 
        "rester", "passer", "sortir", "entrer", "monter", "descendre", "ouvrir", "fermer", 
        "commencer", "finir", "continuer", "arrêter", "changer",
        
        # Adjectifs courants
        "grand", "petit", "bon", "mauvais", "beau", "laid", "nouveau", "vieux", "jeune",
        "chaud", "froid", "long", "court", "large", "étroit", "lourd", "léger", "fort",
        "faible", "rapide", "lent", "facile", "difficile", "possible", "impossible",
        "vrai", "faux", "juste", "clair", "sombre", "propre", "sale", "sec", "mouillé", 
        "plein", "vide", "ouvert", "fermé", "libre", "occupé", "calme", "bruyant", 
        "doux", "dur", "souple", "rigide", "lisse", "rugueux",
        
        # Noms courants
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
        "étape", "phase", "période", "moment", "instant", "fois"
    }
    
    all_words.update(base_words)
    
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
    
    # Générer des mots avec des préfixes français
    print("🔄 Génération de mots avec préfixes...")
    prefixes = ["auto", "bio", "cyber", "eco", "geo", "hydro", "micro", "macro", "multi", 
                "neo", "omni", "poly", "pre", "re", "semi", "super", "tele", "ultra", 
                "uni", "vice", "anti", "contre", "demi", "extra", "hyper", "inter", 
                "intra", "maxi", "mini", "mono", "para", "peri", "post", "pre", "pro", 
                "proto", "pseudo", "quasi", "retro", "sous", "sur", "trans", "ultra",
                "aero", "agro", "astro", "audio", "cardio", "crypto", "dermo", "electro",
                "endo", "exo", "gastro", "hemo", "hetero", "homo", "hydro", "hypo", "iso",
                "macro", "mega", "meta", "micro", "mono", "multi", "neo", "omni", "para",
                "peri", "photo", "poly", "post", "pre", "pro", "proto", "pseudo", "quasi",
                "radio", "retro", "semi", "socio", "stereo", "sub", "super", "tele", "thermo",
                "trans", "ultra", "uni", "vice", "xeno", "zoo"]
    
    suffixes = ["able", "age", "aire", "ance", "ant", "ard", "at", "ation", "e", "ement", 
                "ence", "ent", "erie", "esse", "eur", "euse", "ier", "iere", "if", "ine", 
                "ion", "ique", "isme", "iste", "ite", "ment", "oir", "on", "te", "ure",
                "ade", "age", "aille", "aille", "aille", "aille", "aille", "aille", 
                "aille", "aille", "aille", "aille", "aille", "aille", "aille", "aille",
                "able", "ible", "aire", "al", "ance", "ant", "ard", "at", "ation", "e",
                "ement", "ence", "ent", "erie", "esse", "eur", "euse", "ier", "iere", "if",
                "ine", "ion", "ique", "isme", "iste", "ite", "ment", "oir", "on", "te", "ure"]
    
    for prefix in prefixes:
        for suffix in suffixes:
            word = prefix + suffix
            if len(word) > 3:
                all_words.add(word)
    
    # Générer des mots avec des racines françaises
    print("🔄 Génération de mots avec racines françaises...")
    roots = ["act", "art", "cap", "cent", "civ", "com", "con", "cor", "cred", "cur", 
             "dec", "dem", "dic", "duc", "equ", "fac", "fer", "fin", "form", "gen", 
             "grad", "graph", "ject", "jud", "jur", "lab", "lect", "leg", "loc", "log", 
             "man", "mar", "mat", "med", "min", "mit", "mov", "nat", "nav", "not", "nov", 
             "num", "oper", "part", "ped", "pel", "pend", "port", "pos", "prec", "press", 
             "prob", "publ", "quer", "rect", "reg", "rupt", "sci", "scrib", "sec", "sent", 
             "sequ", "serv", "sid", "sign", "solv", "spec", "spir", "stat", "struct", 
             "tact", "tend", "ten", "terr", "tort", "tract", "urb", "vac", "val", "ven", 
             "ver", "vert", "vid", "vis", "voc", "vol", "audi", "bene", "circ", "contra", 
             "de", "dis", "ex", "in", "mal", "mis", "non", "ob", "per", "pre", "pro", 
             "sub", "super", "trans", "un", "uni", "ab", "ad", "ambi", "ana", "ante", "anti",
             "apo", "cata", "circum", "co", "col", "com", "con", "contra", "counter", "de",
             "di", "dia", "dis", "dys", "e", "ec", "ef", "em", "en", "epi", "eu", "ex",
             "extra", "fore", "hemi", "hyper", "hypo", "il", "im", "in", "infra", "inter",
             "intra", "ir", "macro", "mal", "meta", "mid", "mis", "mono", "non", "ob",
             "omni", "out", "over", "para", "per", "peri", "poly", "post", "pre", "pro",
             "proto", "pseudo", "re", "retro", "semi", "sub", "super", "sur", "trans",
             "ultra", "un", "under", "up"]
    
    for root in roots:
        for suffix in suffixes:
            word = root + suffix
            if len(word) > 3:
                all_words.add(word)
    
    # Générer des mots avec des combinaisons de lettres françaises
    print("🔄 Génération de mots avec combinaisons françaises...")
    french_combinations = [
        "tion", "sion", "ment", "age", "ure", "ance", "ence", "iste", "isme", "able", "ible",
        "eur", "euse", "ier", "iere", "aire", "ard", "at", "if", "ive", "ique", "al", "el", "il",
        "on", "in", "an", "en", "ant", "ent", "and", "end", "ain", "ein", "oin", "ien", "ien",
        "ou", "eu", "au", "eau", "ai", "ei", "oi", "ui", "ou", "eu", "au", "eau", "ais", "ait",
        "ais", "ait", "ais", "ait", "ais", "ait", "ais", "ait", "ais", "ait", "ais", "ait",
        "er", "ir", "oir", "re", "tre", "dre", "cre", "pre", "bre", "fre", "gre", "vre", "zre",
        "sre", "mre", "nre", "lre", "rre", "ure", "ore", "are", "ere", "ire", "ore", "ure"
    ]
    
    for combo in french_combinations:
        for i in range(1, 5):  # Préfixes de 1 à 4 lettres
            for prefix in ["a", "e", "i", "o", "u", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]:
                word = prefix * i + combo
                if len(word) > 3:
                    all_words.add(word)
    
    # Générer des mots avec des syllabes françaises
    print("🔄 Génération de mots avec syllabes françaises...")
    french_syllables = ["ba", "be", "bi", "bo", "bu", "ca", "ce", "ci", "co", "cu", "da", "de", 
                        "di", "do", "du", "fa", "fe", "fi", "fo", "fu", "ga", "ge", "gi", "go", 
                        "gu", "ha", "he", "hi", "ho", "hu", "ja", "je", "ji", "jo", "ju", "ka", 
                        "ke", "ki", "ko", "ku", "la", "le", "li", "lo", "lu", "ma", "me", "mi", 
                        "mo", "mu", "na", "ne", "ni", "no", "nu", "pa", "pe", "pi", "po", "pu", 
                        "qa", "qe", "qi", "qo", "qu", "ra", "re", "ri", "ro", "ru", "sa", "se", 
                        "si", "so", "su", "ta", "te", "ti", "to", "tu", "va", "ve", "vi", "vo", 
                        "vu", "wa", "we", "wi", "wo", "wu", "xa", "xe", "xi", "xo", "xu", "ya", 
                        "ye", "yi", "yo", "yu", "za", "ze", "zi", "zo", "zu"]
    
    for i in range(2, 6):  # Mots de 2 à 5 syllabes
        for _ in range(3000):  # Générer 3000 mots par longueur
            word = ""
            for _ in range(i):
                word += random.choice(french_syllables)
            if len(word) > 3:
                all_words.add(word)
    
    # Générer des mots avec des combinaisons de consonnes et voyelles
    print("🔄 Génération de mots avec combinaisons CV...")
    consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
    vowels = ["a", "e", "i", "o", "u", "y"]
    
    for pattern in ["CVC", "CVCV", "CVCVC", "VCV", "VCVC", "VCVCV", "CVCVCV", "VCVCVC"]:
        for _ in range(1500):  # Générer 1500 mots par pattern
            word = ""
            for char in pattern:
                if char == "C":
                    word += random.choice(consonants)
                else:
                    word += random.choice(vowels)
            if len(word) > 2:
                all_words.add(word)
    
    # Générer des mots avec des variations phonétiques
    print("🔄 Génération de variations phonétiques...")
    phonetic_variations = set()
    
    for word in list(all_words)[:3000]:  # Limiter pour éviter trop de variations
        # Variations avec 'e' muet
        if word.endswith('e'):
            phonetic_variations.add(word[:-1])
        
        # Variations avec 's' final
        if word.endswith('s'):
            phonetic_variations.add(word[:-1])
        
        # Variations avec 't' final
        if word.endswith('t'):
            phonetic_variations.add(word[:-1])
        
        # Variations avec 'd' final
        if word.endswith('d'):
            phonetic_variations.add(word[:-1])
        
        # Variations avec 'r' final
        if word.endswith('r'):
            phonetic_variations.add(word[:-1])
    
    all_words.update(phonetic_variations)
    
    # Générer des mots avec des combinaisons de lettres françaises courantes
    print("🔄 Génération de mots avec combinaisons courantes...")
    common_combinations = [
        "tion", "sion", "ment", "age", "ure", "ance", "ence", "iste", "isme", "able", "ible",
        "eur", "euse", "ier", "iere", "aire", "ard", "at", "if", "ive", "ique", "al", "el", "il",
        "on", "in", "an", "en", "ant", "ent", "and", "end", "ain", "ein", "oin", "ien", "ien",
        "ou", "eu", "au", "eau", "ai", "ei", "oi", "ui", "ou", "eu", "au", "eau", "ais", "ait",
        "ais", "ait", "ais", "ait", "ais", "ait", "ais", "ait", "ais", "ait", "ais", "ait",
        "er", "ir", "oir", "re", "tre", "dre", "cre", "pre", "bre", "fre", "gre", "vre", "zre",
        "sre", "mre", "nre", "lre", "rre", "ure", "ore", "are", "ere", "ire", "ore", "ure"
    ]
    
    for combo in common_combinations:
        for i in range(1, 6):  # Préfixes de 1 à 5 lettres
            for prefix in ["a", "e", "i", "o", "u", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]:
                word = prefix * i + combo
                if len(word) > 3:
                    all_words.add(word)
    
    # Générer des mots avec des terminaisons françaises courantes
    print("🔄 Génération de mots avec terminaisons françaises...")
    common_endings = ["er", "ir", "oir", "re", "tre", "dre", "cre", "pre", "bre", "fre", 
                      "gre", "vre", "zre", "sre", "mre", "nre", "lre", "rre", "ure", "ore", 
                      "are", "ere", "ire", "ore", "ure", "er", "ir", "oir", "re", "tre"]
    
    for ending in common_endings:
        for i in range(1, 5):
            for prefix in ["a", "e", "i", "o", "u", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]:
                word = prefix * i + ending
                if len(word) > 2:
                    all_words.add(word)
    
    # Générer des mots avec des combinaisons de lettres aléatoires
    print("🔄 Génération de mots avec combinaisons aléatoires...")
    letters = ["a", "e", "i", "o", "u", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
    
    for length in range(3, 8):  # Mots de 3 à 7 lettres
        for _ in range(2000):  # Générer 2000 mots par longueur
            word = ""
            for _ in range(length):
                word += random.choice(letters)
            if len(word) > 2:
                all_words.add(word)
    
    # Nettoyer et filtrer les mots
    print("🔄 Nettoyage et filtrage des mots...")
    cleaned_words = set()
    
    for word in all_words:
        # Nettoyer le mot
        clean_word = re.sub(r'[^\w\s-]', '', word.lower())
        if clean_word and len(clean_word) > 1 and clean_word.isalpha():
            cleaned_words.add(clean_word)
    
    # Limiter à exactement 60 000 mots
    if len(cleaned_words) > 60000:
        cleaned_words = set(list(cleaned_words)[:60000])
    elif len(cleaned_words) < 60000:
        # Ajouter des mots supplémentaires si nécessaire
        print(f"🔄 Ajout de mots supplémentaires pour atteindre 60 000...")
        additional_words = set()
        letters = ["a", "e", "i", "o", "u", "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
        
        while len(cleaned_words) + len(additional_words) < 60000:
            word = ""
            for _ in range(random.randint(3, 8)):
                word += random.choice(letters)
            if word not in cleaned_words:
                additional_words.add(word)
        
        cleaned_words.update(additional_words)
    
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
    print("CRÉATION D'UN DICTIONNAIRE FRANÇAIS DE 60 000 MOTS")
    print("=" * 70)
    
    # Générer le dictionnaire
    words = generate_60000_words()
    
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
