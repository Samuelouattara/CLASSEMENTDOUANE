#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaires pour la gestion du dictionnaire français
"""

import os
import re
import json
from typing import Set, List, Dict, Optional
from collections import defaultdict

class DictionnaireFrancais:
    """Classe pour gérer le dictionnaire français"""
    
    def __init__(self, fichier_dictionnaire: str = "dictionnaire_francais.txt", 
                 fichier_metadata: str = "dictionnaire_metadata.json"):
        """
        Initialise le dictionnaire français intelligent
        
        Args:
            fichier_dictionnaire: Chemin vers le fichier dictionnaire
            fichier_metadata: Chemin vers le fichier métadonnées contextuelles
        """
        self.fichier_dictionnaire = fichier_dictionnaire
        self.fichier_metadata = fichier_metadata
        self.mots_francais: Set[str] = set()
        self.contextes_mots = defaultdict(list)
        self.familles_mots = defaultdict(set)
        self.groupes_semantiques = defaultdict(set)
        self.scores_frequence = {}
        
        self.charger_dictionnaire()
        self.charger_metadata()
    
    def charger_dictionnaire(self) -> None:
        """Charge le dictionnaire depuis le fichier"""
        try:
            if os.path.exists(self.fichier_dictionnaire):
                with open(self.fichier_dictionnaire, 'r', encoding='utf-8') as f:
                    for ligne in f:
                        mot = ligne.strip().lower()
                        if mot and len(mot) > 1:
                            self.mots_francais.add(mot)
                print(f"✓ Dictionnaire français chargé: {len(self.mots_francais)} mots")
            else:
                print(f"⚠ Fichier dictionnaire non trouvé: {self.fichier_dictionnaire}")
        except Exception as e:
            print(f"✗ Erreur lors du chargement du dictionnaire: {e}")
    
    def charger_metadata(self) -> None:
        """Charge les métadonnées contextuelles"""
        try:
            if os.path.exists(self.fichier_metadata):
                with open(self.fichier_metadata, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    
                self.contextes_mots = defaultdict(list, metadata.get("word_contexts", {}))
                self.familles_mots = defaultdict(set, 
                    {k: set(v) for k, v in metadata.get("word_families", {}).items()})
                self.groupes_semantiques = defaultdict(set, 
                    {k: set(v) for k, v in metadata.get("semantic_groups", {}).items()})
                self.scores_frequence = metadata.get("frequency_scores", {})
                
                print(f"✓ Métadonnées contextuelles chargées")
            else:
                print(f"⚠ Fichier métadonnées non trouvé: {self.fichier_metadata}")
        except Exception as e:
            print(f"✗ Erreur lors du chargement des métadonnées: {e}")
    
    def est_mot_francais(self, mot: str) -> bool:
        """
        Vérifie si un mot est dans le dictionnaire français
        
        Args:
            mot: Le mot à vérifier
            
        Returns:
            True si le mot est français, False sinon
        """
        return mot.lower().strip() in self.mots_francais
    
    def extraire_mots_francais(self, texte: str) -> List[str]:
        """
        Extrait tous les mots français d'un texte
        
        Args:
            texte: Le texte à analyser
            
        Returns:
            Liste des mots français trouvés
        """
        # Nettoyer le texte
        texte_propre = re.sub(r'[^\w\s]', ' ', texte.lower())
        mots = re.findall(r'\b\w+\b', texte_propre)
        
        mots_francais = []
        for mot in mots:
            if len(mot) > 1 and self.est_mot_francais(mot):
                mots_francais.append(mot)
        
        return mots_francais
    
    def calculer_ratio_francais(self, texte: str) -> float:
        """
        Calcule le ratio de mots français dans un texte
        
        Args:
            texte: Le texte à analyser
            
        Returns:
            Ratio entre 0 et 1 (1 = 100% français)
        """
        mots_francais = self.extraire_mots_francais(texte)
        mots_totaux = len(re.findall(r'\b\w+\b', texte.lower()))
        
        if mots_totaux == 0:
            return 0.0
        
        return len(mots_francais) / mots_totaux
    
    def suggerer_mots_similaires(self, mot: str, limite: int = 5) -> List[str]:
        """
        Suggère des mots français similaires
        
        Args:
            mot: Le mot de référence
            limite: Nombre maximum de suggestions
            
        Returns:
            Liste des mots similaires
        """
        mot_lower = mot.lower()
        suggestions = []
        
        for mot_dict in self.mots_francais:
            # Calcul de similarité simple (distance de Levenshtein simplifiée)
            if len(mot_dict) >= len(mot_lower) - 1 and len(mot_dict) <= len(mot_lower) + 1:
                # Mots de longueur similaire
                if mot_dict.startswith(mot_lower[:3]) or mot_lower.startswith(mot_dict[:3]):
                    suggestions.append(mot_dict)
            
            if len(suggestions) >= limite:
                break
        
        return suggestions[:limite]
    
    def filtrer_texte_francais(self, texte: str, seuil: float = 0.3) -> bool:
        """
        Détermine si un texte est principalement en français
        
        Args:
            texte: Le texte à analyser
            seuil: Seuil minimum de mots français (0.0 à 1.0)
            
        Returns:
            True si le texte est principalement français
        """
        ratio = self.calculer_ratio_francais(texte)
        return ratio >= seuil
    
    def enrichir_dictionnaire(self, nouveaux_mots: List[str]) -> None:
        """
        Ajoute de nouveaux mots au dictionnaire
        
        Args:
            nouveaux_mots: Liste des nouveaux mots à ajouter
        """
        for mot in nouveaux_mots:
            mot_propre = mot.lower().strip()
            if mot_propre and len(mot_propre) > 1:
                self.mots_francais.add(mot_propre)
        
        # Sauvegarder le dictionnaire enrichi
        self.sauvegarder_dictionnaire()
    
    def sauvegarder_dictionnaire(self) -> None:
        """Sauvegarde le dictionnaire dans le fichier"""
        try:
            with open(self.fichier_dictionnaire, 'w', encoding='utf-8') as f:
                for mot in sorted(self.mots_francais):
                    f.write(mot + '\n')
            print(f"✓ Dictionnaire sauvegardé: {len(self.mots_francais)} mots")
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde: {e}")
    
    def obtenir_statistiques(self) -> Dict[str, int]:
        """
        Retourne des statistiques sur le dictionnaire
        
        Returns:
            Dictionnaire avec les statistiques
        """
        mots_par_longueur = {}
        for mot in self.mots_francais:
            longueur = len(mot)
            mots_par_longueur[longueur] = mots_par_longueur.get(longueur, 0) + 1
        
        return {
            "total_mots": len(self.mots_francais),
            "mots_par_longueur": mots_par_longueur,
            "longueur_moyenne": sum(len(mot) for mot in self.mots_francais) / len(self.mots_francais) if self.mots_francais else 0,
            "mots_avec_contexte": len(self.contextes_mots),
            "familles_mots": len(self.familles_mots),
            "groupes_semantiques": len(self.groupes_semantiques)
        }
    
    def obtenir_contexte_mot(self, mot: str) -> List[str]:
        """Récupère le contexte d'un mot"""
        return self.contextes_mots.get(mot.lower(), [])
    
    def obtenir_frequence_mot(self, mot: str) -> int:
        """Récupère la fréquence d'un mot"""
        return self.scores_frequence.get(mot.lower(), 0)
    
    def obtenir_famille_mot(self, mot: str) -> Set[str]:
        """Récupère la famille d'un mot"""
        for racine, famille in self.familles_mots.items():
            if mot.lower() in famille:
                return famille
        return set()
    
    def obtenir_groupe_semantique(self, mot: str) -> Optional[str]:
        """Récupère le groupe sémantique d'un mot"""
        for groupe, mots in self.groupes_semantiques.items():
            if mot.lower() in mots:
                return groupe
        return None
    
    def analyser_contexte_texte(self, texte: str) -> Dict:
        """Analyse le contexte d'un texte"""
        mots = re.findall(r'\b\w+\b', texte.lower())
        mots_francais = []
        analyse_contexte = defaultdict(int)
        analyse_semantique = defaultdict(int)
        
        for mot in mots:
            if self.est_mot_francais(mot):
                mots_francais.append(mot)
                
                # Analyser les contextes
                contextes = self.obtenir_contexte_mot(mot)
                for contexte in contextes:
                    analyse_contexte[contexte] += 1
                
                # Analyser les groupes sémantiques
                groupe_semantique = self.obtenir_groupe_semantique(mot)
                if groupe_semantique:
                    analyse_semantique[groupe_semantique] += 1
        
        return {
            "mots_francais": mots_francais,
            "analyse_contexte": dict(analyse_contexte),
            "analyse_semantique": dict(analyse_semantique),
            "total_mots": len(mots),
            "ratio_francais": len(mots_francais) / len(mots) if mots else 0
        }

# Fonctions utilitaires pour l'intégration avec l'application de classement douanier

def analyser_description_douane(description: str, dictionnaire: DictionnaireFrancais) -> Dict[str, any]:
    """
    Analyse une description douanière avec le dictionnaire français intelligent
    
    Args:
        description: Description du produit
        dictionnaire: Instance du dictionnaire français
        
    Returns:
        Dictionnaire avec l'analyse
    """
    mots_francais = dictionnaire.extraire_mots_francais(description)
    ratio_francais = dictionnaire.calculer_ratio_francais(description)
    
    # Analyse contextuelle intelligente
    analyse_contexte = dictionnaire.analyser_contexte_texte(description)
    
    # Analyser le contexte douanier
    contextes_douane = ["douane", "import", "export", "commerce", "transport"]
    score_contexte_douane = 0
    
    for contexte in contextes_douane:
        score_contexte_douane += analyse_contexte["analyse_contexte"].get(contexte, 0)
    
    # Déterminer la qualité française
    if ratio_francais >= 0.8:
        qualite = "Excellente"
    elif ratio_francais >= 0.6:
        qualite = "Bonne"
    elif ratio_francais >= 0.4:
        qualite = "Moyenne"
    else:
        qualite = "Faible"
    
    return {
        "description_originale": description,
        "mots_francais_trouves": mots_francais,
        "nombre_mots_francais": len(mots_francais),
        "ratio_francais": ratio_francais,
        "qualite_francaise": qualite,
        "est_principalement_francais": ratio_francais >= 0.3,
        "mots_uniques": list(set(mots_francais)),
        "score_contexte_douane": score_contexte_douane,
        "analyse_contexte": analyse_contexte["analyse_contexte"],
        "analyse_semantique": analyse_contexte["analyse_semantique"]
    }

def suggerer_améliorations_description(description: str, dictionnaire: DictionnaireFrancais) -> List[str]:
    """
    Suggère des améliorations pour une description douanière
    
    Args:
        description: Description actuelle
        dictionnaire: Instance du dictionnaire français
        
    Returns:
        Liste des suggestions d'amélioration
    """
    suggestions = []
    
    # Analyser les mots non reconnus
    mots_tous = re.findall(r'\b\w+\b', description.lower())
    mots_non_reconnus = [mot for mot in mots_tous if len(mot) > 2 and not dictionnaire.est_mot_francais(mot)]
    
    for mot in mots_non_reconnus[:5]:  # Limiter à 5 suggestions
        mots_similaires = dictionnaire.suggerer_mots_similaires(mot)
        if mots_similaires:
            suggestions.append(f"'{mot}' → suggestions: {', '.join(mots_similaires)}")
    
    return suggestions

# Instance globale du dictionnaire
_dictionnaire_global: Optional[DictionnaireFrancais] = None

def obtenir_dictionnaire() -> DictionnaireFrancais:
    """
    Retourne l'instance globale du dictionnaire français
    
    Returns:
        Instance du dictionnaire français
    """
    global _dictionnaire_global
    if _dictionnaire_global is None:
        _dictionnaire_global = DictionnaireFrancais()
    return _dictionnaire_global

if __name__ == "__main__":
    # Test du module
    print("Test du module DictionnaireFrancais...")
    
    # Créer une instance
    dico = DictionnaireFrancais()
    
    # Test avec une description douanière
    description_test = "Ballon de football en cuir naturel, fabriqué en France, pour usage sportif"
    
    analyse = analyser_description_douane(description_test, dico)
    print(f"\nAnalyse de la description: {description_test}")
    print(f"Ratio français: {analyse['ratio_francais']:.2%}")
    print(f"Mots français trouvés: {', '.join(analyse['mots_francais_trouves'])}")
    
    # Statistiques
    stats = dico.obtenir_statistiques()
    print(f"\nStatistiques du dictionnaire:")
    print(f"Total mots: {stats['total_mots']}")
    print(f"Longueur moyenne: {stats['longueur_moyenne']:.1f} caractères")
