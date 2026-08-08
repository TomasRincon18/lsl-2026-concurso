# PLAN DERECHO — Legal Strategy Lab 2026

## CALENDARIO REAL
- **Hoy:** 17 de julio (Dia 1)
- **Entrega escrita:** 30 de julio (Dia 13)
- **Fase oral:** 31 jul – 18 ago (20 dias)

---

## TU RESPONSABILIDAD

El peso juridico del documento recae en ustedes. Deben producir:

| Seccion | Pags |
|---|---|
| 4. Analisis juridico | 6-8 |
| 7. Modelo de gobernanza de IA | 3-4 |
| 8. Analisis sociotecnico | 2-3 |
| Anexo A: Minuta contractual | Ilimitado |
| Anexo C: Declaracion de integridad | 1-2 |
| Co-escribir: 5 (macroproceso), 9 (riesgos), 10 (negocio) | 3-5 |

**Y ENTREGAR A DS (URGENTE):** D1-D9 en los primeros 5 dias. Sin esto, DS no puede disenar los modulos.

---

## DIAS 1–2: LECTURA Y PRIMEROS ENTREGABLES (Jul 17–18)

### Lectura urgente

| Prioridad | Documento |
|---|---|
| Critica | Caso (RFP): secciones 2, 3, 5, 7, 8 |
| Critica | CONPES 4144 (2025) - Politica Nacional de IA |
| Critica | Directiva 007/2025 - Transparencia algoritmica |
| Critica | Ley 1581/2012 - Proteccion de datos personales |
| Alta | CPACA - Ley 1437/2011 - Debido proceso |
| Alta | Ley 594/2000 - Gestion documental |
| Media | Constitucion: Arts. 1, 2, 13, 23, 29, 86, 209, 229, 281-284 |

### Entregables para DS (Dia 2 - fin del dia)

| # | Entregable | Contenido |
|---|---|---|
| **D1** | 4 categorias juridicas | Definicion legal precisa de Asesoria, Queja, Solicitud de Mediacion, Solicitud de Conciliacion. Con ejemplos reales. Criterios claros para diferenciarlas |
| **D2** | Catalogo de sub-temas | ~12 sub-temas con definicion y ejemplos: salud, pensiones, prisiones, migracion, discapacidad, ninez, VBG, desaparicion, amenazas, servicios publicos, educacion, vivienda |

---

## DIA 3: SEGUNDO BLOQUE DE ENTREGABLES (Jul 19)

### Para DS (Dia 3 - fin del dia)

| # | Entregable | Contenido |
|---|---|---|
| **D3** | Sujetos de especial proteccion | Lista completa con: grupo, fundamento constitucional, obligaciones reforzadas, indicadores textuales para deteccion automatica. Grupos: NNA, mujeres VBG, personas con discapacidad, adultos mayores, desplazados, minorias etnicas, poblacion privada de libertad, migrantes |
| **D7** | Criterios de urgencia | Definicion juridica de urgencia/riesgo inminente en contexto Defensoria. Con referencias normativas. Categorias: amenaza, desaparicion forzada, riesgo de vida, ninez en peligro, VBG activa. Indicadores textuales para cada una |

### Trabajo de analisis para el documento

| # | Tarea |
|---|---|
| Mapeo norma-articulo-obligacion | Matriz para el analisis juridico. Cada norma aplicable, articulos relevantes, obligacion concreta para el sistema |
| Clasificacion de datos | Segun Ley 1581: que datos maneja el sistema y como se clasifican (publicos, semiprivados, privados, sensibles) |
| Lectura complementaria | UNESCO Ethics of AI, OECD AI Principles, OECD Governing with AI (2024), Council of Europe CETS 225 |

---

## DIA 4: TERCER BLOQUE (Jul 20)

### Para DS (Dia 4 - fin del dia)

| # | Entregable | Contenido |
|---|---|---|
| **D4** | Matriz de competencias | Tabla: (tipo + sub-tema) = entidad competente + direccion + contacto. Incluir: Defensoria (competente), Procuraduria, ICBF, MinSalud, MinTrabajo, Fiscalia, Personerias, etc. Para cada caso donde la Defensoria NO es competente, indicar la entidad correcta |
| **D5** | Catalogo de consultas automatizables | Lista taxativa y cerrada de preguntas que el sistema PUEDE responder sin intervencion humana. Ej: "Cual es mi numero de radicado?", "Quien es mi profesional asignado?", "Reenvio de constancia de radicacion", "Estado actual de mi caso". Con limites explicitos |

---

## DIA 5: ULTIMOS ENTREGABLES PARA DS + INICIO GOBERNANZA (Jul 21)

### Para DS (Dia 5 - fin del dia)

| # | Entregable | Contenido |
|---|---|---|
| **D6** | Templates de respuesta | 10-20 plantillas de respuesta institucional. En tono y formato oficial Defensoria. Para distintos escenarios: respuesta a queja de salud, respuesta a asesoria juridica, respuesta a solicitud de mediacion, respuesta con traslado por incompetencia, respuesta de cierre, respuesta de constancia. Con campos variables (nombre, radicado, fecha) |
| **D8** | Umbral de duplicacion | Criterio juridico: con que nivel de similitud textual + coincidencia de datos (CC, pretension) es razonable considerar dos peticiones como la misma? Recomendar umbral y justificarlo juridicamente (debido proceso, seguridad juridica, eficiencia administrativa) |
| **D9** | Roles RBAC | Definicion de perfiles de acceso: 1) URAB (recepcion y clasificacion inicial), 2) Profesional defensorial (gestion de casos asignados), 3) Auditor (acceso solo lectura a logs y metricas), 4) Administrador (configuracion del sistema). Que puede ver/hacer cada uno. Fundamento legal del acceso diferenciado |

### Inicio diseno de gobernanza

| Tarea |
|---|
| Definir roles y responsabilidades del modelo de gobernanza (dueno del sistema, dueno de datos, dueno misional, Comite de IA, auditoria interna) |
| Definir politicas de uso etico de IA: que puede y no puede hacer el sistema |

---

## DIAS 5–7: GOBERNANZA Y SOCIOTECNICO (Jul 21–23)

### Modelo de gobernanza de IA (seccion 7 del documento)

Respondan cada pregunta:

| Elemento | Preguntas guia |
|---|---|
| **Human-in-the-loop** | En que puntos del proceso DEBE intervenir un humano? Clasificacion? Asignacion? Respuesta? Cierre? Justificar juridicamente cada punto. Minimo: respuesta a quejas (M6), decision de acumulacion (M4), cierre del caso |
| **Explicabilidad** | Como se explica una decision automatizada al ciudadano? Y al profesional? Y al auditor? Que tecnica para cada audiencia? |
| **Gestion de incidentes** | Que pasa si la IA clasifica mal y causa perjuicio? Protocolo: deteccion, escalamiento, correccion inmediata, notificacion al afectado, medida de no repeticion |
| **Mecanismo de quejas** | Como puede un ciudadano impugnar una decision automatizada? Canal accesible (web, telefonico, presencial), plazos de respuesta, recurso |
| **Auditoria algoritmica** | Periodicidad (trimestral/semestral), responsable, alcance (sesgo, precision, cumplimiento normativo), estandares |
| **Enfoque diferencial** | Controles especificos para genero, discapacidad y juventud. Como se evita que la IA amplifique barreras o exclusiones |

### Analisis sociotecnico (seccion 8 del documento)

Respondan las 4 preguntas del caso:

1. **(i) Nuevas capacidades:** Que podran hacer los funcionarios de URAB que antes no podian? (ej: ver historial unificado en segundos, recibir borradores de respuesta, detectar duplicados automaticamente)

2. **(ii) Nuevas conductas:** Que cambiara en su forma de trabajar? (ej: pasan de clasificar manualmente a supervisar clasificacion automatica, dedican mas tiempo a casos complejos y menos a tareas repetitivas)

3. **(iii) Impactos disruptivos:** Analizar minimo estos 5:
   - Deshumanizacion de la atencion (el ciudadano interactua con un sistema, no con una persona)
   - Errores sistematicos por sesgo algoritmico (clasificacion erronea de ciertos grupos)
   - Incentivos a la sobre-automatizacion (tentacion de automatizar decisiones que requieren juicio humano)
   - Perdida de confianza ciudadana (desconfianza en decisiones asistidas por IA)
   - Barreras para poblacion vulnerable (brecha digital, idioma, discapacidad, ruralidad, analfabetismo digital)

4. **(iv) Decisiones de gobernanza:** Para cada impacto identificado en (iii), proponer una medida concreta de gobernanza que lo mitigue

---

## DIAS 7–9: REDACCIÓN SECCIONES JURIDICAS (Jul 23–25)

### Seccion 4: Analisis juridico (~7 pags)

Estructura sugerida:

1. Introduccion: la Defensoria del Pueblo y su mision constitucional
2. Marco normativo aplicable:
   - CONPES 4144 (2025): principios y lineas de accion relevantes
   - Directiva 007/2025: transparencia algoritmica y sus requisitos
   - Ley 1581/2012: proteccion de datos personales en el sistema
   - CPACA: debido proceso administrativo y decisiones automatizadas
   - Ley 594/2000: gestion documental electronica
   - Constitucion: sujetos de especial proteccion y obligaciones del Estado
3. Derechos fundamentales implicados: debido proceso, igualdad, acceso a la justicia, peticion, habeas data
4. Sujetos de especial proteccion: catalogo, fundamento y obligaciones reforzadas
5. Regulacion comparada: EU AI Act, estandares OCDE, UNESCO. Breve mencion de alineacion
6. Conclusion: viabilidad juridica de la solucion condicionada al cumplimiento de salvaguardas

### Seccion 7: Modelo de gobernanza (~3 pags)

Estructura:
1. Estructura de gobernanza: roles y responsabilidades
2. Politicas de uso etico de IA
3. Puntos de human-in-the-loop
4. Mecanismos de explicabilidad
5. Gestion de incidentes algoritmicos
6. Mecanismo de quejas y correccion
7. Auditoria algoritmica
8. Enfoque diferencial: controles especificos

### Seccion 8: Analisis sociotecnico (~2 pags)

Estructura: las 4 preguntas del caso, una sub-seccion por pregunta.

---

## DIAS 9–11: ANEXO CONTRACTUAL (Jul 25–27)

### Minuta del contrato (Anexo A)

Clausulas minimas:

| Clausula | Contenido |
|---|---|
| 1. Partes | Defensoria del Pueblo (contratante) y [nombre del proveedor] (contratista) |
| 2. Objeto | Diseno, desarrollo, implementacion, capacitacion y soporte de solucion integrada de IA |
| 3. Alcance | Modulos M1-M8, fases 0-4, entregables descritos en el caso |
| 4. Obligaciones del contratista | Desarrollo, integracion IRIS/VisionWeb, capacitacion (min. 20 profesionales), soporte 3 anos, cumplimiento normativo, auditoria |
| 5. Obligaciones de la Defensoria | Acceso a datos, infraestructura, personal para capacitacion, contrapartes tecnicas |
| 6. Propiedad intelectual | Alineado con Art. 44 del Reglamento. Considerar licencia de uso vs cesion |
| 7. Proteccion de datos | Clausula de cumplimiento Ley 1581/2012. Deber de confidencialidad. Medidas de seguridad. Prohibicion de uso de datos para fines distintos |
| 8. Niveles de servicio (SLAs) | Disponibilidad 99.5%, precision de clasificacion mayor a 85%, tiempo de respuesta de API menor a 500ms p95, falso positivo en duplicacion menor a 5% |
| 9. Responsabilidad | Limites por decisiones automatizadas. Indemnidad. El profesional siempre tiene la decision final vinculante |
| 10. Auditoria | Derecho de la Defensoria a auditar codigo, modelos, datos. Periodicidad semestral |
| 11. Vigencia | 3 anos con posibilidad de prorroga por periodos iguales |
| 12. Precio y forma de pago | Coherente con modelo de costos de seccion 10. Hitos de pago por fase |
| 13. Terminacion | Causales, liquidacion, deber de transferencia de conocimiento, modelos y datos |
| 14. Solucion de controversias | Conciliacion, arbitraje, jurisdiccion contencioso-administrativa |

---

## DIAS 11–13: REVISION Y ENTREGA (Jul 27–30)

- Revisar coherencia entre seccion juridica y seccion tecnica (DS)
- Verificar que cada requisito normativo de la seccion 4 tenga su traduccion en diseno tecnico (seccion 6) o gobernanza (seccion 7)
- APA 7a ed. en todas las citas juridicas
- Notas al pie, no al final
- Declaracion de integridad y AI Disclosure (Anexo C): lean bien el Anexo 4 del Reglamento. Declaren TODO uso de IA

---

## DIAS 14–33: PITCH (Jul 31 – Ago 18)

### Su rol en la presentacion oral

- **Speaker 1 (Derecho):** Apertura. Contexto del problema. Marco juridico. Gobernanza. Derechos humanos. (7-8 min)
- **Speaker 3 (opcional, Derecho):** Cierre. Modelo de negocio. Sostenibilidad. Escalamiento. (3-4 min)
- **Manejo de preguntas:** 30 puntos de 100 dependen de conocimiento juridico (20) y manejo de preguntas (10). Preparar minimo estas:

### Banco de preguntas a ensayar

1. Como garantizan el debido proceso si una IA clasifica mal una queja?
2. Que pasa si el sistema muestra sesgo contra cierto grupo poblacional?
3. Es constitucional que una IA asista decisiones que afectan derechos fundamentales?
4. Como se cumple la Ley 1581/2012 con datos sensibles (salud, VBG, ninez)?
5. Como impugna un ciudadano una decision automatizada?
6. Quien responde juridicamente si el sistema causa un dano antijuridico?
7. Como se audita que no haya sesgos algoritmicos?
8. Es necesario el consentimiento del ciudadano para procesar su queja con IA?
9. Como se preserva la cadena de custodia del expediente electronico?
10. Que pasa si IRIS o VisionWeb estan caidos? Hay plan de contingencia?
11. Como se alinea la propuesta con la Directiva 007/2025 de transparencia?
12. Que medidas concretas hay para el enfoque diferencial de genero y discapacidad?
13. La solucion cumple con los estandares de la OECD y UNESCO en etica de IA?
14. Como se evita la sobre-automatizacion y deshumanizacion?
15. Que pasa con los ciudadanos sin acceso a internet o en zonas rurales?

---

## CALENDARIO VISUAL DERECHO

```
DIA:  1  2  3  4  5  6  7  8  9  10 11 12 13
      J  V  S  D  L  M  M  J  V  S  D  L  M
      |--|--|--|--|--|--|--|--|--|--|--|--|--|
LECT. ██|██|  |  |  |  |  |  |  |  |  |  |  |
D1-D2 ██|██|  |  |  |  |  |  |  |  |  |  |  |
D3,D7 |  |  |██|  |  |  |  |  |  |  |  |  |  |
D4,D5 |  |  |  |██|  |  |  |  |  |  |  |  |  |
D6,D8 |  |  |  |  |██|  |  |  |  |  |  |  |  |
D9    |  |  |  |  |██|  |  |  |  |  |  |  |  |
GOBERN|  |  |  |  |  |██|██|  |  |  |  |  |  |
REDACC|  |  |  |  |  |  |██|██|██|  |  |  |  |
CONTR. |  |  |  |  |  |  |  |  |██|██|██|  |  |
PULIDO |  |  |  |  |  |  |  |  |  |  |██|██|  |
ENTREGA|  |  |  |  |  |  |  |  |  |  |  |  |██|
```

---

## PUNTOS DE COLABORACION CON DS

| Dia | Actividad | Duracion |
|---|---|---|
| Dia 2 | Validar D1 y D2 con DS | 30 min |
| Dia 3 | Validar D3 y D7 con DS | 30 min |
| Dia 4 | Validar D4 y D5 con DS | 30 min |
| Dia 5 | Cierre de todos los D1-D9. Diseno conjunto de gobernanza, sociotecnico, riesgos y negocio | 2 h |
| Dia 8 | Revision cruzada: DS revisa seccion juridica (4, 7, 8), Derecho revisa seccion tecnica (6) | 1 h |
| Dia 10 | Integracion del documento. Revision conjunta de coherencia juridico-tecnica | 2 h |
| Dia 12 | Lectura final conjunta del documento completo | 2 h |
