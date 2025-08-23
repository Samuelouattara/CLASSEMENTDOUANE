#!/usr/bin/env python3
"""
Test du système intelligent avec marques et synonymes
"""

from app_advanced import AdvancedCEDEAOClassifier

def test_intelligent_classification():
    print("🧠 Test du Système Intelligent avec Marques et Synonymes")
    print("=" * 60)
    
    # Initialisation du classificateur
    classifier = AdvancedCEDEAOClassifier()
    
    # Tests avec différentes descriptions
    test_cases = [
        {
            "description": "Peugeot 208",
            "expected": "87.03",
            "category": "Voiture par marque"
        },
        {
            "description": "iPhone 15 Pro",
            "expected": "85.17", 
            "category": "Smartphone par marque"
        },
        {
            "description": "VTT Trek Marlin",
            "expected": "87.12",
            "category": "Vélo par synonyme + marque"
        },
        {
            "description": "Nike Air Max",
            "expected": "64.03",
            "category": "Chaussures par marque"
        },
        {
            "description": "MacBook Pro",
            "expected": "84.71",
            "category": "Ordinateur portable par marque"
        },
        {
            "description": "Rolex Submariner",
            "expected": "91.02",
            "category": "Montre par marque"
        },
        {
            "description": "Bicyclette en aluminium",
            "expected": "87.12",
            "category": "Vélo par synonyme + matériau"
        },
        {
            "description": "Automobile Toyota",
            "expected": "87.03",
            "category": "Voiture par synonyme + marque"
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
                if match_details.get('function_matches'):
                    print(f"   • ⚙️ Fonctions: {', '.join(match_details['function_matches'])}")
            
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
        
        print("-" * 40)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DES TESTS")
    print("=" * 40)
    print(f"Tests réussis: {sum(results)}/{len(results)}")
    print(f"Taux de réussite: {sum(results)/len(results)*100:.1%}")
    
    if sum(results) == len(results):
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
    else:
        print("⚠️ Certains tests ont échoué")

if __name__ == "__main__":
    test_intelligent_classification()

