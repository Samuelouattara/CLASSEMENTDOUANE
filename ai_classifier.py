import re
import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

# Télécharger les ressources NLTK nécessaires
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class AdvancedCEDEAOClassifier:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.nlp = spacy.load("fr_core_news_sm")
        self.stop_words = set(stopwords.words('french'))
        self.product_embeddings = {}
        self.classification_rules = self.load_classification_rules()
        
    def load_classification_rules(self) -> Dict:
        """Charge les règles de classification avancées"""
        return {
            'material_precedence': {
                'métaux': ['acier', 'fer', 'cuivre', 'aluminium', 'zinc', 'plomb', 'nickel'],
                'plastiques': ['polyéthylène', 'polypropylène', 'pvc', 'polystyrène', 'nylon'],
                'textiles': ['coton', 'laine', 'soie', 'lin', 'polyester', 'acrylique'],
                'bois': ['chêne', 'pin', 'hêtre', 'bambou', 'contreplaqué'],
                'verre': ['verre', 'cristal', 'vitre'],
                'céramique': ['céramique', 'porcelaine', 'faïence']
            },
            'function_keywords': {
                'machines': ['machine', 'appareil', 'équipement', 'outil', 'instrument'],
                'véhicules': ['voiture', 'camion', 'moto', 'vélo', 'avion', 'bateau'],
                'électronique': ['ordinateur', 'téléphone', 'télévision', 'radio', 'écran'],
                'alimentation': ['nourriture', 'boisson', 'aliment', 'produit alimentaire'],
                'textile': ['vêtement', 'tissu', 'étoffe', 'habillement'],
                'chimique': ['produit chimique', 'médicament', 'cosmétique', 'détergent']
            },
            'exclusions': {
                'emballages': ['emballage', 'carton', 'boîte', 'sac', 'sachet'],
                'accessoires': ['accessoire', 'pièce détachée', 'composant']
            }
        }
    
    def preprocess_text(self, text: str) -> str:
        """Prétraite le texte pour l'analyse"""
        # Conversion en minuscules
        text = text.lower()
        
        # Suppression des caractères spéciaux
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Tokenisation
        tokens = word_tokenize(text)
        
        # Suppression des stop words
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def extract_features(self, text: str) -> Dict:
        """Extrait les caractéristiques importantes du texte"""
        doc = self.nlp(text.lower())
        
        features = {
            'materials': [],
            'functions': [],
            'dimensions': [],
            'brands': [],
            'technical_specs': []
        }
        
        # Extraction des matériaux
        for material_type, materials in self.classification_rules['material_precedence'].items():
            for material in materials:
                if material in text.lower():
                    features['materials'].append(material)
        
        # Extraction des fonctions
        for function_type, keywords in self.classification_rules['function_keywords'].items():
            for keyword in keywords:
                if keyword in text.lower():
                    features['functions'].append(function_type)
        
        # Extraction des dimensions
        dimension_pattern = r'(\d+(?:\.\d+)?)\s*(cm|mm|m|kg|g|l|ml)'
        dimensions = re.findall(dimension_pattern, text)
        features['dimensions'] = dimensions
        
        # Extraction des marques (mots commençant par une majuscule)
        brand_pattern = r'\b[A-Z][a-z]+\b'
        brands = re.findall(brand_pattern, text)
        features['brands'] = brands
        
        # Extraction des spécifications techniques
        tech_patterns = [
            r'\d+\s*(GHz|MHz|GB|TB|MB|W|V|A|Hz)',
            r'(HD|4K|8K|WiFi|Bluetooth|USB|HDMI)',
            r'(Intel|AMD|NVIDIA|Qualcomm|MediaTek)'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            features['technical_specs'].extend(matches)
        
        return features
    
    def calculate_semantic_similarity(self, query: str, target: str) -> float:
        """Calcule la similarité sémantique entre deux textes"""
        try:
            # Encodage des textes
            query_embedding = self.model.encode([query])
            target_embedding = self.model.encode([target])
            
            # Calcul de la similarité cosinus
            similarity = cosine_similarity(query_embedding, target_embedding)[0][0]
            return float(similarity)
        except Exception as e:
            print(f"Erreur lors du calcul de similarité: {e}")
            return 0.0
    
    def apply_rgi_rules(self, product_description: str, candidates: List[Dict]) -> List[Dict]:
        """Applique les Règles Générales d'Interprétation"""
        features = self.extract_features(product_description)
        
        for candidate in candidates:
            score = 0.0
            
            # RGI 1: Titres indicatifs - pas d'impact sur le score
            
            # RGI 2: Marchandises incomplètes
            incomplete_keywords = ['partie', 'composant', 'pièce', 'élément']
            if any(keyword in product_description.lower() for keyword in incomplete_keywords):
                # Chercher la version complète
                score += 0.1
            
            # RGI 3: Mélange ou assemblage
            if len(features['materials']) > 1:
                # Déterminer le matériau prépondérant
                material_counts = {}
                for material in features['materials']:
                    material_counts[material] = product_description.lower().count(material)
                
                if material_counts:
                    predominant_material = max(material_counts, key=material_counts.get)
                    if predominant_material.lower() in candidate['description'].lower():
                        score += 0.3
            
            # RGI 4: Analogie
            semantic_sim = self.calculate_semantic_similarity(
                product_description, candidate['description']
            )
            score += semantic_sim * 0.4
            
            # RGI 5: Emballages
            packaging_keywords = ['emballage', 'carton', 'boîte', 'sac']
            if any(keyword in product_description.lower() for keyword in packaging_keywords):
                # L'emballage suit la marchandise
                score += 0.2
            
            # RGI 6: Sous-positions spécifiques
            if candidate['type'] == 'subheading':
                score += 0.2
            
            candidate['rgi_score'] = score
        
        # Trier par score RGI
        candidates.sort(key=lambda x: x.get('rgi_score', 0), reverse=True)
        return candidates
    
    def classify_product(self, description: str, database: Dict) -> List[Dict]:
        """Classification avancée d'un produit"""
        results = []
        preprocessed_desc = self.preprocess_text(description)
        
        # Recherche dans les sous-positions
        for code, data in database.get('subheadings', {}).items():
            preprocessed_target = self.preprocess_text(data['description'])
            
            # Calcul de la similarité
            similarity = self.calculate_semantic_similarity(preprocessed_desc, preprocessed_target)
            
            if similarity > 0.1:  # Seuil minimal de similarité
                results.append({
                    'type': 'subheading',
                    'code': code,
                    'description': data['description'],
                    'rate': data.get('rate', 'À déterminer'),
                    'similarity': similarity,
                    'rgi_score': 0.0
                })
        
        # Recherche dans les chapitres
        for chapter_num, chapter_content in database.get('chapters', {}).items():
            preprocessed_chapter = self.preprocess_text(chapter_content)
            similarity = self.calculate_semantic_similarity(preprocessed_desc, preprocessed_chapter)
            
            if similarity > 0.15:
                results.append({
                    'type': 'chapter',
                    'code': chapter_num,
                    'description': chapter_content[:300] + "...",
                    'rate': 'À déterminer selon sous-position',
                    'similarity': similarity,
                    'rgi_score': 0.0
                })
        
        # Application des règles RGI
        results = self.apply_rgi_rules(description, results)
        
        # Score final combiné
        for result in results:
            result['final_score'] = (
                result['similarity'] * 0.6 + 
                result.get('rgi_score', 0) * 0.4
            )
        
        # Tri par score final
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        return results[:10]
    
    def get_detailed_classification(self, description: str, database: Dict) -> Dict:
        """Retourne une classification détaillée avec explications"""
        features = self.extract_features(description)
        results = self.classify_product(description, database)
        
        if not results:
            return {
                'success': False,
                'message': 'Aucune classification trouvée',
                'suggestions': self.get_suggestions(description)
            }
        
        best_match = results[0]
        
        classification = {
            'success': True,
            'best_match': best_match,
            'all_matches': results,
            'extracted_features': features,
            'confidence': best_match['final_score'],
            'explanation': self.generate_explanation(best_match, features),
            'section': self.get_section_for_chapter(best_match['code'].split('.')[0]),
            'recommendations': self.get_recommendations(best_match, features)
        }
        
        return classification
    
    def generate_explanation(self, match: Dict, features: Dict) -> str:
        """Génère une explication de la classification"""
        explanation = f"Le produit a été classé dans {match['type']} {match['code']} "
        explanation += f"avec un score de confiance de {match['final_score']:.2%}.\n\n"
        
        if features['materials']:
            explanation += f"Matériaux détectés: {', '.join(features['materials'])}\n"
        
        if features['functions']:
            explanation += f"Fonctions détectées: {', '.join(features['functions'])}\n"
        
        if features['technical_specs']:
            explanation += f"Spécifications techniques: {', '.join(features['technical_specs'])}\n"
        
        return explanation
    
    def get_suggestions(self, description: str) -> List[str]:
        """Génère des suggestions d'amélioration de la description"""
        suggestions = []
        
        if len(description.split()) < 5:
            suggestions.append("Ajoutez plus de détails sur le produit")
        
        if not any(material in description.lower() for materials in self.classification_rules['material_precedence'].values() for material in materials):
            suggestions.append("Précisez les matériaux utilisés")
        
        if not any(function in description.lower() for functions in self.classification_rules['function_keywords'].values() for function in functions):
            suggestions.append("Décrivez la fonction principale du produit")
        
        return suggestions
    
    def get_recommendations(self, match: Dict, features: Dict) -> List[str]:
        """Génère des recommandations basées sur la classification"""
        recommendations = []
        
        if match['final_score'] < 0.7:
            recommendations.append("Considérez une description plus détaillée pour améliorer la précision")
        
        if match['type'] == 'chapter':
            recommendations.append("Recherchez des sous-positions plus spécifiques")
        
        if features['materials'] and len(features['materials']) > 1:
            recommendations.append("Vérifiez le matériau prépondérant selon RGI 3")
        
        return recommendations
    
    def get_section_for_chapter(self, chapter_num: str) -> str:
        """Retourne la section correspondant à un chapitre"""
        chapter_to_section = {
            '01': 'I', '02': 'I', '03': 'I', '04': 'I', '05': 'I',
            '06': 'II', '07': 'II', '08': 'II', '09': 'II', '10': 'II', '11': 'II', '12': 'II', '13': 'II', '14': 'II',
            '15': 'III',
            '16': 'IV', '17': 'IV', '18': 'IV', '19': 'IV', '20': 'IV', '21': 'IV', '22': 'IV', '23': 'IV', '24': 'IV',
            '25': 'V', '26': 'V', '27': 'V',
            '28': 'VI', '29': 'VI', '30': 'VI', '31': 'VI', '32': 'VI', '33': 'VI', '34': 'VI', '35': 'VI', '36': 'VI', '37': 'VI', '38': 'VI',
            '39': 'VII', '40': 'VII',
            '41': 'VIII', '42': 'VIII', '43': 'VIII',
            '44': 'IX', '45': 'IX', '46': 'IX',
            '47': 'X', '48': 'X', '49': 'X',
            '50': 'XI', '51': 'XI', '52': 'XI', '53': 'XI', '54': 'XI', '55': 'XI', '56': 'XI', '57': 'XI', '58': 'XI', '59': 'XI', '60': 'XI', '61': 'XI', '62': 'XI', '63': 'XI',
            '64': 'XII', '65': 'XII', '66': 'XII', '67': 'XII',
            '68': 'XIII', '69': 'XIII', '70': 'XIII',
            '71': 'XIV',
            '72': 'XV', '73': 'XV', '74': 'XV', '75': 'XV', '76': 'XV', '77': 'XV', '78': 'XV', '79': 'XV', '80': 'XV', '81': 'XV', '82': 'XV', '83': 'XV',
            '84': 'XVI', '85': 'XVI',
            '86': 'XVII', '87': 'XVII', '88': 'XVII', '89': 'XVII',
            '90': 'XVIII', '91': 'XVIII', '92': 'XVIII',
            '93': 'XIX',
            '94': 'XX', '95': 'XX', '96': 'XX',
            '97': 'XXI',
            '98': 'XXII', '99': 'XXII'
        }
        
        return chapter_to_section.get(chapter_num, 'Non déterminée')

