#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module pour dictionnaire français intelligent avec compréhension contextuelle
"""

import json
import re
from typing import Set, List, Dict, Tuple, Optional
from collections import defaultdict
import difflib

class DictionnaireIntelligent:
    """Dictionnaire français intelligent avec compréhension contextuelle"""
    
    def __init__(self, dict_file: str = "dictionnaire_francais.txt", 
                 metadata_file: str = "dictionnaire_metadata.json"):
        self.words = set()
        self.word_contexts = defaultdict(list)
        self.word_families = defaultdict(set)
        self.semantic_groups = defaultdict(set)
        self.frequency_scores = {}
        
        self.load_dictionary(dict_file)
        self.load_metadata(metadata_file)
        
    def load_dictionary(self, filename: str):
        """Charge le dictionnaire de base"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self.words.add(word)
            print(f"✅ Dictionnaire chargé: {len(self.words)} mots")
        except FileNotFoundError:
            print(f"⚠️ Fichier dictionnaire non trouvé: {filename}")
            
    def load_metadata(self, filename: str):
        """Charge les métadonnées contextuelles"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                
            self.word_contexts = defaultdict(list, metadata.get("word_contexts", {}))
            self.word_families = defaultdict(set, 
                {k: set(v) for k, v in metadata.get("word_families", {}).items()})
            self.semantic_groups = defaultdict(set, 
                {k: set(v) for k, v in metadata.get("semantic_groups", {}).items()})
            self.frequency_scores = metadata.get("frequency_scores", {})
            
            print(f"✅ Métadonnées contextuelles chargées")
            print(f"   Contextes: {len(self.word_contexts)}")
            print(f"   Familles: {len(self.word_families)}")
            print(f"   Groupes sémantiques: {len(self.semantic_groups)}")
            
        except FileNotFoundError:
            print(f"⚠️ Fichier métadonnées non trouvé: {filename}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement des métadonnées: {e}")
    
    def is_french_word(self, word: str) -> bool:
        """Vérifie si un mot est français"""
        return word.lower() in self.words
    
    def get_word_context(self, word: str) -> List[str]:
        """Récupère le contexte d'un mot"""
        return self.word_contexts.get(word.lower(), [])
    
    def get_word_frequency(self, word: str) -> int:
        """Récupère la fréquence d'un mot"""
        return self.frequency_scores.get(word.lower(), 0)
    
    def get_word_family(self, word: str) -> Set[str]:
        """Récupère la famille d'un mot"""
        for root, family in self.word_families.items():
            if word.lower() in family:
                return family
        return set()
    
    def get_semantic_group(self, word: str) -> Optional[str]:
        """Récupère le groupe sémantique d'un mot"""
        for group, words in self.semantic_groups.items():
            if word.lower() in words:
                return group
        return None
    
    def analyze_text_context(self, text: str) -> Dict:
        """Analyse le contexte d'un texte"""
        words = re.findall(r'\b\w+\b', text.lower())
        french_words = []
        context_analysis = defaultdict(int)
        semantic_analysis = defaultdict(int)
        
        for word in words:
            if self.is_french_word(word):
                french_words.append(word)
                
                # Analyser les contextes
                contexts = self.get_word_context(word)
                for context in contexts:
                    context_analysis[context] += 1
                
                # Analyser les groupes sémantiques
                semantic_group = self.get_semantic_group(word)
                if semantic_group:
                    semantic_analysis[semantic_group] += 1
        
        return {
            "french_words": french_words,
            "context_analysis": dict(context_analysis),
            "semantic_analysis": dict(semantic_analysis),
            "total_words": len(words),
            "french_ratio": len(french_words) / len(words) if words else 0
        }
    
    def suggest_similar_words(self, word: str, max_suggestions: int = 5) -> List[str]:
        """Suggère des mots similaires"""
        if self.is_french_word(word):
            return [word]  # Le mot existe déjà
        
        # Chercher dans les familles de mots
        suggestions = []
        word_lower = word.lower()
        
        # Recherche par similarité
        similar_words = difflib.get_close_matches(word_lower, self.words, 
                                                n=max_suggestions, cutoff=0.6)
        suggestions.extend(similar_words)
        
        # Recherche par préfixe/suffixe
        for dict_word in self.words:
            if (dict_word.startswith(word_lower[:3]) or 
                dict_word.endswith(word_lower[-3:])) and len(suggestions) < max_suggestions:
                if dict_word not in suggestions:
                    suggestions.append(dict_word)
        
        return suggestions[:max_suggestions]
    
    def get_contextual_suggestions(self, word: str, context: str = "") -> List[str]:
        """Suggère des mots en fonction du contexte"""
        suggestions = []
        word_lower = word.lower()
        
        # Si on a un contexte, chercher des mots avec le même contexte
        if context and context in self.word_contexts:
            for word_with_context, contexts in self.word_contexts.items():
                if context in contexts and word_with_context != word_lower:
                    suggestions.append(word_with_context)
        
        # Ajouter des suggestions par similarité
        similar_words = self.suggest_similar_words(word, 3)
        suggestions.extend(similar_words)
        
        return list(set(suggestions))[:5]
    
    def analyze_customs_description(self, description: str) -> Dict:
        """Analyse une description douanière avec contexte"""
        analysis = self.analyze_text_context(description)
        
        # Analyser le contexte douanier
        customs_contexts = ["douane", "import", "export", "commerce", "transport"]
        customs_score = 0
        
        for context in customs_contexts:
            customs_score += analysis["context_analysis"].get(context, 0)
        
        # Déterminer la qualité française
        french_ratio = analysis["french_ratio"]
        if french_ratio >= 0.8:
            quality = "Excellente"
        elif french_ratio >= 0.6:
            quality = "Bonne"
        elif french_ratio >= 0.4:
            quality = "Moyenne"
        else:
            quality = "Faible"
        
        # Identifier les mots non français
        words = re.findall(r'\b\w+\b', description.lower())
        non_french_words = [word for word in words if not self.is_french_word(word)]
        
        # Suggestions d'amélioration
        suggestions = {}
        for word in non_french_words[:5]:  # Limiter à 5 suggestions
            suggestions[word] = self.suggest_similar_words(word, 3)
        
        return {
            "description": description,
            "french_ratio": french_ratio,
            "quality": quality,
            "french_words_count": len(analysis["french_words"]),
            "non_french_words": non_french_words,
            "suggestions": suggestions,
            "customs_context_score": customs_score,
            "context_analysis": analysis["context_analysis"],
            "semantic_analysis": analysis["semantic_analysis"]
        }
    
    def get_word_statistics(self) -> Dict:
        """Récupère les statistiques du dictionnaire"""
        return {
            "total_words": len(self.words),
            "words_with_context": len(self.word_contexts),
            "word_families": len(self.word_families),
            "semantic_groups": len(self.semantic_groups),
            "average_frequency": sum(self.frequency_scores.values()) / len(self.frequency_scores) if self.frequency_scores else 0,
            "top_contexts": sorted(self.word_contexts.items(), 
                                 key=lambda x: len(x[1]), reverse=True)[:10],
            "top_semantic_groups": sorted(self.semantic_groups.items(), 
                                        key=lambda x: len(x[1]), reverse=True)[:10]
        }
    
    def search_by_context(self, context: str) -> List[str]:
        """Recherche des mots par contexte"""
        matching_words = []
        for word, contexts in self.word_contexts.items():
            if context.lower() in [c.lower() for c in contexts]:
                matching_words.append(word)
        return matching_words
    
    def search_by_semantic_group(self, group: str) -> List[str]:
        """Recherche des mots par groupe sémantique"""
        return list(self.semantic_groups.get(group.lower(), set()))
    
    def get_related_words(self, word: str) -> Dict:
        """Récupère les mots liés à un mot donné"""
        word_lower = word.lower()
        
        # Même famille
        family = self.get_word_family(word_lower)
        
        # Même contexte
        same_context = []
        word_contexts = self.get_word_context(word_lower)
        for other_word, contexts in self.word_contexts.items():
            if other_word != word_lower and any(c in word_contexts for c in contexts):
                same_context.append(other_word)
        
        # Même groupe sémantique
        semantic_group = self.get_semantic_group(word_lower)
        same_semantic = []
        if semantic_group:
            same_semantic = list(self.semantic_groups[semantic_group] - {word_lower})
        
        return {
            "word": word,
            "family": list(family),
            "same_context": same_context[:10],
            "same_semantic": same_semantic[:10],
            "frequency": self.get_word_frequency(word_lower),
            "contexts": word_contexts
        }

def test_dictionnaire_intelligent():
    """Test du dictionnaire intelligent"""
    print("🧠 Test du dictionnaire français intelligent...")
    
    # Initialiser le dictionnaire
    dict_intelligent = DictionnaireIntelligent()
    
    # Test 1: Reconnaissance de mots
    test_words = ["ballon", "cuir", "football", "smartphone", "velo", "ordinateur"]
    print("\n1. Test de reconnaissance:")
    for word in test_words:
        is_french = dict_intelligent.is_french_word(word)
        contexts = dict_intelligent.get_word_context(word)
        frequency = dict_intelligent.get_word_frequency(word)
        
        status = "✅ Français" if is_french else "❌ Non français"
        context_info = f" (Contexte: {', '.join(contexts[:2])})" if contexts else ""
        freq_info = f" [Fréquence: {frequency}]" if frequency > 0 else ""
        
        print(f"   '{word}': {status}{context_info}{freq_info}")
    
    # Test 2: Analyse de description douanière
    print("\n2. Test d'analyse de description douanière:")
    description = "Ballon de football professionnel en cuir naturel, taille 5, fabriqué en France"
    analysis = dict_intelligent.analyze_customs_description(description)
    
    print(f"   Description: {analysis['description']}")
    print(f"   Ratio français: {analysis['french_ratio']:.1%}")
    print(f"   Qualité: {analysis['quality']}")
    print(f"   Mots français: {analysis['french_words_count']}")
    print(f"   Score contexte douanier: {analysis['customs_context_score']}")
    
    if analysis['suggestions']:
        print(f"   Suggestions d'amélioration:")
        for word, suggestions in analysis['suggestions'].items():
            print(f"     '{word}' → {', '.join(suggestions)}")
    
    # Test 3: Recherche contextuelle
    print("\n3. Test de recherche contextuelle:")
    customs_words = dict_intelligent.search_by_context("douane")
    print(f"   Mots liés à 'douane': {', '.join(customs_words[:10])}")
    
    # Test 4: Statistiques
    print("\n4. Statistiques du dictionnaire:")
    stats = dict_intelligent.get_word_statistics()
    print(f"   Total mots: {stats['total_words']}")
    print(f"   Mots avec contexte: {stats['words_with_context']}")
    print(f"   Familles de mots: {stats['word_families']}")
    print(f"   Groupes sémantiques: {stats['semantic_groups']}")
    
    # Test 5: Mots liés
    print("\n5. Test de mots liés:")
    related = dict_intelligent.get_related_words("transport")
    print(f"   Mots liés à 'transport':")
    print(f"     Famille: {', '.join(related['family'][:5])}")
    print(f"     Même contexte: {', '.join(related['same_context'][:5])}")
    print(f"     Même sémantique: {', '.join(related['same_semantic'][:5])}")

if __name__ == "__main__":
    test_dictionnaire_intelligent()
