import os
import re
import json
import spacy
import torch
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
from nltk.tokenize import sent_tokenize
import nltk

# Descargar recursos de NLTK
nltk.download('punkt')

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CVExtractor:
    def __init__(self, cv_folder: str):
        """
        Inicializar extractor de CVs con modelo de NER y procesadores
        """
        # Cargar modelo de spaCy para reconocimiento de entidades
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except OSError:
            logger.warning("Modelo spaCy no encontrado. Descargando...")
            spacy.cli.download("es_core_news_sm")
            self.nlp = spacy.load("es_core_news_sm")
        
        # Pipeline de transformers para extracción de información
        self.ner_pipeline = pipeline(
            "ner", 
            model="dslim/bert-base-NER",
            aggregation_strategy="simple"
        )
        
        self.cv_folder = cv_folder
        self.cv_files = [f for f in os.listdir(cv_folder) if f.endswith(('.txt', '.pdf', '.docx'))]

    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """
        Extraer información de contacto usando regex y NER
        """
        # Extraer emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        email = emails[0] if emails else None

        # Extraer teléfonos
        phones = re.findall(r'\b(\+?57\s?)?(\d{3}[-.]?\d{3}[-.]?\d{4}|\d{10})\b', text)
        phone = phones[0][1] if phones else None

        return {
            'email': email,
            'phone': phone
        }

    def extract_name(self, text: str) -> str:
        """
        Extraer nombre completo usando spaCy
        """
        doc = self.nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ == 'PER']
        return names[0] if names else None

    def calculate_experience_years(self, text: str) -> float:
        """
        Calcular años de experiencia usando técnicas de NLP
        """
        experience_keywords = [
            'años de experiencia', 'years of experience', 
            'experiencia profesional', 'professional experience'
        ]
        
        years_matches = []
        for keyword in experience_keywords:
            matches = re.findall(r'(\d+)\s*' + re.escape(keyword), text, re.IGNORECASE)
            years_matches.extend(matches)
        
        if years_matches:
            return float(max(years_matches))
        
        # Método alternativo basado en fechas
        dates = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
        if len(dates) > 1:
            return max(int(date) for date in dates) - min(int(date) for date in dates)
        
        return 0

    def check_ai_formation(self, text: str) -> bool:
        """
        Verificar formación en Inteligencia Artificial
        """
        ai_keywords = [
            'inteligencia artificial', 'machine learning', 
            'deep learning', 'aprendizaje profundo', 
            'neural networks', 'redes neuronales',
            'data science', 'ciencia de datos'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in ai_keywords)

    def extract_cv_info(self, file_path: str) -> Dict[str, Any]:
        """
        Método principal de extracción de información del CV
        """
        # Leer contenido del archivo
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            logger.error(f"Error leyendo {file_path}: {e}")
            return None

        # Extraer información
        name = self.extract_name(text)
        contact_info = self.extract_contact_info(text)
        experience_years = self.calculate_experience_years(text)
        ai_formation = self.check_ai_formation(text)

        # Calcular scores
        scores = {
            'name': 0.8 if name else 0,
            'email': 0.9 if contact_info['email'] else 0,
            'phone': 0.7 if contact_info['phone'] else 0,
            'experience_years': 0.6 if experience_years > 0 else 0,
            'ai_formation': 0.7 if ai_formation else 0
        }

        return {
            'name': name,
            'contact': contact_info,
            'experience_years': experience_years,
            'ai_formation': ai_formation,
            'scores': scores
        }

    def process_cvs(self) -> List[Dict[str, Any]]:
        """
        Procesar todos los CVs en la carpeta
        """
        results = []
        for cv_file in self.cv_files:
            file_path = os.path.join(self.cv_folder, cv_file)
            cv_info = self.extract_cv_info(file_path)
            
            if cv_info:
                cv_info['filename'] = cv_file
                results.append(cv_info)
        
        return results

def main():
    cv_folder = './CVs'  # Ajustar ruta de los CVs
    extractor = CVExtractor(cv_folder)
    
    # Procesar CVs
    cv_results = extractor.process_cvs()
    
    # Generar JSON de resultados
    results_json = json.dumps(cv_results, indent=2, ensure_ascii=False)
    print(results_json)
    
    # Opcional: Guardar resultados en archivo
    with open('cv_extraction_results.json', 'w', encoding='utf-8') as f:
        f.write(results_json)

if __name__ == "__main__":
    main()
