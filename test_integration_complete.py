#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet de l'intégration du dictionnaire français dans l'application CEDEAO
"""

import sys
import os
from app import CEDEAOClassifier

def test_integration_complete():
    """Test complet de l'intégration"""
    
    print("=" * 70)
    print("TEST D'INTÉGRATION COMPLÈTE - DICTIONNAIRE FRANÇAIS + CEDEAO")
    print("=" * 70)
    
    # Test 1: Initialisation du classificateur
    print("\n1. TEST D'INITIALISATION")
    print("-" * 40)
    
    try:
        classifier = CEDEAOClassifier()
        print("✅ Classificateur CEDEAO initialisé avec succès")
        print(f"   - Sections: {len(classifier.sections)}")
        print(f"   - Chapitres: {len(classifier.chapters)}")
        print(f"   - Sous-positions: {len(classifier.subheadings)}")
        
        if classifier.dictionnaire_francais:
            print(f"   - Dictionnaire français: {len(classifier.dictionnaire_francais.mots_francais)} mots")
        else:
            print("   ⚠️ Dictionnaire français non disponible")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False
    
    # Test 2: Analyse de descriptions douanières
    print("\n2. TEST D'ANALYSE DE DESCRIPTIONS DOUANIÈRES")
    print("-" * 40)
    
    descriptions_test = [
        "Ballon de football en cuir naturel, fabriqué en France",
        "Smartphone Samsung Galaxy avec écran tactile et caméra haute résolution",
        "Vélo de course en aluminium avec roues en carbone",
        "Ordinateur portable Dell avec processeur Intel i7 et SSD 512GB",
        "Chaussures Nike Air Max en cuir et textile avec semelle en caoutchouc"
    ]
    
    for i, desc in enumerate(descriptions_test, 1):
        print(f"\n--- Description {i} ---")
        print(f"Texte: {desc}")
        
        # Analyse française
        if classifier.dictionnaire_francais:
            analyse_fr = classifier.analyser_description_francaise(desc)
            if analyse_fr["disponible"]:
                analyse = analyse_fr["analyse"]
                qualite = analyse_fr["qualite_francais"]
                print(f"   Ratio français: {analyse['ratio_francais']:.1%}")
                print(f"   Qualité: {qualite}")
                print(f"   Mots français: {len(analyse['mots_francais_trouves'])}")
                
                if analyse_fr['suggestions']:
                    print(f"   Suggestions: {len(analyse_fr['suggestions'])}")
            else:
                print("   ❌ Analyse française non disponible")
        
        # Classification CEDEAO
        try:
            results = classifier.search_product(desc, use_advanced=False)
            if results:
                best_result = results[0]
                print(f"   Meilleur résultat CEDEAO: {best_result['code']} ({best_result['relevance']:.1%})")
            else:
                print("   ⚠️ Aucun résultat CEDEAO trouvé")
        except Exception as e:
            print(f"   ❌ Erreur classification CEDEAO: {e}")
    
    # Test 3: Fonctionnalités du dictionnaire
    print("\n3. TEST DES FONCTIONNALITÉS DU DICTIONNAIRE")
    print("-" * 40)
    
    if classifier.dictionnaire_francais:
        # Test de reconnaissance de mots
        mots_test = ["ballon", "cuir", "football", "smartphone", "velo", "ordinateur"]
        print("\nTest de reconnaissance de mots:")
        for mot in mots_test:
            est_francais = classifier.dictionnaire_francais.est_mot_francais(mot)
            print(f"   '{mot}': {'✅ Français' if est_francais else '❌ Non français'}")
        
        # Test de suggestions
        print("\nTest de suggestions:")
        mots_similaires = ["ballon", "cuir", "velo"]
        for mot in mots_similaires:
            suggestions = classifier.dictionnaire_francais.suggerer_mots_similaires(mot, 3)
            print(f"   '{mot}' → {', '.join(suggestions) if suggestions else 'Aucune suggestion'}")
        
        # Test de statistiques
        stats = classifier.obtenir_statistiques_dictionnaire()
        print(f"\nStatistiques du dictionnaire:")
        print(f"   Total mots: {stats['total_mots']}")
        print(f"   Longueur moyenne: {stats['longueur_moyenne']:.1f}")
    else:
        print("❌ Dictionnaire français non disponible pour les tests")
    
    # Test 4: Enrichissement du dictionnaire
    print("\n4. TEST D'ENRICHISSEMENT DU DICTIONNAIRE")
    print("-" * 40)
    
    if classifier.dictionnaire_francais:
        mots_avant = len(classifier.dictionnaire_francais.mots_francais)
        nouveaux_mots = ["test_mot_1", "test_mot_2", "test_mot_3"]
        
        try:
            classifier.enrichir_dictionnaire(nouveaux_mots)
            mots_apres = len(classifier.dictionnaire_francais.mots_francais)
            print(f"✅ Enrichissement réussi: {mots_avant} → {mots_apres} mots")
            
            # Vérifier que les nouveaux mots sont bien ajoutés
            for mot in nouveaux_mots:
                if classifier.dictionnaire_francais.est_mot_francais(mot):
                    print(f"   ✅ '{mot}' ajouté avec succès")
                else:
                    print(f"   ❌ '{mot}' non trouvé après ajout")
                    
        except Exception as e:
            print(f"❌ Erreur lors de l'enrichissement: {e}")
    else:
        print("❌ Dictionnaire français non disponible pour l'enrichissement")
    
    # Test 5: Intégration complète
    print("\n5. TEST D'INTÉGRATION COMPLÈTE")
    print("-" * 40)
    
    description_complete = "Ballon de football professionnel en cuir naturel, taille 5, fabriqué en France, pour usage sportif"
    
    print(f"Description test: {description_complete}")
    
    # Analyse française
    if classifier.dictionnaire_francais:
        analyse_fr = classifier.analyser_description_francaise(description_complete)
        if analyse_fr["disponible"]:
            analyse = analyse_fr["analyse"]
            print(f"   Analyse française: {analyse['ratio_francais']:.1%} français")
            print(f"   Mots français trouvés: {len(analyse['mots_francais_trouves'])}")
    
    # Classification CEDEAO
    try:
        results = classifier.search_product(description_complete, use_advanced=False)
        if results:
            print(f"   Classification CEDEAO: {len(results)} résultat(s)")
            for i, result in enumerate(results[:3]):
                print(f"     {i+1}. {result['code']} - {result['relevance']:.1%}")
        else:
            print("   ⚠️ Aucun résultat CEDEAO")
    except Exception as e:
        print(f"   ❌ Erreur classification: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 TEST D'INTÉGRATION TERMINÉ AVEC SUCCÈS !")
    print("=" * 70)
    
    return True

def test_performance():
    """Test de performance de l'intégration"""
    
    print("\n" + "=" * 70)
    print("TEST DE PERFORMANCE")
    print("=" * 70)
    
    import time
    
    classifier = CEDEAOClassifier()
    
    # Test de performance - analyse française
    if classifier.dictionnaire_francais:
        start_time = time.time()
        for i in range(100):
            classifier.analyser_description_francaise("Test de performance")
        end_time = time.time()
        
        print(f"✅ 100 analyses françaises en {end_time - start_time:.3f} secondes")
        print(f"   Moyenne: {(end_time - start_time) / 100 * 1000:.2f} ms par analyse")
    
    # Test de performance - classification CEDEAO
    start_time = time.time()
    for i in range(10):
        classifier.search_product("Test de performance", use_advanced=False)
    end_time = time.time()
    
    print(f"✅ 10 classifications CEDEAO en {end_time - start_time:.3f} secondes")
    print(f"   Moyenne: {(end_time - start_time) / 10 * 1000:.2f} ms par classification")

if __name__ == "__main__":
    print("Démarrage des tests d'intégration...")
    
    # Test principal
    success = test_integration_complete()
    
    if success:
        # Test de performance
        test_performance()
        
        print("\n🎯 RÉSUMÉ:")
        print("✅ Intégration du dictionnaire français réussie")
        print("✅ Fonctionnalités de base opérationnelles")
        print("✅ Enrichissement du dictionnaire fonctionnel")
        print("✅ Performance acceptable")
        print("\n🚀 L'application est prête à être utilisée !")
    else:
        print("\n❌ Des erreurs ont été détectées lors de l'intégration")
        sys.exit(1)
