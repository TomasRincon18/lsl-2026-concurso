# Anexo 08 — Pruebas de equidad: protocolo completo

> **Referenciado desde:** §8.2 del cuerpo del documento.

---

## 08.1 Métricas de equidad algorítmica

| Métrica | Definición formal | Qué mide | Rango | Valor ideal |
|---|---|---|---|---|
| **Equal Opportunity** | `|TPR_A - TPR_B|` donde TPR = VP/(VP+FN) | ¿El modelo acierta en la misma proporción sin importar el grupo? | 0–1 (diferencia) | 0 (sin diferencia) |
| **Demographic Parity** | `|P(ŷ=1\|A) - P(ŷ=1\|B)|` | ¿Predice la categoría X en proporciones similares entre grupos? | 0–1 (diferencia) | 0 — con cautela si la distribución real difiere |
| **Disparate Impact Ratio** | `min(P(ŷ=1\|A), P(ŷ=1\|B)) / max(...)` | ¿Qué tan grande es la brecha entre el peor y mejor grupo? | 0–1 | >0.80 (regla del 80% EEOC) |
| **False Negative Rate por grupo** | `FN_grupo / (VP_grupo + FN_grupo)` | ¿El modelo omite casos urgentes más en unos grupos que en otros? | 0–1 | Igual entre grupos (diferencia <5 pp) |

**Módulos evaluados:** M2 (clasificación primaria y urgencias, todas las métricas), M4 (anti-duplicación, EO y DIR), M6 (asistente generativo, FNR de borradores rechazados por grupo).

---

## 08.2 Variables de segmentación

| Variable | Disponibilidad | Tratamiento | Tamaño mínimo |
|---|---|---|---|
| **Género** | Solo si el ciudadano lo declara voluntariamente (campo opcional). Nunca se infiere. | "Femenino", "Masculino", "No binario/Otro", "No declarado". Si "No declarado" >50%, se advierte en el reporte. | ≥30 casos por grupo |
| **Regional / Departamento** | Dato obligatorio en el radicado | Se agrupan regionales con <30 casos en "Otras regionales". | ≥30 casos por regional |
| **Grupo de especial protección** | Detectado por M2 vía indicadores textuales (catálogo D3). No es autodeclarado. | NNA, mujeres VBG, discapacidad, adultos mayores, desplazados, minorías étnicas, PPL, migrantes. Un caso puede pertenecer a múltiples grupos. | ≥30 casos por grupo |
| **Canal de ingreso** | Dato obligatorio (M1) | Web, email, físico, jornada de campo | ≥30 casos por canal |
| **Sub-tema** | Asignado M2 + validado profesional | ~12 sub-temas. Solo se reportan los ≥30 casos en el período. | ≥30 casos por sub-tema |

---

## 08.3 Niveles de alerta y protocolo de actuación

| Nivel | Condición | Acción | Plazo |
|---|---|---|---|
| **Verde** | Diferencia <3 pp en todas las métricas Y Disparate Impact >0.90 | Monitoreo continuo. Sin acción requerida. | — |
| **Amarillo** | Diferencia 3–5 pp O diferencia de precisión >5 pp entre subgrupos O DIR 0.80–0.90 | Equipo MLOps genera informe de causas. Presentación al Comité de IA en siguiente sesión. No detiene despliegue. | 30 días |
| **Naranja** | Diferencia 5–10 pp O cociente FN >1.5 entre grupos O DIR 0.70–0.80 | Escalar al Comité de IA en 5 días hábiles. Activar protocolo de mitigación. Detener despliegue del módulo para el grupo afectado. | 15 días |
| **Rojo** | Diferencia >10 pp O DIR <0.70 | Suspender inmediatamente el módulo para TODOS los grupos. Investigación urgente con dedicación exclusiva. Notificar al Defensor Delegado. | 5 días |

**Ejemplo de activación — Escenario trimestral del piloto:**

| Grupo | Casos | Accuracy M2 | TPR | FNR urgencias |
|---|---|---|---|---|
| Hombres | 2.100 | 91% | 90% | 1.2% |
| Mujeres | 1.800 | 84% | 81% | 3.5% |
| No declarado | 1.100 | 88% | 87% | 2.1% |

Diferencia accuracy = 7 pp → Naranja. Cociente FNR = 3.5/1.2 = 2.92 → **Rojo**. Acción: suspender M2 para decisiones de urgencia en mujeres. Iniciar mitigación inmediata.

---

## 08.4 Estrategias de mitigación

**E1 — Rebalanceo del dataset.** Recolectar y etiquetar más ejemplos del grupo subrepresentado hasta paridad. Tiempo: 1–2 semanas. Verificación: reentrenar y repetir pruebas.

**E2 — Threshold tuning por grupo.** Ajustar el umbral de decisión para el grupo afectado igualando tasas de error. Tiempo: 2–3 días. Se documenta en Ficha de Transparencia.

**E3 — Adversarial debiasing.** Entrenar simultáneamente un "adversario" que intenta predecir el grupo. Penalizar al modelo principal si el adversario acierta. Tiempo: 2–4 semanas.

**E4 — Revisión humana reforzada (contención).** Doble revisión humana para el grupo impactado mientras se implementa E1–E3. Inmediato.

---

## 08.5 Monitoreo continuo

| Variable | Métricas | Frecuencia | Herramienta | Responsable | Reporte a |
|---|---|---|---|---|---|
| Género | EO, DP, DIR, FNR | Trimestral | Evidently AI | MLOps | Comité de IA |
| Regional | Accuracy, F1, FNR | Trimestral | Evidently AI | MLOps | Comité de IA |
| Grupo especial protección | FNR, Recall | **Mensual** | Evidently AI + manual | Comité de IA | Defensor Delegado |
| Canal de ingreso | Accuracy, FNR | Trimestral | Evidently AI | MLOps | Comité de IA |
| Sub-tema | F1 score | Trimestral | Evidently AI | MLOps | Comité de IA |

---

## 08.6 Gate de despliegue

```
NUEVO MODELO → PRUEBAS DE EQUIDAD → ¿Disparidad <3 pp en todas las métricas?
                                              │
                          ┌───────────────────┼───────────────────┐
                          ▼                   ▼                   ▼
                         SÍ              3–5 pp              >5 pp
                          │                   │                   │
                          ▼                   ▼                   ▼
                    DESPLEGAR           MITIGAR Y           NO DESPLEGAR
                    EN PROD             REEVALUAR           (bloqueo automático)
```

**Regla inviolable:** ningún modelo se despliega sin haber pasado pruebas de equidad con nivel verde o, excepcionalmente, amarillo con plan de mitigación aprobado por el Comité de IA y fecha límite. Naranja o rojo bloquean el despliegue automáticamente.

---

## 08.7 Transparencia

Cada evaluación genera un informe público (Ley 1712/2014, Directiva 007/2025) con: período evaluado, distribución de la muestra, métricas por grupo, nivel de alerta, acciones tomadas y aprobación del Comité de IA. Datos individuales nunca publicados; solo agregados con k-anonymity ≥5.
