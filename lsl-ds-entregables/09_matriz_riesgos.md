# 9. Matriz de riesgos (SPI, corrupción y daño antijurídico)

## ¿Qué es esta sección?

Una tabla que identifica todos los riesgos del proyecto organizados en 3 categorías, y propone medidas concretas para mitigar cada uno. Es una sección conjunta: DS escribe los riesgos técnicos, Derecho escribe los riesgos jurídicos.

**Extensión sugerida:** 2-3 páginas (compartidas).

---

## ¿Qué necesitas del equipo de Derecho?

- **Definición jurídica precisa de las 3 categorías** (SPI, corrupción, daño antijurídico) según el contexto del caso.
- **Los riesgos jurídicos** que ellos identifiquen (transparencia, debido proceso, responsabilidad, etc.).
- **Validación de que las mitigaciones técnicas** que propones cumplen con los estándares legales.

---

## Las 3 categorías explicadas (para que entiendas el contexto)

| Categoría | Significado | Ejemplo |
|---|---|---|
| **SPI** | Seguridad y Privacidad de la Información | Que se filtren datos personales de ciudadanos |
| **Corrupción** | Riesgos de integridad, manipulación indebida del sistema | Que alguien borre logs de auditoría para ocultar errores |
| **Daño antijurídico** | Que el sistema cause un perjuicio legal a un ciudadano | Que la IA clasifique mal una queja urgente y el ciudadano pierda su oportunidad procesal |

---

## Paso a paso para redactar esta sección

### Paso 1: Plantilla de la matriz

Cada riesgo se describe en una fila con esta estructura:

| Campo | Descripción |
|---|---|
| **ID** | Código único (R-001, R-002...) |
| **Categoría** | SPI / Corrupción / Daño antijurídico |
| **Riesgo** | Qué puede salir mal (frase corta) |
| **Descripción** | Explicación detallada de en qué consiste el riesgo |
| **Probabilidad** | Baja / Media / Alta |
| **Impacto** | Bajo / Medio / Alto / Crítico |
| **Causa raíz** | Por qué ocurriría |
| **Efecto** | Consecuencia si ocurre |
| **Mitigación** | Qué se hace para evitarlo o reducirlo |
| **Responsable** | Quién se encarga de la mitigación |

### Paso 2: Riesgos técnicos que aporta Ciencia de Datos (mínimo 8)

Aquí tienes los 8 riesgos técnicos ya redactados. Solo tienes que copiarlos a la matriz del documento. Los de Derecho los añade tu equipo.

---

#### R-001: Fuga de datos personales y sensibles

| Campo | Contenido |
|---|---|
| **ID** | R-001 |
| **Categoría** | SPI (Seguridad y Privacidad de la Información) |
| **Riesgo** | Acceso no autorizado o filtración de datos personales, incluyendo datos sensibles (salud, VBG, menores de edad, origen étnico) |
| **Descripción** | El sistema maneja datos clasificados como sensibles según la Ley 1581 de 2012. Una vulnerabilidad en la seguridad o un error de configuración podría exponer datos de miles de ciudadanos, incluyendo víctimas de violencia, menores de edad y poblaciones en situación de vulnerabilidad. |
| **Probabilidad** | Media |
| **Impacto** | Crítico |
| **Causa raíz** | Cifrado débil o ausente, controles de acceso mal configurados, ataque informático externo, amenaza interna (funcionario malintencionado) |
| **Efecto** | Violación de la Ley 1581/2012 de protección de datos personales. Sanciones administrativas y penales. Pérdida irreversible de confianza ciudadana en la Defensoría. Riesgo para la seguridad de personas vulnerables si sus datos quedan expuestos. |
| **Mitigación** | Cifrado AES-256 para datos en reposo. TLS 1.3 para datos en tránsito. RBAC con principio de mínimo privilegio (cada rol accede solo a lo que necesita). Logs inmutables de acceso. Auditoría de seguridad semestral. Capacitación obligatoria en protección de datos para todo el personal. |
| **Responsable** | Oficial de Seguridad de la Información + Equipo Técnico |

---

#### R-002: Sesgo algorítmico discriminatorio

| Campo | Contenido |
|---|---|
| **ID** | R-002 |
| **Categoría** | Daño antijurídico |
| **Riesgo** | El modelo de clasificación (M2) tiene un desempeño significativamente peor para ciertos grupos poblacionales, vulnerando el derecho a la igualdad |
| **Descripción** | Si el dataset de entrenamiento no representa adecuadamente a todos los grupos (mujeres, población rural, minorías étnicas, personas con bajo nivel educativo), el modelo M2 puede clasificar peor las peticiones de esos grupos. Esto equivale a una denegación de acceso a la justicia por origen o condición. |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Dataset de entrenamiento desbalanceado. Patrones lingüísticos diferentes entre grupos no capturados por el modelo. |
| **Efecto** | Ciudadanos de grupos vulnerables reciben peor servicio. Violación del derecho a la igualdad (Art. 13 Constitución). Posibles acciones de tutela contra la Defensoría. Daño reputacional. |
| **Mitigación** | Evaluación de equidad (Equal Opportunity y Demographic Parity) antes del despliegue y trimestralmente. Rebalanceo del dataset si se detecta subrepresentación. Threshold tuning por grupo si es necesario. Adversarial debiasing en el entrenamiento. Reportes públicos de equidad (transparencia algorítmica). |
| **Responsable** | Comité de IA + Equipo Técnico (MLOps) |

---

#### R-003: Clasificación errónea que cause pérdida de oportunidad procesal

| Campo | Contenido |
|---|---|
| **ID** | R-003 |
| **Categoría** | Daño antijurídico |
| **Riesgo** | El clasificador M2 asigna incorrectamente el tipo de caso (falso negativo), lo que retrasa la atención y causa que el ciudadano pierda plazos legales |
| **Descripción** | Si una queja urgente se clasifica erróneamente como "Asesoría" (rutinaria), el caso puede quedar en una cola de baja prioridad mientras el término legal para actuar vence. El ciudadano sufre un perjuicio jurídico por un error del sistema automatizado. |
| **Probabilidad** | Baja (si el modelo cumple métricas) |
| **Impacto** | Crítico |
| **Causa raíz** | Error del modelo en casos atípicos o con redacción ambigua. Datos de entrenamiento insuficientes para ciertos patrones. |
| **Efecto** | Pérdida de oportunidad procesal para el ciudadano. Responsabilidad patrimonial del Estado por falla en el servicio. Deslegitimación del sistema automatizado. |
| **Mitigación** | Human-in-the-loop: todo caso clasificado como no-urgente se revisa por un profesional en las primeras 4 horas. Tasa de falsos negativos objetivo <1%. Canal de queja para ciudadanos que consideren que su caso fue mal clasificado. Protocolo de corrección inmediata con notificación al afectado. |
| **Responsable** | Profesional URAB + Comité de IA |

---

#### R-004: Alucinación del LLM en respuesta oficial

| Campo | Contenido |
|---|---|
| **ID** | R-004 |
| **Categoría** | Daño antijurídico |
| **Riesgo** | El asistente generativo (M6 - Mistral 7B) genera información falsa o inventa normativa inexistente (alucinación) en un borrador de respuesta que, sin revisión adecuada, se envía al ciudadano |
| **Descripción** | Los modelos de lenguaje grande (LLM) pueden generar texto convincente pero falso. Si un profesional, por carga laboral o confianza excesiva en el sistema, aprueba un borrador sin revisarlo a fondo, la Defensoría podría emitir una respuesta oficial con información jurídica incorrecta o inventada. |
| **Probabilidad** | Baja (con RAG + revisión humana) |
| **Impacto** | Crítico |
| **Causa raíz** | Naturaleza probabilística de los LLM. Base de conocimiento insuficiente. Profesional que omite la revisión obligatoria. |
| **Efecto** | Respuesta oficial con información falsa. Desinformación al ciudadano. Posible responsabilidad disciplinaria y patrimonial. Pérdida de credibilidad institucional. |
| **Mitigación** | Arquitectura RAG: el LLM solo genera respuestas basadas en documentos reales recuperados de la base de conocimiento (no "de memoria"). Prompt con instrucción explícita: "NO inventes información. Si no hay base suficiente, indícalo". Revisión humana obligatoria: el profesional siempre debe aprobar explícitamente antes del envío. Log inmutable de cada prompt, respuesta generada y respuesta final. |
| **Responsable** | Profesional defensorial (revisión) + Equipo Técnico (RAG y prompt engineering) |

---

#### R-005: Manipulación de logs de auditoría

| Campo | Contenido |
|---|---|
| **ID** | R-005 |
| **Categoría** | Corrupción |
| **Riesgo** | Un actor interno con privilegios de administrador modifica o elimina registros de auditoría para ocultar errores, mala praxis o uso indebido del sistema |
| **Descripción** | Los logs de auditoría registran cada acción: quién accedió a qué caso, qué respuesta se generó, qué edición se hizo. Si estos logs pueden modificarse o borrarse, se pierde la trazabilidad y se abre la puerta a la impunidad frente a malas prácticas. |
| **Probabilidad** | Baja |
| **Impacto** | Crítico |
| **Causa raíz** | Permisos de administrador mal acotados. Logs almacenados en base de datos modificable. |
| **Efecto** | Imposibilidad de auditar el sistema. Ocultación de errores o conductas indebidas. Incumplimiento de la Directiva 007/2025 de transparencia algorítmica. |
| **Mitigación** | Logs inmutables: tablas append-only (solo se puede añadir, nunca modificar ni borrar). Separación de roles: el administrador del sistema NO tiene acceso a los logs de auditoría. Backup automático diario de logs en almacenamiento externo. Auditoría externa semestral de la integridad de los logs. |
| **Responsable** | Oficial de Cumplimiento + Auditoría Interna |

---

#### R-006: Indisponibilidad del sistema que paralice la recepción de quejas

| Campo | Contenido |
|---|---|
| **ID** | R-006 |
| **Categoría** | SPI (Seguridad y Privacidad de la Información) — Disponibilidad |
| **Riesgo** | El sistema deja de funcionar y la Defensoría no puede recibir, clasificar ni gestionar peticiones ciudadanas |
| **Descripción** | Si el sistema centralizado deja de operar por una falla técnica, ataque informático o error humano, toda la operación de recepción y gestión de peticiones se detiene. Los ciudadanos no pueden ejercer su derecho de petición por canales digitales. |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Falla de infraestructura, ataque DDoS (denegación de servicio), error de configuración, dependencia de un solo proveedor de nube |
| **Efecto** | Paralización de la recepción de quejas. Violación del derecho de petición (Art. 23 Constitución). Posible incumplimiento de términos legales de respuesta. |
| **Mitigación** | Arquitectura en alta disponibilidad (servidores redundantes). Plan de continuidad: si el sistema principal falla, las peticiones se reciben por correo electrónico y se procesan en lote cuando el sistema se recupere. SLA de disponibilidad 99.5%. Pruebas de recuperación ante desastres semestrales. |
| **Responsable** | Equipo de Infraestructura + Equipo Técnico |

---

#### R-007: Doble registro por falla de sincronización IRIS/VisionWeb

| Campo | Contenido |
|---|---|
| **ID** | R-007 |
| **Categoría** | SPI (Seguridad y Privacidad de la Información) — Integridad |
| **Riesgo** | El módulo M7 falla al sincronizar con IRIS o VisionWeb, causando que un mismo caso quede registrado en un sistema pero no en el otro, o se duplique |
| **Descripción** | Si RabbitMQ pierde un mensaje o una API de IRIS/VisionWeb rechaza la solicitud sin que el sistema lo detecte, el caso queda registrado de forma inconsistente entre los tres sistemas. |
| **Probabilidad** | Media |
| **Impacto** | Medio |
| **Causa raíz** | Fallo de red, timeout de API, error en el mapeo de campos, cambio no notificado en la API externa |
| **Efecto** | Inconsistencia entre sistemas. Retrabajo del profesional para corregir manualmente. Riesgo de pérdida de trazabilidad del expediente. |
| **Mitigación** | RabbitMQ con confirmaciones (acknowledgements): cada mensaje se confirma como entregado. Reintentos automáticos con backoff exponencial. Log de sincronización inmutable: cada intento queda registrado. Dashboard de M7 que muestra el estado de sincronización en tiempo real y alerta sobre fallos. Conciliación periódica automática (diaria) entre los tres sistemas. |
| **Responsable** | Equipo Técnico (M7) |

---

#### R-008: Uso indebido de datos agregados para fines distintos a los misionales

| Campo | Contenido |
|---|---|
| **ID** | R-008 |
| **Categoría** | Corrupción |
| **Riesgo** | Datos agregados del dashboard M8 o de la capa de investigación institucional se utilizan para propósitos no autorizados (perfilamiento político, venta de datos, vigilancia) |
| **Descripción** | Aunque M8 anonimiza los datos mediante k-anonymity, existe el riesgo de que los datos agregados sean utilizados por actores internos o externos para fines distintos a la misión de la Defensoría, como perfilamiento de poblaciones o presión política. |
| **Probabilidad** | Baja |
| **Impacto** | Alto |
| **Causa raíz** | Controles de acceso insuficientes a los datos agregados. Falta de políticas claras de uso. |
| **Efecto** | Violación de la finalidad del tratamiento de datos (Ley 1581/2012). Pérdida de confianza ciudadana. Posible uso de datos para persecución o discriminación. |
| **Mitigación** | Acceso a datos agregados solo mediante rol "investigador" con aprobación del Comité de IA. Cada consulta a la capa de investigación queda registrada en logs de auditoría. k-anonymity >= 5 (los datos se agrupan de manera que ningún grupo tenga menos de 5 individuos). Política de uso de datos agregados aprobada por el Comité de IA y publicada en el sitio web de la Defensoría. |
| **Responsable** | Comité de IA + Oficial de Protección de Datos |

---

### Paso 3: Estructura final de la sección en el documento

```
9. Matriz de riesgos (SPI, corrupción y daño antijurídico)

9.1 Definición de categorías de riesgo
    [Derecho escribe la definición jurídica de cada categoría]

9.2 Riesgos técnicos y operacionales
    [Insertar los 8 riesgos de la tabla anterior]

9.3 Riesgos jurídicos y de gobernanza
    [Derecho escribe sus riesgos: transparencia, debido proceso, 
     responsabilidad, propiedad intelectual, etc.]

9.4 Matriz consolidada de riesgos
    [Tabla resumen con los ~15-20 riesgos totales]
```

---

## Glosario de términos técnicos usados en esta sección

| Término | Explicación |
|---|---|
| **Alucinación (en IA)** | Cuando un modelo de lenguaje genera texto que suena creíble pero contiene información falsa o inventada. |
| **RAG** | Retrieval-Augmented Generation. Técnica que obliga al LLM a consultar documentos reales antes de generar una respuesta, reduciendo las alucinaciones. |
| **Log inmutable / Append-only** | Registro de auditoría donde solo se puede añadir información nueva, nunca modificar ni borrar la existente. Como escribir con tinta permanente. |
| **RBAC** | Role-Based Access Control. Cada usuario solo puede ver y hacer lo que su rol le permite. |
| **AES-256 / TLS 1.3** | Estándares de cifrado: AES protege datos guardados, TLS protege datos viajando por internet. |
| **SLA** | Acuerdo de Nivel de Servicio. Compromiso medible: "el sistema estará disponible el 99.5% del tiempo". |
| **k-anonymity** | Técnica de privacidad: agrupar datos para que ningún individuo pueda ser identificado. |
| **DDoS** | Ataque de Denegación de Servicio Distribuido. Alguien satura el sistema con miles de peticiones falsas para que los usuarios reales no puedan usarlo. |
| **Timeout** | Cuando un sistema espera respuesta de otro y esta no llega en el tiempo máximo definido. |
| **Falso negativo** | El modelo dice que NO hay problema cuando SÍ lo hay. El error más peligroso en este contexto. |
| **Dataset** | Conjunto de datos etiquetados usados para entrenar o evaluar un modelo de IA. |
