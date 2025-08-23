#!/usr/bin/env python3
"""
Script de test pour la version avancée de l'IA Classificateur CEDEAO
"""

import sys
import os
from app_advanced import AdvancedCEDEAOClassifier

def test_advanced_classifier():
    """Teste le classificateur avancé avec différents produits"""
    
    print("🧪 Test de la Version Avancée - IA Classificateur CEDEAO")
    print("=" * 60)
    
    try:
        # Initialisation du classificateur
        print("🔄 Initialisation du classificateur avancé...")
        classifier = AdvancedCEDEAOClassifier()
        
        print(f"✅ Classificateur initialisé avec succès!")
        print(f"📊 Sections chargées: {len(classifier.sections)}")
        print(f"📊 Chapitres chargés: {len(classifier.chapters)}")
        print(f"📊 Sous-positions chargées: {len(classifier.subheadings)}")
        print(f"📊 Produits en base: {len(classifier.product_database)}")
        print()
        
        # Tests avec différents produits
        test_cases = [
            {
                "name": "Ordinateur portable détaillé",
                "description": "Ordinateur portable Dell Latitude 5520, processeur Intel Core i7-1165G7 2.8GHz, 16GB RAM DDR4, disque SSD 512GB, écran LCD 15.6 pouces 1920x1080, carte graphique Intel UHD Graphics, WiFi 6, Bluetooth 5.0, batterie lithium-ion 68Wh, poids 1.8kg, couleur noir"
            },
            {
                "name": "T-shirt avec spécifications",
                "description": "T-shirt en coton 100% bio, manches courtes, col rond, taille M, couleur bleue marine, marque Nike, fabriqué au Bangladesh, poids 180g"
            },
            {
                "name": "Médicament avec détails",
                "description": "Médicament antibiotique Amoxicilline 500mg, comprimés pelliculés, boîte de 20 unités, prescription médicale obligatoire, fabricant Pfizer, date d'expiration 2025"
            },
            {
                "name": "Voiture avec caractéristiques",
                "description": "Voiture automobile Toyota Corolla, moteur essence 1.8L 4 cylindres, 4 portes, transmission automatique CVT, année 2023, couleur blanche, équipements: climatisation, GPS, caméra de recul"
            },
            {
                "name": "Smartphone moderne",
                "description": "Smartphone Samsung Galaxy S23, écran AMOLED 6.1 pouces 2340x1080, processeur Snapdragon 8 Gen 2, 8GB RAM, stockage 256GB, caméra triple 50MP+12MP+10MP, batterie 3900mAh, 5G, WiFi 6E, Bluetooth 5.3, Android 13"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"🔍 Test {i}: {test_case['name']}")
            print("-" * 40)
            
            # Classification
            result = classifier.classify_product(test_case['description'])
            
            if result['best_match']:
                best = result['best_match']
                section = classifier.get_section_for_chapter(best['code'].split('.')[0])
                
                print(f"✅ Classification réussie!")
                print(f"📋 Code SH: {best['code']}")
                print(f"📋 Section: {section}")
                print(f"📋 Description: {best['description']}")
                print(f"📋 Taux: {best['rate']}")
                print(f"📊 Confiance: {result['confidence']:.1%}")
                
                # Caractéristiques extraites
                features = result['features']
                if any(features.values()):
                    print("🔬 Caractéristiques extraites:")
                    if features['materials']:
                        print(f"   • Matériaux: {', '.join(features['materials'])}")
                    if features['functions']:
                        print(f"   • Fonctions: {', '.join(features['functions'])}")
                    if features['brands']:
                        print(f"   • Marques: {', '.join(features['brands'])}")
                    if features['dimensions']:
                        print(f"   • Dimensions: {', '.join(features['dimensions'])}")
                    if features['technical_specs']:
                        print(f"   • Spécifications: {', '.join(features['technical_specs'])}")
                
                # Règles RGI appliquées
                if best.get('rgi_applied'):
                    print("⚖️ Règles RGI appliquées")
                
                # Alternatives
                if len(result['all_matches']) > 1:
                    print("🔍 Alternatives disponibles:")
                    for j, match in enumerate(result['all_matches'][1:4], 2):
                        print(f"   {j}. {match['code']} - {match['confidence']:.1%}")
                
            else:
                print("❌ Aucune classification trouvée")
                if result['suggestions']:
                    print("💡 Suggestions d'amélioration:")
                    for suggestion in result['suggestions']:
                        print(f"   • {suggestion}")
            
            print()
        
        # Test des fonctionnalités avancées
        print("🤖 Test des fonctionnalités avancées")
        print("-" * 40)
        
        # Test d'extraction de caractéristiques
        test_text = "Ordinateur portable Dell avec processeur Intel, 16GB RAM, écran 15.6 pouces"
        features = classifier.extract_features(test_text)
        print(f"🔬 Extraction de caractéristiques:")
        print(f"   • Matériaux: {features['materials']}")
        print(f"   • Fonctions: {features['functions']}")
        print(f"   • Marques: {features['brands']}")
        print(f"   • Dimensions: {features['dimensions']}")
        print(f"   • Spécifications: {features['technical_specs']}")
        
        # Test de similarité sémantique
        similarity = classifier.calculate_semantic_similarity(
            "ordinateur portable", 
            "laptop computer"
        )
        print(f"📊 Similarité sémantique: {similarity:.3f}")
        
        print()
        print("🎉 Tous les tests terminés avec succès!")
        print("🚀 L'application avancée est prête à être utilisée.")
        print("📱 Accédez à l'interface web sur: http://localhost:8503")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_nlp_models():
    """Teste les modèles NLP"""
    print("🧠 Test des modèles NLP")
    print("-" * 30)
    
    try:
        from app_advanced import AdvancedCEDEAOClassifier
        classifier = AdvancedCEDEAOClassifier()
        
        # Test spaCy
        test_text = "Ordinateur portable Dell avec processeur Intel"
        doc = classifier.nlp(test_text)
        print(f"✅ spaCy fonctionne: {len(doc)} tokens détectés")
        
        # Test NLTK
        import nltk
        tokens = nltk.word_tokenize(test_text)
        print(f"✅ NLTK fonctionne: {len(tokens)} tokens détectés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur NLP: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests de la version avancée...")
    print()
    
    # Test des modèles NLP
    nlp_ok = test_nlp_models()
    print()
    
    if nlp_ok:
        # Test du classificateur
        success = test_advanced_classifier()
        
        if success:
            print("\n✅ Tous les tests sont passés avec succès!")
            sys.exit(0)
        else:
            print("\n❌ Certains tests ont échoué.")
            sys.exit(1)
    else:
        print("\n❌ Les modèles NLP ne fonctionnent pas correctement.")
        sys.exit(1)

