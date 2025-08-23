#!/usr/bin/env python3
"""
Test de la gestion d'erreur avec détection d'ambiguïté
"""

from app_advanced import AdvancedCEDEAOClassifier

def test_ambiguity_detection():
    print("🔍 Test de la Détection d'Ambiguïté")
    print("=" * 50)
    
    # Initialisation du classificateur
    classifier = AdvancedCEDEAOClassifier()
    
    # Tests avec des descriptions ambiguës
    test_cases = [
        {
            "description": "Ballon",
            "expected_type": "ambiguous_word",
            "category": "Mot ambigu - nécessite précisions"
        },
        {
            "description": "Sac",
            "expected_type": "ambiguous_word", 
            "category": "Mot ambigu - nécessite précisions"
        },
        {
            "description": "Bouteille",
            "expected_type": "ambiguous_word",
            "category": "Mot ambigu - nécessite précisions"
        },
        {
            "description": "Boîte",
            "expected_type": "ambiguous_word",
            "category": "Mot ambigu - nécessite précisions"
        },
        {
            "description": "Chose",
            "expected_type": "very_generic",
            "category": "Mot trop générique"
        },
        {
            "description": "Objet",
            "expected_type": "very_generic",
            "category": "Mot trop générique"
        },
        {
            "description": "A",
            "expected_type": "too_short",
            "category": "Description trop courte"
        },
        {
            "description": "Voiture",
            "expected_type": "ambiguous_word",
            "category": "Mot ambigu - nécessite précisions"
        },
        {
            "description": "Téléphone",
            "expected_type": "ambiguous_word",
            "category": "Mot ambigu - nécessite précisions"
        },
        {
            "description": "Ballon de football en cuir Adidas",
            "expected_type": "clear",
            "category": "Description claire - devrait être classifiée"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test #{i}: {test_case['category']}")
        print(f"📝 Description: {test_case['description']}")
        print(f"🎯 Attendu: Type {test_case['expected_type']}")
        
        # Classification
        result = classifier.classify_product(test_case['description'])
        
        # Vérifier si ambigu
        is_ambiguous = result.get('is_ambiguous', False)
        ambiguity_details = result.get('ambiguity_details', {})
        actual_type = ambiguity_details.get('type', 'clear')
        
        if is_ambiguous:
            print(f"✅ Ambiguïté détectée: {actual_type}")
            print(f"📋 Message: {ambiguity_details.get('message', 'N/A')}")
            
            if ambiguity_details.get('clarifications'):
                print("🔍 Clarifications nécessaires:")
                for j, clarification in enumerate(ambiguity_details['clarifications'], 1):
                    print(f"   {j}. {clarification}")
            
            if result['suggestions']:
                print("💡 Suggestions:")
                for suggestion in result['suggestions']:
                    print(f"   • {suggestion}")
            
            # Vérification
            if actual_type == test_case['expected_type']:
                print("✅ CORRECT!")
                results.append(True)
            else:
                print(f"❌ INCORRECT - Attendu: {test_case['expected_type']}, Obtenu: {actual_type}")
                results.append(False)
        else:
            if test_case['expected_type'] == 'clear':
                print("✅ Description claire - classification réussie")
                if result['best_match']:
                    print(f"📋 Code: {result['best_match']['code']}")
                    print(f"📊 Confiance: {result['confidence']:.1%}")
                results.append(True)
            else:
                print(f"❌ Ambiguïté non détectée - Attendu: {test_case['expected_type']}")
                results.append(False)
        
        print("-" * 40)
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DES TESTS")
    print("=" * 40)
    print(f"Tests réussis: {sum(results)}/{len(results)}")
    print(f"Taux de réussite: {sum(results)/len(results)*100:.1%}")
    
    if sum(results) == len(results):
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("🧠 La détection d'ambiguïté fonctionne parfaitement!")
    else:
        print("⚠️ Certains tests ont échoué")
    
    # Test spécifique pour "Ballon"
    print(f"\n🎈 TEST SPÉCIFIQUE POUR 'BALLON'")
    print("=" * 40)
    
    result = classifier.classify_product("Ballon")
    if result.get('is_ambiguous'):
        ambiguity_details = result.get('ambiguity_details', {})
        print(f"✅ Ambiguïté détectée: {ambiguity_details.get('type')}")
        print(f"📋 Message: {ambiguity_details.get('message')}")
        
        if ambiguity_details.get('clarifications'):
            print("🔍 Clarifications demandées:")
            for i, clarification in enumerate(ambiguity_details['clarifications'], 1):
                print(f"{i}. {clarification}")
        
        print("\n💡 Exemples de descriptions améliorées:")
        print("• Ballon de football en cuir naturel, taille 5, marque Adidas")
        print("• Ballon de baudruche en caoutchouc, couleur rouge, diamètre 30cm")
        print("• Ballon gonflable en plastique, forme ronde, pour piscine")
    else:
        print("❌ Ambiguïté non détectée pour 'Ballon'")

if __name__ == "__main__":
    test_ambiguity_detection()

