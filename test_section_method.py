#!/usr/bin/env python3
"""
Test rapide pour vérifier que la méthode get_section_for_chapter fonctionne
"""

from app_advanced import AdvancedCEDEAOClassifier

def test_section_method():
    print("🔍 Test de la méthode get_section_for_chapter")
    print("=" * 50)
    
    # Initialisation du classificateur
    classifier = AdvancedCEDEAOClassifier()
    
    # Tests de quelques chapitres
    test_chapters = [
        ('87', 'XVII'),  # Véhicules
        ('84', 'XVI'),   # Machines
        ('85', 'XVI'),   # Appareils électriques
        ('61', 'XI'),    # Vêtements
        ('1', 'I'),      # Animaux vivants
        ('99', 'XXII')   # Non déterminée
    ]
    
    for chapter, expected_section in test_chapters:
        result = classifier.get_section_for_chapter(chapter)
        status = "✅" if result == expected_section else "❌"
        print(f"{status} Chapitre {chapter} → Section {result} (attendu: {expected_section})")
    
    print("\n🎉 Test terminé!")

if __name__ == "__main__":
    test_section_method()

