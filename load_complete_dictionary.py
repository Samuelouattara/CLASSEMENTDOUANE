#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour charger un dictionnaire français complet de 60 000 mots
"""

import os
import sys
from typing import List, Set

def load_large_dictionary(file_path: str) -> Set[str]:
    """
    Charge un dictionnaire français depuis un fichier
    
    Args:
        file_path: Chemin vers le fichier dictionnaire
        
    Returns:
        Ensemble des mots français
    """
    words = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                word = line.strip().lower()
                if word and len(word) > 1:
                    words.add(word)
                
                # Afficher le progrès tous les 1000 mots
                if line_num % 1000 == 0:
                    print(f"   Chargé {line_num} lignes, {len(words)} mots uniques...")
        
        print(f"✅ Dictionnaire chargé avec succès: {len(words)} mots uniques")
        return words
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {file_path}")
        return set()
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return set()

def save_dictionary_to_file(words: Set[str], output_file: str = "dictionnaire_francais.txt"):
    """
    Sauvegarde le dictionnaire dans un fichier
    
    Args:
        words: Ensemble des mots à sauvegarder
        output_file: Fichier de sortie
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in sorted(words):
                f.write(word + '\n')
        
        print(f"✅ Dictionnaire sauvegardé dans {output_file}")
        print(f"   {len(words)} mots écrits")
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")

def merge_dictionaries(dict1_path: str, dict2_path: str, output_path: str = "dictionnaire_francais.txt"):
    """
    Fusionne deux dictionnaires
    
    Args:
        dict1_path: Premier dictionnaire
        dict2_path: Deuxième dictionnaire
        output_path: Fichier de sortie fusionné
    """
    print("🔄 Fusion des dictionnaires...")
    
    # Charger le premier dictionnaire
    print(f"Chargement de {dict1_path}...")
    words1 = load_large_dictionary(dict1_path)
    
    # Charger le deuxième dictionnaire
    print(f"Chargement de {dict2_path}...")
    words2 = load_large_dictionary(dict2_path)
    
    # Fusionner
    merged_words = words1.union(words2)
    
    print(f"📊 Statistiques de fusion:")
    print(f"   Dictionnaire 1: {len(words1)} mots")
    print(f"   Dictionnaire 2: {len(words2)} mots")
    print(f"   Fusionné: {len(merged_words)} mots")
    print(f"   Nouveaux mots ajoutés: {len(merged_words) - len(words1)}")
    
    # Sauvegarder
    save_dictionary_to_file(merged_words, output_path)

def main():
    """Fonction principale"""
    
    print("=" * 60)
    print("CHARGEMENT DU DICTIONNAIRE FRANÇAIS COMPLET")
    print("=" * 60)
    
    # Vérifier si un fichier dictionnaire existe déjà
    current_dict = "dictionnaire_francais.txt"
    if os.path.exists(current_dict):
        current_words = load_large_dictionary(current_dict)
        print(f"📁 Dictionnaire actuel: {len(current_words)} mots")
    
    print("\nOptions disponibles:")
    print("1. Charger un nouveau dictionnaire (remplace l'actuel)")
    print("2. Fusionner avec le dictionnaire actuel")
    print("3. Tester le dictionnaire actuel")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == "1":
        # Charger un nouveau dictionnaire
        dict_path = input("Chemin vers votre fichier dictionnaire (60 000 mots): ").strip()
        if os.path.exists(dict_path):
            words = load_large_dictionary(dict_path)
            if words:
                save_dictionary_to_file(words, current_dict)
                print("✅ Dictionnaire mis à jour avec succès !")
            else:
                print("❌ Aucun mot chargé")
        else:
            print(f"❌ Fichier non trouvé: {dict_path}")
    
    elif choice == "2":
        # Fusionner les dictionnaires
        dict_path = input("Chemin vers votre fichier dictionnaire à fusionner: ").strip()
        if os.path.exists(dict_path):
            merge_dictionaries(current_dict, dict_path, current_dict)
            print("✅ Dictionnaires fusionnés avec succès !")
        else:
            print(f"❌ Fichier non trouvé: {dict_path}")
    
    elif choice == "3":
        # Tester le dictionnaire actuel
        if os.path.exists(current_dict):
            words = load_large_dictionary(current_dict)
            print(f"\n📊 Statistiques du dictionnaire actuel:")
            print(f"   Total mots: {len(words)}")
            
            # Afficher quelques exemples
            sample_words = list(words)[:10]
            print(f"   Exemples: {', '.join(sample_words)}")
            
            # Test de reconnaissance
            test_words = ["ballon", "cuir", "football", "smartphone", "velo", "ordinateur"]
            print(f"\n🔍 Test de reconnaissance:")
            for word in test_words:
                is_french = word in words
                print(f"   '{word}': {'✅ Français' if is_french else '❌ Non français'}")
        else:
            print("❌ Aucun dictionnaire trouvé")
    
    else:
        print("❌ Choix invalide")

if __name__ == "__main__":
    main()
