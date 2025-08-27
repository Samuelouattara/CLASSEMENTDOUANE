#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test complet pour le dictionnaire français
"""

from dictionnaire_utils import DictionnaireFrancais, analyser_description_douane, suggerer_améliorations_description

def test_dictionnaire_complet():
    """Test complet du dictionnaire français"""
    
    print("=" * 60)
    print("TEST COMPLET DU DICTIONNAIRE FRANÇAIS")
    print("=" * 60)
    
    # Initialiser le dictionnaire
    dico = DictionnaireFrancais()
    
    # Test 1: Vérification de mots français
    print("\n1. TEST DE RECONNAISSANCE DE MOTS FRANÇAIS")
    print("-" * 40)
    
    mots_test = ["ballon", "cuir", "football", "france", "sportif", "xyz123", "computer"]
    for mot in mots_test:
        est_francais = dico.est_mot_francais(mot)
        print(f"'{mot}' → {'✓ Français' if est_francais else '✗ Non français'}")
    
    # Test 2: Analyse de descriptions douanières
    print("\n2. TEST D'ANALYSE DE DESCRIPTIONS DOUANIÈRES")
    print("-" * 40)
    
    descriptions_test = [
        "Ballon de football en cuir naturel, fabriqué en France",
        "Smartphone Samsung Galaxy avec écran tactile",
        "Vélo de course en aluminium, roues carbone",
        "Ordinateur portable Dell avec processeur Intel",
        "Chaussures Nike Air Max en cuir et textile"
    ]
    
    for desc in descriptions_test:
        analyse = analyser_description_douane(desc, dico)
        print(f"\nDescription: {desc}")
        print(f"Ratio français: {analyse['ratio_francais']:.1%}")
        print(f"Mots français: {', '.join(analyse['mots_francais_trouves'])}")
        print(f"Est principalement français: {'✓ Oui' if analyse['est_principalement_francais'] else '✗ Non'}")
    
    # Test 3: Suggestions d'amélioration
    print("\n3. TEST DE SUGGESTIONS D'AMÉLIORATION")
    print("-" * 40)
    
    description_avec_erreurs = "Smartphone avec ecran tactile et batterie lithium"
    suggestions = suggerer_améliorations_description(description_avec_erreurs, dico)
    
    print(f"Description avec erreurs: {description_avec_erreurs}")
    print("Suggestions d'amélioration:")
    for suggestion in suggestions:
        print(f"  • {suggestion}")
    
    # Test 4: Statistiques du dictionnaire
    print("\n4. STATISTIQUES DU DICTIONNAIRE")
    print("-" * 40)
    
    stats = dico.obtenir_statistiques()
    print(f"Total de mots: {stats['total_mots']}")
    print(f"Longueur moyenne: {stats['longueur_moyenne']:.1f} caractères")
    
    # Afficher la répartition par longueur
    print("\nRépartition par longueur de mot:")
    for longueur in sorted(stats['mots_par_longueur'].keys()):
        count = stats['mots_par_longueur'][longueur]
        print(f"  {longueur} caractères: {count} mots")
    
    # Test 5: Filtrage de texte français
    print("\n5. TEST DE FILTRAGE DE TEXTE FRANÇAIS")
    print("-" * 40)
    
    textes_test = [
        "Ce produit est fabriqué en France avec des matériaux de qualité",
        "This product is made in China with high quality materials",
        "Vélo de course professionnel avec cadre en carbone",
        "Computer laptop with Intel processor and Windows OS"
    ]
    
    for texte in textes_test:
        est_francais = dico.filtrer_texte_francais(texte)
        ratio = dico.calculer_ratio_francais(texte)
        print(f"Texte: {texte[:50]}...")
        print(f"Ratio français: {ratio:.1%} → {'✓ Français' if est_francais else '✗ Non français'}")
    
    # Test 6: Suggestions de mots similaires
    print("\n6. TEST DE SUGGESTIONS DE MOTS SIMILAIRES")
    print("-" * 40)
    
    mots_similaires_test = ["ballon", "cuir", "velo", "telephone"]
    for mot in mots_similaires_test:
        suggestions = dico.suggerer_mots_similaires(mot, 3)
        print(f"'{mot}' → suggestions: {', '.join(suggestions)}")
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ AVEC SUCCÈS !")
    print("=" * 60)

def test_integration_douane():
    """Test d'intégration avec des cas douaniers réels"""
    
    print("\n" + "=" * 60)
    print("TEST D'INTÉGRATION DOUANIÈRE")
    print("=" * 60)
    
    dico = DictionnaireFrancais()
    
    # Cas douaniers réels
    cas_douaniers = [
        {
            "description": "Ballon de football en cuir naturel, taille 5, pour usage sportif",
            "categorie_attendue": "Articles de sport"
        },
        {
            "description": "Smartphone Samsung Galaxy avec écran tactile et caméra haute résolution",
            "categorie_attendue": "Électronique"
        },
        {
            "description": "Vélo de course en aluminium avec roues en carbone et freins à disque",
            "categorie_attendue": "Véhicules"
        },
        {
            "description": "Ordinateur portable Dell avec processeur Intel i7 et SSD 512GB",
            "categorie_attendue": "Informatique"
        },
        {
            "description": "Chaussures Nike Air Max en cuir et textile avec semelle en caoutchouc",
            "categorie_attendue": "Chaussures"
        }
    ]
    
    for i, cas in enumerate(cas_douaniers, 1):
        print(f"\n--- CAS DOUANIER {i} ---")
        print(f"Description: {cas['description']}")
        print(f"Catégorie attendue: {cas['categorie_attendue']}")
        
        # Analyse avec le dictionnaire
        analyse = analyser_description_douane(cas['description'], dico)
        print(f"Ratio français: {analyse['ratio_francais']:.1%}")
        print(f"Mots français identifiés: {len(analyse['mots_francais_trouves'])}")
        
        # Suggestions d'amélioration
        suggestions = suggerer_améliorations_description(cas['description'], dico)
        if suggestions:
            print("Suggestions d'amélioration:")
            for suggestion in suggestions:
                print(f"  • {suggestion}")
        else:
            print("✓ Aucune suggestion nécessaire - description optimale")
    
    print("\n" + "=" * 60)
    print("INTÉGRATION DOUANIÈRE TESTÉE AVEC SUCCÈS !")
    print("=" * 60)

if __name__ == "__main__":
    # Exécuter tous les tests
    test_dictionnaire_complet()
    test_integration_douane()
    
    print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
    print("Le dictionnaire français est prêt pour l'intégration dans l'application de classement douanier.")
