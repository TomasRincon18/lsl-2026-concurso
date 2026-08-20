# Guía simple: los conceptos que hay que entender bien

> Explicaciones sin tecnicismos para presentar con seguridad. Si te preguntan
> por alguno de estos temas, aquí está la respuesta en "lenguaje humano".

---

## 1. ¿Qué es el "drift" en producción?

**La idea en una frase:** el mundo cambia y el modelo ya no reconoce lo que antes
reconocía bien.

**Analogía:** imagina que entrenas a un asistente con correos del año 2020. En
2026 la gente escribe distinto, aparecen palabras nuevas, cambian los temas. El
asistente sigue aplicando reglas viejas y empieza a equivocarse. Eso es *drift*
(deriva): el desempeño del modelo se degrada porque **los datos reales ya no se
parecen a los datos con los que aprendió**.

**En la Defensoría:** si mañana aparece un nuevo tipo de queja o cambia la
normativa, el modelo que clasificaba bien puede empezar a fallar sin que nadie se
dé cuenta. Por eso hay que **vigilarlo**.

**El semáforo de drift** (así lo maneja el sistema):

| Nivel | Qué significa | Qué se hace |
|---|---|---|
| 🟢 < 3% | Todo estable | Seguir monitoreando |
| 🟡 3–5% | Algo está cambiando | Revisión técnica, no se detiene |
| 🟠 5–10% | Degradación real | Comité en 5 días, mitigar |
| 🔴 > 10% | Ya no sirve | Suspender el módulo y arreglar |

En el simulador, el slider "Drift en producción" simula cuánto se degrada el
modelo; al final, el "Monitoreo en producción" muestra en qué color quedó.

---

## 2. ¿Qué hace cada módulo (M1–M8)?

> Piénsalos como una cadena de montaje. Cada módulo es una estación.

| Módulo | Nombre | Qué hace (en una frase) |
|---|---|---|
| **M1** | Recepción | Lee el documento, extrae nombre, cédula, hecho y pretensión, y genera el radicado. *Como un digitador que no se cansa.* |
| **M2** | Clasificación y triaje | Dice qué tipo de caso es (4 categorías), su sub-tema y si es urgente (nivel 1–5). *Como el funcionario que decide qué va a cada fila.* |
| **M3** | Asignación | Determina qué entidad es competente y a qué profesional va. *Como el repartidor de casos.* |
| **M4** | Anti-duplicación | Detecta si la misma queja ya llegó antes. *Evita responder dos veces lo mismo.* |
| **M5** | Historial | Muestra en segundos toda la historia del ciudadano. *La ficha completa sin buscar en archivos.* |
| **M6** | Asistente (RAG) | Redacta un **borrador** de respuesta usando normativa real. *El profesional siempre revisa y firma.* |
| **M7** | Interoperabilidad | Escribe el caso una sola vez y lo sincroniza con IRIS y VisionWeb. *Adiós a la doble digitación.* |
| **M8** | Tableros | Muestra carga, tiempos y alertas en tiempo real. *El panel de control del jefe.* |

**Punto clave:** M1–M6 hacen el trabajo pesado; **M7 y M8** lo conectan con los
sistemas existentes y lo hacen visible.

### ¿Por qué el simulador solo evalúa M1, M2, M4 y M6? ¿Y los otros?

Los ocho módulos no son del mismo tipo. Se dividen en dos grupos:

**Los que "aprenden" (y por eso se evalúan con métricas de calidad):**

- **M1** (reconocer datos), **M2** (clasificar), **M4** (detectar duplicados) y
  **M6** (redactar borradores) son **modelos entrenados con datos**. Su desempeño
  se mide como un porcentaje (90%, 99%...) y **mejora con los ciclos de
  refinamiento**. Por eso son los protagonistas del simulador: ahí se ve la
  "historia" de la IA aprendiendo.

**Los que "funcionan o no" (y por eso no se evalúan igual):**

- **M3** (asignación) es una **matriz de reglas** decididas por el equipo de
  Derecho, no un modelo que aprende. Su meta es de **tiempo** (asignar en ≤ 15
  min), no de "acierto".
- **M5** (historial) es un **buscador** (índice). Su meta es **velocidad**
  (consultar en < 500 ms), no acierto.
- **M7** (interoperabilidad) es una **conexión** entre sistemas. Su meta es de
  **fiabilidad** (sincronizar el 99,5% de las veces).
- **M8** (tableros) es **visualización**. No tiene "meta de acierto": muestra la
  información correcta o no la muestra.

**En resumen:** el simulador se enfoca en M1, M2, M4 y M6 porque son los que
tienen una métrica de **calidad que evoluciona** (y que se puede mostrar
aprendiendo ciclo a ciclo). M3, M5, M7 y M8 son reglas, búsqueda, conexión y
paneles: su éxito se mide en **tiempo, velocidad y fiabilidad**, no en un
porcentaje de aciertos. Por eso el simulador menciona el drift en producción
(degradación de M2 y M6) pero no "entrena" a M3 o M7.

---

## 3. ¿Qué se hace en cada "ciclo / refinamiento"?

**La idea:** el modelo rara vez nace perfecto; se **pule por iteraciones**.

El ciclo es un bucle de cuatro pasos:

1. **Evaluar:** se mide qué tan bien lo hace (accuracy, recall, etc.).
2. **Refinar:** se ajusta el modelo con los errores que se encontraron (más datos,
   mejor calibración).
3. **Validación humana:** los profesionales de la URAB revisan y corrigen los
   resultados.
4. **Verificar criterios:** ¿ya cumple las metas? Si no, se repite el ciclo.

**Analogía:** es como afilar un cuchillo. No afilas una vez y listo; afilas,
pruebas, afilas, pruebas… hasta que corta como debe. El simulador muestra este
bucle: cada "ciclo" sube un poco las métricas hasta alcanzar las metas.

**¿Cuántas veces?** Hasta que cumpla todos los umbrales (o hasta un máximo de
ciclos). Si no los cumple, **no sale a producción** — se sigue refinando.

---

## 4. ¿De dónde salen las metas/umbrales de cada M?

No son números al azar. Se construyen con tres criterios:

1. **Línea base (cómo está hoy):** se mide el proceso manual actual. Por ejemplo,
   hoy la clasificación humana acierta ~80% y tarda ~15 min por caso.

2. **Exigencia jurídica:** algunos umbrales los dicta el riesgo legal. El ejemplo
   más importante es el **recall de urgencias ≥ 99%**: no se tolera que se escape
   un solo caso de riesgo vital (una amenaza, un menor en peligro). Aquí la meta
   es casi perfecta **porque un error cuesta vidas**, no por capricho técnico.

3. **Costo del error ("umbral asimétrico"):** se compara el costo de equivocarse
   en una dirección vs. en la otra.
   - *Falso negativo* (decir "no urgente" cuando sí lo es) → daño irreparable.
   - *Falso positivo* (decir "urgente" cuando no lo es) → ~15 min de revisión extra.
   - Como el primero es mucho más caro, **se mueve el umbral para errar del lado
     barato**: detectar de más antes que dejar pasar uno solo.

**Resumen de las metas clave:**

| Métrica | Meta | Por qué ese número |
|---|---|---|
| Extracción (M1) | ≥ 90% | Menos retrabajo por datos mal digitados |
| Accuracy (M2) | ≥ 90% | Clasificar bien la gran mayoría |
| Recall urgencias (M2) | ≥ 99% | Un riesgo vital sin detectar es inadmisible |
| Precisión duplicados (M4) | ≥ 85% | No molestar con falsos duplicados |
| Recall duplicados (M4) | ≥ 90% | Detectar casi todos los repetidos |
| Aceptación borradores (M6) | ≥ 70% | El borrador es útil, se edita poco |
| Sincronización (M7) | ≥ 99,5% | Un solo registro, siempre consistente |

---

## 5. ¿Qué es "Human in the loop"?

**La idea:** la máquina **propone**, el humano **dispone**. El profesional siempre
está dentro del circuito, nunca fuera.

**Por qué es central en este caso:** la Defensoría no puede (ni debe) dejar que una
máquina decida sobre derechos fundamentales. Así que la IA:

- **Sugiere** la clasificación → el profesional la **valida o corrige**.
- **Recomienda** la entidad competente → el profesional la **confirma**.
- **Redacta un borrador** de respuesta → el profesional **revisa, edita y firma**.

**Las 5 decisiones que NUNCA se automatizan:**
1. Competencia de la entidad (¿es de la Defensoría o de otra entidad?).
2. Priorización final de riesgo vital.
3. Respuesta de fondo al ciudadano (la IA solo hace el borrador).
4. Corrección de duplicados (acumular o no casos repetidos).
5. Cierre del caso.

**Frase para el jurado:** "La IA le devuelve tiempo al profesional; no le quita la
responsabilidad. El humano decide, siempre."

---

## 6. ¿Qué significa "8–10 profesionales · 8 semanas de operación controlada"?

Es la descripción del **piloto** (la fase de prueba real) que aparece en la app.
Son dos cifras distintas:

**8–10 profesionales** → cuántas personas de la URAB usarán el sistema en la
prueba. No se lanza a toda la Defensoría de golpe: se arranca con un equipo
pequeño y manejable en una sola sede (URAB Bogotá).

**8 semanas de operación controlada** → cuánto dura esa prueba. Durante ese
tiempo el sistema funciona **en paralelo** al proceso manual, no lo reemplaza:

- Los profesionales usan la IA, pero también hay respaldo humano en todo.
- Se mide constantemente si cumple las metas (accuracy, recall, tiempos).
- Se compara contra el proceso de antes para demostrar la mejora real.
- Si algo falla, se detecta a tiempo y se corrige **antes** de escalar.

**Analogía:** es como el "piloto de una serie". No grabas las 10 temporadas de una
vez: grabas un episodio, lo mides, y si funciona, lo amplías.

**Por qué se dice así en la presentación:** porque demuestra que no prometemos
magia a gran escala — proponemos **probar en pequeño, medir y luego escalar** a
más regionales con datos reales en la mano.

---

## 7. Mini-glosario de una línea

- **Accuracy:** de 100 casos, ¿en cuántos acertó el tipo?
- **Precisión (precision):** de lo que dijo "Queja", ¿cuántas realmente lo eran?
- **Recall (sensibilidad):** de todas las quejas reales, ¿cuántas detectó?
- **Falso negativo:** el error grave — decir "no es urgente" cuando sí lo es.
- **Falso positivo:** el error menor — marcar como urgente algo que no lo es.
- **Conjunto gold:** ejemplos etiquetados a mano por juristas, que sirven de
  "respuesta oficial" para entrenar y medir el modelo.
- **Fine-tuning:** enseñarle a un modelo ya entrenado las particularidades de
  nuestro tema (aquí, lenguaje jurídico de la Defensoría).
- **RAG:** antes de responder, el modelo consulta una biblioteca de normativa real
  para no inventar.
- **MLOps:** la disciplina de mantener el modelo sano en producción (medir,
  monitorear drift, reentrenar).
- **SLA:** compromiso formal de tiempo/servicio (ej.: asignar en ≤ 4 h).

---

## 8. Preguntas técnicas frecuentes (FAQ)

> Respuestas rápidas a las dudas técnicas más comunes, en lenguaje humano.

**¿Qué es el drift en producción?**
El mundo cambia y el modelo deja de reconocer lo que antes reconocía bien. Se
vigila con un semáforo (verde/amarillo/naranja/rojo). *(Detalle en la sección 1.)*

**¿Por qué el drift sube periodo a periodo en la gráfica?**
Es una rampa lineal intencional: cuanto más tiempo corre el modelo en producción
sin reentrenarse, más se acumula la deriva. Son **periodos de producción**, no
ciclos de refinamiento.

**¿Qué pasa cuando la versión no se promueve a producción?**
No se escala: vuelve al ciclo de refinamiento hasta cumplir las metas de calidad
y de equidad. No se arriesga nada en producción.

**¿Qué decisiones se toman con datos de baja calidad?**
El validador pide la información que falta, se mejora OCR/NER, se etiqueta más
conjunto gold, se aplica el umbral asimétrico, y se arranca con un subconjunto
limpio en lugar de meter datos sucios al modelo.

**¿Las categorías jurídicas son solo 4?**
Sí: Asesoría, Queja, Solicitud de Mediación y Solicitud de Conciliación. La
palabra "PQRSD" es la taxonomía administrativa genérica (5 tipos); dentro de la
Defensoría todo se reclasifica en esas 4, más ~12 sub-temas y urgencia 1–5.

**¿Todos los casos los revisa un profesional en el refinamiento?**
No el 100%. Se automatiza lo de alta confianza y se revisa **todo lo importante**:
baja confianza, riesgo vital y las decisiones de fondo. *(Detalle en la sección 5.)*

**¿Qué hace el simulador?**
Reproduce el ciclo de vida de la solución —datos → entrenar → refinar → validar →
desplegar → monitorear— de forma visual e interactiva.

**¿El simulador entrena un modelo de verdad?**
No. Usa números aleatorios dentro de rangos realistas. El **proceso** que se ve es
el real; las **cifras** son de ejemplo.

**¿Cuál es el producto final del modelo?**
No es solo clasificar. Es llevar cada PQRSD de la recepción hasta una respuesta
oportuna y trazable, con el profesional decidiendo en cada paso.

**¿La respuesta al ciudadano la da solo el profesional?**
La de fondo, sí: M6 hace el borrador y el profesional revisa, edita y firma. Lo
administrativo (acuses y plantillas de consultas simples) se automatiza con
plantillas ya aprobadas por Derecho.

**¿Cuándo acaba la simulación, las PQRS ya están listas?**
Sí: el modelo cumplió sus metas (y la equidad) y está desplegado. Las PQRS nuevas
salen bien clasificadas y priorizadas, listas para que el profesional las resuelva.

**¿Qué datos da M5 (historial)?**
Por número de cédula: radicados, fechas, tipos, estados, profesionales asignados
y respuestas previas, en menos de 500 ms.

**¿Qué papel tienen IRIS y VisionWeb?**
Son los dos sistemas de gestión que hoy no se comunican. La solución escribe una
sola vez y **M7** los sincroniza, eliminando la doble digitación.

**¿Por qué la recepción no muestra la asignación (M3)?**
Porque la recepción modela solo el ingreso (M1, radicado). M3 (asignación) ocurre
después, una vez el caso está clasificado y validado por un profesional.
