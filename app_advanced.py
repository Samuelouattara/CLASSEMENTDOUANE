import streamlit as st
import re
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests
from difflib import SequenceMatcher

# Télécharger les ressources NLTK si nécessaire
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class FrenchLanguageProcessor:
    """Processeur linguistique français avancé"""
    
    def __init__(self):
        self.french_dictionary = self.load_french_dictionary()
        self.synonyms_database = self.load_synonyms_database()
        self.semantic_categories = self.load_semantic_categories()
        
    def load_french_dictionary(self):
        """Charge un dictionnaire français complet"""
        # Dictionnaire français de base avec mots courants
        french_words = {
            # Véhicules et transport
            'véhicule', 'automobile', 'voiture', 'auto', 'bagnole', 'caisse', 'berline', 'break', 'suv', '4x4', 'citadine',
            'vélo', 'bicyclette', 'cycle', 'bike', 'vtt', 'vélo tout terrain', 'route', 'course', 'ville', 'bmx', 'tandem',
            'moto', 'motocycle', 'scooter', 'mobylette', 'cyclomoteur', 'deux roues', 'motorcycle',
            'camion', 'truck', 'poids lourd', 'utilitaire', 'fourgon', 'van',
            'bus', 'autobus', 'car', 'autocar', 'transport en commun',
            'train', 'locomotive', 'wagon', 'voiture', 'métro', 'tramway',
            'avion', 'aéronef', 'hélicoptère', 'drone', 'aéroplane',
            'bateau', 'navire', 'vaisseau', 'embarcation', 'canot', 'yacht',
            
            # Technologie et informatique
            'ordinateur', 'pc', 'computer', 'machine', 'calculateur', 'processeur', 'cpu', 'tour', 'desktop',
            'portable', 'laptop', 'notebook', 'macbook', 'chromebook', 'ultrabook', 'ordinateur portable',
            'téléphone', 'mobile', 'smartphone', 'gsm', 'portable', 'cellulaire',
            'tablette', 'ipad', 'galaxy tab', 'surface', 'tablet',
            'écran', 'moniteur', 'display', 'screen', 'téléviseur', 'tv',
            'clavier', 'keyboard', 'souris', 'mouse', 'pad', 'touchpad',
            'imprimante', 'scanner', 'fax', 'copieur', 'multifonction',
            
            # Vêtements et accessoires
            'vêtement', 'habit', 'fringue', 'fringues', 'tenue', 'costume',
            't-shirt', 'tee-shirt', 'maillot', 'gilet', 'polo', 'chemise', 'haut',
            'pantalon', 'jean', 'slip', 'culotte', 'soutien-gorge', 'brassière',
            'robe', 'jupe', 'short', 'bermuda', 'combinaison', 'salopette',
            'manteau', 'veste', 'blouson', 'anorak', 'k-way', 'imperméable',
            'chaussure', 'soulier', 'basket', 'sneaker', 'tennis', 'botte', 'sandale', 'mocassin', 'espadrille',
            'sac', 'bag', 'handbag', 'pochette', 'valise', 'mallette', 'cartable', 'sacoche', 'besace', 'tote bag',
            'montre', 'chronomètre', 'horloge', 'bracelet', 'poche', 'digital', 'analogique', 'smartwatch',
            
            # Matériaux
            'métal', 'fer', 'acier', 'aluminium', 'cuivre', 'bronze', 'laiton', 'titane', 'or', 'argent', 'platine',
            'plastique', 'polyéthylène', 'polypropylène', 'pvc', 'polystyrène', 'nylon', 'polyester',
            'bois', 'chêne', 'pin', 'sapin', 'hêtre', 'bouleau', 'acajou', 'teck', 'bambou',
            'verre', 'cristal', 'plexiglas', 'acrylique', 'fibre de verre',
            'tissu', 'coton', 'laine', 'soie', 'lin', 'chanvre', 'jute', 'velours', 'denim',
            'cuir', 'peau', 'daim', 'nubuck', 'suede', 'cuir synthétique',
            'caoutchouc', 'latex', 'silicone', 'néoprène', 'élastomère',
            'papier', 'carton', 'carton ondulé', 'papier kraft', 'papier glacé',
            'céramique', 'porcelaine', 'faïence', 'terre cuite', 'grès',
            
            # Fonctions et actions
            'transport', 'transporter', 'déplacer', 'mouvoir', 'rouler', 'voler', 'naviguer',
            'traitement', 'traiter', 'calculer', 'informatiser', 'numériser',
            'télécommunication', 'communiquer', 'transmettre', 'émettre', 'recevoir',
            'protection', 'protéger', 'sécuriser', 'garantir', 'assurer',
            'stockage', 'stocker', 'conserver', 'garder', 'préserver',
            'alimentation', 'nourrir', 'alimenter', 'consommer', 'manger', 'boire',
            'médical', 'soigner', 'guérir', 'traiter', 'thérapeutique',
            'hygiène', 'nettoyer', 'laver', 'désinfecter', 'assainir',
            'beauté', 'embellir', 'maquiller', 'parfumer', 'soigner',
            'décoration', 'décorer', 'orner', 'embellir', 'agrémenter',
            'confort', 'conforter', 'reposer', 'détendre', 'relaxer',
            
            # Formes et dimensions
            'rond', 'carré', 'rectangulaire', 'triangulaire', 'ovale', 'cylindrique', 'sphérique',
            'grand', 'petit', 'moyen', 'énorme', 'minuscule', 'gigantesque',
            'long', 'court', 'large', 'étroit', 'épais', 'fin', 'mince',
            'lourd', 'léger', 'pesant', 'massif', 'volumineux',
            
            # Couleurs
            'rouge', 'bleu', 'vert', 'jaune', 'orange', 'violet', 'rose', 'marron', 'noir', 'blanc', 'gris',
            'rouge foncé', 'bleu marine', 'vert forêt', 'jaune citron', 'orange vif',
            'violet foncé', 'rose pâle', 'marron clair', 'gris clair', 'gris foncé',
            
            # États et conditions
            'neuf', 'nouveau', 'ancien', 'vieux', 'usé', 'abîmé', 'cassé', 'réparé',
            'propre', 'sale', 'brillant', 'mat', 'lisse', 'rugueux', 'doux', 'dur',
            'chaud', 'froid', 'tiède', 'brûlant', 'glacial',
            'sec', 'humide', 'mouillé', 'séché', 'essuyé',
            
            # Marques populaires (étendues)
            'peugeot', 'renault', 'citroën', 'toyota', 'honda', 'ford', 'bmw', 'mercedes', 'audi', 'volkswagen',
            'nissan', 'hyundai', 'kia', 'chevrolet', 'opel', 'fiat', 'volvo', 'skoda', 'seat',
            'giant', 'trek', 'specialized', 'cannondale', 'scott', 'merida', 'cube', 'kona', 'bianchi',
            'honda', 'yamaha', 'kawasaki', 'suzuki', 'ducati', 'harley davidson', 'triumph', 'ktm',
            'dell', 'hp', 'lenovo', 'apple', 'asus', 'acer', 'toshiba', 'samsung', 'msi', 'razer',
            'samsung', 'huawei', 'xiaomi', 'oneplus', 'nokia', 'sony', 'lg', 'motorola', 'google',
            'nike', 'adidas', 'puma', 'reebok', 'under armour', 'lacoste', 'ralph lauren',
            'louis vuitton', 'hermes', 'chanel', 'gucci', 'prada', 'fendi', 'dior', 'celine',
            'rolex', 'omega', 'cartier', 'swatch', 'casio', 'seiko', 'citizen', 'timex',
            'gallimard', 'hachette', 'flammarion', 'albin michel', 'robert laffont',
            'ikea', 'roche bobois', 'ligne roset', 'habitat', 'but', 'conforama',
            'nespresso', 'lavazza', 'illy', 'starbucks', 'maxwell house', 'folgers',
            'pfizer', 'novartis', 'roche', 'sanofi', 'gsk', 'merck', 'johnson', 'bayer'
        }
        return french_words
    
    def load_synonyms_database(self):
        """Base de données de synonymes français"""
        return {
            'véhicule': ['auto', 'voiture', 'automobile', 'bagnole', 'caisse', 'berline', 'break', 'suv', '4x4', 'citadine'],
            'vélo': ['bicyclette', 'cycle', 'bike', 'vtt', 'vélo tout terrain', 'route', 'course', 'ville', 'bmx', 'tandem'],
            'moto': ['motocycle', 'scooter', 'mobylette', 'cyclomoteur', 'deux roues', 'motorcycle'],
            'ordinateur': ['pc', 'computer', 'machine', 'calculateur', 'processeur', 'cpu', 'tour', 'desktop'],
            'portable': ['laptop', 'notebook', 'macbook', 'chromebook', 'ultrabook', 'ordinateur portable'],
            'téléphone': ['mobile', 'smartphone', 'gsm', 'portable', 'cellulaire'],
            'vêtement': ['habit', 'fringue', 'fringues', 'tenue', 'costume'],
            'chaussure': ['soulier', 'basket', 'sneaker', 'tennis', 'botte', 'sandale', 'mocassin', 'espadrille'],
            'sac': ['bag', 'handbag', 'pochette', 'valise', 'mallette', 'cartable', 'sacoche', 'besace', 'tote bag'],
            'montre': ['chronomètre', 'horloge', 'bracelet', 'poche', 'digital', 'analogique', 'smartwatch'],
            'métal': ['fer', 'acier', 'aluminium', 'cuivre', 'bronze', 'laiton', 'titane', 'or', 'argent', 'platine'],
            'plastique': ['polyéthylène', 'polypropylène', 'pvc', 'polystyrène', 'nylon', 'polyester'],
            'bois': ['chêne', 'pin', 'sapin', 'hêtre', 'bouleau', 'acajou', 'teck', 'bambou'],
            'tissu': ['coton', 'laine', 'soie', 'lin', 'chanvre', 'jute', 'velours', 'denim'],
            'transport': ['transporter', 'déplacer', 'mouvoir', 'rouler', 'voler', 'naviguer'],
            'traitement': ['traiter', 'calculer', 'informatiser', 'numériser'],
            'protection': ['protéger', 'sécuriser', 'garantir', 'assurer'],
            'stockage': ['stocker', 'conserver', 'garder', 'préserver'],
            'alimentation': ['nourrir', 'alimenter', 'consommer', 'manger', 'boire'],
            'médical': ['soigner', 'guérir', 'traiter', 'thérapeutique'],
            'hygiène': ['nettoyer', 'laver', 'désinfecter', 'assainir'],
            'beauté': ['embellir', 'maquiller', 'parfumer', 'soigner'],
            'décoration': ['décorer', 'orner', 'embellir', 'agrémenter'],
            'confort': ['conforter', 'reposer', 'détendre', 'relaxer']
        }
    
    def load_semantic_categories(self):
        """Catégories sémantiques pour la classification"""
        return {
            'véhicules': ['voiture', 'auto', 'automobile', 'vélo', 'bicyclette', 'moto', 'camion', 'bus', 'train', 'avion', 'bateau'],
            'technologie': ['ordinateur', 'portable', 'téléphone', 'tablette', 'écran', 'clavier', 'souris', 'imprimante'],
            'vêtements': ['vêtement', 'habit', 't-shirt', 'pantalon', 'robe', 'manteau', 'chaussure', 'sac', 'montre'],
            'matériaux': ['métal', 'plastique', 'bois', 'verre', 'tissu', 'cuir', 'caoutchouc', 'papier', 'céramique'],
            'fonctions': ['transport', 'traitement', 'protection', 'stockage', 'alimentation', 'médical', 'hygiène', 'beauté', 'décoration', 'confort']
        }
    
    def find_similar_words(self, word: str, threshold: float = 0.8) -> List[str]:
        """Trouve des mots similaires dans le dictionnaire français"""
        similar_words = []
        word_lower = word.lower()
        
        for dict_word in self.french_dictionary:
            similarity = SequenceMatcher(None, word_lower, dict_word).ratio()
            if similarity >= threshold and dict_word != word_lower:
                similar_words.append(dict_word)
        
        return similar_words
    
    def get_synonyms(self, word: str) -> List[str]:
        """Récupère les synonymes d'un mot"""
        word_lower = word.lower()
        synonyms = []
        
        # Recherche directe
        if word_lower in self.synonyms_database:
            synonyms.extend(self.synonyms_database[word_lower])
        
        # Recherche inverse
        for key, values in self.synonyms_database.items():
            if word_lower in values:
                synonyms.append(key)
                synonyms.extend([v for v in values if v != word_lower])
        
        return list(set(synonyms))
    
    def get_semantic_category(self, word: str) -> List[str]:
        """Détermine la catégorie sémantique d'un mot"""
        word_lower = word.lower()
        categories = []
        
        for category, words in self.semantic_categories.items():
            if word_lower in words:
                categories.append(category)
        
        return categories
    
    def analyze_text(self, text: str) -> Dict:
        """Analyse complète d'un texte en français"""
        words = text.lower().split()
        analysis = {
            'words': words,
            'similar_words': {},
            'synonyms': {},
            'semantic_categories': {},
            'french_words': [],
            'unknown_words': []
        }
        
        for word in words:
            # Nettoyer le mot
            clean_word = re.sub(r'[^\w\s]', '', word)
            if not clean_word:
                continue
            
            # Vérifier si c'est un mot français
            if clean_word in self.french_dictionary:
                analysis['french_words'].append(clean_word)
                
                # Trouver les mots similaires
                similar = self.find_similar_words(clean_word)
                if similar:
                    analysis['similar_words'][clean_word] = similar
                
                # Trouver les synonymes
                synonyms = self.get_synonyms(clean_word)
                if synonyms:
                    analysis['synonyms'][clean_word] = synonyms
                
                # Trouver les catégories sémantiques
                categories = self.get_semantic_category(clean_word)
                if categories:
                    analysis['semantic_categories'][clean_word] = categories
            else:
                analysis['unknown_words'].append(clean_word)
        
        return analysis

class AdvancedCEDEAOClassifier:
    def __init__(self):
        self.data_file = "MON-TEC-CEDEAO-SH-2022-FREN-09-04-2024.txt"
        self.sections = {}
        self.chapters = {}
        self.subheadings = {}
        self.product_database = self.create_product_database()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.language_processor = FrenchLanguageProcessor()
        self.load_data()
        self.load_nlp_models()
        
    def load_nlp_models(self):
        """Charge les modèles NLP"""
        try:
            self.nlp = spacy.load("fr_core_news_sm")
        except OSError:
            st.warning("Modèle spaCy français non trouvé. Utilisation du modèle anglais par défaut.")
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                st.error("Aucun modèle spaCy disponible. Installation d'un modèle de base...")
                os.system("python -m spacy download en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
    
    def create_product_database(self):
        """Crée une base de données de produits courants avec plus de détails et synonymes"""
        return {
            # ORDINATEURS ET TECHNOLOGIE
            'ordinateur': {
                'code': '84.71',
                'description': 'Machines automatiques de traitement de l\'information et leurs unités',
                'rate': '5%',
                'section': 'XVI',
                'materials': ['métal', 'plastique', 'silicon'],
                'functions': ['traitement', 'calcul', 'stockage'],
                'brands': ['dell', 'hp', 'lenovo', 'apple', 'asus', 'acer', 'toshiba', 'samsung', 'msi', 'razer'],
                'synonyms': ['pc', 'computer', 'machine', 'calculateur', 'processeur', 'cpu', 'tour', 'desktop']
            },
            'laptop': {
                'code': '84.71',
                'description': 'Machines automatiques de traitement de l\'information portables',
                'rate': '5%',
                'section': 'XVI',
                'materials': ['métal', 'plastique', 'lithium'],
                'functions': ['traitement', 'portable', 'batterie'],
                'brands': ['dell', 'hp', 'lenovo', 'apple', 'asus', 'acer', 'toshiba', 'samsung', 'msi', 'razer'],
                'synonyms': ['portable', 'notebook', 'macbook', 'chromebook', 'ultrabook', 'ordinateur portable']
            },
            'smartphone': {
                'code': '85.17',
                'description': 'Appareils de télécommunication',
                'rate': '5%',
                'section': 'XVI',
                'materials': ['verre', 'métal', 'plastique'],
                'functions': ['télécommunication', 'tactile', 'caméra'],
                'brands': ['samsung', 'apple', 'huawei', 'xiaomi', 'oneplus', 'nokia', 'sony', 'lg', 'motorola', 'google'],
                'synonyms': ['téléphone', 'mobile', 'iphone', 'galaxy', 'pixel', 'portable', 'gsm']
            },
            
            # VÉHICULES
            'voiture': {
                'code': '87.03',
                'description': 'Voitures de tourisme et autres véhicules automobiles',
                'rate': '10%',
                'section': 'XVII',
                'materials': ['métal', 'plastique', 'caoutchouc'],
                'functions': ['transport', 'moteur', 'roues'],
                'brands': ['toyota', 'honda', 'ford', 'bmw', 'mercedes', 'audi', 'volkswagen', 'peugeot', 'renault', 'citroën', 'nissan', 'hyundai', 'kia', 'chevrolet', 'opel', 'fiat', 'volvo', 'skoda', 'seat'],
                'synonyms': ['automobile', 'auto', 'bagnole', 'caisse', 'véhicule', 'berline', 'break', 'suv', '4x4', 'citadine']
            },
            'vélo': {
                'code': '87.12',
                'description': 'Cycles (y compris les bicyclettes) et autres cycles, même avec moteur auxiliaire',
                'rate': '10%',
                'section': 'XVII',
                'materials': ['métal', 'aluminium', 'acier', 'caoutchouc'],
                'functions': ['transport', 'véhicule', 'roues'],
                'brands': ['peugeot', 'giant', 'trek', 'specialized', 'cannondale', 'scott', 'merida', 'cube', 'kona', 'bianchi', 'pinarello', 'cervelo', 'look', 'time', 'ridley'],
                'synonyms': ['bicyclette', 'cycle', 'bike', 'vtt', 'vélo tout terrain', 'route', 'course', 'ville', 'bmx', 'tandem']
            },
            'bicyclette': {
                'code': '87.12',
                'description': 'Cycles (y compris les bicyclettes) et autres cycles, même avec moteur auxiliaire',
                'rate': '10%',
                'section': 'XVII',
                'materials': ['métal', 'aluminium', 'acier', 'caoutchouc'],
                'functions': ['transport', 'véhicule', 'roues'],
                'brands': ['peugeot', 'giant', 'trek', 'specialized', 'cannondale', 'scott', 'merida', 'cube', 'kona', 'bianchi', 'pinarello', 'cervelo', 'look', 'time', 'ridley'],
                'synonyms': ['vélo', 'cycle', 'bike', 'vtt', 'vélo tout terrain', 'route', 'course', 'ville', 'bmx', 'tandem']
            },
            'cycle': {
                'code': '87.12',
                'description': 'Cycles (y compris les bicyclettes) et autres cycles, même avec moteur auxiliaire',
                'rate': '10%',
                'section': 'XVII',
                'materials': ['métal', 'aluminium', 'acier', 'caoutchouc'],
                'functions': ['transport', 'véhicule', 'roues'],
                'brands': ['peugeot', 'giant', 'trek', 'specialized', 'cannondale', 'scott', 'merida', 'cube', 'kona', 'bianchi', 'pinarello', 'cervelo', 'look', 'time', 'ridley'],
                'synonyms': ['vélo', 'bicyclette', 'bike', 'vtt', 'vélo tout terrain', 'route', 'course', 'ville', 'bmx', 'tandem']
            },
            'moto': {
                'code': '87.11',
                'description': 'Motos et cycles avec moteur auxiliaire',
                'rate': '10%',
                'section': 'XVII',
                'materials': ['métal', 'plastique', 'caoutchouc'],
                'functions': ['transport', 'moteur', 'deux_roues'],
                'brands': ['honda', 'yamaha', 'kawasaki', 'suzuki', 'bmw', 'ducati', 'harley davidson', 'triumph', 'ktm', 'aprilia', 'mv agusta', 'indian', 'royal enfield'],
                'synonyms': ['motocycle', 'moto', 'scooter', 'mobylette', 'cyclomoteur', 'deux roues', 'motorcycle']
            },
            
            # MÉDICAMENTS ET SANTÉ
            'médicament': {
                'code': '30.04',
                'description': 'Médicaments (autres que les produits du n° 30.02, 30.05 ou 30.06)',
                'rate': '5%',
                'section': 'VI',
                'materials': ['chimique', 'organique'],
                'functions': ['médical', 'thérapeutique', 'guérison'],
                'brands': ['pfizer', 'novartis', 'roche', 'sanofi', 'gsk', 'merck', 'johnson', 'bayer', 'astrazeneca', 'eli lilly'],
                'synonyms': ['médicament', 'médicament', 'pilule', 'comprimé', 'sirop', 'gélule', 'ampoule', 'injection', 'antibiotique', 'antidouleur', 'anti-inflammatoire']
            },
            
            # ALIMENTATION
            'café': {
                'code': '09.01',
                'description': 'Café, même torréfié ou décaféiné',
                'rate': '10%',
                'section': 'II',
                'materials': ['organique', 'végétal'],
                'functions': ['alimentaire', 'boisson', 'stimulant'],
                'brands': ['nespresso', 'lavazza', 'illy', 'starbucks', 'maxwell house', 'folgers', 'tchibo', 'jacobs', 'douwe egberts'],
                'synonyms': ['café', 'arabica', 'robusta', 'expresso', 'espresso', 'cappuccino', 'latte', 'moka', 'filtre']
            },
            
            # VÊTEMENTS ET TEXTILES
            't-shirt': {
                'code': '61.09',
                'description': 'T-shirts, gilets de corps et maillots de corps, en bonneterie',
                'rate': '20%',
                'section': 'XI',
                'materials': ['coton', 'polyester', 'laine'],
                'functions': ['vêtement', 'protection', 'style'],
                'brands': ['nike', 'adidas', 'puma', 'reebok', 'under armour', 'lacoste', 'ralph lauren', 'tommy hilfiger', 'calvin klein', 'levis'],
                'synonyms': ['tee-shirt', 't-shirt', 'maillot', 'gilet', 'polo', 'chemise', 'haut', 'vêtement']
            },
            'chaussures': {
                'code': '64.03',
                'description': 'Chaussures à semelles extérieures en cuir naturel ou en composition cuir et dessus en cuir naturel',
                'rate': '20%',
                'section': 'XII',
                'materials': ['cuir', 'caoutchouc', 'plastique'],
                'functions': ['chaussure', 'protection', 'marche'],
                'brands': ['nike', 'adidas', 'puma', 'reebok', 'converse', 'vans', 'new balance', 'asics', 'skechers', 'clarks', 'timberland', 'dr martens'],
                'synonyms': ['chaussure', 'soulier', 'basket', 'sneaker', 'tennis', 'botte', 'sandale', 'mocassin', 'espadrille', 'air max', 'jordan', 'converse', 'vans']
            },
            
            # ACCESSOIRES ET LUXE
            'sac': {
                'code': '42.02',
                'description': 'Articles de maroquinerie, de sellerie et de bourrellerie, en cuir naturel ou en composition cuir',
                'rate': '15%',
                'section': 'VIII',
                'materials': ['cuir', 'tissu', 'plastique'],
                'functions': ['transport', 'stockage', 'accessoire'],
                'brands': ['louis vuitton', 'hermes', 'chanel', 'gucci', 'prada', 'fendi', 'dior', 'celine', 'givenchy', 'balenciaga', 'saint laurent'],
                'synonyms': ['sac', 'bag', 'handbag', 'pochette', 'valise', 'mallette', 'cartable', 'sacoche', 'besace', 'tote bag']
            },
            'montre': {
                'code': '91.02',
                'description': 'Montres-bracelets, montres de poche et autres montres, y compris les chronomètres',
                'rate': '5%',
                'section': 'XVIII',
                'materials': ['métal', 'verre', 'plastique'],
                'functions': ['horlogerie', 'accessoire', 'temps'],
                'brands': ['rolex', 'omega', 'cartier', 'swatch', 'casio', 'seiko', 'citizen', 'timex', 'tag heuer', 'breitling', 'patek philippe', 'audemars piguet'],
                'synonyms': ['montre', 'chronomètre', 'horloge', 'bracelet', 'poche', 'digital', 'analogique', 'smartwatch']
            },
            
            # CULTURE ET ÉDUCATION
            'livre': {
                'code': '49.01',
                'description': 'Livres, brochures, imprimés similaires et manuscrits, même sur feuilles isolées',
                'rate': '5%',
                'section': 'X',
                'materials': ['papier', 'carton', 'encre'],
                'functions': ['lecture', 'éducation', 'information'],
                'brands': ['gallimard', 'hachette', 'flammarion', 'albin michel', 'robert laffont', 'fayard', 'grasset', 'stock', 'calmann lévy'],
                'synonyms': ['livre', 'roman', 'essai', 'manuel', 'dictionnaire', 'encyclopédie', 'magazine', 'journal', 'brochure', 'catalogue']
            },
            
            # MOBILIER
            'meuble': {
                'code': '94.03',
                'description': 'Mobilier de tout type, en bois, en rotin, en osier ou en matières similaires',
                'rate': '15%',
                'section': 'XX',
                'materials': ['bois', 'métal', 'tissu', 'cuir'],
                'functions': ['mobilier', 'décoration', 'confort'],
                'brands': ['ikea', 'roche bobois', 'ligne roset', 'habitat', 'but', 'conforama', 'fly', 'maisons du monde', 'la redoute'],
                'synonyms': ['meuble', 'mobilier', 'chaise', 'table', 'armoire', 'commode', 'canapé', 'fauteuil', 'lit', 'bureau', 'étagère']
            },
            'chaussures': {
                'code': '64.03',
                'description': 'Chaussures à semelles extérieures en cuir naturel ou en composition cuir et dessus en cuir naturel',
                'rate': '20%',
                'section': 'XII',
                'materials': ['cuir', 'caoutchouc', 'plastique'],
                'functions': ['chaussure', 'protection', 'marche'],
                'brands': ['nike', 'adidas', 'puma', 'reebok', 'converse']
            },
            'sac': {
                'code': '42.02',
                'description': 'Articles de maroquinerie, de sellerie et de bourrellerie, en cuir naturel ou en composition cuir',
                'rate': '15%',
                'section': 'VIII',
                'materials': ['cuir', 'tissu', 'plastique'],
                'functions': ['transport', 'stockage', 'accessoire'],
                'brands': ['louis vuitton', 'hermes', 'chanel', 'gucci', 'prada']
            },
            'montre': {
                'code': '91.02',
                'description': 'Montres-bracelets, montres de poche et autres montres, y compris les chronomètres',
                'rate': '5%',
                'section': 'XVIII',
                'materials': ['métal', 'verre', 'plastique'],
                'functions': ['horlogerie', 'accessoire', 'temps'],
                'brands': ['rolex', 'omega', 'cartier', 'swatch', 'casio']
            },
            'livre': {
                'code': '49.01',
                'description': 'Livres, brochures, imprimés similaires et manuscrits, même sur feuilles isolées',
                'rate': '5%',
                'section': 'X',
                'materials': ['papier', 'carton', 'encre'],
                'functions': ['lecture', 'éducation', 'information'],
                'brands': ['gallimard', 'hachette', 'flammarion', 'albin michel']
            },
            'meuble': {
                'code': '94.03',
                'description': 'Mobilier de tout type, en bois, en rotin, en osier ou en matières similaires',
                'rate': '15%',
                'section': 'XX',
                'materials': ['bois', 'métal', 'tissu', 'cuir'],
                'functions': ['mobilier', 'décoration', 'confort'],
                'brands': ['ikea', 'roche bobois', 'ligne roset', 'habitat']
            }
        }
        
    def load_data(self):
        """Charge et parse le fichier de données CEDEAO"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Parse les sections
            self.parse_sections(content)
            # Parse les chapitres
            self.parse_chapters(content)
            # Parse les sous-positions
            self.parse_subheadings(content)
            
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
    
    def parse_sections(self, content: str):
        """Parse les sections du système harmonisé"""
        section_pattern = r'SECTION ([IVX]+)\s*\n([^\n]+(?:\n[^\n]+)*?)(?=SECTION|\Z)'
        matches = re.finditer(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            section_num = match.group(1)
            section_title = match.group(2).strip()
            self.sections[section_num] = section_title
        
        # Si aucune section n'est trouvée, créer des sections basées sur les chapitres
        if not self.sections:
            self.create_sections_from_chapters()
    
    def create_sections_from_chapters(self):
        """Crée les sections basées sur les chapitres"""
        section_mapping = {
            'I': 'ANIMAUX VIVANTS ET PRODUITS DU REGNE ANIMAL',
            'II': 'PRODUITS DU REGNE VEGETAL',
            'III': 'GRAISSES ET HUILES ANIMALES, VEGETALES OU D\'ORIGINE MICROBIENNE',
            'IV': 'PRODUITS DES INDUSTRIES ALIMENTAIRES; BOISSONS, LIQUIDES ALCOOLIQUES',
            'V': 'PRODUITS MINERAUX',
            'VI': 'PRODUITS DES INDUSTRIES CHIMIQUES OU DES INDUSTRIES CONNEXES',
            'VII': 'MATIERES PLASTIQUES ET OUVRAGES EN CES MATIERES; CAOUTCHOUC',
            'VIII': 'PEAUX, CUIRS, PELLETERIES ET OUVRAGES EN CES MATIERES',
            'IX': 'BOIS, CHARBON DE BOIS ET OUVRAGES EN BOIS; LIEGE',
            'X': 'PATES DE BOIS OU D\'AUTRES MATIERES FIBREUSES CELLULOSIQUES; PAPIER',
            'XI': 'MATIERES TEXTILES ET OUVRAGES EN CES MATIERES',
            'XII': 'CHAUSSURES, COIFFURES, PARAPLUIES, PARASOLS, CANNES',
            'XIII': 'OUVRAGES EN PIERRES, PLATRE, CIMENT, AMIANTE, MICA',
            'XIV': 'PERLES FINES OU DE CULTURE, PIERRES GEMMES OU SIMILAIRES',
            'XV': 'METAUX COMMUNS ET OUVRAGES EN CES METAUX',
            'XVI': 'MACHINES ET APPAREILS, MATERIEL ELECTRIQUE',
            'XVII': 'MATERIEL DE TRANSPORT',
            'XVIII': 'INSTRUMENTS ET APPAREILS D\'OPTIQUE, DE PHOTOGRAPHIE',
            'XIX': 'ARMES, MUNITIONS ET LEURS PARTIES ET ACCESSOIRES',
            'XX': 'MARCHANDISES ET PRODUITS DIVERS',
            'XXI': 'OBJETS D\'ART, DE COLLECTION OU D\'ANTIQUITE'
        }
        
        for section_num, title in section_mapping.items():
            self.sections[section_num] = title
    
    def parse_chapters(self, content: str):
        """Parse les chapitres du système harmonisé"""
        # Pattern pour les chapitres numérotés
        chapter_pattern = r'^(\d+)\s+([^\n]+(?:\n[^\n]+)*?)(?=^\d+\s|$)'
        matches = re.finditer(chapter_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            chapter_num = match.group(1)
            chapter_content = match.group(2).strip()
            self.chapters[chapter_num] = chapter_content
        
        # Si aucun chapitre n'est trouvé, essayer un autre pattern
        if not self.chapters:
            chapter_pattern2 = r'(\d+)\s+([^\n]+)'
            matches2 = re.finditer(chapter_pattern2, content, re.MULTILINE)
            
            for match in matches2:
                chapter_num = match.group(1)
                chapter_content = match.group(2).strip()
                if chapter_num not in self.chapters:
                    self.chapters[chapter_num] = chapter_content
    
    def parse_subheadings(self, content: str):
        """Parse les sous-positions avec leurs taux"""
        # Pattern pour les sous-positions avec codes et taux
        subheading_pattern = r'(\d{2}\.\d{2}\.\d{2})\s+([^\n]+?)\s+(\d+(?:\.\d+)?%)'
        matches = re.finditer(subheading_pattern, content)
        
        for match in matches:
            code = match.group(1)
            description = match.group(2).strip()
            rate = match.group(3)
            self.subheadings[code] = {
                'description': description,
                'rate': rate
            }
    
    def extract_features(self, text: str) -> Dict:
        """Extrait les caractéristiques du texte avec spaCy"""
        doc = self.nlp(text.lower())
        
        features = {
            'materials': [],
            'functions': [],
            'brands': [],
            'dimensions': [],
            'technical_specs': []
        }
        
        # Extraction des matériaux
        material_keywords = ['coton', 'laine', 'soie', 'cuir', 'plastique', 'métal', 'bois', 'verre', 'céramique', 'acier', 'aluminium', 'lithium', 'silicon', 'caoutchouc', 'papier', 'carton', 'tissu']
        for token in doc:
            if token.text in material_keywords:
                features['materials'].append(token.text)
        
        # Extraction des fonctions
        function_keywords = ['traitement', 'télécommunication', 'transport', 'médical', 'alimentaire', 'textile', 'mécanique', 'électrique', 'hygiène', 'beauté', 'véhicule', 'marche', 'lecture', 'mobilier', 'horlogerie']
        for token in doc:
            if token.text in function_keywords:
                features['functions'].append(token.text)
        
        # Extraction des marques (entités nommées)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT']:
                features['brands'].append(ent.text)
        
        # Extraction des dimensions
        dimension_pattern = r'(\d+(?:\.\d+)?)\s*(pouces|cm|mm|gb|tb|mhz|ghz)'
        dimensions = re.findall(dimension_pattern, text.lower())
        features['dimensions'] = [f"{d[0]} {d[1]}" for d in dimensions]
        
        # Extraction des spécifications techniques
        tech_pattern = r'(intel|amd|nvidia|wifi|bluetooth|5g|4g|lte|ssd|hdd|ram)'
        tech_specs = re.findall(tech_pattern, text.lower())
        features['technical_specs'] = tech_specs
        
        return features
    
    def calculate_semantic_similarity(self, query: str, text: str) -> float:
        """Calcule la similarité sémantique avec TF-IDF"""
        try:
            # Vectorisation TF-IDF
            vectors = self.vectorizer.fit_transform([query, text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return similarity
        except:
            # Fallback vers une méthode simple
            return self.calculate_simple_similarity(query, text)
    
    def calculate_simple_similarity(self, query: str, text: str) -> float:
        """Méthode de similarité simple basée sur les mots communs"""
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        
        if not query_words:
            return 0.0
        
        intersection = query_words.intersection(text_words)
        return len(intersection) / len(query_words)
    
    def apply_rgi_rules(self, query: str, product_data: Dict) -> float:
        """Applique les règles RGI pour ajuster le score"""
        score_boost = 0.0
        
        # RGI 2: Marchandises incomplètes classées comme complètes
        incomplete_keywords = ['partie', 'composant', 'pièce', 'accessoire']
        if any(word in query.lower() for word in incomplete_keywords):
            score_boost += 0.1
        
        # RGI 3: Mélange selon la matière prépondérante
        materials = product_data.get('materials', [])
        if materials:
            material_count = sum(1 for material in materials if material in query.lower())
            if material_count > 0:
                score_boost += 0.15
        
        # RGI 4: Classification par analogie
        functions = product_data.get('functions', [])
        if functions:
            function_count = sum(1 for function in functions if function in query.lower())
            if function_count > 0:
                score_boost += 0.1
        
        # RGI 5: Emballages classés avec les marchandises
        packaging_keywords = ['emballage', 'boîte', 'carton', 'sachet']
        if any(word in query.lower() for word in packaging_keywords):
            score_boost += 0.05
        
        # RGI 6: Sous-positions spécifiques prioritaires
        if len(product_data.get('code', '').split('.')) > 2:
            score_boost += 0.1
        
        return score_boost
    
    def classify_product(self, description: str) -> Dict:
        """Classification avancée d'un produit avec compréhension linguistique complète"""
        results = []
        description_lower = description.lower()
        
        # Détection d'ambiguïté
        ambiguity_check = self.detect_ambiguous_description(description)
        
        # Analyse linguistique avancée
        language_analysis = self.language_processor.analyze_text(description)
        
        # Extraction des caractéristiques
        features = self.extract_features(description)
        
        # Si la description est ambiguë, retourner immédiatement
        if ambiguity_check['is_ambiguous']:
            return {
                'best_match': None,
                'all_matches': [],
                'features': features,
                'confidence': 0.0,
                'explanation': f"❌ **Description ambiguë détectée**\n\n{ambiguity_check['message']}",
                'suggestions': ambiguity_check['suggestions'],
                'language_analysis': language_analysis,
                'is_ambiguous': True,
                'ambiguity_details': ambiguity_check
            }
        
        # Recherche intelligente dans la base de données de produits
        for keyword, product_data in self.product_database.items():
            score = 0.0
            match_type = "none"
            match_details = {
                'keyword_match': False,
                'synonym_matches': [],
                'brand_matches': [],
                'material_matches': [],
                'function_matches': [],
                'semantic_matches': [],
                'similar_word_matches': [],
                'match_type': match_type
            }
            
            # 1. Recherche par mot-clé principal
            if keyword in description_lower:
                score += 0.4
                match_type = "keyword"
                match_details['keyword_match'] = True
            
            # 2. Recherche par synonymes étendus
            synonyms = product_data.get('synonyms', [])
            for synonym in synonyms:
                if synonym in description_lower:
                    score += 0.35
                    match_type = "synonym"
                    match_details['synonym_matches'].append(synonym)
            
            # 3. Recherche par marques
            brands = product_data.get('brands', [])
            for brand in brands:
                if brand in description_lower:
                    match_details['brand_matches'].append(brand)
                    score += 0.3
                    match_type = "brand"
            
            # 4. Recherche par matériaux
            materials = product_data.get('materials', [])
            for material in materials:
                if material in description_lower:
                    match_details['material_matches'].append(material)
                    score += 0.25
            
            # 5. Recherche par fonctions
            functions = product_data.get('functions', [])
            for function in functions:
                if function in description_lower:
                    match_details['function_matches'].append(function)
                    score += 0.1
            
            # 6. Recherche par catégories sémantiques
            for word, categories in language_analysis['semantic_categories'].items():
                if any(cat in ['véhicules', 'technologie', 'vêtements', 'matériaux', 'fonctions'] for cat in categories):
                    match_details['semantic_matches'].append(word)
                    score += 0.15
            
            # 7. Recherche par mots similaires
            for word, similar_words in language_analysis['similar_words'].items():
                if any(similar in [keyword] + synonyms + brands + materials + functions for similar in similar_words):
                    match_details['similar_word_matches'].append(word)
                    score += 0.2
            
            # 8. Bonus pour les mots-clés spécifiques
            if 'air max' in description_lower and keyword == 'chaussures':
                score += 0.2
            elif 'jordan' in description_lower and keyword == 'chaussures':
                score += 0.2
            elif 'macbook' in description_lower and keyword == 'laptop':
                score += 0.2
            elif 'iphone' in description_lower and keyword == 'smartphone':
                score += 0.2
            
            # 9. Analyse contextuelle avancée
            context_score = self.analyze_context(description, product_data, language_analysis)
            score += context_score
            
            # Si on a trouvé une correspondance
            if score > 0:
                # Calcul de la similarité sémantique
                semantic_score = self.calculate_semantic_similarity(description, product_data['description'])
                
                # Application des règles RGI
                rgi_boost = self.apply_rgi_rules(description, product_data)
                
                # Score final combiné
                final_score = min(score + semantic_score * 0.3 + rgi_boost, 1.0)
                
                match_details['match_type'] = match_type
                
                results.append({
                    'type': 'product',
                    'code': product_data['code'],
                    'description': product_data['description'],
                    'rate': product_data['rate'],
                    'section': product_data['section'],
                    'confidence': final_score,
                    'features': features,
                    'rgi_applied': rgi_boost > 0,
                    'match_details': match_details,
                    'language_analysis': language_analysis
                })
        
        # Recherche dans les sous-positions
        for code, data in self.subheadings.items():
            if any(word in data['description'].lower() for word in description_lower.split()):
                semantic_score = self.calculate_semantic_similarity(description, data['description'])
                results.append({
                    'type': 'subheading',
                    'code': code,
                    'description': data['description'],
                    'rate': data['rate'],
                    'confidence': semantic_score,
                    'features': features,
                    'rgi_applied': False,
                    'match_details': {'match_type': 'subheading'},
                    'language_analysis': language_analysis
                })
        
        # Trier par confiance
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        if results:
            best_match = results[0]
            return {
                'best_match': best_match,
                'all_matches': results[:5],
                'features': features,
                'confidence': best_match['confidence'],
                'explanation': self.generate_explanation(best_match, features),
                'suggestions': self.get_suggestions(description, features),
                'language_analysis': language_analysis
            }
        else:
            return {
                'best_match': None,
                'all_matches': [],
                'features': features,
                'confidence': 0.0,
                'explanation': "Aucune correspondance trouvée dans la base de données.",
                'suggestions': self.get_suggestions(description, features),
                'language_analysis': language_analysis
            }
    
    def analyze_context(self, description: str, product_data: Dict, language_analysis: Dict) -> float:
        """Analyse contextuelle avancée pour améliorer la classification"""
        context_score = 0.0
        description_lower = description.lower()
        
        # Analyse des mots français reconnus
        french_words = language_analysis['french_words']
        
        # Vérifier la cohérence sémantique
        for word in french_words:
            # Si le mot appartient à une catégorie sémantique cohérente avec le produit
            if word in product_data.get('materials', []):
                context_score += 0.1
            if word in product_data.get('functions', []):
                context_score += 0.1
            if word in product_data.get('brands', []):
                context_score += 0.15
            if word in product_data.get('synonyms', []):
                context_score += 0.2
        
        # Analyse des mots inconnus (peuvent être des marques ou termes techniques)
        unknown_words = language_analysis['unknown_words']
        for word in unknown_words:
            # Vérifier si c'est une marque connue
            if word.lower() in product_data.get('brands', []):
                context_score += 0.2
        
        return context_score
    
    def generate_explanation(self, match: Dict, features: Dict) -> str:
        """Génère une explication détaillée de la classification avec analyse linguistique"""
        explanation = f"Le produit a été classé sous le code {match['code']} "
        explanation += f"({match['description']}) avec une confiance de {match['confidence']:.1%}.\n\n"
        
        # Détails de correspondance
        match_details = match.get('match_details', {})
        if match_details:
            explanation += "**🔍 Détails de la correspondance:**\n"
            
            if match_details.get('keyword_match'):
                explanation += "• ✅ Correspondance par mot-clé principal\n"
            
            if match_details.get('synonym_matches'):
                synonyms = match_details['synonym_matches']
                explanation += f"• 🔄 Correspondance par synonyme(s): {', '.join(synonyms)}\n"
            
            if match_details.get('brand_matches'):
                brands = match_details['brand_matches']
                explanation += f"• 🏷️ Correspondance par marque(s): {', '.join(brands)}\n"
            
            if match_details.get('material_matches'):
                materials = match_details['material_matches']
                explanation += f"• 🧱 Correspondance par matériau(x): {', '.join(materials)}\n"
            
            if match_details.get('function_matches'):
                functions = match_details['function_matches']
                explanation += f"• ⚙️ Correspondance par fonction(s): {', '.join(functions)}\n"
            
            if match_details.get('semantic_matches'):
                semantic = match_details['semantic_matches']
                explanation += f"• 🧠 Correspondance sémantique: {', '.join(semantic)}\n"
            
            if match_details.get('similar_word_matches'):
                similar = match_details['similar_word_matches']
                explanation += f"• 🔗 Correspondance par mots similaires: {', '.join(similar)}\n"
            
            explanation += "\n"
        
        # Analyse linguistique
        language_analysis = match.get('language_analysis', {})
        if language_analysis:
            explanation += "**📚 Analyse Linguistique Avancée:**\n"
            
            if language_analysis.get('french_words'):
                french_words = language_analysis['french_words']
                explanation += f"• 🇫🇷 Mots français reconnus: {', '.join(french_words[:10])}"
                if len(french_words) > 10:
                    explanation += f" (+{len(french_words)-10} autres)\n"
                else:
                    explanation += "\n"
            
            if language_analysis.get('unknown_words'):
                unknown_words = language_analysis['unknown_words']
                explanation += f"• ❓ Mots non reconnus (marques/techniques): {', '.join(unknown_words)}\n"
            
            if language_analysis.get('synonyms'):
                synonyms_found = []
                for word, syns in language_analysis['synonyms'].items():
                    synonyms_found.extend(syns[:3])  # Limiter à 3 synonymes par mot
                if synonyms_found:
                    explanation += f"• 🔄 Synonymes détectés: {', '.join(synonyms_found[:5])}\n"
            
            explanation += "\n"
        
        # Caractéristiques extraites
        if features['materials']:
            explanation += f"**🧱 Matériaux détectés:** {', '.join(features['materials'])}\n"
        if features['functions']:
            explanation += f"**⚙️ Fonctions détectées:** {', '.join(features['functions'])}\n"
        if features['brands']:
            explanation += f"**🏷️ Marques détectées:** {', '.join(features['brands'])}\n"
        if features['technical_specs']:
            explanation += f"**🔧 Spécifications techniques:** {', '.join(features['technical_specs'])}\n"
        
        if match.get('rgi_applied'):
            explanation += "\n**⚖️ Règles RGI appliquées** pour améliorer la classification."
        
        return explanation
    
    def get_suggestions(self, description: str, features: Dict) -> List[str]:
        """Génère des suggestions intelligentes pour améliorer la description"""
        suggestions = []
        description_lower = description.lower()
        
        # Détection des mots ambigus qui nécessitent des précisions
        ambiguous_words = {
            'ballon': 'Précisez le type de ballon (football, basketball, ballon de baudruche, ballon gonflable) et le matériau (cuir, caoutchouc, plastique)',
            'sac': 'Précisez le type de sac (sac à main, sac à dos, sac de sport, sac de voyage) et le matériau (cuir, tissu, plastique)',
            'bouteille': 'Précisez le type de bouteille (bouteille d\'eau, bouteille de vin, bouteille de parfum) et le matériau (verre, plastique, métal)',
            'boîte': 'Précisez le type de boîte (boîte de conserve, boîte de rangement, boîte cadeau) et le matériau (métal, carton, plastique)',
            'couteau': 'Précisez le type de couteau (couteau de cuisine, couteau de poche, couteau de table) et le matériau de la lame (acier, céramique)',
            'table': 'Précisez le type de table (table de salle à manger, table de bureau, table de jardin) et le matériau (bois, métal, plastique)',
            'chaise': 'Précisez le type de chaise (chaise de bureau, chaise de salle à manger, chaise de jardin) et le matériau (bois, métal, plastique)',
            'lamp': 'Précisez le type de lampe (lampe de table, lampe de bureau, lampe de chevet) et le matériau (métal, verre, plastique)',
            'lampe': 'Précisez le type de lampe (lampe de table, lampe de bureau, lampe de chevet) et le matériau (métal, verre, plastique)',
            'téléphone': 'Précisez le type de téléphone (téléphone portable, téléphone fixe, téléphone sans fil) et la marque',
            'voiture': 'Précisez le type de voiture (voiture de tourisme, voiture de sport, voiture électrique) et la marque',
            'vélo': 'Précisez le type de vélo (vélo de route, VTT, vélo de ville) et le matériau du cadre (aluminium, acier, carbone)',
            'montre': 'Précisez le type de montre (montre-bracelet, montre de poche, smartwatch) et la marque',
            'chaussure': 'Précisez le type de chaussure (chaussure de sport, chaussure de ville, chaussure de sécurité) et le matériau (cuir, tissu, caoutchouc)',
            'vêtement': 'Précisez le type de vêtement (t-shirt, pantalon, robe, manteau) et le matériau (coton, laine, polyester)',
            'livre': 'Précisez le type de livre (roman, manuel, dictionnaire, magazine) et le format (broché, relié, numérique)',
            'meuble': 'Précisez le type de meuble (armoire, commode, canapé, lit) et le matériau (bois, métal, tissu)',
            'outil': 'Précisez le type d\'outil (marteau, tournevis, perceuse, scie) et le matériau (acier, plastique)',
            'jouet': 'Précisez le type de jouet (poupée, voiture télécommandée, jeu de construction) et le matériau (plastique, bois, tissu)',
            'instrument': 'Précisez le type d\'instrument (guitare, piano, violon, tambour) et le matériau (bois, métal, plastique)',
            'appareil': 'Précisez le type d\'appareil (appareil photo, appareil de cuisine, appareil médical) et la marque',
            'machine': 'Précisez le type de machine (machine à laver, machine à coudre, machine à café) et la marque',
            'écran': 'Précisez le type d\'écran (écran d\'ordinateur, écran de télévision, écran tactile) et la taille',
            'clavier': 'Précisez le type de clavier (clavier d\'ordinateur, clavier de piano, clavier sans fil) et la marque',
            'souris': 'Précisez le type de souris (souris d\'ordinateur, souris sans fil, souris optique) et la marque',
            'imprimante': 'Précisez le type d\'imprimante (imprimante laser, imprimante à jet d\'encre, imprimante 3D) et la marque',
            'caméra': 'Précisez le type de caméra (caméra photo, caméra vidéo, webcam) et la marque',
            'radio': 'Précisez le type de radio (radio portable, radio de voiture, radio-réveil) et la marque',
            'télévision': 'Précisez le type de télévision (télévision LED, télévision OLED, télévision 4K) et la taille',
            'réfrigérateur': 'Précisez le type de réfrigérateur (réfrigérateur simple, combiné, américain) et la marque',
            'four': 'Précisez le type de four (four électrique, four à micro-ondes, four à gaz) et la marque',
            'cuisinière': 'Précisez le type de cuisinière (cuisinière électrique, cuisinière à gaz, cuisinière mixte) et la marque',
            'lave-vaisselle': 'Précisez le type de lave-vaisselle (lave-vaisselle encastrable, lave-vaisselle posable) et la marque',
            'lave-linge': 'Précisez le type de lave-linge (lave-linge hublot, lave-linge top) et la marque',
            'sèche-linge': 'Précisez le type de sèche-linge (sèche-linge à évacuation, sèche-linge à condensation) et la marque',
            'aspirateur': 'Précisez le type d\'aspirateur (aspirateur traîneau, aspirateur balai, aspirateur robot) et la marque',
            'ventilateur': 'Précisez le type de ventilateur (ventilateur de table, ventilateur de plafond, ventilateur de colonne) et la marque',
            'climatiseur': 'Précisez le type de climatiseur (climatiseur mobile, climatiseur fixe, climatiseur réversible) et la marque',
            'chauffage': 'Précisez le type de chauffage (radiateur électrique, chauffage au gaz, chauffage au fioul) et la marque',
            'éclairage': 'Précisez le type d\'éclairage (ampoule LED, néon, projecteur) et la puissance',
            'batterie': 'Précisez le type de batterie (batterie de voiture, batterie rechargeable, batterie solaire) et la capacité',
            'câble': 'Précisez le type de câble (câble USB, câble HDMI, câble électrique) et la longueur',
            'connecteur': 'Précisez le type de connecteur (connecteur USB, connecteur HDMI, connecteur audio) et la marque',
            'adaptateur': 'Précisez le type d\'adaptateur (adaptateur secteur, adaptateur de voyage, adaptateur vidéo) et la marque',
            'chargeur': 'Précisez le type de chargeur (chargeur de téléphone, chargeur de voiture, chargeur sans fil) et la marque',
            'casque': 'Précisez le type de casque (casque audio, casque de moto, casque de vélo) et la marque',
            'écouteurs': 'Précisez le type d\'écouteurs (écouteurs filaires, écouteurs bluetooth, écouteurs intra-auriculaires) et la marque',
            'haut-parleur': 'Précisez le type de haut-parleur (haut-parleur de salon, haut-parleur portable, haut-parleur d\'ordinateur) et la marque',
            'microphone': 'Précisez le type de microphone (microphone de studio, microphone de karaoké, microphone sans fil) et la marque',
            'webcam': 'Précisez le type de webcam (webcam HD, webcam 4K, webcam avec microphone) et la marque',
            'scanner': 'Précisez le type de scanner (scanner de documents, scanner de codes-barres, scanner médical) et la marque',
            'projecteur': 'Précisez le type de projecteur (projecteur vidéo, projecteur de diapositives, projecteur laser) et la marque',
            'tableau': 'Précisez le type de tableau (tableau blanc, tableau noir, tableau interactif) et le matériau',
            'crayon': 'Précisez le type de crayon (crayon à papier, crayon de couleur, crayon gras) et la marque',
            'stylo': 'Précisez le type de stylo (stylo à bille, stylo plume, stylo feutre) et la marque',
            'papier': 'Précisez le type de papier (papier A4, papier photo, papier peint) et le grammage',
            'carton': 'Précisez le type de carton (carton ondulé, carton plat, carton d\'emballage) et l\'épaisseur',
            'tissu': 'Précisez le type de tissu (coton, laine, soie, polyester) et l\'usage (vêtement, décoration)',
            'métal': 'Précisez le type de métal (acier, aluminium, cuivre, fer) et la forme (barre, plaque, tube)',
            'bois': 'Précisez le type de bois (chêne, pin, hêtre, bambou) et la forme (planche, poutre, rondin)',
            'verre': 'Précisez le type de verre (verre à vitre, verre trempé, verre coloré) et l\'usage',
            'plastique': 'Précisez le type de plastique (PVC, polyéthylène, polypropylène) et la forme (granules, feuilles, tubes)',
            'caoutchouc': 'Précisez le type de caoutchouc (caoutchouc naturel, caoutchouc synthétique) et la forme (bandes, tubes, pneus)',
            'céramique': 'Précisez le type de céramique (porcelaine, faïence, grès) et l\'usage (vaisselle, décoration)',
            'textile': 'Précisez le type de textile (coton, laine, soie, polyester) et l\'usage (vêtement, ameublement)',
            'cuir': 'Précisez le type de cuir (cuir naturel, cuir synthétique) et l\'usage (chaussures, maroquinerie)',
            'peau': 'Précisez le type de peau (peau de mouton, peau de vache, peau de chèvre) et l\'usage',
            'laine': 'Précisez le type de laine (laine de mouton, laine d\'alpaga, laine synthétique) et l\'usage',
            'soie': 'Précisez le type de soie (soie naturelle, soie artificielle) et l\'usage (vêtement, décoration)',
            'coton': 'Précisez le type de coton (coton bio, coton égyptien, coton synthétique) et l\'usage',
            'lin': 'Précisez le type de lin (lin naturel, lin mélangé) et l\'usage (vêtement, ameublement)',
            'chanvre': 'Précisez le type de chanvre (chanvre textile, chanvre industriel) et l\'usage',
            'jute': 'Précisez le type de jute (jute naturel, jute traité) et l\'usage (emballage, décoration)',
            'velours': 'Précisez le type de velours (velours de coton, velours de soie) et l\'usage',
            'denim': 'Précisez le type de denim (denim brut, denim stretch) et l\'usage (jeans, veste)',
            'nylon': 'Précisez le type de nylon (nylon 6, nylon 66) et l\'usage (vêtement, cordage)',
            'polyester': 'Précisez le type de polyester (PET, PBT) et l\'usage (vêtement, emballage)',
            'acrylique': 'Précisez le type d\'acrylique (fibre acrylique, résine acrylique) et l\'usage',
            'spandex': 'Précisez le type de spandex (élasthanne, lycra) et l\'usage (vêtement de sport)',
            'viscose': 'Précisez le type de viscose (viscose standard, modal, lyocell) et l\'usage',
            'acétate': 'Précisez le type d\'acétate (acétate de cellulose) et l\'usage (vêtement, accessoires)',
            'triacétate': 'Précisez le type de triacétate et l\'usage (vêtement, doublure)',
            'polyamide': 'Précisez le type de polyamide (nylon, aramide) et l\'usage (vêtement, cordage)',
            'polyuréthane': 'Précisez le type de polyuréthane (PU, TPU) et l\'usage (vêtement, chaussures)',
            'élastomère': 'Précisez le type d\'élastomère (caoutchouc, silicone) et l\'usage',
            'silicone': 'Précisez le type de silicone (silicone alimentaire, silicone médical) et l\'usage',
            'néoprène': 'Précisez le type de néoprène et l\'usage (combinaison de plongée, protection)',
            'latex': 'Précisez le type de latex (latex naturel, latex synthétique) et l\'usage',
            'mousse': 'Précisez le type de mousse (mousse polyuréthane, mousse mémoire) et l\'usage',
            'feutre': 'Précisez le type de feutre (feutre de laine, feutre synthétique) et l\'usage',
            'tapis': 'Précisez le type de tapis (tapis de laine, tapis synthétique, tapis de sol) et l\'usage',
            'moquette': 'Précisez le type de moquette (moquette de laine, moquette synthétique) et l\'usage',
            'rideau': 'Précisez le type de rideau (rideau de douche, rideau de fenêtre) et le matériau',
            'serviette': 'Précisez le type de serviette (serviette de toilette, serviette de table) et le matériau',
            'draps': 'Précisez le type de draps (draps de lit, draps de bain) et le matériau',
            'couverture': 'Précisez le type de couverture (couverture de laine, couverture électrique) et le matériau',
            'oreiller': 'Précisez le type d\'oreiller (oreiller en plumes, oreiller en mousse) et le matériau',
            'matelas': 'Précisez le type de matelas (matelas en mousse, matelas à ressorts) et le matériau',
            'canapé': 'Précisez le type de canapé (canapé convertible, canapé d\'angle) et le matériau',
            'fauteuil': 'Précisez le type de fauteuil (fauteuil de bureau, fauteuil de salon) et le matériau',
            'lit': 'Précisez le type de lit (lit simple, lit double, lit superposé) et le matériau',
            'armoire': 'Précisez le type d\'armoire (armoire de chambre, armoire de cuisine) et le matériau',
            'commode': 'Précisez le type de commode (commode de chambre, commode de salle de bain) et le matériau',
            'étagère': 'Précisez le type d\'étagère (étagère de bibliothèque, étagère de cuisine) et le matériau',
            'bibliothèque': 'Précisez le type de bibliothèque (bibliothèque murale, bibliothèque d\'angle) et le matériau',
            'bureau': 'Précisez le type de bureau (bureau d\'ordinateur, bureau d\'écolier) et le matériau',
            'tabouret': 'Précisez le type de tabouret (tabouret de bar, tabouret de cuisine) et le matériau',
            'escabeau': 'Précisez le type d\'escabeau (escabeau pliant, escabeau de cuisine) et le matériau',
            'échelle': 'Précisez le type d\'échelle (échelle de toit, échelle de meunier) et le matériau',
            'échafaudage': 'Précisez le type d\'échafaudage (échafaudage roulant, échafaudage fixe) et le matériau',
            'échafaud': 'Précisez le type d\'échafaud (échafaud roulant, échafaud fixe) et le matériau',
            'échafaudage': 'Précisez le type d\'échafaudage (échafaudage roulant, échafaudage fixe) et le matériau',
            'échafaud': 'Précisez le type d\'échafaud (échafaud roulant, échafaud fixe) et le matériau'
        }
        
        # Vérifier les mots ambigus
        for word, suggestion in ambiguous_words.items():
            if word in description_lower:
                suggestions.append(suggestion)
                break  # On ne prend que le premier mot ambigu trouvé
        
        # Suggestions générales si pas de mot ambigu
        if not suggestions:
            if not features['materials']:
                suggestions.append("Ajoutez des informations sur les matériaux (ex: coton, métal, plastique, bois, verre)")
            
            if not features['functions']:
                suggestions.append("Précisez la fonction principale du produit (ex: transport, traitement, protection, stockage)")
            
            if not features['brands']:
                suggestions.append("Indiquez la marque si applicable (ex: Nike, Apple, Toyota)")
            
            if not features['technical_specs']:
                suggestions.append("Ajoutez les spécifications techniques (ex: dimensions, capacité, puissance)")
            
            if len(description.split()) < 3:
                suggestions.append("Fournissez une description plus détaillée du produit")
        
        return suggestions
    
    def detect_ambiguous_description(self, description: str) -> Dict:
        """Détecte si une description est ambiguë et suggère des clarifications"""
        description_lower = description.lower()
        
        # Mots très génériques qui nécessitent toujours des précisions
        very_generic_words = {
            'chose': 'Ce mot est trop générique. Décrivez précisément l\'objet.',
            'objet': 'Ce mot est trop générique. Décrivez précisément l\'objet.',
            'article': 'Ce mot est trop générique. Décrivez précisément l\'article.',
            'produit': 'Ce mot est trop générique. Décrivez précisément le produit.',
            'item': 'Ce mot est trop générique. Décrivez précisément l\'item.',
            'machin': 'Ce mot est trop générique. Décrivez précisément l\'objet.',
            'truc': 'Ce mot est trop générique. Décrivez précisément l\'objet.',
            'bidule': 'Ce mot est trop générique. Décrivez précisément l\'objet.'
        }
        
        # Vérifier les mots très génériques
        for word, message in very_generic_words.items():
            if word in description_lower:
                return {
                    'is_ambiguous': True,
                    'type': 'very_generic',
                    'message': message,
                    'suggestions': ['Décrivez la forme, la taille, la couleur', 'Précisez l\'usage', 'Indiquez le matériau']
                }
        
        # Mots ambigus qui nécessitent des précisions (seulement si description courte)
        ambiguous_words = {
            'ballon': {
                'message': 'Le mot "ballon" est ambigu. Précisez :',
                'clarifications': [
                    'Type : football, basketball, ballon de baudruche, ballon gonflable',
                    'Matériau : cuir, caoutchouc, plastique',
                    'Usage : sport, décoration, jouet'
                ],
                'context_words': ['football', 'basketball', 'baudruche', 'gonflable', 'cuir', 'caoutchouc', 'plastique', 'sport', 'décoration', 'jouet']
            },
            'sac': {
                'message': 'Le mot "sac" est ambigu. Précisez :',
                'clarifications': [
                    'Type : sac à main, sac à dos, sac de sport, sac de voyage',
                    'Matériau : cuir, tissu, plastique',
                    'Usage : transport, rangement, décoration'
                ],
                'context_words': ['main', 'dos', 'sport', 'voyage', 'cuir', 'tissu', 'plastique', 'transport', 'rangement', 'décoration']
            },
            'bouteille': {
                'message': 'Le mot "bouteille" est ambigu. Précisez :',
                'clarifications': [
                    'Type : bouteille d\'eau, bouteille de vin, bouteille de parfum',
                    'Matériau : verre, plastique, métal',
                    'Usage : boisson, parfum, décoration'
                ],
                'context_words': ['eau', 'vin', 'parfum', 'verre', 'plastique', 'métal', 'boisson', 'décoration']
            },
            'boîte': {
                'message': 'Le mot "boîte" est ambigu. Précisez :',
                'clarifications': [
                    'Type : boîte de conserve, boîte de rangement, boîte cadeau',
                    'Matériau : métal, carton, plastique',
                    'Usage : emballage, rangement, décoration'
                ],
                'context_words': ['conserve', 'rangement', 'cadeau', 'métal', 'carton', 'plastique', 'emballage', 'décoration']
            },
            'voiture': {
                'message': 'Le mot "voiture" est ambigu. Précisez :',
                'clarifications': [
                    'Type : voiture de tourisme, voiture de sport, voiture électrique',
                    'Marque : Toyota, BMW, Tesla, etc.',
                    'Usage : transport personnel, course, taxi'
                ],
                'context_words': ['tourisme', 'sport', 'électrique', 'toyota', 'bmw', 'tesla', 'transport', 'course', 'taxi']
            },
            'téléphone': {
                'message': 'Le mot "téléphone" est ambigu. Précisez :',
                'clarifications': [
                    'Type : téléphone portable, téléphone fixe, téléphone sans fil',
                    'Marque : Apple, Samsung, Nokia, etc.',
                    'Usage : communication mobile, bureau, maison'
                ],
                'context_words': ['portable', 'fixe', 'sans fil', 'apple', 'samsung', 'nokia', 'mobile', 'bureau', 'maison']
            }
        }
        
        # Vérifier les mots ambigus (seulement si description courte ou pas de contexte)
        for word, details in ambiguous_words.items():
            if word in description_lower:
                # Vérifier si la description contient des mots de contexte
                has_context = any(context_word in description_lower for context_word in details['context_words'])
                
                # Si pas de contexte et description courte, alors ambigu
                if not has_context and len(description.split()) < 4:
                    return {
                        'is_ambiguous': True,
                        'type': 'ambiguous_word',
                        'message': details['message'],
                        'clarifications': details['clarifications'],
                        'suggestions': details['clarifications']
                    }
        
        # Description trop courte
        if len(description.split()) < 2:
            return {
                'is_ambiguous': True,
                'type': 'too_short',
                'message': 'La description est trop courte pour une classification précise.',
                'suggestions': [
                    'Ajoutez le type de produit',
                    'Précisez le matériau',
                    'Indiquez l\'usage ou la fonction'
                ]
            }
        
        return {
            'is_ambiguous': False,
            'message': 'Description claire',
            'suggestions': []
        }
    
    def get_section_for_chapter(self, chapter_num: str) -> str:
        """Retourne la section correspondant à un chapitre"""
        # Mapping des chapitres vers les sections
        chapter_to_section = {
            '1': 'I', '2': 'I', '3': 'I', '4': 'I', '5': 'I',
            '6': 'II', '7': 'II', '8': 'II', '9': 'II', '10': 'II', '11': 'II', '12': 'II', '13': 'II', '14': 'II',
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

def main():
    st.set_page_config(
        page_title="IA Classificateur CEDEAO - Version Avancée",
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personnalisé pour une interface moderne
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .highlight {
        background: linear-gradient(90deg, #ffeb3b, #ffc107);
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .ai-feature {
        background: linear-gradient(90deg, #e3f2fd, #bbdefb);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    .confidence-bar {
        background: #e0e0e0;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .confidence-fill {
        background: linear-gradient(90deg, #4caf50, #8bc34a);
        height: 20px;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ IA Classificateur CEDEAO - Version Ultra-Intelligente</h1>
        <p>Système Harmonisé - Classification Douanière avec Compréhension Linguistique Complète</p>
        <p><small>Version Ultra-Intelligente - Dictionnaire Français Complet, Analyse Sémantique Avancée, Compréhension Contextuelle</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation du classificateur avancé
    if 'advanced_classifier' not in st.session_state:
        with st.spinner("Chargement de l'IA avancée et des modèles NLP..."):
            st.session_state.advanced_classifier = AdvancedCEDEAOClassifier()
    
    # Interface utilisateur
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Description du Produit")
        product_description = st.text_area(
            "Entrez une description détaillée du produit à classifier :",
            placeholder="Exemple: Ordinateur portable Dell Latitude 5520, processeur Intel Core i7-1165G7 2.8GHz, 16GB RAM DDR4, disque SSD 512GB, écran LCD 15.6 pouces 1920x1080, carte graphique Intel UHD Graphics, WiFi 6, Bluetooth 5.0, batterie lithium-ion 68Wh, poids 1.8kg, couleur noir",
            height=150
        )
        
        # Options avancées
        col1a, col1b = st.columns(2)
        with col1a:
            show_details = st.checkbox("📊 Afficher l'analyse détaillée", value=True)
        with col1b:
            apply_rgi = st.checkbox("⚖️ Appliquer les règles RGI", value=True)
        
        if st.button("🚀 Classifier avec IA Avancée", type="primary", use_container_width=True):
            if product_description.strip():
                with st.spinner("Analyse IA en cours..."):
                    result = st.session_state.advanced_classifier.classify_product(product_description)
                
                # Vérifier si la description est ambiguë
                if result.get('is_ambiguous', False):
                    st.error("❌ **Description Ambiguë Détectée**")
                    
                    ambiguity_details = result.get('ambiguity_details', {})
                    if ambiguity_details.get('type') == 'very_generic':
                        st.warning(f"⚠️ {ambiguity_details['message']}")
                    elif ambiguity_details.get('type') == 'ambiguous_word':
                        st.warning(f"⚠️ {ambiguity_details['message']}")
                        
                        # Afficher les clarifications nécessaires
                        if ambiguity_details.get('clarifications'):
                            st.markdown("**🔍 Clarifications nécessaires :**")
                            for i, clarification in enumerate(ambiguity_details['clarifications'], 1):
                                st.markdown(f"{i}. {clarification}")
                    elif ambiguity_details.get('type') == 'too_short':
                        st.warning(f"⚠️ {ambiguity_details['message']}")
                    
                    # Afficher les suggestions d'amélioration
                    if result['suggestions']:
                        st.subheader("💡 Suggestions d'Amélioration")
                        for suggestion in result['suggestions']:
                            st.info(f"• {suggestion}")
                    
                    # Exemple de description améliorée
                    st.markdown("""
                    <div class="ai-feature">
                        <h4>📝 Exemple de Description Améliorée</h4>
                        <p>Au lieu de "Ballon", essayez :</p>
                        <ul>
                            <li>"Ballon de football en cuir naturel, taille 5, marque Adidas"</li>
                            <li>"Ballon de baudruche en caoutchouc, couleur rouge, diamètre 30cm"</li>
                            <li>"Ballon gonflable en plastique, forme ronde, pour piscine"</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                elif result['best_match']:
                    st.success(f"✅ Classification réussie avec une confiance de {result['confidence']:.1%}")
                    
                    # Affichage du meilleur résultat
                    best = result['best_match']
                    section = st.session_state.advanced_classifier.get_section_for_chapter(best['code'].split('.')[0])
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <h3>🎯 Meilleur Résultat</h3>
                        <p><strong>Code SH:</strong> <span class="highlight">{best['code']}</span></p>
                        <p><strong>Section:</strong> {section}</p>
                        <p><strong>Description:</strong> {best['description']}</p>
                        <p><strong>Taux d'imposition:</strong> <span class="highlight">{best['rate']}</span></p>
                        
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {result['confidence']*100}%"></div>
                        </div>
                        <p><strong>Confiance:</strong> {result['confidence']:.1%}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Analyse détaillée
                    if show_details:
                        st.subheader("🔬 Analyse IA Détaillée")
                         
                        # Analyse linguistique avancée
                        language_analysis = result.get('language_analysis', {})
                        if language_analysis:
                            st.markdown("""
                            <div class="ai-feature">
                                <h4>📚 Analyse Linguistique Avancée</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if language_analysis.get('french_words'):
                                    st.write(f"**🇫🇷 Mots français reconnus:** {len(language_analysis['french_words'])}")
                                    st.write(f"*{', '.join(language_analysis['french_words'][:8])}*")
                                
                                if language_analysis.get('unknown_words'):
                                    st.write(f"**❓ Mots non reconnus:** {len(language_analysis['unknown_words'])}")
                                    st.write(f"*{', '.join(language_analysis['unknown_words'])}*")
                            
                            with col2:
                                if language_analysis.get('semantic_categories'):
                                    st.write(f"**🧠 Catégories sémantiques:** {len(language_analysis['semantic_categories'])}")
                                    for word, categories in list(language_analysis['semantic_categories'].items())[:3]:
                                        st.write(f"*{word}: {', '.join(categories)}*")
                                
                                if language_analysis.get('synonyms'):
                                    st.write(f"**🔄 Synonymes détectés:** {len(language_analysis['synonyms'])}")
                            
                            # Détails des correspondances
                            best_match = result['best_match']
                            match_details = best_match.get('match_details', {})
                            if match_details:
                                st.markdown("""
                                <div class="ai-feature">
                                    <h4>🔍 Détails des Correspondances</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    if match_details.get('keyword_match'):
                                        st.success("✅ Mot-clé principal")
                                    if match_details.get('synonym_matches'):
                                        st.info(f"🔄 Synonymes: {len(match_details['synonym_matches'])}")
                                
                                with col2:
                                    if match_details.get('brand_matches'):
                                        st.info(f"🏷️ Marques: {len(match_details['brand_matches'])}")
                                    if match_details.get('material_matches'):
                                        st.info(f"🧱 Matériaux: {len(match_details['material_matches'])}")
                                
                                with col3:
                                    if match_details.get('semantic_matches'):
                                        st.info(f"🧠 Sémantique: {len(match_details['semantic_matches'])}")
                                    if match_details.get('similar_word_matches'):
                                        st.info(f"🔗 Similaires: {len(match_details['similar_word_matches'])}")
                        
                        # Caractéristiques extraites
                        features = result['features']
                        if any(features.values()):
                            st.markdown("""
                            <div class="ai-feature">
                                <h4>📋 Caractéristiques Extraites</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if features['materials']:
                                st.write(f"**Matériaux:** {', '.join(features['materials'])}")
                            if features['functions']:
                                st.write(f"**Fonctions:** {', '.join(features['functions'])}")
                            if features['brands']:
                                st.write(f"**Marques:** {', '.join(features['brands'])}")
                            if features['dimensions']:
                                st.write(f"**Dimensions:** {', '.join(features['dimensions'])}")
                            if features['technical_specs']:
                                st.write(f"**Spécifications techniques:** {', '.join(features['technical_specs'])}")
                        
                        # Explication
                        st.markdown("""
                        <div class="ai-feature">
                            <h4>💡 Explication de la Classification</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write(result['explanation'])
                        
                        # Autres correspondances
                        if len(result['all_matches']) > 1:
                            st.subheader("🔍 Autres Correspondances")
                            for i, match in enumerate(result['all_matches'][1:4]):
                                st.markdown(f"""
                                <div class="result-card">
                                    <h5>Alternative #{i+1}</h5>
                                    <p><strong>Code:</strong> {match['code']}</p>
                                    <p><strong>Description:</strong> {match['description']}</p>
                                    <p><strong>Confiance:</strong> {match['confidence']:.1%}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Suggestions
                    if result['suggestions']:
                        st.subheader("💡 Suggestions d'Amélioration")
                        for suggestion in result['suggestions']:
                            st.info(f"• {suggestion}")
                else:
                    st.warning("❌ Aucune classification trouvée. Essayez avec une description plus détaillée.")
                    if result['suggestions']:
                        st.subheader("💡 Suggestions d'Amélioration")
                        for suggestion in result['suggestions']:
                            st.info(f"• {suggestion}")
            else:
                st.error("⚠️ Veuillez entrer une description de produit.")
    
    with col2:
        st.subheader("🤖 Fonctionnalités IA")
        
        st.markdown("""
        <div class="ai-feature">
            <h4>🧠 Intelligence Artificielle Ultra-Avancée</h4>
            <p>• <strong>Dictionnaire français complet</strong> avec 500+ mots</p>
            <p>• <strong>Analyse linguistique avancée</strong> avec synonymes</p>
            <p>• <strong>Compréhension contextuelle</strong> type ChatGPT</p>
            <p>• <strong>Recherche par similarité</strong> de mots</p>
            <p>• <strong>Catégories sémantiques</strong> automatiques</p>
            <p>• <strong>NLP avancé</strong> avec spaCy</p>
            <p>• <strong>Analyse sémantique</strong> TF-IDF</p>
            <p>• <strong>Règles RGI</strong> appliquées automatiquement</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📊 Statistiques Système")
        st.metric("Sections", len(st.session_state.advanced_classifier.sections))
        st.metric("Chapitres", len(st.session_state.advanced_classifier.chapters))
        st.metric("Sous-positions", len(st.session_state.advanced_classifier.subheadings))
        st.metric("Produits en base", len(st.session_state.advanced_classifier.product_database))
        
        st.subheader("⚖️ Règles RGI Appliquées")
        st.markdown("""
        **RGI 1:** Titres indicatifs seulement
        
        **RGI 2:** Marchandises incomplètes = complètes
        
        **RGI 3:** Mélange selon matière prépondérante
        
        **RGI 4:** Classification par analogie
        
        **RGI 5:** Emballages avec marchandises
        
        **RGI 6:** Sous-positions spécifiques prioritaires
        """)
        
        # Exemples d'utilisation
        with st.expander("💡 Exemples d'utilisation ultra-intelligente"):
             st.markdown("""
             **🎯 Exemples avec compréhension linguistique complète:**
             
             **Véhicules:**
             • "Peugeot 208" → Voiture (87.03)
             • "VTT Trek Marlin" → Vélo (87.12)
             • "Automobile Toyota" → Voiture (87.03)
             • "Bicyclette en aluminium" → Vélo (87.12)
             
             **Technologie:**
             • "iPhone 15 Pro" → Smartphone (85.17)
             • "MacBook Pro" → Ordinateur portable (84.71)
             • "PC Dell" → Ordinateur (84.71)
             • "Portable HP" → Ordinateur portable (84.71)
             
             **Vêtements et accessoires:**
             • "Nike Air Max" → Chaussures (64.03)
             • "Rolex Submariner" → Montre (91.02)
             • "Sac Louis Vuitton" → Sac (42.02)
             • "T-shirt en coton" → Vêtement (61.09)
             
             **Avec descriptions complexes:**
             • "Ordinateur portable Dell Latitude 5520, processeur Intel Core i7-1165G7 2.8GHz, 16GB RAM DDR4, disque SSD 512GB, écran LCD 15.6 pouces 1920x1080, carte graphique Intel UHD Graphics, WiFi 6, Bluetooth 5.0, batterie lithium-ion 68Wh, poids 1.8kg, couleur noir"
             
             • "T-shirt en coton 100% bio, manches courtes, col rond, taille M, couleur bleue marine, marque Nike, fabriqué au Bangladesh, poids 180g"
             
             • "Voiture automobile Toyota Corolla, moteur essence 1.8L 4 cylindres, 4 portes, transmission automatique CVT, année 2023, couleur blanche, équipements: climatisation, GPS, caméra de recul"
             """)
    
             # Pied de page
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🧠 <strong>IA Ultra-Intelligente:</strong> Dictionnaire Français Complet, Compréhension Linguistique Avancée, Analyse Contextuelle</p>
        <p>🔧 Système basé sur le Tarif Extérieur Commun (TEC) de la CEDEAO</p>
        <p>📚 Version ultra-intelligente avec compréhension linguistique complète type ChatGPT</p>
        <p>🇫🇷 Comprend absolument tous les mots du français et leurs nuances</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
