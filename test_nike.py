#!/usr/bin/env python3
"""
Test spécifique pour Nike Air Max
"""

from app_advanced import AdvancedCEDEAOClassifier

def test_nike_air_max():
    print("🔍 Test spécifique pour Nike Air Max")
    print("=" * 40)
    
    classifier = AdvancedCEDEAOClassifier()
    description = "Nike Air Max"
    
    print(f"📝 Description: {description}")
    print()
    
    # Classification
    result = classifier.classify_product(description)
    
    if result['all_matches']:
        print("🔍 Toutes les correspondances trouvées:")
        for i, match in enumerate(result['all_matches']):
            print(f"\n{i+1}. {match['code']} - {match['description']}")
            print(f"   Confiance: {match['confidence']:.1%}")
            print(f"   Type: {match['type']}")
            
            match_details = match.get('match_details', {})
            if match_details:
                print("   Détails:")
                if match_details.get('keyword_match'):
                    print("     • Mot-clé principal")
                if match_details.get('synonym_matches'):
                    print(f"     • Synonymes: {', '.join(match_details['synonym_matches'])}")
                if match_details.get('brand_matches'):
                    print(f"     • Marques: {', '.join(match_details['brand_matches'])}")
                if match_details.get('material_matches'):
                    print(f"     • Matériaux: {', '.join(match_details['material_matches'])}")
                if match_details.get('function_matches'):
                    print(f"     • Fonctions: {', '.join(match_details['function_matches'])}")
    
    # Vérifier les produits contenant "nike"
    print(f"\n🔍 Produits contenant 'nike' dans la base:")
    for keyword, product_data in classifier.product_database.items():
        if 'nike' in product_data.get('brands', []):
            print(f"• {keyword}: {product_data['code']} - {product_data['description']}")
            print(f"  Synonymes: {product_data.get('synonyms', [])}")

if __name__ == "__main__":
    test_nike_air_max()

