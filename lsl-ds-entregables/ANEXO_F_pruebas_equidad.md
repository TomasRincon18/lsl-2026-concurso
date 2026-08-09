# Anexo F — Pruebas de equidad: protocolo completo

> **Referenciado desde:** §8.2 del borrador principal.

---

## F.1 Principio rector

Los sistemas de inteligencia artificial, si no se diseñan y monitorean cuidadosamente, pueden reproducir e incluso amplificar sesgos presentes en los datos de entrenamiento o en la sociedad. En el contexto de la Defensoría del Pueblo, cuya misión constitucional es proteger los derechos humanos de toda la población con énfasis en los grupos más vulnerables, un sesgo algorítmico no es un error técnico: es una vulneración del derecho fundamental a la igualdad (Art. 13 CP) y una forma de discriminación indirecta que el Estado tiene la obligación de prevenir, investigar y sancionar.

Este protocolo establece el marco de pruebas de equidad que todo módulo de IA debe superar antes de ser desplegado en producción y durante toda su vida operativa. Las pruebas de equidad son un **gate de calidad obligatorio**: ningún modelo se despliega sin haberlas superado.

---

## F.2 Métricas de equidad algorítmica

### F.2.1 Definiciones

| Métrica | Definición formal | Qué mide en lenguaje sencillo | Rango | Valor ideal |
|---|---|---|---|---|
| **Equal Opportunity** (Igualdad de Oportunidad) | `|TPR_grupo_A - TPR_grupo_B|` donde TPR = VP / (VP + FN) | ¿El modelo acierta en la misma proporción cuando el caso realmente es de tipo X, sin importar el grupo? | 0 a 1 (diferencia) | 0 (sin diferencia) |
| **Demographic Parity** (Paridad Demográfica) | `|P(ŷ=1\|A) - P(ŷ=1\|B)|` donde ŷ es la predicción positiva | ¿El modelo predice la categoría X en proporciones similares entre grupos? | 0 a 1 (diferencia) | 0 (sin diferencia) — con cautela si la distribución real es diferente |
| **Disparate Impact Ratio** (Ratio de Impacto Dispar) | `min(P(ŷ=1\|A), P(ŷ=1\|B)) / max(P(ŷ=1\|A), P(ŷ=1\|B))` | ¿Qué tan grande es la brecha entre el grupo con peor resultado y el mejor? | 0 a 1 | >0.80 (regla del 80% de la EEOC) |
| **False Negative Rate por grupo** | `FN_grupo / (VP_grupo + FN_grupo)` | ¿El modelo "se equivoca por omisión" más en unos grupos que en otros? | 0 a 1 | Igual entre grupos (diferencia <5 pp) |

### F.2.2 Por qué estas métricas y no otras

- **Equal Opportunity** es la métrica prioritaria para M2 porque lo más grave en el contexto de la Defensoría es que el modelo falle en detectar correctamente el tipo de caso de una persona por su pertenencia a un grupo. Si una mujer víctima de VBG tiene menos probabilidad de que su caso se clasifique correctamente como "Queja" que un hombre en situación similar, hay un sesgo inaceptable.
- **Demographic Parity** complementa a Equal Opportunity detectando si el modelo sistemáticamente asigna ciertas categorías más a unos grupos que a otros. Se interpreta con cautela porque una diferencia puede reflejar una diferencia real en la población (ej: más quejas de salud de adultos mayores), no necesariamente un sesgo. Por eso siempre se contextualiza con la distribución real de los datos.
- **Disparate Impact Ratio** es el estándar internacional (EEOC, Unión Europea) para medir discriminación indirecta. Es un resumen en un solo número.
- **False Negative Rate por grupo** es crítico para M2 (urgencias) y M4 (duplicados): un falso negativo significa que se dejó pasar un caso urgente sin marcar, o un duplicado sin detectar.

### F.2.3 Módulos evaluados y métricas aplicables

| Módulo | Equal Opportunity | Demographic Parity | Disparate Impact | FN Rate por grupo |
|---|---|---|---|---|
| M2 — Clasificación primaria | ✅ (por tipo) | ✅ (por tipo) | ✅ | ✅ (urgencias) |
| M2 — Sub-clasificador | ✅ (por sub-tema) | — | — | ✅ (sub-temas críticos) |
| M4 — Anti-duplicación | ✅ (detección) | — | ✅ | ✅ (FN = duplicado no detectado) |
| M6 — Asistente generativo | — | — | — | ✅ (borradores rechazados por grupo) |

---

## F.3 Variables de segmentación

| Variable | Disponibilidad | Tratamiento | Tamaño mínimo de muestra |
|---|---|---|---|
| **Género** | Solo si el ciudadano lo proporciona voluntariamente en el formulario (campo opcional). Nunca se infiere. | Se reporta como "Femenino", "Masculino", "No binario/Otro", "No declarado". Si "No declarado" >50%, se advierte en el reporte. | ≥30 casos por grupo |
| **Regional / Departamento** | Dato obligatorio en el radicado. | Se agrupan regionales con <30 casos en "Otras regionales" para el reporte. | ≥30 casos por regional |
| **Grupo de especial protección** | Detectado por M2 vía indicadores textuales (D3 del equipo de Derecho). No es autodeclarado. | Grupos: NNA, mujeres VBG, personas con discapacidad, adultos mayores, desplazados, minorías étnicas, población privada de libertad, migrantes. Un caso puede pertenecer a múltiples grupos. | ≥30 casos por grupo |
| **Canal de ingreso** | Dato obligatorio (M1). | Web, email, físico, jornada de campo. | ≥30 casos por canal |
| **Sub-tema** | Asignado por M2 y validado por profesional. | Los ~12 sub-temas. Se reportan solo los que tengan ≥30 casos en el período. | ≥30 casos por sub-tema |

**Regla de significancia estadística:** si un grupo tiene menos de 30 casos en el período de medición, esa segmentación NO se reporta. Se registra internamente como "muestra insuficiente" y se acumula para el siguiente período.

---

## F.4 Niveles de alerta y protocolo de actuación

### F.4.1 Umbrales

| Nivel | Condición | Gravedad | Acción | Plazo |
|---|---|---|---|---|
| **Verde** | Diferencia <3 pp en todas las métricas y Disparate Impact >0.90 | Aceptable | Monitoreo continuo. No se requiere acción. | — |
| **Amarillo** | Diferencia 3–5 pp en alguna métrica O diferencia de precisión >5 pp entre subgrupos O Disparate Impact 0.80–0.90 | Leve | El equipo MLOps genera un informe de causas potenciales (distribución del dataset, tamaño de muestra, patrones lingüísticos). Se presenta al Comité de IA en la siguiente sesión. No se detiene el despliegue. | 30 días |
| **Naranja** | Diferencia 5–10 pp en alguna métrica O cociente de FN >1.5 entre grupos O Disparate Impact 0.70–0.80 | Moderado | Se escala al Comité de IA en máximo 5 días hábiles. Se activa el protocolo de mitigación (ver §F.5). El despliegue del módulo afectado se detiene para nuevos casos del grupo impactado. | 15 días |
| **Rojo** | Diferencia >10 pp en alguna métrica O Disparate Impact <0.70 | Grave | Se suspende inmediatamente el uso del módulo para TODAS las decisiones que afecten a cualquier grupo. Investigación urgente con dedicación exclusiva del equipo MLOps. Se notifica al Defensor Delegado. | 5 días |

### F.4.2 Ejemplo numérico de activación de alerta

**Escenario:** evaluación trimestral del clasificador M2 sobre 5.000 peticiones del piloto.

| Grupo | Casos evaluados | Accuracy M2 | TPR (recall) | FNR urgencias |
|---|---|---|---|---|
| Hombres | 2.100 | 91% | 90% | 1.2% |
| Mujeres | 1.800 | 84% | 81% | 3.5% |
| No declarado | 1.100 | 88% | 87% | 2.1% |

**Análisis:**
- Diferencia de accuracy hombres vs. mujeres = |91% - 84%| = **7 pp** → ⚠️ **Alerta NARANJA**
- Diferencia de TPR = |90% - 81%| = **9 pp** → ⚠️ **Alerta NARANJA**
- Cociente de FNR urgencias mujeres/hombres = 3.5/1.2 = **2.92** → 🔴 **Alerta ROJA** (las mujeres tienen casi 3 veces más probabilidad de que una urgencia no se detecte)

**Acción:** se suspende el uso del clasificador M2 para decisiones de urgencia que afecten a mujeres. Se inicia protocolo de mitigación inmediato (ver §F.5). Se notifica al Comité de IA en 24 horas.

---

## F.5 Estrategias de mitigación

Cuando se detecta un sesgo (nivel naranja o rojo), se aplican las siguientes estrategias en orden de prioridad:

### Estrategia 1 — Rebalanceo del dataset de entrenamiento

**Cuándo:** la causa raíz es subrepresentación del grupo afectado en los datos de entrenamiento.  
**Qué se hace:** se recolectan y etiquetan más ejemplos del grupo subrepresentado hasta alcanzar paridad. Si el grupo son "mujeres" y solo hay 300 ejemplos vs. 800 de hombres, se etiquetan 500 ejemplos adicionales de mujeres.  
**Tiempo estimado:** 1–2 semanas (dependiendo de disponibilidad de datos).  
**Verificación:** se reentrena el modelo y se repiten las pruebas de equidad. El modelo no se despliega hasta que la disparidad baje de 5 pp.

### Estrategia 2 — Threshold tuning por grupo

**Cuándo:** el modelo funciona bien en general pero el umbral de decisión no es óptimo para un grupo específico.  
**Qué se hace:** se ajusta el umbral de clasificación para el grupo afectado. Ej: si el modelo requiere 70% de confianza para clasificar como "Queja" y esto perjudica a mujeres, se baja el threshold a 60% solo para ese grupo, igualando las tasas de error.  
**Tiempo estimado:** 2–3 días (solo requiere recalibración, no reentrenamiento completo).  
**Verificación:** se mide el impacto en falsos positivos del grupo (efecto colateral aceptable si es menor al beneficio en recall). Se documenta el threshold diferenciado en la Ficha de Transparencia Algorítmica.

### Estrategia 3 — Adversarial debiasing

**Cuándo:** el sesgo es profundo y no se resuelve con rebalanceo ni threshold tuning.  
**Qué se hace:** durante el fine-tuning, se entrena simultáneamente un "adversario" que intenta predecir el grupo de pertenencia (género, región) a partir de las representaciones internas del modelo. El modelo principal recibe una penalización si el adversario acierta, obligándolo a generar representaciones que no contengan información del grupo. Es como entrenar a un evaluador para que califique exámenes sin poder distinguir la letra del estudiante.  
**Tiempo estimado:** 2–4 semanas (requiere modificar la arquitectura de entrenamiento).  
**Verificación:** se mide que el adversario no supere el 55% de accuracy (equivalente a aleatoriedad + ligero margen).

### Estrategia 4 — Revisión humana reforzada (medida de contención mientras se aplican E1–E3)

**Cuándo:** se necesita una medida inmediata mientras se implementa la solución técnica.  
**Qué se hace:** toda clasificación automática que afecte al grupo impactado pasa por doble revisión humana (dos profesionales independientes). Se registra en logs con flag de "revisión reforzada por sesgo detectado".  
**Tiempo:** inmediato (se activa en el mismo sprint).  
**Verificación:** se monitorea la tasa de corrección en la doble revisión. Si tras 4 semanas la tasa de corrección es baja (<5%), se puede reducir a revisión simple.

---

## F.6 Plan de monitoreo continuo

| Variable | Métricas | Frecuencia | Herramienta | Responsable | Reporte a |
|---|---|---|---|---|---|
| Género | EO, DP, DIR, FNR | Trimestral | Evidently AI (reporte automático) | Equipo MLOps | Comité de IA |
| Regional | Accuracy, F1, FNR | Trimestral | Evidently AI | Equipo MLOps | Comité de IA |
| Grupo de especial protección | FNR, Recall | **Mensual** (mayor frecuencia por criticidad) | Evidently AI + análisis manual de casos | Comité de IA | Defensor Delegado |
| Canal de ingreso | Accuracy, FNR | Trimestral | Evidently AI | Equipo MLOps | Comité de IA |
| Sub-tema | F1 score | Trimestral | Evidently AI | Equipo MLOps | Comité de IA |

---

## F.7 Documentación y transparencia

Cada evaluación de equidad genera un informe que incluye:

1. **Período evaluado** y volumen de datos.
2. **Distribución de la muestra** por cada variable de segmentación (con advertencia si algún grupo tiene <30 casos).
3. **Tabla de métricas** por grupo para cada métrica aplicable.
4. **Nivel de alerta resultante** (verde/amarillo/naranja/rojo) con justificación.
5. **Acciones tomadas** (si aplica): mitigación aplicada, resultados post-mitigación.
6. **Aprobación del Comité de IA** con fecha y firmas.

Estos informes son públicos (Ley 1712 de 2014, Directiva 007 de 2025) y se publican en el sitio web de la Defensoría en la sección de Transparencia Algorítmica, junto con las Fichas de cada sistema automatizado (SDA). Los datos individuales nunca se publican; solo agregados con k-anonymity ≥5.

---

## F.8 Integración con el ciclo de vida del modelo

```
NUEVO MODELO / REENTRENAMIENTO
         │
         ▼
┌─────────────────────┐
│ Entrenamiento sobre │
│ dataset etiquetado  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐     ┌──────────────────────────────┐
│ PRUEBAS DE EQUIDAD  │────▶│ ¿Disparidad <3 pp en todas   │
│ (gate obligatorio)  │     │ las métricas?                │
└─────────────────────┘     └──────────────────────────────┘
                                       │
                         ┌─────────────┼─────────────┐
                         ▼             ▼             ▼
                        SÍ       3–5 pp        >5 pp
                         │             │             │
                         ▼             ▼             ▼
                   ┌──────────┐ ┌──────────┐ ┌──────────────┐
                   │DESPLEGAR │ │MITIGAR Y │ │NO DESPLEGAR  │
                   │EN PROD   │ │REEVALUAR │ │hasta resolver│
                   └──────────┘ └──────────┘ └──────────────┘
```

**Regla inviolable:** ningún modelo se despliega en producción sin haber pasado las pruebas de equidad con nivel verde o, excepcionalmente, amarillo con plan de mitigación aprobado por el Comité de IA y fecha límite de resolución. Niveles naranja o rojo bloquean el despliegue automáticamente.
