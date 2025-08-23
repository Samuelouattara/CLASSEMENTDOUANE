#!/usr/bin/env python3
"""
Script de test simple pour l'IA Classificateur CEDEAO
"""

from app_simple import SimpleCEDEAOClassifier

def main():
    print("🏛️ Test de l'IA Classificateur CEDEAO - Version Simple")
    print("=" * 60)
    
    # Test du classificateur
    print("🧪 Initialisation du classificateur...")
    classifier = SimpleCEDEAOClassifier()
    
    print(f"📊 Sections chargées: {len(classifier.sections)}")
    print(f"📊 Chapitres chargés: {len(classifier.chapters)}")
    print(f"📊 Sous-positions chargées: {len(classifier.subheadings)}")
    
    # Afficher quelques exemples
    print("\n📋 Exemples de sections:")
    for i, (section_num, title) in enumerate(list(classifier.sections.items())[:5]):
        print(f"  Section {section_num}: {title[:50]}...")
    
    print("\n📋 Exemples de chapitres:")
    for i, (chapter_num, content) in enumerate(list(classifier.chapters.items())[:5]):
        print(f"  Chapitre {chapter_num}: {content[:50]}...")
    
    print("\n📋 Exemples de sous-positions:")
    for i, (code, data) in enumerate(list(classifier.subheadings.items())[:3]):
        print(f"  {code}: {data['description'][:50]}... (taux: {data['rate']})")
    
    # Test de recherche
    print("\n🔍 Test de recherche:")
    test_queries = [
        "ordinateur portable",
        "voiture automobile",
        "médicament",
        "café",
        "t-shirt coton"
    ]
    
    for query in test_queries:
        print(f"\nRecherche: '{query}'")
        results = classifier.search_product(query)
        print(f"  Résultats trouvés: {len(results)}")
        
        if results:
            for i, result in enumerate(results[:3]):
                print(f"    {i+1}. {result['code']}: {result['description'][:80]}... (pertinence: {result['relevance']:.2%})")
        else:
            print("    Aucun résultat trouvé")
    
    print("\n✅ Test terminé!")

if __name__ == "__main__":
    main()

