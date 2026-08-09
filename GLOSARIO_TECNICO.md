# Glosario de términos y abreviaturas técnicas

> Referencia para el equipo de Derecho al leer el documento de especificaciones técnicas (DS_CUERPO.md).
> Las definiciones están pensadas para lectores sin formación técnica previa.

---

## Modelos e inteligencia artificial

| Término | Definición |
|---|---|
| **IA** | Inteligencia Artificial. Sistemas que realizan tareas que normalmente requieren inteligencia humana. |
| **LLM** | Large Language Model (Modelo de Lenguaje Grande). Tipo de IA entrenada con cantidades masivas de texto, capaz de entender y generar lenguaje natural. Ej: Mistral 7B, GPT-4. |
| **NLP** | Natural Language Processing (Procesamiento de Lenguaje Natural). Rama de la IA que se ocupa de que las máquinas entiendan texto humano. |
| **BETO** | Modelo de lenguaje en español entrenado por la Universidad de Chile (similar a BERT pero en español). Se usa para clasificar textos. |
| **Mistral 7B** | Modelo de lenguaje de código abierto con 7 mil millones de parámetros, desarrollado por Mistral AI. Se usa para generar borradores de respuesta. |
| **Fine-tuning** | Proceso de tomar un modelo de IA que ya sabe español (pre-entrenado) y enseñarle una tarea específica con ejemplos etiquetados. Similar a especializar a un médico general en dermatología. |
| **WWM** | Whole Word Masking. Técnica de entrenamiento donde el modelo aprende palabras completas, no fragmentos. Mejora la comprensión del lenguaje. |
| **Modelo fundacional** | Modelo de IA base entrenado por terceros (universidades, empresas) que se puede adaptar a tareas específicas mediante fine-tuning. |

---

## Técnicas de procesamiento de texto

| Término | Definición |
|---|---|
| **NER** | Named Entity Recognition (Reconocimiento de Entidades Nombradas). Técnica que extrae automáticamente datos estructurados de un texto libre: nombres, números de cédula, direcciones, fechas. |
| **OCR** | Optical Character Recognition (Reconocimiento Óptico de Caracteres). Tecnología que convierte una imagen o un PDF escaneado en texto que la computadora puede leer y procesar. |
| **CER** | Character Error Rate (Tasa de Error de Caracteres). Porcentaje de letras mal reconocidas por el OCR. Un CER <5% significa que de cada 100 caracteres, menos de 5 se leyeron mal. |
| **RAG** | Retrieval-Augmented Generation (Generación Aumentada por Recuperación). Técnica que hace que la IA primero busque información en documentos reales (leyes, sentencias) y luego genere una respuesta basada en lo que encontró, en vez de inventar. |
| **Embedding** | Representación numérica de un texto. Convierte una oración en una lista de ~768 números que capturan su significado. Permite comparar matemáticamente si dos textos dicen lo mismo aunque usen palabras distintas. |
| **Cosine similarity** | Medida matemática (0 a 1) que indica qué tan parecidos son dos textos comparando sus embeddings. 1 = idénticos, 0 = completamente distintos. |
| **Prompt** | Instrucción en lenguaje natural que se le da al LLM para guiar su respuesta. Ej: "Redacta un borrador de respuesta usando lenguaje ciudadano. No inventes información." |
| **Alucinación** | Fenómeno donde un LLM genera información que suena creíble pero es falsa (ej: citar una ley que no existe). El RAG y la revisión humana son las defensas contra esto. |
| **Threshold** | Umbral de decisión. El punto de corte que determina una clasificación. Ej: si el modelo tiene 60% de confianza en que algo es urgente y el threshold es 50%, lo marca como urgente. |

---

## Infraestructura y computación

| Término | Definición |
|---|---|
| **Cloud / Nube** | Infraestructura de cómputo (servidores, almacenamiento, redes) alquilada a un proveedor externo, accesible por internet. Elimina la necesidad de comprar y mantener servidores físicos. |
| **IaaS** | Infrastructure as a Service (Infraestructura como Servicio). Modalidad de nube donde se alquilan servidores virtuales, almacenamiento y redes. |
| **PaaS** | Platform as a Service (Plataforma como Servicio). Modalidad de nube que incluye, además de infraestructura, herramientas de desarrollo y bases de datos gestionadas. |
| **vCPU** | CPU virtual. Unidad de procesamiento asignada por el proveedor cloud. Equivale aproximadamente a un núcleo de procesador físico. |
| **GPU** | Graphics Processing Unit (Unidad de Procesamiento Gráfico). Procesador especializado, originalmente para videojuegos, que resulta mucho más rápido que una CPU para entrenar y ejecutar modelos de IA. |
| **T4** | Modelo específico de GPU de NVIDIA, optimizado para inferencia de IA. 16 GB de memoria. |
| **HA** | High Availability (Alta Disponibilidad). Configuración donde hay al menos dos servidores idénticos; si uno falla, el otro toma el control sin interrupción del servicio. |
| **Auto-scaling** | Capacidad de la nube de añadir o quitar recursos automáticamente según la demanda. Si llegan más peticiones, se activan más servidores; si baja la carga, se apagan. |

---

## Métricas y rendimiento

| Término | Definición |
|---|---|
| **Accuracy** | Porcentaje de aciertos del modelo. Si clasificó 100 peticiones y acertó en 85, accuracy = 85%. |
| **Precision** | Del total de casos que el modelo marcó como "X", qué porcentaje realmente eran "X". Mide qué tan confiable es cuando afirma algo. |
| **Recall / Sensibilidad** | Del total de casos que realmente son "X", qué porcentaje detectó el modelo. Mide qué tan bueno es encontrando cosas. |
| **F1 Score** | Promedio entre precision y recall. Un solo número (0 a 1) para evaluar el modelo. |
| **FN / Falso Negativo** | El modelo dice que NO hay problema, pero SÍ lo hay. Es el error más peligroso: dejar pasar un caso urgente sin marcarlo. |
| **FP / Falso Positivo** | El modelo dice que SÍ hay problema, pero NO lo hay. Genera una revisión innecesaria pero no causa daño directo. |
| **FNR** | False Negative Rate (Tasa de Falsos Negativos). Porcentaje de casos reales que el modelo no detectó. |
| **p90 / p95** | Percentil 90 o 95. "El 90% (o 95%) de los casos cumple esta métrica". Más realista que el promedio, que puede ser engañoso con valores extremos. Ej: "≤4h en p90" significa que 9 de cada 10 peticiones se asignan en 4 horas o menos. |
| **Recall urgencias** | Porcentaje de casos verdaderamente urgentes que el sistema marcó correctamente como urgentes. Objetivo: ≥99%. |
| **Umbral asimétrico** | Estrategia de calibración donde se prioriza no omitir ningún caso grave (maximizar recall) a costa de generar más falsas alarmas (falsos positivos), porque el costo de omitir un riesgo vital es infinitamente mayor que el de revisar un caso de más. |

---

## Equidad algorítmica

| Término | Definición |
|---|---|
| **Equal Opportunity** | Métrica de equidad: mide si el modelo acierta en la misma proporción para todos los grupos. Si acierta el 90% de quejas de hombres pero solo el 70% de mujeres, hay un sesgo. |
| **Demographic Parity** | Métrica de equidad: mide si el modelo asigna categorías en proporciones similares entre grupos. |
| **Disparate Impact Ratio** | Cociente entre el rendimiento del grupo con peores resultados y el del grupo con mejores resultados. Debe ser >0.80. Por debajo de ese valor se considera que hay impacto desproporcionado. |
| **k-anonymity** | Técnica de privacidad que agrupa datos para que ningún individuo pueda ser identificado. k=5 significa que cualquier estadística publicada agrupa al menos a 5 personas. |
| **Adversarial debiasing** | Técnica de entrenamiento donde se obliga al modelo a clasificar correctamente sin poder distinguir a qué grupo (género, origen) pertenece la persona. |
| **Threshold tuning** | Ajuste del umbral de decisión por grupo para igualar las tasas de error. Ej: bajar el threshold para mujeres si el modelo es más conservador con ese grupo. |

---

## Operaciones y MLOps

| Término | Definición |
|---|---|
| **MLOps** | Machine Learning Operations. Conjunto de prácticas para mantener modelos de IA funcionando bien en producción: versionarlos, monitorearlos, detectar cuándo se degradan y reentrenarlos. |
| **DVC** | Data Version Control. Herramienta que versiona conjuntos de datos etiquetados, como Git versiona código. Permite saber exactamente con qué datos se entrenó cada modelo. |
| **MLflow** | Plataforma para gestionar el ciclo de vida de modelos de IA: registrar experimentos, versionar modelos y desplegarlos. |
| **Evidently AI** | Herramienta que monitorea modelos en producción: detecta si los datos cambiaron (drift), si el rendimiento bajó, y genera reportes automáticos de equidad. |
| **Drift** | Degradación del rendimiento de un modelo con el tiempo porque los datos del mundo real cambiaron. Como un mapa que se vuelve obsoleto porque construyeron nuevas calles. |
| **Feedback loop** | Canal donde los profesionales reportan errores del sistema. Esos datos etiquetados por humanos se usan para reentrenar y mejorar el modelo. |
| **Conjunto gold** | Muestra de datos etiquetados manualmente por expertos (en este caso, juristas de la URAB) que sirve como referencia de máxima calidad para entrenar y evaluar modelos. |
| **Dataset** | Conjunto de datos etiquetados usados para entrenar o evaluar un modelo de IA. |

---

## Seguridad

| Término | Definición |
|---|---|
| **RBAC** | Role-Based Access Control (Control de Acceso Basado en Roles). Sistema de permisos donde cada tipo de usuario ve y hace solo lo que su rol le permite. |
| **OAuth2** | Estándar de autenticación que permite verificar la identidad de un usuario sin que el sistema tenga que guardar su contraseña. |
| **JWT** | JSON Web Token. Un "carnet digital" cifrado que demuestra la identidad del usuario. No requiere mantener sesiones en el servidor. |
| **TLS 1.3** | Transport Layer Security versión 1.3. Tecnología que cifra los datos mientras viajan por internet. Es lo que activa el candado en el navegador (HTTPS). |
| **AES-256** | Advanced Encryption Standard de 256 bits. Estándar de cifrado que protege datos almacenados (en discos, bases de datos). Convierte la información en texto ilegible sin la clave correcta. |
| **WAF** | Web Application Firewall. Sistema que protege las aplicaciones web de ataques comunes (inyección de código, tráfico malicioso). |
| **DDoS** | Distributed Denial of Service (Denegación de Servicio Distribuida). Ataque que satura un sistema con miles de peticiones falsas para que los usuarios reales no puedan usarlo. |
| **Pentesting** | Pruebas de penetración. Simulación controlada de un ataque informático para detectar vulnerabilidades antes de que lo haga un atacante real. |
| **Red teaming** | Ejercicio donde un equipo independiente simula ser un atacante real para probar las defensas de la organización. |
| **Append-only** | Modo de almacenamiento donde solo se puede añadir información nueva, nunca modificar ni borrar la existente. Garantiza que los registros de auditoría no puedan ser alterados. |
| **Responsabilidad compartida** | Modelo de seguridad cloud donde el proveedor garantiza la seguridad física y de red, y el contratista garantiza la seguridad de la aplicación y los datos. |
| **AIA** | Evaluación de Impacto Algorítmico. Análisis de los riesgos que un sistema automatizado puede tener sobre los derechos de las personas. |

---

## Disponibilidad y continuidad

| Término | Definición |
|---|---|
| **SLA** | Service Level Agreement (Acuerdo de Nivel de Servicio). Compromiso medible de calidad. Ej: "el sistema estará disponible el 99.5% del tiempo" (máximo ~43 horas de caída al año). |
| **RPO** | Recovery Point Objective (Objetivo de Punto de Recuperación). Cantidad máxima de datos que se acepta perder ante un desastre. RPO ≤24h significa que los backups se hacen cada 24 horas; en el peor caso se pierde un día de datos. |
| **RTO** | Recovery Time Objective (Objetivo de Tiempo de Recuperación). Tiempo máximo para restaurar el servicio tras una caída. RTO ≤4h significa que el sistema debe volver a funcionar en 4 horas o menos. |

---

## Integración y sistemas

| Término | Definición |
|---|---|
| **API** | Application Programming Interface (Interfaz de Programación de Aplicaciones). Conjunto de reglas que permite que dos sistemas se comuniquen entre sí. Como un mesero: lleva tu pedido a la cocina y te trae la respuesta. |
| **REST** | Estilo de arquitectura para APIs que usa HTTP (el protocolo de la web). |
| **OpenAPI 3.0** | Estándar para documentar APIs de forma que cualquier desarrollador entienda cómo usarlas. |
| **RabbitMQ** | Software de mensajería que garantiza que los mensajes entre sistemas se entreguen, incluso si el destinatario está temporalmente caído. |
| **ACK** | Acknowledgment (Acuse de recibo). Confirmación de que un mensaje fue recibido y procesado correctamente. |
| **DLQ** | Dead Letter Queue (Cola de Mensajes No Entregados). Cola donde van los mensajes que no pudieron entregarse tras varios intentos, para que un operador los revise. |
| **Backoff exponencial** | Estrategia de reintentos donde el tiempo de espera entre intentos crece progresivamente (1s, 2s, 4s, 8s...). Evita saturar el sistema destino. |
| **RPA** | Robotic Process Automation (Automatización Robótica de Procesos). Software que imita las acciones de un humano en la interfaz de otro sistema (hacer clics, copiar y pegar, llenar formularios). Se usa como último recurso cuando no existe API. |
| **ETL/ELT** | Extract, Transform, Load. Procesos de integración de datos: extraer de un sistema, transformar al formato destino y cargar en el otro sistema. |

---

## Bases de datos y almacenamiento

| Término | Definición |
|---|---|
| **PostgreSQL** | Sistema de base de datos relacional de código abierto, estándar en el sector público colombiano. |
| **pgvector** | Extensión de PostgreSQL que permite almacenar y buscar vectores (embeddings) en la misma base de datos, sin necesidad de un sistema separado. |
| **Elasticsearch** | Motor de búsqueda textual que permite encontrar documentos por palabras clave, filtrar por múltiples criterios y generar estadísticas en milisegundos. |
| **ChromaDB** | Base de datos especializada en almacenar embeddings (vectores semánticos) y buscar los más parecidos a una consulta. Es ligera y no requiere servidor aparte. |
| **ACID** | Propiedades que garantizan que las transacciones en una base de datos sean confiables: Atomicidad, Consistencia, Aislamiento y Durabilidad. |
| **SSD** | Solid State Drive (Unidad de Estado Sólido). Tipo de disco de almacenamiento mucho más rápido que los discos tradicionales. |

---

## Herramientas y frameworks

| Término | Definición |
|---|---|
| **FastAPI** | Framework para crear APIs en Python. Es rápido, genera documentación automática y está optimizado para tareas concurrentes. |
| **spaCy** | Biblioteca de procesamiento de lenguaje natural para Python, optimizada para velocidad y uso en producción. |
| **Sentence-Transformers** | Biblioteca que convierte textos en embeddings (vectores numéricos) para comparar significados. |
| **LangChain** | Framework que facilita construir aplicaciones con LLMs, especialmente las que usan RAG. |
| **Tesseract** | Motor de OCR de código abierto mantenido por Google. El modelo `spa` está entrenado específicamente para español. |
| **OpenCV** | Biblioteca de procesamiento de imágenes usada para mejorar la calidad de documentos escaneados antes de pasarlos al OCR. |
| **Streamlit** | Herramienta para crear dashboards y aplicaciones web de datos usando solo Python, sin necesidad de saber HTML o JavaScript. |
| **Power BI** | Plataforma de visualización de datos de Microsoft, usada en el sector público colombiano para tableros de control. |
| **MLflow** | Plataforma para gestionar experimentos, versionar modelos y desplegarlos en producción. |
| **Git / GitHub** | Sistema de control de versiones de código. Permite trabajar en equipo, mantener historial de cambios y revertir errores. |

---

## Siglas institucionales y normativas

| Término | Definición |
|---|---|
| **URAB** | Unidad de Recepción y Atención Básica. Oficina de la Defensoría del Pueblo que recibe y clasifica las peticiones ciudadanas. |
| **IRIS** | Sistema de gestión documental y reparto de la Defensoría del Pueblo. |
| **VisionWeb** | Sistema misional de estadísticas de la Defensoría del Pueblo. |
| **CP** | Constitución Política de Colombia. |
| **CPACA** | Código de Procedimiento Administrativo y de lo Contencioso Administrativo (Ley 1437 de 2011). |
| **AGN** | Archivo General de la Nación. |
| **MIPG** | Modelo Integrado de Planeación y Gestión. Marco de referencia para la gestión pública colombiana. |
| **ISO/IEC 42001:2023** | Estándar internacional para sistemas de gestión de inteligencia artificial. |
| **NIST AI RMF 1.0** | Marco de Gestión de Riesgos de IA del Instituto Nacional de Estándares y Tecnología de EE.UU. |
| **CONPES 4144** | Documento del Consejo Nacional de Política Económica y Social que define la Política Nacional de IA de Colombia (2025). |
| **Directiva 007/2025** | Directiva conjunta sobre transparencia algorítmica en entidades públicas colombianas. |
| **SIC** | Superintendencia de Industria y Comercio. Autoridad de protección de datos en Colombia. |
| **VBG** | Violencia Basada en Género. |
| **NNA** | Niños, Niñas y Adolescentes. |
| **SMLMV** | Salarios Mínimos Legales Mensuales Vigentes. Unidad de referencia para multas y sanciones. |
| **D1–D9** | Entregables que el equipo de Derecho proporciona al equipo de Ciencia de Datos para diseñar los módulos: D1 (4 categorías jurídicas), D2 (sub-temas), D3 (sujetos de especial protección), D4 (matriz de competencias), D5 (consultas automatizables), D6 (templates de respuesta), D7 (criterios de urgencia), D8 (umbral de duplicación), D9 (roles RBAC). |
| **Q10, Q18, etc.** | Referencias al Banco de Preguntas y Respuestas del concurso LSL 2026. |
| **§2.3, §4.2, etc.** | Referencias a secciones específicas del Caso oficial URAB (RFP). |
| **DOC_1** | Documento interno del equipo que registra el antecedente del incidente de ciberseguridad de noviembre de 2025 en la Defensoría. |
| **SECOP IA.xlsx** | Archivo del equipo con el estudio de mercado de contratación de IA en el Estado colombiano. |
| **Matriz_SGIA_ISO42001.xlsx** | Archivo del equipo con la matriz de riesgos alineada al sistema de gestión de IA según ISO 42001. |
| **dh** | Días hábiles. |

---

## Métricas de equidad (siglas)

| Sigla | Significado |
|---|---|
| **EO** | Equal Opportunity (Igualdad de Oportunidad) |
| **DP** | Demographic Parity (Paridad Demográfica) |
| **DIR** | Disparate Impact Ratio (Ratio de Impacto Dispar) |
| **FNR** | False Negative Rate (Tasa de Falsos Negativos) |
| **TPR** | True Positive Rate (Tasa de Verdaderos Positivos) — sinónimo de Recall |

---

*Este glosario complementa el documento DS_CUERPO.md. Cualquier abreviatura o término técnico no definido aquí puede consultarse con el equipo de Ciencia de Datos.*
