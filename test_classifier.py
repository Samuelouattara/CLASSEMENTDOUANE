#!/usr/bin/env python3
"""
Script de test pour l'IA Classificateur CEDEAO
Teste le classificateur avec des exemples concrets de produits
"""

import sys
import os
from typing import Dict, List

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import CEDEAOClassifier
from ai_classifier import AdvancedCEDEAOClassifier

def test_basic_classifier():
    """Test du classificateur de base"""
    print("🧪 Test du classificateur de base...")
    
    try:
        classifier = CEDEAOClassifier()
        print(f"✅ Classificateur initialisé avec succès")
        print(f"📊 Sections chargées: {len(classifier.sections)}")
        print(f"📊 Chapitres chargés: {len(classifier.chapters)}")
        print(f"📊 Sous-positions chargées: {len(classifier.subheadings)}")
        return classifier
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return None

def test_advanced_classifier():
    """Test du classificateur avancé"""
    print("\n🤖 Test du classificateur avancé...")
    
    try:
        advanced_classifier = AdvancedCEDEAOClassifier()
        print("✅ Classificateur avancé initialisé avec succès")
        return advanced_classifier
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du classificateur avancé: {e}")
        return None

def test_product_classification(classifier, advanced_classifier=None):
    """Test de classification de produits"""
    print("\n🔍 Test de classification de produits...")
    
    # Exemples de produits à tester
    test_products = [
        {
            "name": "Ordinateur portable",
            "description": "Ordinateur portable Dell avec processeur Intel i7, 16GB RAM, 512GB SSD, écran 15 pouces",
            "expected_chapter": "84"
        },
        {
            "name": "T-shirt en coton",
            "description": "T-shirt en coton 100%, manches courtes, col rond, taille M",
            "expected_chapter": "61"
        },
        {
            "name": "Médicament",
            "description": "Médicament antibiotique en comprimés, boîte de 20 unités",
            "expected_chapter": "30"
        },
        {
            "name": "Voiture",
            "description": "Voiture automobile Toyota Corolla, moteur essence 1.8L, 4 portes, transmission automatique",
            "expected_chapter": "87"
        },
        {
            "name": "Café",
            "description": "Café en grains arabica, torréfié, emballé sous vide, origine Colombie",
            "expected_chapter": "09"
        }
    ]
    
    results = []
    
    for product in test_products:
        print(f"\n📦 Test: {product['name']}")
        print(f"Description: {product['description']}")
        
        # Test avec le classificateur de base
        try:
            basic_results = classifier.search_product(product['description'], use_advanced=False)
            if basic_results:
                best_basic = basic_results[0]
                print(f"✅ Classification de base: {best_basic['code']} - {best_basic['relevance']:.2%}")
            else:
                print("❌ Aucun résultat avec le classificateur de base")
        except Exception as e:
            print(f"❌ Erreur classification de base: {e}")
        
        # Test avec le classificateur avancé
        if advanced_classifier:
            try:
                database = {
                    'subheadings': classifier.subheadings,
                    'chapters': classifier.chapters,
                    'sections': classifier.sections
                }
                advanced_results = advanced_classifier.classify_product(product['description'], database)
                if advanced_results:
                    best_advanced = advanced_results[0]
                    print(f"🤖 Classification avancée: {best_advanced['code']} - {best_advanced['final_score']:.2%}")
                    
                    # Vérifier si le chapitre attendu est trouvé
                    found_chapter = best_advanced['code'].split('.')[0]
                    if found_chapter == product['expected_chapter']:
                        print(f"🎯 CORRECT: Chapitre attendu {product['expected_chapter']} trouvé!")
                    else:
                        print(f"⚠️  ATTENTION: Chapitre attendu {product['expected_chapter']}, trouvé {found_chapter}")
                else:
                    print("❌ Aucun résultat avec le classificateur avancé")
            except Exception as e:
                print(f"❌ Erreur classification avancée: {e}")
        
        print("-" * 80)

def test_feature_extraction(advanced_classifier):
    """Test de l'extraction de caractéristiques"""
    print("\n🔧 Test d'extraction de caractéristiques...")
    
    test_text = "Ordinateur portable Dell Latitude 5520, processeur Intel Core i7-1165G7 2.8GHz, 16GB RAM DDR4, disque SSD 512GB, écran LCD 15.6 pouces 1920x1080"
    
    try:
        features = advanced_classifier.extract_features(test_text)
        print("✅ Extraction de caractéristiques réussie:")
        print(f"   Matériaux: {features['materials']}")
        print(f"   Fonctions: {features['functions']}")
        print(f"   Dimensions: {features['dimensions']}")
        print(f"   Marques: {features['brands']}")
        print(f"   Spécifications techniques: {features['technical_specs']}")
    except Exception as e:
        print(f"❌ Erreur extraction de caractéristiques: {e}")

def test_semantic_similarity(advanced_classifier):
    """Test de la similarité sémantique"""
    print("\n🧠 Test de similarité sémantique...")
    
    test_pairs = [
        ("ordinateur portable", "laptop computer"),
        ("voiture automobile", "car vehicle"),
        ("médicament", "medicine drug"),
        ("café en grains", "coffee beans")
    ]
    
    for text1, text2 in test_pairs:
        try:
            similarity = advanced_classifier.calculate_semantic_similarity(text1, text2)
            print(f"   '{text1}' vs '{text2}': {similarity:.3f}")
        except Exception as e:
            print(f"❌ Erreur similarité sémantique: {e}")

def test_rgi_rules(advanced_classifier):
    """Test des règles RGI"""
    print("\n📋 Test des règles RGI...")
    
    # Test RGI 3 (matériau prépondérant)
    test_description = "Sac en cuir avec poignées en métal et fermeture en plastique"
    
    try:
        features = advanced_classifier.extract_features(test_description)
        print(f"   Matériaux détectés: {features['materials']}")
        
        if len(features['materials']) > 1:
            material_counts = {}
            for material in features['materials']:
                material_counts[material] = test_description.lower().count(material)
            
            predominant = max(material_counts, key=material_counts.get)
            print(f"   Matériau prépondérant (RGI 3): {predominant}")
    except Exception as e:
        print(f"❌ Erreur test RGI: {e}")

def main():
    """Fonction principale de test"""
    print("🏛️ Test de l'IA Classificateur CEDEAO")
    print("=" * 80)
    
    # Test du classificateur de base
    classifier = test_basic_classifier()
    if not classifier:
        print("❌ Impossible de continuer sans le classificateur de base")
        return
    
    # Test du classificateur avancé
    advanced_classifier = test_advanced_classifier()
    
    # Tests de classification
    test_product_classification(classifier, advanced_classifier)
    
    # Tests avancés si disponible
    if advanced_classifier:
        test_feature_extraction(advanced_classifier)
        test_semantic_similarity(advanced_classifier)
        test_rgi_rules(advanced_classifier)
    
    print("\n✅ Tests terminés!")
    print("\n💡 Pour lancer l'application complète:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    main()

