# URAB IA — Guion hablado (5–8 min, versión técnica)

> Esto es **lo que dices**. El simulador se muestra todo el tiempo; las notas
> `[SIMULADOR]` indican qué hacer en cada momento. Tono: técnico pero fluido,
> ~140 palabras/min. Léelo en voz alta y ajústalo a tu ritmo.
>
> **Orden de las pestañas (ya alineado con la app):**
> Simulación en vivo → Resultados → Recepción de PQRSD.

---

## Configuración recomendada de los sliders

> Deja estos valores **antes** de empezar a hablar, para que el demo fluya solo.

**Pestaña "Simulación en vivo":**

| Slider | Valor |
|---|---|
| PQRSD de entrenamiento | 1000 |
| Calidad inicial de datos | 0.85 |
| Ciclos de refinamiento | 5 |
| Drift en producción | 0.10 |
| Duración | 30 segundos |

*(Con estos valores el modelo llega a producción en 2–3 ciclos y el drift sube
hasta naranja, perfecto para el cierre de "no se envejece".)*

**Pestaña "Recepción de PQRSD" (solo en el cierre):**

| Slider | Valor |
|---|---|
| Velocidad | 1.0 |
| PQRSD por pulso | 10 |
| Total a recibir | 60 |

---

## Apertura técnica — 45 segundos

No venimos a prometer una inteligencia artificial que inventamos desde cero. Eso
sería lento, carísimo y arriesgado.

Nosotros hicimos algo más inteligente: **tomamos modelos que ya existen, que ya
son de clase mundial, y los especializamos en la Defensoría.**

Modelos que ya **leen imágenes** —un escaneado, una foto de un documento— y
extraen los datos. Modelos que **entienden español jurídico** y clasifican un
texto. Modelos que **leen datos no estructurados** —un correo, una carta libre—
y los convierten en información ordenada. Y modelos que **redactan** respuestas
basándose en normativa real.

¿La ventaja? No pagamos millones entrenando desde cero. **Aprovechamos años de
investigación ya hecha, la adaptamos, y reducimos drásticamente el costo y el
tiempo.** Es como no tener que inventar la rueda para construir el carro.

Eso es lo que nos permite, con un presupuesto razonable, resolver un problema
enorme.

---

## El problema — 40 segundos

La Defensoría recibe ~300 peticiones al día, y hoy todo se hace a mano: quince
minutos por caso para clasificar, dos días para asignar, y hasta veinte días para
la primera respuesta.

No es falta de talento. Es que la puerta de entrada —la URAB— funciona con
procesos manuales que no dan abasto. Y lo más grave: sin priorización automática,
un **riesgo vital** puede quedar enterrado debajo de cientos de consultas
rutinarias.

---

## Nuestra solución: arquitectura modular — 1 minuto

**[SIMULADOR: pestaña "Simulación en vivo" → configura los sliders → "Ejecutar
simulación".]**

Nuestra solución es una **arquitectura modular: ocho piezas que se enchufan
entre sí**, no un monolito.

Cada pieza hace una cosa, y la hace con el mejor modelo para esa tarea: una
**lee y extrae los datos** del documento, otra **clasifica** el tipo de caso y si
es urgente, otra **detecta duplicados**, otra **prepara el borrador de
respuesta**... y una última lo **sincroniza** con IRIS y VisionWeb, sin doble
digitación.

**[SIMULADOR: deja correr la simulación mientras hablas — el flujo muestra cada
etapa.]**

¿Por qué modular? Porque si una pieza falla, **se repara esa pieza, no todo el
sistema**. Porque se puede **auditar** módulo por módulo. Y sobre todo, porque
**escala**.

Piensen en la escalabilidad. Hoy empezamos con el piloto en la URAB de Bogotá:
ocho a diez profesionales, una sola sede. Cuando toque crecer a otras regionales,
**no hay que rehacer nada**: se replican los módulos en un servidor nuevo y listo.
¿Llega un pico de demanda? Se sube la capacidad solo en el módulo que se satura,
sin tocar el resto. Y si mañana aparece una nueva necesidad —digamos, un nuevo
canal de entrada o un nuevo tipo de documento— se agrega una pieza más, sin
romper lo que ya funciona.

Eso es lo contrario de un sistema rígido: es una solución que **crece con la
institución**, pieza por pieza, cuando y donde se necesite.

---

## La proyección — 1 minuto y medio

**[SIMULADOR: la simulación ya corre — señala el flujo y la barra de progreso.]**

Hagamos cuentas con un número concreto: **novecientas PQRSD estancadas** hoy.

Sin IA, cada profesional despeja treinta al día... y siguen llegando trescientas.
El represamiento no se despeja: **crece**.

Con URAB IA, la clasificación pasa de quince minutos a **menos de treinta
segundos**. La asignación, de dos días a **menos de cuatro horas**. El equipo
entero deja de gastar el día clasificando y se dedica a resolver.

Miren el ciclo: la IA entrena, se evalúa, se refina, la validan los profesionales
de la URAB... y **no sale a producción hasta cumplir todas sus metas**: 90% de
precisión, 99% de detección de urgencias. Con esto, proyectamos despejar esas
novecientas en **cuatro a seis semanas** y sostener el flujo dentro de los
términos legales.

---

## Lo que ustedes necesitan, resuelto — 45 segundos

**[SIMULADOR: deja la simulación corriendo de fondo.]**

Recepción con errores de digitación → la IA lee y extrae, con 90% de acierto.
Clasificación sin criterios uniformes → clasifica con 90% de precisión, y 99% en
riesgo vital: no dejamos escapar ni uno.
Doble registro en IRIS y VisionWeb → se escribe una vez y se sincroniza solo.
Quejas repetidas, historial inexistente, respuestas desde cero, sin visibilidad
→ resuelto por los módulos M4, M5, M6 y M8.

No son deseos: son **compromisos medibles** que el sistema reporta y que sus
propios profesionales validan.

---

## Equidad y sesgos — 1 minuto

**[SIMULADOR: en "Resultados", señala la sección "Equidad algorítmica" (o el nodo
"Pruebas de equidad" del flujo).]**

Hay algo que nos separa de cualquier chatbot: **tratamos la equidad como un
requisito de ingeniería, no como una promesa.**

Porque un modelo puede ser preciso en promedio... y aun así tratar peor a un
grupo. Medimos cuatro cosas: que detecte **igual de bien a todos los grupos**, que
los resultados se repartan parejo, que ningún grupo rinda por debajo del 80% del
mejor, y que no se le escapen más casos urgentes a un grupo que a otro.

Miren el flujo: antes de desplegar hay un **gate de equidad**. La disparidad
tiene que bajar del **5%**. Si no, no sale.

Y esto no es teoría. Un ejemplo real: imaginen que el modelo acierta el **91%
para hombres** y el **84% para mujeres**. Son solo siete puntos... pero para una
mujer cuyo caso de riesgo vital se clasificó mal, son siete puntos inaceptables.
Nuestro sistema lo detecta, lo marca en naranja y **detiene el despliegue** hasta
corregirlo.

Si la disparidad pasa del 10%, se suspende el módulo y se notifica al Defensor
Delegado. La regla es innegociable: **sin equidad superada, no hay despliegue.**

---

## Por qué la nuestra — 45 segundos

**[SIMULADOR: pestaña "Resultados" → señala el monitoreo de producción.]**

Entonces, ¿por qué comprar esta y no otra?

**Uno:** se apoya en modelos ya probados, así que es **más barata y más rápida**
de poner en marcha.

**Dos:** es **modular**, así que es auditable, reparable y escalable.

**Tres:** tiene el **ser humano siempre al centro** —la IA sugiere, el profesional
decide— y la **equidad como puerta de despliegue**.

Y cuatro: **no se envejece**. Miren el monitoreo: el mundo cambia y los modelos se
degradan; nuestro sistema **lo detecta** —ahí está el semáforo subiendo— y se
reentrena solo con la retroalimentación de sus profesionales. No vendemos un
modelo que funciona hoy y falla mañana.

---

## Cierre — 30 segundos

**[SIMULADOR: pestaña "Recepción de PQRSD" → "Iniciar recepción".]**

La Defensoría ya tiene el talento y la misión. Le falta una puerta de entrada que
no se atore, construida con la mejor tecnología disponible —y con la equidad y la
decisión humana como cimientos.

**[SIMULADOR: deja que los casos lleguen mientras cierras.]**

Miren: así se ve la Defensoría con URAB IA. Los casos entran, se radican, se
clasifican... y el profesional se dedica a lo que importa.

**URAB IA no reemplaza a los profesionales: les devuelve las horas que hoy gastan
en papel, para dedicarlas a las personas.**

Muchas gracias.

---

### Resumen de movimientos en el simulador

| Sección | Acción en el simulador |
|---|---|
| Arquitectura modular | "Simulación en vivo" → configurar sliders → "Ejecutar simulación" |
| Proyección | Dejar correr la simulación (flujo + barra de progreso) |
| Necesidades resueltas | Dejar la simulación corriendo de fondo |
| Equidad y sesgos | "Resultados" → sección "Equidad algorítmica" |
| Por qué la nuestra | "Resultados" → monitoreo de producción |
| Cierre | "Recepción de PQRSD" → "Iniciar recepción" |
