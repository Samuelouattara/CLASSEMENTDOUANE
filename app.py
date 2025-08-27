import streamlit as st
import pandas as pd
import re
from typing import Dict, List, Tuple, Optional
import json
import os
from ai_classifier import AdvancedCEDEAOClassifier
from dictionnaire_utils import DictionnaireFrancais, analyser_description_douane, suggerer_améliorations_description

class CEDEAOClassifier:
    def __init__(self):
        self.data_file = "MON-TEC-CEDEAO-SH-2022-FREN-09-04-2024.txt"
        self.sections = {}
        self.chapters = {}
        self.subheadings = {}
        self.advanced_classifier = None
        self.dictionnaire_francais = None
        self.load_data()
        self.initialize_advanced_classifier()
        self.initialize_dictionnaire_francais()
    
    def initialize_advanced_classifier(self):
        """Initialise le classificateur avancé"""
        try:
            with st.spinner("Initialisation de l'IA avancée..."):
                self.advanced_classifier = AdvancedCEDEAOClassifier()
        except Exception as e:
            st.warning(f"L'IA avancée n'est pas disponible: {e}")
            self.advanced_classifier = None
    
    def initialize_dictionnaire_francais(self):
        """Initialise le dictionnaire français"""
        try:
            with st.spinner("Chargement du dictionnaire français..."):
                self.dictionnaire_francais = DictionnaireFrancais()
                st.success(f"✓ Dictionnaire français chargé: {len(self.dictionnaire_francais.mots_francais)} mots")
        except Exception as e:
            st.warning(f"Le dictionnaire français n'est pas disponible: {e}")
            self.dictionnaire_francais = None
        
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
    
    def parse_chapters(self, content: str):
        """Parse les chapitres du système harmonisé"""
        chapter_pattern = r'Chapitre (\d+)\s*\n([^\n]+(?:\n[^\n]+)*?)(?=Chapitre|\Z)'
        matches = re.finditer(chapter_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            chapter_num = match.group(1)
            chapter_content = match.group(2).strip()
            self.chapters[chapter_num] = chapter_content
    
    def parse_subheadings(self, content: str):
        """Parse les sous-positions avec leurs taux"""
        # Pattern pour les sous-positions avec codes et taux (format CEDEAO)
        subheading_pattern = r'(\d{4}\.\d{2}\.\d{2}\.\d{2})\s+--\s+([^\n]+?)\s+([a-z]+)\s+(\d+)\s+\d+'
        matches = re.finditer(subheading_pattern, content)
        
        for match in matches:
            code = match.group(1)
            description = match.group(2).strip()
            unit = match.group(3)
            rate = match.group(4) + "%"
            self.subheadings[code] = {
                'description': description,
                'rate': rate,
                'unit': unit
            }
    
    def search_product(self, description: str, use_advanced: bool = True) -> List[Dict]:
        """Recherche un produit dans la base de données"""
        if use_advanced and self.advanced_classifier:
            # Utiliser le classificateur avancé
            database = {
                'subheadings': self.subheadings,
                'chapters': self.chapters,
                'sections': self.sections
            }
            return self.advanced_classifier.classify_product(description, database)
        else:
            # Méthode de base
            results = []
            description_lower = description.lower()
            
            # Recherche dans les sous-positions
            for code, data in self.subheadings.items():
                if any(word in data['description'].lower() for word in description_lower.split()):
                    results.append({
                        'type': 'subheading',
                        'code': code,
                        'description': data['description'],
                        'rate': data['rate'],
                        'relevance': self.calculate_relevance(description_lower, data['description'].lower())
                    })
            
            # Recherche dans les chapitres
            for chapter_num, chapter_content in self.chapters.items():
                if any(word in chapter_content.lower() for word in description_lower.split()):
                    results.append({
                        'type': 'chapter',
                        'code': chapter_num,
                        'description': chapter_content[:200] + "...",
                        'rate': 'À déterminer selon sous-position',
                        'relevance': self.calculate_relevance(description_lower, chapter_content.lower())
                    })
            
            # Trier par pertinence
            results.sort(key=lambda x: x['relevance'], reverse=True)
            return results[:10]  # Retourner les 10 meilleurs résultats
    
    def calculate_relevance(self, query: str, text: str) -> float:
        """Calcule la pertinence d'une correspondance"""
        query_words = set(query.split())
        text_words = set(text.split())
        
        if not query_words:
            return 0.0
        
        intersection = query_words.intersection(text_words)
        return len(intersection) / len(query_words)
    
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
    
    def analyser_description_francaise(self, description: str) -> Dict:
        """Analyse une description avec le dictionnaire français"""
        if not self.dictionnaire_francais:
            return {
                "disponible": False,
                "message": "Dictionnaire français non disponible"
            }
        
        try:
            analyse = analyser_description_douane(description, self.dictionnaire_francais)
            suggestions = suggerer_améliorations_description(description, self.dictionnaire_francais)
            
            return {
                "disponible": True,
                "analyse": analyse,
                "suggestions": suggestions,
                "qualite_francais": self._evaluer_qualite_francais(analyse['ratio_francais'])
            }
        except Exception as e:
            return {
                "disponible": False,
                "erreur": str(e)
            }
    
    def _evaluer_qualite_francais(self, ratio: float) -> str:
        """Évalue la qualité française d'une description"""
        if ratio >= 0.7:
            return "Excellente"
        elif ratio >= 0.5:
            return "Bonne"
        elif ratio >= 0.3:
            return "Moyenne"
        else:
            return "Faible"
    
    def enrichir_dictionnaire(self, nouveaux_mots: List[str]):
        """Enrichit le dictionnaire avec de nouveaux mots"""
        if self.dictionnaire_francais:
            self.dictionnaire_francais.enrichir_dictionnaire(nouveaux_mots)
            st.success(f"✓ Dictionnaire enrichi avec {len(nouveaux_mots)} nouveaux mots")
    
    def obtenir_statistiques_dictionnaire(self) -> Dict:
        """Retourne les statistiques du dictionnaire français"""
        if self.dictionnaire_francais:
            return self.dictionnaire_francais.obtenir_statistiques()
        return {"disponible": False}

def main():
    st.set_page_config(
        page_title="IA Classificateur CEDEAO",
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
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ IA Classificateur CEDEAO</h1>
        <p>Système Harmonisé - Classification Douanière Intelligente</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation du classificateur
    if 'classifier' not in st.session_state:
        with st.spinner("Chargement de la base de données CEDEAO..."):
            st.session_state.classifier = CEDEAOClassifier()
    
    # Interface utilisateur avec onglets
    tab1, tab2 = st.tabs(["🔍 Classification", "🇫🇷 Dictionnaire Français"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🔍 Description du Produit")
            product_description = st.text_area(
                "Entrez une description détaillée du produit à classifier :",
                placeholder="Exemple: Ordinateur portable avec écran tactile, processeur Intel i7, 16GB RAM, 512GB SSD...",
                height=150
            )
        
        # Options de classification
        col1, col2 = st.columns(2)
        with col1:
            use_advanced_ai = st.checkbox("🤖 Utiliser l'IA avancée", value=True, help="Active l'analyse sémantique et les règles RGI")
        with col2:
            show_details = st.checkbox("📊 Afficher les détails", value=False, help="Affiche l'analyse détaillée et les explications")
        
        if st.button("🚀 Classifier le Produit", type="primary", use_container_width=True):
            if product_description.strip():
                with st.spinner("Analyse en cours..."):
                    if use_advanced_ai and st.session_state.classifier.advanced_classifier:
                        # Classification avancée
                        database = {
                            'subheadings': st.session_state.classifier.subheadings,
                            'chapters': st.session_state.classifier.chapters,
                            'sections': st.session_state.classifier.sections
                        }
                        classification = st.session_state.classifier.advanced_classifier.get_detailed_classification(
                            product_description, database
                        )
                        
                        if classification['success']:
                            st.success(f"✅ Classification réussie avec {classification['confidence']:.2%} de confiance")
                            
                            # Affichage du meilleur résultat
                            best_match = classification['best_match']
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>🎯 Meilleure Classification</h3>
                                <p><strong>Type:</strong> {best_match['type'].title()}</p>
                                <p><strong>Code:</strong> <span class="highlight">{best_match['code']}</span></p>
                                <p><strong>Section:</strong> {classification['section']}</p>
                                <p><strong>Description:</strong> {best_match['description']}</p>
                                <p><strong>Taux d'imposition:</strong> <span class="highlight">{best_match['rate']}</span></p>
                                <p><strong>Confiance:</strong> {best_match['final_score']:.2%}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if show_details:
                                # Affichage des détails
                                with st.expander("🔍 Analyse détaillée", expanded=True):
                                    st.write("**Explication:**", classification['explanation'])
                                    
                                    if classification['extracted_features']['materials']:
                                        st.write("**Matériaux détectés:**", ", ".join(classification['extracted_features']['materials']))
                                    
                                    if classification['extracted_features']['functions']:
                                        st.write("**Fonctions détectées:**", ", ".join(classification['extracted_features']['functions']))
                                    
                                    if classification['extracted_features']['technical_specs']:
                                        st.write("**Spécifications techniques:**", ", ".join(classification['extracted_features']['technical_specs']))
                                    
                                    if classification['recommendations']:
                                        st.write("**Recommandations:**")
                                        for rec in classification['recommendations']:
                                            st.write(f"• {rec}")
                            
                            # Autres résultats
                            if len(classification['all_matches']) > 1:
                                with st.expander("📋 Autres résultats possibles"):
                                    for i, result in enumerate(classification['all_matches'][1:6]):
                                        st.markdown(f"""
                                        <div style="background: #f0f0f0; padding: 1rem; margin: 0.5rem 0; border-radius: 5px;">
                                            <strong>#{i+2}</strong> {result['type'].title()} {result['code']} - {result['final_score']:.2%}
                                            <br><small>{result['description'][:100]}...</small>
                                        </div>
                                        """, unsafe_allow_html=True)
                        else:
                            st.warning(f"❌ {classification['message']}")
                            if classification.get('suggestions'):
                                st.write("**Suggestions:**")
                                for suggestion in classification['suggestions']:
                                    st.write(f"• {suggestion}")
                    else:
                        # Classification de base
                        results = st.session_state.classifier.search_product(product_description, use_advanced=False)
                        
                        if results:
                            st.success(f"✅ {len(results)} résultat(s) trouvé(s)")
                            
                            for i, result in enumerate(results):
                                with st.container():
                                    st.markdown(f"""
                                    <div class="result-card">
                                        <h4>Résultat #{i+1}</h4>
                                        <p><strong>Type:</strong> {result['type'].title()}</p>
                                        <p><strong>Code:</strong> <span class="highlight">{result['code']}</span></p>
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
            
            # Statistiques du dictionnaire français
            if st.session_state.classifier.dictionnaire_francais:
                stats_dico = st.session_state.classifier.obtenir_statistiques_dictionnaire()
                if stats_dico.get("disponible", False):
                    st.metric("Mots français", stats_dico["total_mots"])
            
            # Analyse française de la description
            if product_description.strip():
                st.subheader("🇫🇷 Analyse Française")
                
                analyse_fr = st.session_state.classifier.analyser_description_francaise(product_description)
                
                if analyse_fr["disponible"]:
                    analyse = analyse_fr["analyse"]
                    suggestions = analyse_fr["suggestions"]
                    qualite = analyse_fr["qualite_francais"]
                    
                    # Indicateur de qualité
                    if qualite == "Excellente":
                        st.success(f"✅ Qualité française: {qualite}")
                    elif qualite == "Bonne":
                        st.info(f"ℹ️ Qualité française: {qualite}")
                    elif qualite == "Moyenne":
                        st.warning(f"⚠️ Qualité française: {qualite}")
                    else:
                        st.error(f"❌ Qualité française: {qualite}")
                    
                    # Ratio français
                    st.metric("Ratio français", f"{analyse['ratio_francais']:.1%}")
                    
                    # Mots français trouvés
                    if analyse['mots_francais_trouves']:
                        st.write(f"**Mots français:** {len(analyse['mots_francais_trouves'])}")
                        with st.expander("Voir les mots français"):
                            st.write(", ".join(analyse['mots_francais_trouves'][:10]))
                            if len(analyse['mots_francais_trouves']) > 10:
                                st.write(f"... et {len(analyse['mots_francais_trouves']) - 10} autres")
                    
                    # Suggestions d'amélioration
                    if suggestions:
                        st.write("**Suggestions d'amélioration:**")
                        for suggestion in suggestions[:3]:  # Limiter à 3 suggestions
                            st.write(f"• {suggestion}")
                else:
                    st.warning("⚠️ Analyse française non disponible")
            
            st.subheader("📋 Règles Générales")
            st.markdown("""
            **RGI 1:** Les titres des sections, chapitres et sous-chapitres n'ont qu'une valeur indicative.
            
            **RGI 2:** Les marchandises incomplètes ou non finies sont classées comme complètes.
            
            **RGI 3:** Le mélange ou l'assemblage de matières ou d'articles est classé selon la matière prépondérante.
            
            **RGI 4:** Les marchandises qui ne peuvent être classées selon les règles 1 à 3 sont classées dans la position la plus analogue.
            
            **RGI 5:** Les emballages sont classés avec les marchandises qu'ils contiennent.
            
            **RGI 6:** Le classement des marchandises dans les sous-positions d'une même position est déterminé selon les termes de ces sous-positions.
            """)
    
    # Onglet Dictionnaire Français
    with tab2:
        st.subheader("🇫🇷 Gestion du Dictionnaire Français")
        
        if st.session_state.classifier.dictionnaire_francais:
            # Statistiques du dictionnaire
            stats = st.session_state.classifier.obtenir_statistiques_dictionnaire()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total mots", stats["total_mots"])
            with col2:
                st.metric("Longueur moyenne", f"{stats['longueur_moyenne']:.1f}")
            with col3:
                st.metric("Mots uniques", len(set(st.session_state.classifier.dictionnaire_francais.mots_francais)))
            
            # Test de mots
            st.subheader("🔍 Test de Mots")
            test_word = st.text_input("Entrez un mot à tester :", placeholder="Exemple: ballon")
            
            if test_word:
                is_french = st.session_state.classifier.dictionnaire_francais.est_mot_francais(test_word)
                if is_french:
                    st.success(f"✅ '{test_word}' est un mot français")
                else:
                    st.error(f"❌ '{test_word}' n'est pas reconnu comme français")
                    
                    # Suggestions
                    suggestions = st.session_state.classifier.dictionnaire_francais.suggerer_mots_similaires(test_word)
                    if suggestions:
                        st.write("**Suggestions similaires:**")
                        st.write(", ".join(suggestions))
            
            # Enrichissement du dictionnaire
            st.subheader("➕ Enrichir le Dictionnaire")
            new_words = st.text_area(
                "Ajouter de nouveaux mots (un par ligne) :",
                placeholder="nouveau_mot1\nnouveau_mot2\nnouveau_mot3",
                height=100
            )
            
            if st.button("Ajouter les mots", type="primary"):
                if new_words.strip():
                    words_list = [word.strip() for word in new_words.split('\n') if word.strip()]
                    st.session_state.classifier.enrichir_dictionnaire(words_list)
                    st.rerun()
            
            # Analyse de texte
            st.subheader("📝 Analyse de Texte")
            text_to_analyze = st.text_area(
                "Texte à analyser :",
                placeholder="Entrez un texte pour analyser sa qualité française...",
                height=150
            )
            
            if text_to_analyze:
                analyse = st.session_state.classifier.analyser_description_francaise(text_to_analyze)
                if analyse["disponible"]:
                    st.write(f"**Ratio français:** {analyse['analyse']['ratio_francais']:.1%}")
                    st.write(f"**Mots français trouvés:** {len(analyse['analyse']['mots_francais_trouves'])}")
                    
                    if analyse['suggestions']:
                        st.write("**Suggestions d'amélioration:**")
                        for suggestion in analyse['suggestions']:
                            st.write(f"• {suggestion}")
        else:
            st.error("❌ Dictionnaire français non disponible")
            st.info("Le dictionnaire français n'a pas pu être chargé. Vérifiez que le fichier 'dictionnaire_francais.txt' existe.")
    
    # Pied de page
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>💡 <strong>Conseil:</strong> Plus votre description est détaillée, plus la classification sera précise.</p>
        <p>🔧 Système basé sur le Tarif Extérieur Commun (TEC) de la CEDEAO</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
