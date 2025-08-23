#!/usr/bin/env python3
"""
Script d'installation pour l'IA Classificateur CEDEAO
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erreur: {e}")
        print(f"   Sortie d'erreur: {e.stderr}")
        return False

def check_python_version():
    """Vérifie la version de Python"""
    print("🐍 Vérification de la version Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ requis, version actuelle: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_dependencies():
    """Installe les dépendances Python"""
    print("\n📦 Installation des dépendances...")
    
    # Mettre à jour pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Mise à jour de pip"):
        return False
    
    # Installer les dépendances
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installation des dépendances"):
        return False
    
    return True

def download_spacy_model():
    """Télécharge le modèle spaCy français"""
    print("\n🤖 Téléchargement du modèle spaCy français...")
    
    try:
        import spacy
        # Vérifier si le modèle est déjà installé
        try:
            nlp = spacy.load("fr_core_news_sm")
            print("✅ Modèle spaCy français déjà installé")
            return True
        except OSError:
            # Modèle non trouvé, le télécharger
            if run_command(f"{sys.executable} -m spacy download fr_core_news_sm", "Téléchargement du modèle spaCy"):
                return True
            else:
                print("⚠️  Le modèle spaCy n'a pas pu être téléchargé. L'IA avancée pourrait ne pas fonctionner.")
                return False
    except ImportError:
        print("⚠️  spaCy non installé. L'IA avancée ne sera pas disponible.")
        return False

def download_nltk_data():
    """Télécharge les données NLTK nécessaires"""
    print("\n📚 Téléchargement des données NLTK...")
    
    try:
        import nltk
        
        # Créer un script temporaire pour télécharger les données
        nltk_script = """
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
print("NLTK data downloaded successfully")
"""
        
        with open("temp_nltk_download.py", "w") as f:
            f.write(nltk_script)
        
        if run_command(f"{sys.executable} temp_nltk_download.py", "Téléchargement des données NLTK"):
            os.remove("temp_nltk_download.py")
            return True
        else:
            if os.path.exists("temp_nltk_download.py"):
                os.remove("temp_nltk_download.py")
            return False
    except ImportError:
        print("⚠️  NLTK non installé. Certaines fonctionnalités pourraient être limitées.")
        return False

def test_installation():
    """Teste l'installation"""
    print("\n🧪 Test de l'installation...")
    
    # Test d'import des modules principaux
    try:
        import streamlit
        print("✅ Streamlit - OK")
    except ImportError:
        print("❌ Streamlit - Erreur")
        return False
    
    try:
        import pandas
        print("✅ Pandas - OK")
    except ImportError:
        print("❌ Pandas - Erreur")
        return False
    
    try:
        import numpy
        print("✅ NumPy - OK")
    except ImportError:
        print("❌ NumPy - Erreur")
        return False
    
    # Test du classificateur de base
    try:
        from app import CEDEAOClassifier
        classifier = CEDEAOClassifier()
        print("✅ Classificateur de base - OK")
    except Exception as e:
        print(f"❌ Classificateur de base - Erreur: {e}")
        return False
    
    # Test du classificateur avancé (optionnel)
    try:
        from ai_classifier import AdvancedCEDEAOClassifier
        print("✅ Classificateur avancé - OK")
    except Exception as e:
        print(f"⚠️  Classificateur avancé - Limité: {e}")
    
    return True

def create_launcher_script():
    """Crée un script de lancement"""
    print("\n🚀 Création du script de lancement...")
    
    launcher_content = """#!/usr/bin/env python3
\"\"\"
Script de lancement pour l'IA Classificateur CEDEAO
\"\"\"

import subprocess
import sys
import os

def main():
    print("🏛️ Lancement de l'IA Classificateur CEDEAO...")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("app.py"):
        print("❌ Erreur: app.py non trouvé. Assurez-vous d'être dans le répertoire du projet.")
        return
    
    # Lancer l'application
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\\n👋 Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()
"""
    
    with open("launch.py", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    # Rendre le script exécutable (Unix/Linux)
    try:
        os.chmod("launch.py", 0o755)
    except:
        pass
    
    print("✅ Script de lancement créé: launch.py")

def main():
    """Fonction principale d'installation"""
    print("🏛️ Installation de l'IA Classificateur CEDEAO")
    print("=" * 60)
    
    # Vérifier la version Python
    if not check_python_version():
        print("❌ Installation annulée - Version Python incompatible")
        return False
    
    # Installer les dépendances
    if not install_dependencies():
        print("❌ Installation annulée - Erreur lors de l'installation des dépendances")
        return False
    
    # Télécharger les modèles
    download_spacy_model()
    download_nltk_data()
    
    # Tester l'installation
    if not test_installation():
        print("❌ Installation annulée - Erreur lors du test")
        return False
    
    # Créer le script de lancement
    create_launcher_script()
    
    print("\n" + "=" * 60)
    print("✅ Installation terminée avec succès!")
    print("\n🚀 Pour lancer l'application:")
    print("   python launch.py")
    print("   ou")
    print("   streamlit run app.py")
    print("\n📖 Pour plus d'informations, consultez README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

