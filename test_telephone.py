#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_classifier import AdvancedCEDEAOClassifier

def test_telephone_classification():
    """Test spécifique pour la classification des téléphones"""
    
    print("🔍 Test de classification pour 'téléphone portable'")
    print("=" * 60)
    
    # Initialiser le classificateur
    try:
        classifier = AdvancedCEDEAOClassifier()
        print("✅ Classificateur initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return
    
    # Charger les données CEDEAO
    try:
        with open('MON-TEC-CEDEAO-SH-2022-FREN-09-04-2024.txt', 'r', encoding='utf-8') as f:
            cedeao_data = f.read()
        print("✅ Données CEDEAO chargées")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données CEDEAO: {e}")
        return
    
    # Créer une base de données simplifiée pour le test
    database = {
        'subheadings': {
            '8517.13.00.00': {
                'description': 'Téléphones intelligents',
                'rate': '10%'
            },
            '8517.14.00.00': {
                'description': 'Autres téléphones pour réseaux cellulaires',
                'rate': '10%'
            },
            '8517.18.00.00': {
                'description': 'Autres téléphones',
                'rate': '10%'
            }
        },
        'chapters': {
            '85': 'Machines, appareils et matériels électriques et leurs parties; appareils d\'enregistrement ou de reproduction du son, appareils d\'enregistrement ou de reproduction des images et du son en télévision, et parties et accessoires de ces appareils'
        }
    }
    
    # Test avec différentes descriptions
    test_cases = [
        "téléphone portable",
        "téléphone intelligent",
        "smartphone",
        "téléphone mobile",
        "téléphone cellulaire",
        "iPhone",
        "Samsung Galaxy"
    ]
    
    for description in test_cases:
        print(f"\n📱 Test avec: '{description}'")
        print("-" * 40)
        
        try:
            # Test de prétraitement
            preprocessed = classifier.preprocess_text(description)
            print(f"Prétraitement: '{preprocessed}'")
            
            # Test d'extraction de caractéristiques
            features = classifier.extract_features(description)
            print(f"Caractéristiques extraites: {features}")
            
            # Test de classification
            results = classifier.classify_product(description, database)
            print(f"Résultats de classification: {len(results)} trouvés")
            
            for i, result in enumerate(results[:3]):
                print(f"  {i+1}. {result['code']} - {result['description']} (score: {result['final_score']:.3f})")
            
            if not results:
                print("  ❌ Aucun résultat trouvé")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    # Test de similarité sémantique
    print(f"\n🔍 Test de similarité sémantique")
    print("-" * 40)
    
    query = "téléphone portable"
    targets = [
        "Téléphones intelligents",
        "Autres téléphones pour réseaux cellulaires",
        "Machines électriques"
    ]
    
    for target in targets:
        similarity = classifier.calculate_semantic_similarity(query, target)
        print(f"'{query}' vs '{target}': {similarity:.3f}")

if __name__ == "__main__":
    test_telephone_classification()
