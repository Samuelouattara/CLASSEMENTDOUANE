#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import CEDEAOClassifier

def test_parser():
    """Test du parser corrigé"""
    
    print("🔍 Test du parser CEDEAO corrigé")
    print("=" * 50)
    
    # Initialiser le classificateur
    try:
        classifier = CEDEAOClassifier()
        print("✅ Classificateur initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return
    
    # Vérifier les sous-positions téléphones
    print(f"\n📱 Sous-positions téléphones trouvées: {len([k for k in classifier.subheadings.keys() if '8517' in k])}")
    
    telephone_codes = [k for k in classifier.subheadings.keys() if '8517' in k]
    for code in telephone_codes:
        data = classifier.subheadings[code]
        print(f"  {code}: {data['description']} - {data['rate']}")
    
    # Test de recherche
    print(f"\n🔍 Test de recherche pour 'téléphone portable'")
    results = classifier.search_product("téléphone portable", use_advanced=True)
    
    print(f"Résultats trouvés: {len(results)}")
    for i, result in enumerate(results[:5]):
        print(f"  {i+1}. {result['code']} - {result['description']} (score: {result.get('final_score', result.get('relevance', 0)):.3f})")

if __name__ == "__main__":
    test_parser()
