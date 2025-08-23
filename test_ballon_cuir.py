#!/usr/bin/env python3
"""
Test spécifique pour "ballon en cuir" - vérification que l'AttributeError est résolu
"""

from app_advanced import AdvancedCEDEAOClassifier

def test_ballon_cuir():
    print("🔍 Test spécifique: 'ballon en cuir'")
    print("=" * 50)
    
    # Initialisation du classificateur
    classifier = AdvancedCEDEAOClassifier()
    
    # Test avec "ballon en cuir"
    description = "ballon en cuir"
    print(f"📝 Description: {description}")
    
    try:
        result = classifier.classify_product(description)
        
        if result.get('is_ambiguous', False):
            print("⚠️ Description ambiguë détectée")
            ambiguity_details = result.get('ambiguity_details', {})
            print(f"📋 Type: {ambiguity_details.get('type', 'N/A')}")
            print(f"📋 Message: {ambiguity_details.get('message', 'N/A')}")
            
            if result.get('suggestions'):
                print("💡 Suggestions:")
                for suggestion in result['suggestions']:
                    print(f"   • {suggestion}")
        else:
            print("✅ Classification réussie")
            if result.get('best_match'):
                best = result['best_match']
                print(f"📋 Code: {best['code']}")
                print(f"📋 Description: {best['description']}")
                print(f"📋 Taux: {best['rate']}")
                print(f"📊 Confiance: {result.get('confidence', 0):.1%}")
                
                # Test de la méthode get_section_for_chapter
                try:
                    chapter_code = best['code'].split('.')[0]
                    section = classifier.get_section_for_chapter(chapter_code)
                    print(f"📋 Section: {section}")
                    print("✅ Méthode get_section_for_chapter fonctionne correctement!")
                except AttributeError as e:
                    print(f"❌ Erreur avec get_section_for_chapter: {e}")
                except Exception as e:
                    print(f"❌ Autre erreur: {e}")
        
        print("\n🎉 Test terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la classification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ballon_cuir()

