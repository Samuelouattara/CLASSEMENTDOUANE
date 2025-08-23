#!/usr/bin/env python3
"""
Script de debug pour examiner le contenu des chapitres
"""

from app_simple import SimpleCEDEAOClassifier

def main():
    classifier = SimpleCEDEAOClassifier()
    
    print("🔍 Debug des chapitres:")
    print("=" * 50)
    
    # Chercher des chapitres spécifiques
    search_terms = ['ordinateur', 'machine', 'voiture', 'automobile', 'médicament', 'pharmaceutique', 'café', 'coton']
    
    for term in search_terms:
        print(f"\nRecherche du terme '{term}':")
        found = False
        
        for chapter_num, content in classifier.chapters.items():
            if term.lower() in content.lower():
                print(f"  Chapitre {chapter_num}: {content[:100]}...")
                found = True
        
        if not found:
            print(f"  Aucun chapitre trouvé contenant '{term}'")
    
    # Afficher quelques chapitres complets
    print("\n📋 Contenu de quelques chapitres:")
    for i, (chapter_num, content) in enumerate(list(classifier.chapters.items())[:10]):
        print(f"\nChapitre {chapter_num}:")
        print(f"  {content}")

if __name__ == "__main__":
    main()

