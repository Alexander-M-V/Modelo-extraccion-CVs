cv-extraction-model

Una herramienta de Python para extraer automáticamente información relevante de currículums vitae (CVs) utilizando técnicas de Procesamiento de Lenguaje Natural (NLP) y Machine Learning.

🚀 Características

- Extracción de información de contacto (email, teléfono)
- Identificación de nombres mediante reconocimiento de entidades nombradas (NER)
- Cálculo de años de experiencia
- Detección de formación en Inteligencia Artificial
- Sistema de puntuación para evaluar la completitud de la información
- Soporte para múltiples formatos de archivo (.txt, .pdf, .docx)
- Generación de resultados en formato JSON

## 📋 Requisitos

```
python >= 3.7
spacy
torch
transformers
nltk
numpy
pandas
```

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/your-username/cv-extraction-model.git
cd cv-extraction-model
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Descarga el modelo de spaCy en español:
```bash
python -m spacy download es_core_news_sm
```

## 💻 Uso

1. Coloca tus archivos de CV en la carpeta `CVs/`

2. Ejecuta el script principal:
```bash
python cv-extraction-model.py
```

3. Los resultados se guardarán en `cv_extraction_results.json`

## 📊 Estructura de Resultados

El script genera un JSON con la siguiente estructura para cada CV:

```json
{
  "name": "Nombre Completo",
  "contact": {
    "email": "ejemplo@email.com",
    "phone": "1234567890"
  },
  "experience_years": 5.0,
  "ai_formation": true,
  "scores": {
    "name": 0.8,
    "email": 0.9,
    "phone": 0.7,
    "experience_years": 0.6,
    "ai_formation": 0.7
  },
  "filename": "ejemplo_cv.pdf"
}
```

## 🛠️ Personalización

Puedes ajustar los siguientes parámetros en el código:

- Palabras clave de IA en `check_ai_formation()`
- Expresiones regulares para email y teléfono en `extract_contact_info()`
- Pesos de puntuación en `extract_cv_info()`

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor, siéntete libre de:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## ✨ Próximas Mejoras

- [ ] Soporte para más idiomas
- [ ] Mejora en la extracción de fechas
- [ ] Interfaz web
- [ ] Exportación a diferentes formatos
- [ ] Análisis de habilidades técnicas
