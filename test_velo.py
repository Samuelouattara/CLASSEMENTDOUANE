#!/usr/bin/env python3
"""
Test simple pour vérifier la classification du vélo
"""

from app_advanced import AdvancedCEDEAOClassifier

def test_velo():
    print("🚲 Test de classification du vélo")
    print("=" * 40)
    
    # Initialisation du classificateur
    classifier = AdvancedCEDEAOClassifier()
    
    # Test avec description de vélo
    description = "Vélo de route en aluminium, cadre rigide, 21 vitesses, roues 700c, freins à disque, guidon de course, selle sportive, pédales automatiques, poids 12kg, couleur rouge"
    
    print(f"📝 Description: {description}")
    print()
    
    # Classification
    result = classifier.classify_product(description)
    
    if result['best_match']:
        best = result['best_match']
        section = classifier.get_section_for_chapter(best['code'].split('.')[0])
        
        print("✅ Classification réussie!")
        print(f"📋 Code SH: {best['code']}")
        print(f"📋 Section: {section}")
        print(f"📋 Description: {best['description']}")
        print(f"📋 Taux: {best['rate']}")
        print(f"📊 Confiance: {result['confidence']:.1%}")
        
        # Caractéristiques extraites
        features = result['features']
        if any(features.values()):
            print("\n🔬 Caractéristiques extraites:")
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
            print("\n⚖️ Règles RGI appliquées")
        
        print(f"\n🎯 Résultat attendu: Code 87.12 - Cycles")
        print(f"🎯 Résultat obtenu: Code {best['code']}")
        
        if best['code'] == '87.12':
            print("✅ Classification correcte!")
        else:
            print("❌ Classification incorrecte")
            
    else:
        print("❌ Aucune classification trouvée")
        if result['suggestions']:
            print("💡 Suggestions d'amélioration:")
            for suggestion in result['suggestions']:
                print(f"   • {suggestion}")

if __name__ == "__main__":
    test_velo()

