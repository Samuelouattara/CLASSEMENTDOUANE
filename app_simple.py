import streamlit as st
import re
from typing import Dict, List, Tuple, Optional
import json
import os

class SimpleCEDEAOClassifier:
    def __init__(self):
        self.data_file = "MON-TEC-CEDEAO-SH-2022-FREN-09-04-2024.txt"
        self.sections = {}
        self.chapters = {}
        self.subheadings = {}
        self.product_database = self.create_product_database()
        self.load_data()
    
    def create_product_database(self):
        """Crée une base de données de produits courants"""
        return {
            # Électronique et informatique
            'ordinateur': {
                'code': '84.71',
                'description': 'Machines automatiques de traitement de l\'information et leurs unités',
                'rate': '5%',
                'section': 'XVI'
            },
            'laptop': {
                'code': '84.71',
                'description': 'Machines automatiques de traitement de l\'information portables',
                'rate': '5%',
                'section': 'XVI'
            },
            'smartphone': {
                'code': '85.17',
                'description': 'Appareils de télécommunication',
                'rate': '5%',
                'section': 'XVI'
            },
            'téléphone': {
                'code': '85.17',
                'description': 'Appareils de télécommunication',
                'rate': '5%',
                'section': 'XVI'
            },
            
            # Véhicules
            'voiture': {
                'code': '87.03',
                'description': 'Voitures de tourisme et autres véhicules automobiles',
                'rate': '10%',
                'section': 'XVII'
            },
            'automobile': {
                'code': '87.03',
                'description': 'Voitures de tourisme et autres véhicules automobiles',
                'rate': '10%',
                'section': 'XVII'
            },
            'moto': {
                'code': '87.11',
                'description': 'Motos et cycles avec moteur auxiliaire',
                'rate': '10%',
                'section': 'XVII'
            },
            
            # Médicaments et produits pharmaceutiques
            'médicament': {
                'code': '30.04',
                'description': 'Médicaments (autres que les produits du n° 30.02, 30.05 ou 30.06)',
                'rate': '5%',
                'section': 'VI'
            },
            'antibiotique': {
                'code': '30.04',
                'description': 'Médicaments antibiotiques',
                'rate': '5%',
                'section': 'VI'
            },
            
            # Alimentation
            'café': {
                'code': '09.01',
                'description': 'Café, même torréfié ou décaféiné',
                'rate': '10%',
                'section': 'II'
            },
            'thé': {
                'code': '09.02',
                'description': 'Thé, même parfumé',
                'rate': '10%',
                'section': 'II'
            },
            'chocolat': {
                'code': '18.06',
                'description': 'Chocolat et autres préparations alimentaires contenant du cacao',
                'rate': '10%',
                'section': 'IV'
            },
            
            # Textiles et vêtements
            't-shirt': {
                'code': '61.09',
                'description': 'T-shirts, gilets de corps et maillots de corps, en bonneterie',
                'rate': '20%',
                'section': 'XI'
            },
            'coton': {
                'code': '52.01',
                'description': 'Coton, non peigné',
                'rate': '5%',
                'section': 'XI'
            },
            'vêtement': {
                'code': '61.00',
                'description': 'Vêtements et accessoires du vêtement, en bonneterie',
                'rate': '20%',
                'section': 'XI'
            },
            
            # Machines et équipements
            'machine': {
                'code': '84.00',
                'description': 'Réacteurs nucléaires, chaudières, machines, appareils et engins mécaniques',
                'rate': '5%',
                'section': 'XVI'
            },
            'outil': {
                'code': '82.00',
                'description': 'Outils et outillage, articles de coutellerie et couverts de table',
                'rate': '5%',
                'section': 'XV'
            },
            
            # Produits chimiques
            'savon': {
                'code': '34.01',
                'description': 'Savons; produits et préparations tensio-actifs',
                'rate': '10%',
                'section': 'VI'
            },
            'parfum': {
                'code': '33.03',
                'description': 'Parfums et eaux de toilette',
                'rate': '10%',
                'section': 'VI'
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
    
    def search_product(self, description: str) -> List[Dict]:
        """Recherche un produit dans la base de données"""
        results = []
        description_lower = description.lower()
        
        # Recherche dans la base de données de produits courants
        for keyword, product_data in self.product_database.items():
            if keyword in description_lower:
                relevance = self.calculate_relevance(description_lower, product_data['description'].lower())
                # Bonus pour les correspondances exactes de mots-clés
                if keyword in description_lower:
                    relevance += 0.2
                results.append({
                    'type': 'product',
                    'code': product_data['code'],
                    'description': product_data['description'],
                    'rate': product_data['rate'],
                    'section': product_data['section'],
                    'relevance': min(relevance, 1.0)
                })
        
        # Recherche dans les sous-positions (si disponibles)
        for code, data in self.subheadings.items():
            if any(word in data['description'].lower() for word in description_lower.split()):
                results.append({
                    'type': 'subheading',
                    'code': code,
                    'description': data['description'],
                    'rate': data['rate'],
                    'relevance': self.calculate_relevance(description_lower, data['description'].lower())
                })
        
        # Recherche dans les chapitres (si disponibles)
        for chapter_num, chapter_content in self.chapters.items():
            if any(word in chapter_content.lower() for word in description_lower.split()):
                results.append({
                    'type': 'chapter',
                    'code': chapter_num,
                    'description': chapter_content[:200] + "...",
                    'rate': 'À déterminer selon sous-position',
                    'relevance': self.calculate_relevance(description_lower, chapter_content.lower())
                })
        
        # Si aucun résultat, essayer une recherche par mots-clés
        if not results:
            keywords = description_lower.split()
            for keyword, product_data in self.product_database.items():
                if any(kw in keyword for kw in keywords):
                    results.append({
                        'type': 'product',
                        'code': product_data['code'],
                        'description': product_data['description'],
                        'rate': product_data['rate'],
                        'section': product_data['section'],
                        'relevance': 0.5  # Pertinence moyenne pour les correspondances partielles
                    })
        
        # Trier par pertinence
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:10]  # Retourner les 10 meilleurs résultats
    
    def calculate_relevance(self, query: str, text: str) -> float:
        """Calcule la pertinence d'une correspondance"""
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        
        if not query_words:
            return 0.0
        
        # Calcul de la pertinence basé sur l'intersection des mots
        intersection = query_words.intersection(text_words)
        base_relevance = len(intersection) / len(query_words)
        
        # Bonus pour les correspondances exactes
        if query.lower() in text.lower():
            base_relevance += 0.3
        
        # Bonus pour les mots-clés importants
        important_words = ['ordinateur', 'voiture', 'médicament', 'café', 'coton', 'machine', 'laptop', 'smartphone', 'téléphone', 'automobile', 'antibiotique', 'thé', 'chocolat', 't-shirt', 'vêtement', 'outil', 'savon', 'parfum']
        for word in important_words:
            if word in query.lower() and word in text.lower():
                base_relevance += 0.2
        
        # Bonus pour les correspondances partielles
        for query_word in query_words:
            for text_word in text_words:
                if query_word in text_word or text_word in query_word:
                    base_relevance += 0.1
        
        # Bonus pour les correspondances de matériaux
        materials = ['coton', 'laine', 'soie', 'cuir', 'plastique', 'métal', 'bois', 'verre', 'céramique']
        for material in materials:
            if material in query.lower() and material in text.lower():
                base_relevance += 0.15
        
        # Bonus pour les correspondances de fonctions
        functions = ['traitement', 'télécommunication', 'transport', 'médical', 'alimentaire', 'textile', 'mécanique', 'électrique']
        for function in functions:
            if function in query.lower() and function in text.lower():
                base_relevance += 0.15
        
        # Garantir une pertinence minimale pour les correspondances trouvées
        if base_relevance > 0:
            base_relevance = max(base_relevance, 0.3)  # Minimum 30% si correspondance trouvée
        
        return min(base_relevance, 1.0)  # Limiter à 100%
    
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
        page_title="IA Classificateur CEDEAO - Version Simple",
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
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ IA Classificateur CEDEAO</h1>
        <p>Système Harmonisé - Classification Douanière Intelligente</p>
        <p><small>Version Simplifiée - Compatible Python 3.13</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation du classificateur
    if 'classifier' not in st.session_state:
        with st.spinner("Chargement de la base de données CEDEAO..."):
            st.session_state.classifier = SimpleCEDEAOClassifier()
    
    # Interface utilisateur
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Description du Produit")
        product_description = st.text_area(
            "Entrez une description détaillée du produit à classifier :",
            placeholder="Exemple: Ordinateur portable avec écran tactile, processeur Intel i7, 16GB RAM, 512GB SSD...",
            height=150
        )
        
        if st.button("🚀 Classifier le Produit", type="primary", use_container_width=True):
            if product_description.strip():
                with st.spinner("Analyse en cours..."):
                    results = st.session_state.classifier.search_product(product_description)
                
                if results:
                    st.success(f"✅ {len(results)} résultat(s) trouvé(s)")
                    
                    for i, result in enumerate(results):
                        with st.container():
                            section = st.session_state.classifier.get_section_for_chapter(result['code'].split('.')[0])
                            st.markdown(f"""
                            <div class="result-card">
                                <h4>Résultat #{i+1}</h4>
                                <p><strong>Type:</strong> {result['type'].title()}</p>
                                <p><strong>Code:</strong> <span class="highlight">{result['code']}</span></p>
                                <p><strong>Section:</strong> {section}</p>
                                <p><strong>Description:</strong> {result['description']}</p>
                                <p><strong>Taux d'imposition:</strong> <span class="highlight">{result['rate']}</span></p>
                                <p><strong>Pertinence:</strong> {result['relevance']:.2%}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("❌ Aucun résultat trouvé. Essayez avec des mots-clés plus généraux.")
            else:
                st.error("⚠️ Veuillez entrer une description de produit.")
    
    with col2:
        st.subheader("📊 Informations Système")
        
        # Statistiques
        st.metric("Sections", len(st.session_state.classifier.sections))
        st.metric("Chapitres", len(st.session_state.classifier.chapters))
        st.metric("Sous-positions", len(st.session_state.classifier.subheadings))
        
        st.subheader("📋 Règles Générales")
        st.markdown("""
        **RGI 1:** Les titres des sections, chapitres et sous-chapitres n'ont qu'une valeur indicative.
        
        **RGI 2:** Les marchandises incomplètes ou non finies sont classées comme complètes.
        
        **RGI 3:** Le mélange ou l'assemblage de matières ou d'articles est classé selon la matière prépondérante.
        
        **RGI 4:** Les marchandises qui ne peuvent être classées selon les règles 1 à 3 sont classées dans la position la plus analogue.
        
        **RGI 5:** Les emballages sont classés avec les marchandises qu'ils contiennent.
        
        **RGI 6:** Le classement des marchandises dans les sous-positions d'une même position est déterminé selon les termes de ces sous-positions.
        """)
        
        # Exemples d'utilisation
        with st.expander("💡 Exemples d'utilisation"):
            st.markdown("""
            **Ordinateur portable:**
            "Ordinateur portable Dell avec processeur Intel i7, 16GB RAM, 512GB SSD, écran 15 pouces"
            
            **T-shirt en coton:**
            "T-shirt en coton 100%, manches courtes, col rond, taille M"
            
            **Médicament:**
            "Médicament antibiotique en comprimés, boîte de 20 unités"
            
            **Voiture:**
            "Voiture automobile Toyota Corolla, moteur essence 1.8L, 4 portes"
            """)
    
    # Pied de page
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>💡 <strong>Conseil:</strong> Plus votre description est détaillée, plus la classification sera précise.</p>
        <p>🔧 Système basé sur le Tarif Extérieur Commun (TEC) de la CEDEAO</p>
        <p>📝 Version simplifiée - Pour la version complète avec IA avancée, installez les dépendances complètes</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
