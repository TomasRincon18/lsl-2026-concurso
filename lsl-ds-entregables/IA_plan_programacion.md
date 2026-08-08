# PLAN DE PROGRAMACIÓN DE LA IA

## Investigación legal: ¿podemos usar modelos de IA públicos?

**Respuesta: SÍ, absolutamente. Es el enfoque correcto y esperado.**

### Lo que dice el reglamento del concurso

Basado en el análisis de los planes del proyecto (PLAN_COMPLETO.md, PLAN_CIENCIA_DE_DATOS.md):

1. **El concurso ES de Legal Tech.** Aplicar inteligencia artificial a problemas jurídicos. Usar modelos existentes y adaptarlos es la práctica estándar de la industria.

2. **La declaración de uso de IA es obligatoria, no una prohibición.** El reglamento exige un "Anexo C: Declaración de integridad y AI Disclosure" donde se listan TODAS las herramientas de IA utilizadas. Ocultar el uso de IA = descalificación. Declararlo = completamente válido.

3. **Todos los modelos propuestos son open-source con licencias que permiten uso comercial y modificación:**

| Modelo | Procedencia | Licencia | ¿Se puede usar? | ¿Se puede modificar? | ¿Se puede usar en gobierno? |
|---|---|---|---|---|---|
| BETO (bert-base-spanish-wwm-uncased) | Universidad de Chile, disponible en Hugging Face | MIT | Sí | Sí | Sí |
| Mistral 7B | Mistral AI, disponible en Hugging Face | Apache 2.0 | Sí | Sí | Sí |
| Sentence-Transformers (paraphrase-multilingual-mpnet-base-v2) | UKP Lab, Hugging Face | Apache 2.0 | Sí | Sí | Sí |
| spaCy (es_core_news_lg) | Explosion AI | MIT | Sí | Sí | Sí |
| Tesseract OCR | Google (mantenido por la comunidad) | Apache 2.0 | Sí | Sí | Sí |

4. **¿Qué hay del Art. 44 de propiedad intelectual?** El equipo de Derecho debe revisarlo con su mentor jurídico. Pero usar modelos open-source con licencias MIT/Apache 2.0 no genera conflicto de propiedad intelectual porque estas licencias explícitamente permiten el uso, modificación y redistribución.

### Conclusión legal

Usar modelos públicos pre-entrenados es **legal, ético y recomendado**. No solo está permitido por el concurso, sino que es exactamente lo que el sector público y la industria hacen en proyectos reales de IA. Lo ÚNICO obligatorio es declararlo en el Anexo C.

---

## ¿Qué es "usar un modelo público ya existente"?

Imagina que necesitas un médico especialista en dermatología. Tienes dos opciones:

- **Opción A (imposible/absurda):** Criar a un bebé, educarlo durante 25 años, que estudie medicina general, luego se especialice en dermatología. Tiempo: 30 años. Costo: millones de dólares.
- **Opción B (inteligente):** Contratar a un médico general ya graduado y pagarle una especialización en dermatología de 2 años. Tiempo: 2 años. Costo: razonable.

En inteligencia artificial es igual:

- **Entrenar desde cero:** Juntar millones de textos en español, alquilar cientos de GPUs (tarjetas gráficas especializadas) durante semanas, gastar decenas de miles de dólares en electricidad y cómputo. Esto lo hacen universidades y grandes empresas (Google, Meta, Mistral).
- **Fine-tuning (lo que harás tú):** Descargar un modelo que ya "sabe español" (BETO, entrenado por la Universidad de Chile con millones de textos) y enseñarle ÚNICAMENTE a clasificar peticiones de la Defensoría con unos cientos de ejemplos etiquetados. Tiempo: minutos a horas. Costo: CPU normal o GPU gratuita de Google Colab.

---

## Arquitectura general: cómo encajan todos los modelos

```
                         ENTRADA (petición del ciudadano)
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              M1: Tesseract    M1: spaCy NER    M2: BETO
              OCR (lee         (extrae nombre,   (clasifica tipo:
              documentos       CC, dirección,    Asesoría/Queja/
              escaneados)      pretensión)       Mediación/Conciliación)
                                                    │
                                    ┌───────────────┼───────────────┐
                                    ▼               ▼               ▼
                              M4: Sentence-    M6: ChromaDB     M6: Mistral 7B
                              Transformers     + LangChain      (genera borrador
                              (busca           (recupera        de respuesta
                              duplicados)      normativa)       oficial)
```

**Esto es lo que NO necesitas hacer (porque ya está hecho por otros):**
- Enseñarle español a la IA
- Enseñarle gramática
- Enseñarle qué es una oración, un párrafo, un documento

**Esto es lo que SÍ necesitas hacer (fine-tuning):**
- Darle ejemplos etiquetados de peticiones de la Defensoría: "Este texto → Asesoría", "Este otro → Queja"
- La IA ya sabe español. Solo necesita aprender la tarea específica.

---

## Plan detallado de implementación de IA

### FASE A: Preparación del entorno (día 1)

#### ¿Qué computador necesitas?

**Para el PoC (prueba de concepto) y fine-tuning ligero:**
- Cualquier laptop con 8GB+ de RAM funciona
- Alternativa gratuita: Google Colab (te da una GPU gratis por sesión)

**Para fine-tuning serio (opcional, si sobra tiempo):**
- Google Colab Pro (~$40.000 COP/mes) o Kaggle Notebooks (gratis, 30h/semana de GPU)

#### Instalación del entorno Python

```bash
# 1. Crear carpeta del proyecto
mkdir lsl-ia && cd lsl-ia

# 2. Crear ambiente virtual (evita conflictos con otras bibliotecas)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar las bibliotecas necesarias
pip install torch transformers datasets accelerate evaluate
pip install spacy sentence-transformers scikit-learn pandas numpy
pip install fastapi uvicorn

# 4. Descargar modelo de lenguaje español para spaCy
python -m spacy download es_core_news_lg
```

#### Verificar que todo funciona

```python
# test_instalacion.py
import torch
import transformers
import spacy
import sentence_transformers

print(f"PyTorch: {torch.__version__}")
print(f"Transformers: {transformers.__version__}")
print(f"spaCy: {spacy.__version__}")
print(f"GPU disponible: {torch.cuda.is_available()}")

# Cargar modelo de español
nlp = spacy.load("es_core_news_lg")
doc = nlp("La Defensoría del Pueblo recibió una queja sobre salud en Bogotá.")
for ent in doc.ents:
    print(f"  Entidad: {ent.text} -> Tipo: {ent.label_}")
```

---

### FASE B: Preparación de datos de entrenamiento (día 1-2)

Los datos de entrenamiento son ejemplos que le das a la IA para que aprenda.

#### Formato de los datos

Cada ejemplo es un par **(texto de petición → etiqueta correcta)**. Necesitas que el equipo de **Derecho** te entregue ejemplos REALES o REALISTAS de cada categoría.

```json
[
  {
    "texto": "Necesito información sobre cómo interponer una tutela para proteger mi derecho a la salud, tengo una enfermedad crónica y la EPS me niega el medicamento",
    "tipo": "Asesoría",
    "sub_tema": "Salud",
    "urgencia": 3
  },
  {
    "texto": "Denuncio que en la cárcel La Picota de Bogotá no me permiten acceder a mis medicamentos para la diabetes desde hace dos semanas, mi vida corre peligro",
    "tipo": "Queja",
    "sub_tema": "Prisiones",
    "urgencia": 5
  },
  {
    "texto": "Solicito mediación con mi empleador porque fui despedido sin justa causa después de 8 años de trabajo y no me quieren pagar la indemnización",
    "tipo": "Solicitud de Mediación",
    "sub_tema": "Trabajo",
    "urgencia": 2
  },
  {
    "texto": "Quiero solicitar una conciliación con mi arrendador, me quiere desalojar sin orden judicial y tengo dos niños pequeños",
    "tipo": "Solicitud de Conciliación",
    "sub_tema": "Vivienda",
    "urgencia": 4
  }
]
```

#### ¿Cuántos ejemplos necesitas?

| Para el documento (diseño conceptual) | Para un PoC funcional (opcional) |
|---|---|
| Solo necesitas describir el proceso. No necesitas datos reales. | Mínimo 50-100 ejemplos etiquetados (~25 por categoría) |
| Los D1 y D2 de Derecho YA son esto: definiciones + ejemplos de cada categoría. | Pedirle a Derecho 25 ejemplos por cada tipo (D1) y 5-10 por sub-tema (D2) |

#### ¿De dónde salen los datos?

1. **De los entregables D1 y D2 del equipo de Derecho** — ellos deben darte definiciones y ejemplos concretos de cada categoría.
2. **De tu creación de ejemplos sintéticos** — tú mismo puedes redactar ejemplos realistas basándote en lo que describe el caso. Esto es válido para el diseño conceptual.
3. **Para un PoC:** Combinar ejemplos del caso + ejemplos creados por ustedes + cualquier dato anonimizado que tengan.

---

### FASE C: Fine-tuning del clasificador (M2) — El corazón del sistema

#### ¿Qué modelo usar?

**Modelo base:** `dccuchile/bert-base-spanish-wwm-uncased` (BETO)

- **Quién lo creó:** Universidad de Chile, Departamento de Ciencias de la Computación
- **Dónde descargarlo:** https://huggingface.co/dccuchile/bert-base-spanish-wwm-uncased
- **Qué sabe hacer:** Entiende español a nivel profundo (gramática, contexto, significado)
- **Qué NO sabe hacer (aún):** Clasificar peticiones de la Defensoría
- **Qué aprenderá con fine-tuning:** "Este texto es una Queja", "Este otro es una Asesoría"

#### Código paso a paso

```python
# ============================================================
# PASO 1: Cargar el modelo pre-entrenado
# ============================================================
from transformers import (
    AutoTokenizer,          # Convierte texto en números que la IA entiende
    AutoModelForSequenceClassification,  # El modelo con "cabeza" de clasificación
    Trainer,                # Orquesta el entrenamiento
    TrainingArguments       # Configuración: cuántas vueltas, velocidad, etc.
)
from datasets import Dataset  # Estructura de datos para entrenar
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

# Nombre del modelo en Hugging Face
MODELO_BASE = "dccuchile/bert-base-spanish-wwm-uncased"

# Cargar el tokenizador: convierte "Hola, necesito ayuda" → [234, 456, 789, ...]
# (cada número representa una palabra o parte de palabra)
tokenizer = AutoTokenizer.from_pretrained(MODELO_BASE)

# Cargar el modelo con una "cabeza" de 4 categorías
# num_labels=4 porque tenemos: Asesoría, Queja, Mediación, Conciliación
model = AutoModelForSequenceClassification.from_pretrained(
    MODELO_BASE,
    num_labels=4
)

print("Modelo cargado correctamente")
print(f"El modelo tiene {model.num_parameters():,} parámetros")
# BETO tiene ~110 millones de parámetros.
# Un parámetro es como una "perilla" que se ajusta durante el entrenamiento.

# ============================================================
# PASO 2: Preparar los datos de entrenamiento
# ============================================================
# Mapeo de categorías a números
CATEGORIAS = {
    "Asesoría": 0,
    "Queja": 1,
    "Solicitud de Mediación": 2,
    "Solicitud de Conciliación": 3
}

# Aquí pones tus ejemplos etiquetados (los que te dé Derecho o crees tú)
datos = [
    {"texto": "Necesito saber cómo solicitar una tutela para salud...", "tipo": "Asesoría"},
    {"texto": "Denuncio que en la cárcel no me dan medicamentos...", "tipo": "Queja"},
    # ... (mínimo 50-100 ejemplos)
]

# Convertir textos y etiquetas
textos = [d["texto"] for d in datos]
etiquetas = [CATEGORIAS[d["tipo"]] for d in datos]

# Dividir: 80% para entrenar, 20% para probar
textos_train, textos_test, etiquetas_train, etiquetas_test = train_test_split(
    textos, etiquetas, test_size=0.2, random_state=42
)

# Tokenizar: convertir texto a números que el modelo entiende
def tokenizar(ejemplos):
    return tokenizer(
        ejemplos["texto"],
        truncation=True,   # Corta textos muy largos
        padding=True,      # Rellena textos cortos para que todos midan igual
        max_length=512     # Máximo de palabras por texto
    )

# Crear datasets
train_dataset = Dataset.from_dict({
    "texto": textos_train,
    "labels": etiquetas_train
}).map(tokenizar, batched=True)

test_dataset = Dataset.from_dict({
    "texto": textos_test,
    "labels": etiquetas_test
}).map(tokenizar, batched=True)

# ============================================================
# PASO 3: Configurar el entrenamiento
# ============================================================
training_args = TrainingArguments(
    output_dir="./resultados_beto",       # Carpeta donde se guarda el modelo entrenado
    num_train_epochs=3,                   # Cuántas veces "lee" todos los ejemplos (3 es suficiente para empezar)
    per_device_train_batch_size=8,        # Cuántos ejemplos procesa a la vez (depende de tu RAM)
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",          # Evalúa al final de cada época
    save_strategy="epoch",                # Guarda el modelo al final de cada época
    load_best_model_at_end=True,          # Al finalizar, carga la mejor versión (no la última)
    metric_for_best_model="f1",           # Usa F1 score para decidir cuál es "la mejor"
    logging_dir="./logs",
    logging_steps=10,
)

# Función para calcular métricas durante el entrenamiento
def calcular_metricas(pred):
    predictions = np.argmax(pred.predictions, axis=1)
    labels = pred.label_ids
    f1 = f1_score(labels, predictions, average="weighted")
    acc = accuracy_score(labels, predictions)
    return {"accuracy": acc, "f1": f1}

# Crear el entrenador
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=calcular_metricas,
)

# ============================================================
# PASO 4: ¡ENTRENAR!
# ============================================================
print("Iniciando fine-tuning...")
trainer.train()

# Guardar el modelo entrenado
model.save_pretrained("./modelo_beto_defensoria")
tokenizer.save_pretrained("./modelo_beto_defensoria")
print("Modelo guardado en ./modelo_beto_defensoria")

# ============================================================
# PASO 5: Evaluar el modelo
# ============================================================
resultados = trainer.evaluate()
print(f"Resultados en datos de prueba:")
print(f"  Accuracy: {resultados['eval_accuracy']:.2%}")
print(f"  F1 Score: {resultados['eval_f1']:.2%}")
```

#### ¿Qué está pasando en este código? (Explicación línea a línea)

1. **Cargar el modelo pre-entrenado:** Descargamos BETO de internet. BETO ya "sabe español" porque fue entrenado con millones de textos (Wikipedia, noticias, libros en español). Es como un médico general recién graduado.

2. **Preparar los datos:** Convertimos cada texto de petición en una lista de números (tokens) usando el tokenizador. La IA no entiende letras, entiende números. También le decimos cuál es la categoría correcta (etiqueta).

3. **Dividir los datos (80/20):** El 80% de los ejemplos se usan para enseñar. El 20% se reserva para "hacer el examen" al final. **Nunca se evalúa con los mismos datos con los que se entrenó** (sería como pasarle el examen con las respuestas).

4. **Configurar el entrenamiento:** Definimos cuántas "vueltas" (épocas) da el modelo sobre los datos. Cada época, el modelo lee todos los ejemplos, predice, mide su error, y ajusta sus parámetros para mejorar.

5. **Entrenar:** El modelo pasa por todos los ejemplos 3 veces (3 épocas). En cada paso: predice la categoría, compara con la respuesta real, calcula el error, y ajusta sus "perillas" internas (parámetros) para equivocarse menos la próxima vez.

6. **Guardar y evaluar:** Guardamos la mejor versión del modelo (la que tuvo mejor F1 en los datos de prueba). Imprimimos accuracy y F1.

---

### FASE D: Embeddings para anti-duplicación (M4)

```python
# ============================================================
# M4: Detección de duplicados con Sentence-Transformers
# ============================================================
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Cargar modelo de embeddings multilingüe
modelo_emb = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Ejemplo: dos peticiones muy similares (paráfrasis)
peticion_1 = "Denuncio que en la cárcel La Picota no me dan acceso a mis medicamentos para la diabetes"
peticion_2 = "Llevo dos semanas sin recibir mi tratamiento para la diabetes en el centro penitenciario La Picota"

# Convertir textos a vectores numéricos (embeddings)
vector_1 = modelo_emb.encode(peticion_1)  # Lista de 768 números
vector_2 = modelo_emb.encode(peticion_2)  # Lista de 768 números

# Calcular similitud: ¿qué tan parecidos son?
similitud = cosine_similarity([vector_1], [vector_2])[0][0]

print(f"Similitud entre las dos peticiones: {similitud:.2%}")
# Resultado esperado: ~90% (son la misma queja con distintas palabras)

UMBRAL = 0.85  # 85% de similitud = probable duplicado
if similitud >= UMBRAL:
    print("⚠️  ALERTA: Posible duplicado detectado. Sugerir acumulación.")
else:
    print("✓ Petición nueva. Crear caso.")
```

#### ¿Qué es un embedding?

Un embedding es una "huella digital numérica" de un texto. Convierte "Me quejo de mala atención médica" en una lista de 768 números que representan su significado. La magia: textos con significados similares tienen embeddings cercanos entre sí (cosine similarity alta), aunque usen palabras completamente diferentes.

---

### FASE E: RAG — Asistente generativo para respuestas (M6)

```python
# ============================================================
# M6: RAG - Búsqueda en conocimiento + generación de respuesta
# ============================================================
# NOTA: Esta es una versión conceptual. Para un PoC funcional
# se necesita Mistral 7B corriendo localmente (vía Ollama)
# o una GPU con al menos 16GB de VRAM.

# CONCEPTUAL: Así funciona el pipeline RAG

# 1. El ciudadano escribe su petición
peticion = "Solicito información sobre mis derechos como desplazado"

# 2. Se busca información relevante en la base de conocimiento (ChromaDB)
#    ChromaDB contiene fragmentos de:
#    - Ley 1448 de 2011 (Víctimas)
#    - Ley 387 de 1997 (Desplazamiento forzado)
#    - Sentencias de la Corte Constitucional sobre desplazamiento
#    - Templates de respuesta de la Defensoría (D6 de Derecho)
documentos_relevantes = chroma_db.buscar(peticion, k=5)  # Top 5 más relevantes

# 3. Se construye un "prompt" (instrucción) que incluye la pregunta y el contexto
prompt = f"""
Eres un asistente de la Defensoría del Pueblo de Colombia.
Tu función es redactar borradores de respuesta para revisión de un profesional.

REGLAS:
1. Usa lenguaje claro, respetuoso y ciudadano. Evita tecnicismos.
2. Cita la normativa aplicable cuando corresponda.
3. NO inventes información. Si no hay base suficiente, indícalo.
4. NO tomes decisiones vinculantes. El profesional siempre revisa y aprueba.

CONTEXTO NORMATIVO:
{documentos_relevantes}

PETICIÓN DEL CIUDADANO:
{peticion}

Redacta un borrador de respuesta:
"""

# 4. Mistral 7B genera el borrador
borrador = mistral_7b.generar(prompt)

# 5. El profesional revisa, edita y aprueba (HUMAN-IN-THE-LOOP OBLIGATORIO)
print("BORRADOR GENERADO (pendiente de revisión):")
print(borrador)
print("\n⚠️  RECUERDE: Este borrador DEBE ser revisado y aprobado por un profesional.")
```

#### ¿Qué es RAG y por qué lo usamos?

**RAG (Retrieval-Augmented Generation)** es una técnica que evita que la IA "alucine" (invente información).

- **Sin RAG:** Le preguntas a la IA "¿Qué derechos tiene un desplazado?" y ella responde de memoria. Puede acertar o puede inventar una ley que no existe.
- **Con RAG:** La IA primero BUSCA en documentos reales (leyes, sentencias, templates oficiales), luego RESPONDE basándose ÚNICAMENTE en lo que encontró. Si no encuentra nada, lo dice.

---

### FASE F: Ciclo de vida de la IA (cómo se mantiene viva)

```
                     ┌──────────────────┐
                     │   DATOS NUEVOS   │
                     │  (peticiones que │
                     │   llegan cada    │
                     │      día)        │
                     └────────┬─────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │      MODELO EN PRODUCCIÓN     │
              │  (BETO fine-tuned clasificando│
              │   peticiones en tiempo real)  │
              └───────────────┬───────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────┐
        │ MÉTRICAS │  │  DRIFT?  │  │  FEEDBACK DE │
        │Accuracy, │  │¿Cambiaron│  │PROFESIONALES │
        │F1, etc.  │  │los datos?│  │ "Este caso   │
        └────┬─────┘  └────┬─────┘  │está mal      │
             │             │        │clasificado"  │
             │             │        └──────┬───────┘
             └─────────────┼───────────────┘
                           │
                           ▼
              ┌───────────────────────────────┐
              │   ¿TOCA REENTRENAR?           │
              │                               │
              │  - ¿Accuracy bajó de 85%?     │──No──▶ Seguir monitoreando
              │  - ¿Drift significativo?      │
              │  - ¿Muchos errores marcados?  │
              └───────────────┬───────────────┘
                              │Sí
                              ▼
              ┌───────────────────────────────┐
              │      REENTRENAMIENTO          │
              │                               │
              │  1. Juntar datos originales   │
              │     + nuevos casos etiquetados│
              │  2. Volver a hacer fine-tuning│
              │  3. Evaluar equidad           │
              │  4. Si todo OK → desplegar    │
              └───────────────────────────────┘
```

**¿Cada cuánto se reentrena?**

| En el piloto (6 meses) | En producción continua |
|---|---|
| Al final del piloto (1 vez), usando todos los datos acumulados y el feedback de profesionales | Trimestral o cuando el monitoreo de drift lo indique |

**¿Quién lo hace?**

| Durante el proyecto (contratista) | Después de la transferencia (Defensoría) |
|---|---|
| El equipo de Ciencia de Datos del contratista | El equipo interno de TI de la Defensoría, capacitado en Fase 4 |

---

### FASE G: Pruebas (cómo saber si la IA funciona bien)

#### Tipos de prueba

| Tipo | ¿Qué prueba? | ¿Cómo se hace? | ¿Cuándo? |
|---|---|---|---|
| **Precisión (accuracy)** | ¿Cuántas peticiones clasifica correctamente? | Comparar predicción vs etiqueta real en datos de prueba (20% reservado) | Al terminar el fine-tuning |
| **F1 por clase** | ¿Funciona igual de bien para todas las categorías? O falla más en "Conciliación" que en "Asesoría"? | Calcular F1 para cada una de las 4 categorías por separado | Al terminar el fine-tuning |
| **Equidad (fairness)** | ¿Funciona igual de bien para hombres, mujeres, desplazados, etc.? | Segmentar los datos de prueba por grupo y comparar métricas | Antes del despliegue + trimestral |
| **Aceptación humana** | ¿Los profesionales consideran útiles los resultados? | Encuesta + tasa de aceptación de borradores M6 | Durante el piloto |
| **Robustez** | ¿Qué pasa si llega un texto con errores de ortografía, mayúsculas, o muy corto? | Crear casos "difíciles" a propósito y ver cómo responde el modelo | Antes del despliegue |

#### Código para evaluar el modelo (matriz de confusión y reporte)

```python
from sklearn.metrics import classification_report, confusion_matrix

# Predecir con el modelo entrenado
predicciones = trainer.predict(test_dataset)
y_pred = np.argmax(predicciones.predictions, axis=1)
y_true = predicciones.label_ids

# Nombres de las categorías
nombres = list(CATEGORIAS.keys())

# Reporte detallado
print("=" * 50)
print("REPORTE DE CLASIFICACIÓN")
print("=" * 50)
print(classification_report(y_true, y_pred, target_names=nombres))

# Matriz de confusión: ¿con qué categorías se confunde el modelo?
print("MATRIZ DE CONFUSIÓN")
print("Filas = Categoría REAL | Columnas = Categoría PREDICHA")
print(confusion_matrix(y_true, y_pred))
```

**Ejemplo de salida del reporte:**

```
                  precision    recall  f1-score   support

       Asesoría       0.88      0.91      0.89        45
          Queja       0.85      0.82      0.83        38
      Mediación       0.82      0.79      0.80        29
   Conciliación       0.90      0.88      0.89        34

       accuracy                           0.86       146
      macro avg       0.86      0.85      0.85       146
   weighted avg       0.86      0.86      0.86       146
```

**Cómo leer este reporte:**
- **Precision (Asesoría = 0.88):** Cuando el modelo dijo "Asesoría", acertó el 88% de las veces.
- **Recall (Asesoría = 0.91):** De todas las Asesorías reales, el modelo encontró el 91%.
- **F1 (Asesoría = 0.89):** Promedio armónico de las dos anteriores.
- **Support:** Cuántos ejemplos había de esa categoría en los datos de prueba.
- **Accuracy total = 0.86:** El modelo acertó en el 86% de todas las predicciones.

---

## Resumen: ¿Qué necesitas para programar la IA?

| Componente | Modelo | ¿Dónde se consigue? | ¿Se entrena? | ¿Para qué sirve? |
|---|---|---|---|---|
| Clasificador (M2) | BETO | huggingface.co/dccuchile/bert-base-spanish-wwm-uncased | Sí, fine-tuning | Clasificar peticiones en 4 tipos |
| Anti-duplicados (M4) | Sentence-Transformers | huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2 | No (se usa tal cual) | Detectar peticiones duplicadas |
| Asistente (M6) | Mistral 7B | huggingface.co/mistralai/Mistral-7B-Instruct-v0.2 | No (se usa tal cual + RAG) | Generar borradores de respuesta |
| NER (M1) | spaCy | es_core_news_lg (descarga automática) | Opcional (fine-tuning con datos propios) | Extraer nombres, CC, etc. |
| OCR (M1) | Tesseract | github.com/tesseract-ocr/tesseract | No (se usa tal cual) | Leer documentos escaneados |

---

## Glosario completo de términos de IA

| Término | Explicación simple |
|---|---|
| **Modelo pre-entrenado** | IA que ya fue entrenada por una universidad o empresa con millones de textos. La descargas y está lista para usar o adaptar. |
| **Fine-tuning** | "Especialización": tomas un modelo que ya sabe español y le enseñas tu tarea específica con ejemplos. Como especializar a un médico general. |
| **Token** | Unidad mínima de texto que la IA entiende. Puede ser una palabra completa ("queja") o parte de una palabra ("##ción"). El tokenizador convierte texto en tokens. |
| **Tokenizador** | Programa que convierte texto humano ("Hola, necesito ayuda") en una lista de números que la IA puede procesar. |
| **Época (epoch)** | Una "pasada" completa por todos los datos de entrenamiento. Si tienes 100 ejemplos, una época = el modelo ve los 100 ejemplos una vez. |
| **Batch** | Cuántos ejemplos procesa el modelo a la vez. Batch de 8 = el modelo lee 8 peticiones, predice, calcula error, ajusta. Luego las siguientes 8. |
| **Embedding** | "Huella digital numérica" de un texto. Convierte una oración en una lista de ~768 números que capturan su significado. |
| **Cosine similarity** | Número de 0 a 1 que mide qué tan parecidos son dos embeddings (y por tanto dos textos). 1 = idénticos. |
| **RAG** | Retrieval-Augmented Generation. La IA busca en documentos reales antes de responder. Evita que invente información. |
| **Alucinación** | Cuando un LLM genera información falsa pero convincente. Ej: citar una ley que no existe. El RAG ayuda a prevenirlo. |
| **LLM** | Large Language Model. Modelo de lenguaje grande (como Mistral 7B). Capaz de entender y generar texto. |
| **Accuracy** | Porcentaje de aciertos. ¿Cuántas predicciones fueron correctas del total? |
| **Precision** | De lo que el modelo dijo "X", ¿qué porcentaje realmente era "X"? Mide qué tan confiable es cuando afirma algo. |
| **Recall** | De todo lo que realmente es "X", ¿qué porcentaje encontró el modelo? Mide qué tan bueno es detectando. |
| **F1 Score** | Promedio entre precision y recall. Un solo número para evaluar el modelo. 1.0 = perfecto. |
| **Falso positivo** | El modelo dijo "SÍ" pero era "NO". Ej: dijo "es una Queja urgente" pero era una consulta rutinaria. |
| **Falso negativo** | El modelo dijo "NO" pero era "SÍ". El error más peligroso. Ej: dijo "no es urgente" pero el ciudadano estaba amenazado de muerte. |
| **Matriz de confusión** | Tabla que muestra en qué se equivoca el modelo: ¿confunde Quejas con Asesorías? |
| **GPU** | Graphics Processing Unit. Tarjeta gráfica especializada para entrenar IA. Mucho más rápida que una CPU normal. Google Colab te presta una gratis. |
| **Parámetros** | "Perillas" internas del modelo que se ajustan durante el entrenamiento. BETO tiene ~110 millones. |
| **Overfitting** | El modelo "se memoriza" los ejemplos de entrenamiento pero falla con datos nuevos. Como un estudiante que memoriza el examen pero no entiende la materia. |
| **Dataset** | Conjunto de datos etiquetados para entrenar o evaluar. |
| **Train/Test split** | Dividir datos: 80% para enseñar, 20% para examinar. Fundamental para no hacer trampa. |
| **Drift** | El rendimiento del modelo empeora porque el mundo cambió (nuevos tipos de quejas, cambio de gobierno, etc.). |
| **MLOps** | Prácticas para mantener modelos de IA saludables en producción: monitorearlos, reentrenarlos, versionarlos. |
| **Hugging Face** | El "GitHub de la IA". Sitio web (huggingface.co) donde se comparten modelos, datasets y herramientas. Gratuito. |

---

## Recursos recomendados para aprender

| Recurso | Enlace | ¿Para qué? |
|---|---|---|
| Hugging Face Course | https://huggingface.co/learn/nlp-course | Curso gratuito de NLP con transformers |
| Documentación de BETO | https://huggingface.co/dccuchile/bert-base-spanish-wwm-uncased | Ficha técnica del modelo |
| Google Colab | https://colab.research.google.com | GPU gratis para entrenar modelos |
| Mermaid Live | https://mermaid.live | Editor de diagramas (los que usamos en los .md) |
| FastAPI docs | https://fastapi.tiangolo.com | Documentación del backend |
| spaCy Spanish models | https://spacy.io/models/es | Modelos de lenguaje español |
