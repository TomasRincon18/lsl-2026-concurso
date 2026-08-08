# PLAN COMPLETO — Legal Strategy Lab 2026

## CALENDARIO REAL
- **Entrega escrita:** 30 de julio de 2026 (13 días)
- **Fase oral (Bogotá):** 19–21 de agosto de 2026 (+20 días tras entrega)

---

## OBJETIVO
Producir el documento "Estrategia Jurídica" (≤25 págs + anexos) con:
- Análisis jurídico completo
- Diseño técnico detallado (arquitectura, módulos M1-M8, diagramas)
- Modelo de gobernanza de IA
- Análisis sociotécnico
- Matriz de riesgos
- Modelo de negocio
- Anexo contractual
- Declaración de integridad y AI Disclosure

**No hay tiempo para prototipado completo. DS entrega diseño conceptual/arquitectónico detallado + especificaciones + diagramas + PoC mínimo si sobra tiempo.**

---

## DÍAS 1–3: INVESTIGACIÓN Y ANÁLISIS (Jul 17–19)

### Derecho

| # | Tarea | Deadline |
|---|---|---|
| Leer el Caso (RFP) completo | Día 1 |
| Leer CONPES 4144, Directiva 007/2025, Ley 1581/2012, CPACA | Día 1–2 |
| Producir matriz norma-artículo-obligación-implicación | Día 2 |
| Producir D1: Definiciones jurídicas de las 4 categorías con ejemplos | **Día 2** |
| Producir D2: Catálogo de sub-temas (~12) con definiciones | **Día 2** |
| Producir D3: Catálogo de sujetos de especial protección constitucional | **Día 3** |
| Producir D7: Criterios de urgencia con base normativa | **Día 3** |
| Leer resto de bibliografía (UNESCO, OECD, Amnesty, Council of Europe) | Día 2–3 |

### Ciencia de Datos

| # | Tarea | Deadline |
|---|---|---|
| Leer el Caso (RFP) completo, enfocarse en secciones 2, 3, 4, 5, 6 | Día 1 |
| Leer NIST AI RMF 1.0, ISO/IEC 42001:2023, UNESCO, OECD | Día 1–2 |
| Investigar modelos NLP español (BETO, RoBERTa-es, MarIA) — benchmark rápido | Día 1–2 |
| Investigar LLMs open-source español (Llama 3, Mistral, Qwen) | Día 2 |
| Investigar arquitecturas GovTech existentes | Día 2 |
| Hacer diagrama AS-IS del macroproceso | Día 2–3 |
| Mapear puntos de falla técnicos actuales | Día 3 |
| Definir stack tecnológico propuesto con justificación | Día 3 |
| Configurar entorno Python + descargar modelos base | Día 1 |

### Ambos

| # | Tarea |
|---|---|
| Crear espacio compartido (Google Drive + GitHub) | Día 1 |
| Calendarizar reuniones diarias de 30 min (sincronización) | Día 1 |
| Preparar preguntas para sesión de Q&A con el cliente (Art. 13) | Día 1 |

---

## DÍAS 3–5: DISEÑO CONJUNTO (Jul 19–21)

### Entregables de Derecho para DS (¡bloqueantes!)

| # | Entregable | Deadline |
|---|---|---|
| D1 | Definiciones de las 4 categorías + ejemplos reales | Día 2 ✅ |
| D2 | Catálogo de sub-temas | Día 2 ✅ |
| D3 | Sujetos de especial protección constitucional | Día 3 ✅ |
| D4 | Matriz tipo/subtema → entidad competente | **Día 4** |
| D5 | Catálogo de consultas automatizables | **Día 4** |
| D6 | Templates de respuesta institucional (10-20) | **Día 5** |
| D7 | Criterios de urgencia | Día 3 ✅ |
| D8 | Umbral de duplicación jurídicamente defendible | **Día 5** |
| D9 | Esquema de roles RBAC con fundamento legal | **Día 5** |

### Diseño conjunto

| # | Tarea | Responsable |
|---|---|---|
| Diseñar macroproceso TO-BE con IA integrada | DS lidera, Derecho valida |
| Definir modelo de gobernanza de IA (roles, políticas, human-in-the-loop, incidentes, auditoría) | Derecho lidera, DS valida viabilidad |
| Análisis sociotécnico: 4 preguntas del caso | Derecho lidera, DS da input |
| Matriz de riesgos (técnicos → operacionales → jurídicos) | Conjunto |
| Modelo de negocio (costos 3 años, sostenibilidad) | Conjunto |
| Arquitectura lógica y de datos (alto nivel) | DS |
| Diseño detallado de cada módulo M1-M8 | DS |
| Especificaciones de APIs (IRIS, VisionWeb, internas) | DS |

---

## DÍAS 5–8: PRODUCCIÓN DE CONTENIDO TÉCNICO (Jul 21–24)

> **DS trabaja intensivo. Derecho avanza secciones escritas en paralelo.**

### DS — Diseño detallado de módulos (no prototipos, sino especificaciones)

| Módulo | Entregable |
|---|---|
| **M1** | Diagrama del pipeline de ingesta. Especificación de endpoints. Estrategia OCR (Tesseract + preprocesamiento OpenCV). Esquema NER (entidades a extraer). Lógica de detección de datos faltantes |
| **M2** | Diseño del pipeline de clasificación. Estrategia de fine-tuning (BETO). Métricas esperadas. Sistema de reglas para urgencia. Sistema de priorización (determinístico). Plan de evaluación de equidad (fairness) |
| **M3** | Matriz de reglas de competencia (con input D4 de Derecho). Diseño de bandejas de trabajo. Indicadores SLA |
| **M4** | Diseño del pipeline de similitud (embeddings + cosine similarity). Reglas de duplicación (con umbral D8 de Derecho). Métricas de evaluación |
| **M5** | Diseño de índice de búsqueda (Elasticsearch). Esquema de vista unificada del ciudadano |
| **M6** | Arquitectura RAG detallada. Diagrama de flujo: consulta → retrieval → prompt → LLM → borrador → revisión humana. Selección justificada del LLM. Sistema de logs de auditoría. Estrategia anti-alucinaciones |
| **M7** | Diagrama de secuencia de integración IRIS/VisionWeb. Contratos de API (OpenAPI). Estrategia anti-doble registro. Mecanismo de sincronización event-driven |
| **M8** | Diseño de dashboards (mockups o descripciones). Métricas por dashboard. Estrategia de privacidad para datos agregados |
| **MLOps** | Pipeline de versionamiento (DVC + Git). Estrategia de monitoreo de drift (Evidently). Política de actualización controlada. Canal de feedback |

### DS — Diagramas obligatorios a producir

1. Arquitectura lógica (capas)
2. Arquitectura de datos (modelo entidad-relación)
3. Diagrama de integración IRIS/VisionWeb (secuencia)
4. Diagrama de seguridad (RBAC, autenticación, cifrado)
5. Diagrama de flujo TO-BE del macroproceso
6. Diagrama del pipeline MLOps
7. Diagrama del pipeline RAG (M6)

### Derecho — Avance de secciones escritas

| Sección | Deadline borrador |
|---|---|
| 4. Análisis jurídico | Día 7 |
| 7. Modelo de gobernanza de IA | Día 7 |
| 8. Análisis sociotécnico | Día 7 |

---

## DÍAS 8–11: REDACCIÓN DEL DOCUMENTO (Jul 24–27)

### Estructura del documento final

| # | Sección | Responsable | Págs |
|---|---|---|---|
| 1 | Portada (solo letra del equipo) | Derecho | 1 |
| 2 | Índice | Derecho | 1 |
| 3 | Resumen ejecutivo | Conjunto | 1-2 |
| 4 | Análisis jurídico | **Derecho** | 6-8 |
| 5 | Análisis del macroproceso (AS-IS vs TO-BE) | Conjunto | 3-4 |
| 6 | Diseño técnico (arquitectura + M1-M8 + MLOps + seguridad) | **DS** | 6-8 |
| 7 | Modelo de gobernanza de IA | **Derecho** | 3-4 |
| 8 | Análisis sociotécnico | **Derecho** | 2-3 |
| 9 | Matriz de riesgos | Conjunto | 2-3 |
| 10 | Modelo de negocio (costos, sostenibilidad, escalamiento) | Conjunto | 2-3 |
| 11 | Bibliografía (APA 7ª ed.) | Ambos | 1-2 |
| — | **Anexo A: Minuta contractual** | **Derecho** | Ilimitado |
| — | **Anexo B: Especificaciones técnicas** | **DS** | Ilimitado |
| — | **Anexo C: Declaración de integridad y AI Disclosure** | Derecho | 1-2 |

| Día | Meta de redacción |
|---|---|
| **Día 8** | Secciones 4 (borrador final Derecho) + 6 (borrador final DS). Paralelo |
| **Día 9** | Secciones 5, 7, 8, 9. Primera integración del documento |
| **Día 10** | Sección 10. Anexos A (Derecho) y B (DS). Revisión cruzada |
| **Día 11** | Documento integrado completo. Lectura completa por todos |

---

## DÍAS 11–13: PULIDO Y ENTREGA (Jul 27–30)

| Día | Tarea |
|---|---|
| **Día 11** | Revisión de contenido: cada sección por el responsable opuesto (DS revisa secciones jurídicas, Derecho revisa secciones técnicas). Correcciones |
| **Día 12** | Pulido de formato: Arial 12, espacio sencillo, márgenes 1.5 cm, tamaño carta. APA 7ª ed. Notas al pie. Ajuste final a ≤25 págs |
| **Día 13 (Jul 30)** | Revisión final. Checklist de verificación. Conversión a PDF único. **ENTREGA antes de las 23:59** |

### Checklist de entrega

- [ ] Sin logotipos, imágenes, nombres, ni referencias a la universidad
- [ ] Solo letra del equipo en la portada
- [ ] ≤25 páginas (sin contar bibliografía ni anexos)
- [ ] APA 7ª edición en todas las citas
- [ ] Notas al pie (no al final)
- [ ] Formato correcto: Arial 12, espacio sencillo, márgenes 1.5 cm, tamaño carta
- [ ] PDF único
- [ ] Anexo contractual incluido
- [ ] Declaración de integridad y AI Disclosure firmada

---

## DÍAS 14–33: PITCH Y PREPARACIÓN ORAL (Jul 31 – Ago 18)

> **20 días para preparar la presentación oral. Entrega escrita ya está hecha.**

### Semana del 31 jul – 6 ago

| # | Tarea | Responsable |
|---|---|---|
| Definir narrativa central (storytelling tipo Shark Tank) | Conjunto |
| Estructura de la presentación (≤20 min) | Conjunto |
| Diseño de diapositivas | DS: técnicas/diagramas; Derecho: jurídicas/gobernanza |
| Banco de 30-50 posibles preguntas con respuestas | Conjunto |
| Asignación de speakers (mín. 2) | Conjunto |

### Semana del 7 – 13 ago

| # | Tarea |
|---|---|
| Primer ensayo completo con cronómetro |
| Ajustar tiempos y transiciones |
| Ensayo con simulacro de preguntas (compañeros hacen de jurado) |

### Semana del 14 – 18 ago

| # | Tarea |
|---|---|
| Ensayos diarios (mín. 1 por día) |
| Simulacro final con mentor o profesor invitado |
| Preparar logística de viaje |

### Speakers sugeridos

- **Speaker 1 (Derecho):** Contexto, problema, marco jurídico, gobernanza, derechos humanos
- **Speaker 2 (DS):** Solución técnica, arquitectura, módulos M1-M8, innovación
- **Speaker 3 (Derecho, opcional):** Modelo de negocio, sostenibilidad, escalamiento, cierre

### Logística Bogotá (19–21 ago)

- [ ] Laptop con HDMI + respaldo
- [ ] Prohibida comunicación externa durante presentación
- [ ] Vestimenta formal
- [ ] Impresión de respaldo del documento escrito

---

## CRONOGRAMA VISUAL

```
DÍA:     1  2  3  4  5  6  7  8  9  10 11 12 13 | 14        ···        33 | 19-21 Ago
         J  V  S  D  L  M  M  J  V  S  D  L  M  |                              
         17 18 19 20 21 22 23 24 25 26 27 28 29  | 30 Jul ENTREGA              
         |--|--|--|--|--|--|--|--|--|--|--|--|--|--|----------···----------|--|
INVEST.  ██|██|██|  |  |  |  |  |  |  |  |  |  |  |          ···          |  |
DISEÑO   |  |██|██|██|  |  |  |  |  |  |  |  |  |  |          ···          |  |
DS TÉC.  |  |  |██|██|██|██|██|  |  |  |  |  |  |  |          ···          |  |
REDACCIÓN|  |  |  |  |██|██|██|██|██|██|  |  |  |  |          ···          |  |
PULIDO   |  |  |  |  |  |  |  |  |  |██|██|██|  |  |          ···          |  |
ENTREGA  |  |  |  |  |  |  |  |  |  |  |  |  |██|  |          ···          |  |
PITCH    |  |  |  |  |  |  |  |  |  |  |  |  |  |████████████···████████████|  |
CONCURSO |  |  |  |  |  |  |  |  |  |  |  |  |  |  |          ···          |████|

LEYENDA: J=Jueves, V=Viernes, S=Sábado, D=Domingo, L=Lunes, M=Martes, M=Miércoles
```

---

## REUNIONES CLAVE

| Día | Reunión | Asistentes | Duración |
|---|---|---|
| **Diario** | Sync rápido de avances y bloqueos | Todos | 30 min |
| **Día 3** | Validación de D1, D2, D3, D7 con DS | Todos | 1 h |
| **Día 4** | Validación de D4, D5 con DS | Todos | 1 h |
| **Día 5** | Cierre de diseño: gobernanza, sociotécnico, riesgos, negocio | Todos | 2 h |
| **Día 8** | Revisión de borradores secciones 4, 6 | Todos | 1 h |
| **Día 10** | Revisión cruzada del documento integrado | Todos | 2 h |
| **Día 12** | Lectura final conjunta | Todos | 2 h |

---

## ENTREGABLES DE DERECHO PARA DS (RESUMEN)

| # | Entregable | Deadline | Para módulo |
|---|---|---|---|
| D1 | 4 categorías con definiciones y ejemplos | Día 2 | M2 |
| D2 | Catálogo de sub-temas | Día 2 | M2 |
| D3 | Sujetos de especial protección | Día 3 | M2 |
| D4 | Matriz de competencias | Día 4 | M3 |
| D5 | Consultas automatizables | Día 4 | M6 |
| D6 | Templates de respuesta (10-20) | Día 5 | M6 |
| D7 | Criterios de urgencia | Día 3 | M2, M6 |
| D8 | Umbral de duplicación | Día 5 | M4 |
| D9 | Roles RBAC | Día 5 | Seguridad |

---

## OBSERVACIONES IMPORTANTES

1. **Sesión de Q&A con el cliente (Art. 13):** Si aún no ha ocurrido, todos deben asistir. Preparar preguntas sobre datos, APIs, interpretación normativa.

2. **Charlas de preparación (Art. 14):** Asistir si se programan antes del 30 de julio. Si son después, igual son útiles para el pitch.

3. **Mentores:** Contactar ya mismo para tener feedback sobre borradores antes de la entrega.

4. **Anonimato:** NUNCA incluir nombres, logos ni referencias a la universidad.

5. **Declaración de IA:** Todo uso de ChatGPT/Claude/etc. debe declararse. Mentir = descalificación.

6. **Propiedad Intelectual (Art. 44):** Consultar con mentor jurídico las implicaciones.

7. **Paralelismo:** Derecho y DS trabajan en paralelo. No esperar a que uno termine para que el otro empiece. Usar las reuniones diarias para destrabar dependencias.
