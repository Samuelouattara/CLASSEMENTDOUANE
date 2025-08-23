#!/usr/bin/env python3
"""
Test du système ultra-intelligent avec dictionnaire français complet
"""

from app_advanced import AdvancedCEDEAOClassifier

def test_ultra_intelligent_classification():
    print("🧠 Test du Système Ultra-Intelligent avec Dictionnaire Français Complet")
    print("=" * 70)
    
    # Initialisation du classificateur
    classifier = AdvancedCEDEAOClassifier()
    
    # Tests avec différentes descriptions utilisant le vocabulaire français complet
    test_cases = [
        {
            "description": "Bicyclette en aluminium avec cadre rigide",
            "expected": "87.12",
            "category": "Vélo par synonyme + matériau français"
        },
        {
            "description": "Automobile Toyota Corolla essence",
            "expected": "87.03",
            "category": "Voiture par synonyme + marque"
        },
        {
            "description": "Ordinateur portable Dell Latitude",
            "expected": "84.71",
            "category": "Ordinateur par synonyme + marque"
        },
        {
            "description": "Téléphone mobile Samsung Galaxy",
            "expected": "85.17",
            "category": "Smartphone par synonyme + marque"
        },
        {
            "description": "Vêtement en coton bio",
            "expected": "61.09",
            "category": "Vêtement par mot-clé + matériau"
        },
        {
            "description": "Sac en cuir naturel",
            "expected": "42.02",
            "category": "Sac par mot-clé + matériau"
        },
        {
            "description": "Montre bracelet Rolex",
            "expected": "91.02",
            "category": "Montre par synonyme + marque"
        },
        {
            "description": "Chaussure en caoutchouc",
            "expected": "64.03",
            "category": "Chaussure par synonyme + matériau"
        },
        {
            "description": "Mobilier en bois massif",
            "expected": "94.03",
            "category": "Meuble par synonyme + matériau"
        },
        {
            "description": "Écran LCD 24 pouces",
            "expected": "84.71",
            "category": "Technologie par mot-clé + spécifications"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test #{i}: {test_case['category']}")
        print(f"📝 Description: {test_case['description']}")
        print(f"🎯 Attendu: Code {test_case['expected']}")
        
        # Classification
        result = classifier.classify_product(test_case['description'])
        
        if result['best_match']:
            best = result['best_match']
            section = classifier.get_section_for_chapter(best['code'].split('.')[0])
            
            print(f"✅ Résultat: Code {best['code']} - {best['description']}")
            print(f"📊 Confiance: {result['confidence']:.1%}")
            print(f"📋 Section: {section}")
            print(f"💰 Taux: {best['rate']}")
            
            # Analyse linguistique
            language_analysis = result.get('language_analysis', {})
            if language_analysis:
                print("📚 Analyse Linguistique:")
                if language_analysis.get('french_words'):
                    print(f"   • Mots français reconnus: {len(language_analysis['french_words'])}")
                    print(f"     {', '.join(language_analysis['french_words'][:5])}")
                
                if language_analysis.get('unknown_words'):
                    print(f"   • Mots non reconnus: {language_analysis['unknown_words']}")
                
                if language_analysis.get('semantic_categories'):
                    print(f"   • Catégories sémantiques: {len(language_analysis['semantic_categories'])}")
            
            # Détails de correspondance
            match_details = best.get('match_details', {})
            if match_details:
                print("🔍 Détails de correspondance:")
                if match_details.get('keyword_match'):
                    print("   • ✅ Mot-clé principal")
                if match_details.get('synonym_matches'):
                    print(f"   • 🔄 Synonymes: {', '.join(match_details['synonym_matches'])}")
                if match_details.get('brand_matches'):
                    print(f"   • 🏷️ Marques: {', '.join(match_details['brand_matches'])}")
                if match_details.get('material_matches'):
                    print(f"   • 🧱 Matériaux: {', '.join(match_details['material_matches'])}")
                if match_details.get('semantic_matches'):
                    print(f"   • 🧠 Sémantique: {', '.join(match_details['semantic_matches'])}")
                if match_details.get('similar_word_matches'):
                    print(f"   • 🔗 Mots similaires: {', '.join(match_details['similar_word_matches'])}")
            
            # Vérification
            if best['code'] == test_case['expected']:
                print("✅ CORRECT!")
                results.append(True)
            else:
                print(f"❌ INCORRECT - Attendu: {test_case['expected']}, Obtenu: {best['code']}")
                results.append(False)
        else:
            print("❌ Aucune classification trouvée")
            results.append(False)
        
        print("-" * 50)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"Tests réussis: {sum(results)}/{len(results)}")
    print(f"Taux de réussite: {sum(results)/len(results)*100:.1%}")
    
    if sum(results) == len(results):
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("🧠 Le système ultra-intelligent fonctionne parfaitement!")
    else:
        print("⚠️ Certains tests ont échoué")
    
    # Test du dictionnaire français
    print(f"\n📚 TEST DU DICTIONNAIRE FRANÇAIS")
    print("=" * 50)
    processor = classifier.language_processor
    
    test_words = ['véhicule', 'automobile', 'bicyclette', 'ordinateur', 'téléphone', 'vêtement', 'chaussure']
    for word in test_words:
        synonyms = processor.get_synonyms(word)
        categories = processor.get_semantic_category(word)
        similar = processor.find_similar_words(word)
        
        print(f"📖 '{word}':")
        print(f"   • Synonymes: {len(synonyms)} - {', '.join(synonyms[:3])}")
        print(f"   • Catégories: {', '.join(categories)}")
        print(f"   • Mots similaires: {len(similar)}")

if __name__ == "__main__":
    test_ultra_intelligent_classification()

