#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour récupérer tous les mots du dictionnaire Larousse
"""

import requests
import re
import time
import json
from typing import Set, List
from urllib.parse import urljoin, quote
import os

class LarousseScraper:
    """Classe pour récupérer les mots du dictionnaire Larousse"""
    
    def __init__(self):
        self.base_url = "https://www.larousse.fr"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.words = set()
        
    def get_alphabet_links(self) -> List[str]:
        """Récupère les liens vers toutes les lettres de l'alphabet"""
        try:
            print("🔍 Récupération des liens alphabet...")
            url = f"{self.base_url}/dictionnaires/francais"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Chercher les liens vers les lettres
                pattern = r'href="(/dictionnaires/francais/[a-z])"'
                matches = re.findall(pattern, response.text)
                
                alphabet_links = []
                for match in matches:
                    full_url = urljoin(self.base_url, match)
                    alphabet_links.append(full_url)
                
                print(f"✅ {len(alphabet_links)} liens alphabet trouvés")
                return alphabet_links
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des liens: {e}")
            return []
    
    def get_words_from_letter(self, letter_url: str) -> Set[str]:
        """Récupère tous les mots commençant par une lettre"""
        words = set()
        
        try:
            print(f"📖 Récupération des mots pour: {letter_url}")
            response = self.session.get(letter_url, timeout=10)
            
            if response.status_code == 200:
                # Chercher les mots dans la page
                # Pattern pour les liens vers les définitions de mots
                word_pattern = r'href="/dictionnaires/francais/[^"]*">([^<]+)</a>'
                matches = re.findall(word_pattern, response.text)
                
                for match in matches:
                    word = match.strip().lower()
                    # Nettoyer le mot
                    word = re.sub(r'[^\w\s-]', '', word)
                    if word and len(word) > 1 and word.isalpha():
                        words.add(word)
                
                print(f"   ✅ {len(words)} mots trouvés")
                
                # Chercher s'il y a une pagination
                pagination_pattern = r'href="([^"]*page=\d+[^"]*)"'
                pagination_matches = re.findall(pagination_pattern, response.text)
                
                # Traiter les pages suivantes
                for page_link in pagination_matches[:5]:  # Limiter à 5 pages par lettre
                    full_page_url = urljoin(letter_url, page_link)
                    page_words = self.get_words_from_page(full_page_url)
                    words.update(page_words)
                    time.sleep(1)  # Pause pour être respectueux
                
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        return words
    
    def get_words_from_page(self, page_url: str) -> Set[str]:
        """Récupère les mots d'une page spécifique"""
        words = set()
        
        try:
            response = self.session.get(page_url, timeout=10)
            
            if response.status_code == 200:
                word_pattern = r'href="/dictionnaires/francais/[^"]*">([^<]+)</a>'
                matches = re.findall(word_pattern, response.text)
                
                for match in matches:
                    word = match.strip().lower()
                    word = re.sub(r'[^\w\s-]', '', word)
                    if word and len(word) > 1 and word.isalpha():
                        words.add(word)
                        
        except Exception as e:
            print(f"   ❌ Erreur page: {e}")
        
        return words
    
    def scrape_all_words(self) -> Set[str]:
        """Récupère tous les mots du Larousse"""
        print("🚀 Début de la récupération des mots Larousse...")
        
        # Récupérer les liens alphabet
        alphabet_links = self.get_alphabet_links()
        
        if not alphabet_links:
            print("❌ Impossible de récupérer les liens alphabet")
            return set()
        
        all_words = set()
        
        # Traiter chaque lettre
        for i, letter_url in enumerate(alphabet_links, 1):
            print(f"\n📚 Lettre {i}/{len(alphabet_links)}")
            letter_words = self.get_words_from_letter(letter_url)
            all_words.update(letter_words)
            
            print(f"   📊 Total accumulé: {len(all_words)} mots")
            
            # Pause entre les lettres
            time.sleep(2)
        
        return all_words
    
    def save_words(self, words: Set[str], filename: str = "dictionnaire_larousse.txt"):
        """Sauvegarde les mots dans un fichier"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in sorted(words):
                    f.write(word + '\n')
            
            print(f"✅ {len(words)} mots sauvegardés dans {filename}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")

def scrape_common_french_words():
    """Récupère des mots français courants depuis d'autres sources"""
    print("🔄 Récupération de mots français courants...")
    
    # Liste de mots français courants
    common_words = {
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
        "vrai", "faux", "juste", "clair", "sombre", "propre", "sale", "sec",
        "mouillé", "plein", "vide", "ouvert", "fermé", "libre", "occupé", "calme",
        "bruyant", "doux", "dur", "souple", "rigide", "lisse", "rugueux",
        
        # Noms courants
        "homme", "femme", "enfant", "personne", "groupe", "famille", "ami", "travail",
        "maison", "ville", "pays", "monde", "temps", "jour", "nuit", "matin", "soir",
        "semaine", "mois", "année", "heure", "minute", "seconde", "maintenant",
        "eau", "air", "feu", "terre", "soleil", "lune", "étoile", "ciel", "mer",
        "montagne", "forêt", "champ", "route", "chemin", "pont", "porte", "fenêtre",
        "mur", "toit", "sol", "plafond", "escalier", "couloir", "salle", "chambre",
        "cuisine", "bureau", "magasin", "école", "hôpital", "banque",
        "restaurant", "hôtel", "théâtre", "cinéma", "musée", "parc", "jardin",
        "voiture", "train", "avion", "bateau", "vélo", "moto", "bus", "métro",
        "livre", "journal", "lettre", "téléphone", "radio", "télévision", "musique",
        "film", "photo", "image", "couleur", "forme", "taille", "poids", "prix",
        "argent", "monnaie", "billet", "pièce", "carte", "chèque", "facture",
        "nom", "prénom", "âge", "adresse", "email", "date", "lieu",
        "raison", "cause", "effet", "résultat", "problème", "solution", "question",
        "réponse", "exemple", "cas", "situation", "état", "condition", "niveau",
        "qualité", "quantité", "nombre", "total", "partie", "ensemble", "groupe",
        "système", "méthode", "technique", "procédé", "processus", "étape", "phase",
        "période", "moment", "instant", "fois"
    }
    
    return common_words

def main():
    """Fonction principale"""
    
    print("=" * 70)
    print("SCRAPING DU DICTIONNAIRE LAROUSSE")
    print("=" * 70)
    
    # Option 1: Scraping Larousse (peut prendre du temps)
    print("\n1. Scraping complet du Larousse (long)")
    print("2. Utiliser des mots français courants (rapide)")
    print("3. Combiner les deux")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    all_words = set()
    
    if choice == "1":
        # Scraping Larousse
        scraper = LarousseScraper()
        larousse_words = scraper.scrape_all_words()
        all_words.update(larousse_words)
        scraper.save_words(larousse_words, "dictionnaire_larousse.txt")
        
    elif choice == "2":
        # Mots courants
        common_words = scrape_common_french_words()
        all_words.update(common_words)
        print(f"✅ {len(common_words)} mots courants récupérés")
        
    elif choice == "3":
        # Combiner les deux
        print("🔄 Récupération des mots courants...")
        common_words = scrape_common_french_words()
        all_words.update(common_words)
        
        print("🔄 Scraping Larousse...")
        scraper = LarousseScraper()
        larousse_words = scraper.scrape_all_words()
        all_words.update(larousse_words)
        
    else:
        print("❌ Choix invalide")
        return
    
    # Sauvegarder le dictionnaire final
    if all_words:
        with open("dictionnaire_francais.txt", 'w', encoding='utf-8') as f:
            for word in sorted(all_words):
                f.write(word + '\n')
        
        print(f"\n🎉 DICTIONNAIRE CRÉÉ AVEC SUCCÈS !")
        print(f"📊 Total: {len(all_words)} mots français")
        print(f"💾 Sauvegardé dans: dictionnaire_francais.txt")
        
        # Afficher quelques exemples
        sample_words = list(all_words)[:20]
        print(f"📝 Exemples: {', '.join(sample_words)}")
        
    else:
        print("❌ Aucun mot récupéré")

if __name__ == "__main__":
    main()
