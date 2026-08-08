# Borrador — Marco jurídico, decisiones de cumplimiento y Contrato (Equipo J)

> Complementa `borrador_secciones_tecnicas.md`. Corresponde a las secciones "Marco jurídico y decisiones de cumplimiento" y "Contrato" del Escrito 1, redactado en paralelo al cuerpo técnico conforme al Artículo 22 del Reglamento. Celdas `[validar]` pendientes de mentoría.

---

## 1. Marco jurídico y decisiones de cumplimiento

### 1.1 Decisión de modalidad contractual (Q3 del Banco)
- **Tipología:** contrato estatal de **prestación de servicios y desarrollo tecnológico con IA, de carácter integral** (diseño, construcción, operación y gobernanza del piloto URAB). Coherente con la estadística SECOP construida en §5.1 del borrador técnico: **736 de 909 contratos de IA en el Estado (≈81%) son de prestación de servicios** y **672 (73%) se celebraron por Contratación Directa**.
- **Causal de contratación directa:** desarrollo de actividades de tecnología/IA — es la vía efectivamente usada por las entidades para este objeto en el mercado colombiano `[validar numeral aplicable de la Ley 80 de 1993]`. Alternativa evaluada: régimen especial por convenios con universidades (98 contratos en la base).
- **Fundamento:** la libertad confirmada en Q3 (prestación de servicios, desarrollo, licenciamiento o mixto) se cierra en un **modelo mixto**: (i) servicios de implementación por fases (§6 del caso), (ii) licenciamiento de la plataforma NLP/RPA y (iii) suscripción de soporte y evolución — estructura que reproduce exactamente la línea de costos de §7.2 ya costeada en §5.2 del borrador técnico.

### 1.2 Alcance, presupuesto y ejecución
- Contratación **por etapas (Fase 0 a Fase 4)** con entregables verificables y **pagos por hitos** (no por tiempo), ligados a los criterios de aceptación de la sección 6 del caso y al cronograma de 32 semanas del borrador técnico (§5.0).
- **Vigencia sugerida: 36 meses** (diseño, construcción, operación y evolución del modelo a tres años de §5.2).
- **Presupuesto:** como aclara §7.2, no se exige el presupuesto oficial de la entidad sino un modelo con **consistencia y trazabilidad**. Se presenta el modelo a 3 años (≈ **$1.125 M COP**, p95 de mercado) y un **evento de cotización** en la Fase 0 para validar los supuestos unitarios antes de la firma del contrato.

### 1.3 Mapa del marco de alineación mínima (§5.1) → componente del sistema
| Norma / insumo | Componente del sistema que la activa | Decisión de cumplimiento en el escrito |
|---|---|---|
| **CONPES 4144 de 2025** (Política Nacional de IA) | Arquitectura (§2 borrador), decisión nube/on-prem | Soberanía de datos: supuesto de infraestructura explícito (Q7): cómputo en GovCloud del MinTIC **o** on-prem, con el costo total reflejado en §5.2 (la línea de infraestructura de $70 M ya contempla la opción on-prem). |
| **Directiva Conjunta 007 de 2025** (transparencia algorítmica) | M2 (triage), M4 (deduplicación) — SAD; M6 | **Ficha de Transparencia Algorítmica** de diseño propio, alineada a la Directiva y a **NIST AI RMF 1.0** (Q9) — se entrega como Anexo F. |
| **Régimen de protección de datos** (Ley 1581 de 2012, Decreto 1377 de 2013) | Todo tratamiento de datos personales y sensibles | Calificación de roles: Defensoría = **responsable**, proveedor = **encargado** con instrucciones documentadas. Régimen reforzado de datos sensibles activado: las peticiones versan mayormente sobre **salud**; las alertas de M6 cubren niñez, discapacidad, VBG, amenazas y desaparición. |
| **Debido proceso y términos** (Const. arts. 15 y 23; Ley 1755 de 2015; CPACA) | M2, M3, M6 | El debido proceso impone que **ninguna decisión de fondo se automatice**; el art. 23 exige términos → las métricas de tiempo (§6) y la prohibición de respuesta íntegramente automatizada. |
| **Gestión documental y conservación** (Ley 594 de 2000 – AGN) | M8, capa de auditoría, integración IRIS/VisionWeb | El requisito mínimo de Q8 es la **consistencia de estados** IRIS/VisionWeb; se ofrece como diferenciador la **foliación electrónica con firma de índice digital** bajo estándares AGN (costeada en la línea de evolución de §5.2). |
| **Ley 1712 de 2014** (transparencia y acceso a la información) | Fichas de Transparencia, Fase 4 | Publicación de la Ficha de cada sistema automatizado y del modelo de rendición de cuentas. |

### 1.4 Decisiones que nunca se automatizan (supervisión humana significativa §5.4)
| Decisión | Módulo | Mecanismo |
|---|---|---|
| Evaluación de **competencia** de la entidad para conocer | M3 | decisión humana; la IA solo sugiere direccionamiento |
| **Priorización de casos de riesgo vital** (desapariciones, amenazas, niñez) | M6 | alerta automática, pero la prioridad la decide el funcionario; umbral asimétrico §6.2 del borrador |
| **Respuesta de fondo al peticionario** | M6 (solo redacta borrador) | revisión y firma humana |
| Corrección de errores de deduplicación y decisiones de archivo | M4 | revisión humana; rutas de queja y corrección §5.4 |

### 1.5 Tratamiento de datos — contenido mínimo de la cláusula
- Finalidad determinada y legítima: misión constitucional de la Defensoría (CP arts. 15, 86 y 282); **sin usos secundarios**.
- Encargo al proveedor con instrucciones documentadas, prohibición de tratamientos posteriores y medidas de minimización.
- Derechos de los titulares (hábeas data): acceso, rectificación, supresión y revocatoria, canalizados a través de la URAB.
- Notificación de brechas de seguridad conforme al régimen de la Superintendencia de Industria y Comercio.
- Evaluación de impacto en la protección de datos (salud, niñez, VBG, desaparición), integrada al plan de pruebas de equidad (§4 del borrador).

---

## 2. Contrato (anexo del Escrito 1 — Art. 22 del Reglamento)

Borrador de cláusulas del **CONTRATO DE PRESTACIÓN DE SERVICIOS, DESARROLLO TECNOLÓGICO Y LICENCIAMIENTO CON COMPONENTE DE IA** entre la **DEFENSORÍA DEL PUEBLO** (Responsable/Contratante) y **[PROVEEDOR]** (Encargado/Contratista). Cumple los mínimos exigidos por Q6 y el Caso §7.1.

### 2.1 Cláusulas propuestas

1. **Partes y naturaleza.** Defensoría del Pueblo (contratante, responsable del tratamiento) y [PROVEEDOR] (contratista, encargado). Contrato estatal integral de tecnología con IA, celebrado por contratación directa.
2. **Objeto y alcance por fases.** Corresponden a las fases F0–F4 del borrador técnico (§5.0): diagnóstico y alistamiento; diseño de arquitectura e integración; construcción y pruebas de los módulos M1–M8; despliegue del piloto URAB; y gobernanza, operación y evolución. El alcance del piloto se limita a URAB; el escalamiento se pacta mediante anexo.
3. **Entregables y criterios de aceptación.** Remisión a la tabla de entregables verificables por fase, cada una con criterios de aceptación y métricas de desempeño (§6 del caso; §6 del borrador).
4. **Niveles de servicio (SLA) verificables, ligados a §4.4.** Clasificación sugerida ≤15 min en 90% (p90); recall de urgencias ≥99% (falso negativo ≈ 0); deduplicación con FP ≤15% y FN ≤10%; reducción de reprocesos ≥50%. SLA de plataforma: disponibilidad 99,5% mensual, copia de seguridad diaria con RPO/RTO definidos en el Anexo técnico. Incumplimiento: causales de descuento, suspensión y terminación.
5. **Tratamiento de datos personales.** Encargo expreso (Ley 1581/2012, Decreto 1377/2013), finalidad, prohibición de usos secundarios, medidas de seguridad, derechos de los titulares y notificación de incidentes — según §1.5.
6. **Propiedad intelectual.** Los desarrollos a medida, modelos entrenados (M2, M4, M5, M6), scripts y configuraciones se entregan a la Entidad con licenciamiento perpetuo e irrevocable; los datos y registros son de la Entidad. La plataforma NLP/RPA permanece en licencia comercial (suscripción), consistente con la separación "implementación vs. licencias" de §5.2.
7. **Seguridad de la información y continuidad.** Controles de §4.5: acceso por roles, cifrado en tránsito y reposo, registro de actividad, contingencia ante indisponibilidad de IRIS/VisionWeb, esquema de respaldo. La opción GovCloud/on-prem se fija como supuesto de infraestructura y es auditable.
8. **Gobernanza y auditoría (§5.4).** Comité de IA de la Entidad, con propietario del sistema, dueño de datos y responsable misional definidos. Derecho de auditoría técnica de la Entidad sobre logs, Fichas de Transparencia y resultados de pruebas de equidad (§4 del borrador); auditoría periódica del proveedor.
9. **Gestión de incidentes.** Protocolo de detección y escalamiento por severidad (P1–P4), tiempos de mitigación, registro y análisis posterior; notificación al comité de IA.
10. **Régimen de responsabilidad.** Responsabilidad contractual y extracontractual por daño antijurídico (CP art. 90 y régimen contencioso administrativo). El proveedor asume indemnidad frente a reclamaciones derivadas de defectos técnicos de los módulos, sin trasladar a la IA decisiones misionales que siempre conserva la Entidad.
11. **Garantías.** De seriedad de la oferta; de cumplimiento (10% del valor); de calidad del servicio; y de estabilidad de los desarrollos, con vigencia acorde a las fases.
12. **Pagos por hitos y estructura financiera.** Remisión a la tabla anual de §5.2 del borrador (Año 1 ≈ $733 M, con 55% de implementación; Años 2 y 3 ≈ $196 M cada uno; total ≈ $1.125 M). Pago contra recibo a satisfacción y certificación de cumplimiento.
13. **Terminación.** Mutuo acuerdo, incumplimiento previo requerimiento, fuerza mayor, infracción del régimen de protección de datos y causales de la Ley 80 de 1993. Se pacta además la posibilidad de redefinir el alcance si el diagnóstico de la Fase 0 lo exige.
14. **Solución de controversias.** Conciliación previa y cláusula compromisoria (tribunal de arbitraje) o jurisdicción de lo contencioso administrativo, conforme al manual de contratación de la Entidad `[validar]`.

### 2.2 Fuentes
Banco de preguntas oficial (Q3, Q6, Q7, Q8, Q9); Caso §5.1–§5.5, §6 y §7.1–§7.2; Reglamento art. 22; análisis SECOP (§5.1 borrador técnico). Cláusulas redactadas en paralelo al cuerpo técnico, como exige el Artículo 22.

---

*Borrador inicial para revisión con la mentoría. Las marcas `[validar]` señalan puntos que deben confirmarse antes de la entrega.*
