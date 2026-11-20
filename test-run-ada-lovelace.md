# Test End-to-End — Figura de prueba: Ada Lovelace

**Aviso de alcance:** las etapas 1, 2, 3 (contenido/razonamiento), 7 y 8 producen aquí su output **real** — son generables sin infraestructura externa. Las etapas 4 (RunComfy), 5 (Fish Audio) y 6 (HyperFrames) requieren credenciales/infra que no están conectadas en este entorno de prueba — para esas se muestra el **payload exacto** que se enviaría, no una ejecución real. Donde el pipeline detectó un problema real durante este test, se deja visible en vez de corregirlo en silencio — es justamente lo que la etapa de QA está diseñada para atrapar.

---

## [1] Historytelling Design — output

```json
{
  "script_id": "ada_lovelace_v1",
  "narrative_approach": "Hero's Journey con giro de legado no reconocido",
  "approaches_considered": [
    "Hero's Journey — la visionaria que vio un siglo antes de tiempo",
    "Arco de Redención — reescribir la herencia temida de un padre ausente",
    "Legado No Reconocido — la autora borrada que la historia tuvo que redescubrir"
  ],
  "script_text": "[ver narration_text por escena abajo, en 02-shotlist-breakdown]",
  "historical_accuracy_notes": "Verificar en QA: (1) orden cronológico Difference Engine (1833, demo que Ada ve siendo adolescente) vs Analytical Engine (1840s, trabajo principal de Ada); (2) la Analytical Engine NUNCA se construyó en vida de Babbage ni de Ada — no confundir con 'construyeron la máquina' en el guion; (3) fecha de redescubrimiento de las notas (B.V. Bowden las republica en 1953) vs. nombramiento del lenguaje de programación Ada (1980) son dos hitos distintos, no el mismo momento."
}
```

**Nota de diseño (enfoque elegido):** Hero's Journey combinado con el ángulo de "legado no reconocido" — encaja con el patrón que mejor performa en tu canal (contenido que revela historias ocultas + figuras de resistencia/resiliencia), y da una lección de valores fuerte: ver más allá de lo que tu época puede entender, aunque nadie te crea.

---

## [2] Shot-List / Desglose de Escenas — output

11 escenas, 90s total (10×8s + 1×10s).

| scene_id | narration_text | start_frame_prompt | end_frame_prompt | camera_movement (seleccionado) | variant_suggestions | continuity_notes |
|---|---|---|---|---|---|---|
| scene_01 | "En 1843, una joven inglesa escribió el primer programa de la historia — para una máquina que nunca llegó a existir." | Ada adulta (28 años), de pie frente a una ventana con luz tenue, vestido victoriano oscuro, mirada fija y seria hacia cámara | Mismo encuadre, leve giro de cabeza hacia una mesa con papeles y diagramas mecánicos | **push-in lento** | push-in lento (bajo riesgo) / pan lateral revelando los papeles (medio riesgo) | El end-frame introduce los papeles que anclan la escena 2 |
| scene_02 | "Hija del poeta Lord Byron, a quien nunca conoció — su madre temía que heredara la 'locura poética' de su padre." | Retrato de infancia de Ada (~7 años), interior victoriano, luz fría | Mismo encuadre, la madre (Annabella) entra al cuadro con libros de matemáticas | pan lateral revelando a la madre | pan lateral (medio riesgo) / corte estático con la madre ya en cuadro (bajo riesgo) | Introduce el conflicto madre-hija que resuelve la escena 3 |
| scene_03 | "Para 'curarla', la sometió a matemáticas rigurosas desde niña. La disciplina que debía apagarla, la encendió." | Ada niña, escribiendo ecuaciones en una pizarra, concentración intensa | Mismo encuadre, su expresión cambia a asombro/descubrimiento | encuadre estático, foco en manos y pizarra | estático (bajo riesgo) — rostro en primer plano, evitar movimiento grande | Rostro en primer plano — prioridad de consistencia alta |
| scene_04 | "A los 17 años, en una fiesta, vio una demostración del Motor Diferencial de Charles Babbage. Quedó fascinada." | Salón de fiesta victoriano, Ada joven (17) observando una máquina de engranajes en funcionamiento | Mismo encuadre, acercamiento a los engranajes girando | push-in lento hacia la máquina | push-in lento (bajo riesgo) / corte a detalle de engranajes (medio riesgo — cambia de sujeto) | Introduce la máquina que vuelve a aparecer en escena 5 |
| scene_05 | "Años después, Babbage diseñó algo más ambicioso: el Motor Analítico. Nunca llegó a construirse — pero Ada entendió su verdadero alcance." | Ada adulta junto a Babbage, revisando planos de una máquina más compleja (no la misma del Motor Diferencial) | Mismo encuadre, Ada señala un diagrama, Babbage al fondo desenfocado | pan lateral lento hacia los planos | pan lateral (medio riesgo) / estático con zoom a los planos (bajo riesgo) | El plano enlaza con los "papeles" de la escena 6 |
| scene_06 | "Escribió notas explicando cómo la máquina podía ejecutar instrucciones paso a paso. Hoy se le considera el primer programa de computadora." | Ada escribiendo en su escritorio, papeles cubiertos de notación matemática | Mismo encuadre, acercamiento a la página con el algoritmo (Nota G) | encuadre estático, foco en manos y papel | estático (bajo riesgo) — rostro en primer plano parcial | Rostro parcialmente visible — vigilar consistencia |
| scene_07 | "Fue más allá: imaginó que una máquina así podría componer música. Lo llamó 'ciencia poética'." | Ada mirando hacia una ventana, luz cálida, expresión soñadora | Mismo encuadre, superposición sutil de notas musicales/partitura en su mente (tratamiento visual, no literal) | push-in lento con luz cálida | push-in lento (bajo riesgo) / disolución a notas musicales (medio riesgo — requiere efecto visual adicional en etapa 6, no solo FLF2V) | — |
| scene_08 | "Murió a los 36 años, sin ver reconocido su trabajo. Durante casi un siglo, su nombre fue solo una nota al pie de la historia de Babbage." | Ada enferma, recostada, luz fría y tenue | Mismo encuadre, fundido lento a un retrato enmarcado cubierto de polvo (paso del tiempo) | corte estático, luz decreciente | estático (bajo riesgo) — rostro en primer plano | Rostro en primer plano — prioridad de consistencia alta |
| scene_09 | "Sus notas originales durmieron casi cien años en archivos, citadas por pocos, comprendidas por menos." | Archivo/biblioteca victoriana, documentos apilados, polvo, luz tenue | Mismo encuadre, acercamiento a una carpeta con su nombre | pan lateral lento por estantes | pan lateral (medio riesgo — sin rostro, riesgo bajo de todas formas) | Sin personaje en cuadro — riesgo de drift mínimo en esta escena |
| scene_10 | "En 1953 un científico redescubrió sus notas. En 1980, un lenguaje de programación llevó su nombre: Ada." | Transición visual: papel antiguo se transforma en pantalla de computadora temprana (tratamiento estilizado, no literal) | Pantalla con el texto "ADA" como nombre de lenguaje, estética retro-computación | transición estilizada | — (escena de transición, sin rostro — no requiere variantes de riesgo) | Enlaza el pasado con el presente antes del cierre |
| scene_11 (10s) | "Ada vio una máquina que nadie más podía ver. Ver más allá de tu tiempo, aunque nadie te crea, es el acto de valentía que cambia el futuro." | Ada adulta, misma pose/vestuario de scene_01, mirando directo a cámara | Mismo encuadre, leve sonrisa final | encuadre estático, cierre directo a cámara | estático (bajo riesgo) — rostro en primer plano, cierre | Rostro en primer plano — máxima prioridad de consistencia (es el frame de cierre del short) |

**Nota de corrección aplicada en este draft:** la versión inicial de la escena 5 decía "Babbage y Ada construyeron el Motor Analítico" — **históricamente falso** (nunca se construyó). Se corrigió a "diseñó... nunca llegó a construirse" antes de pasar a la etapa 3, para no tener que descartar keyframes ya generados más adelante. Esto es exactamente el tipo de error que la etapa 7 (QA) está diseñada para atrapar si se cuela — aquí se atrapó una etapa antes.

---

## [3] Generación de Keyframes — output (prompts; no se renderizó imagen real en este test)

```json
{
  "reference_image_prompt": "Retrato de Ada Lovelace, mujer inglesa de ~28 años, cabello oscuro rizado peinado hacia atrás, vestido victoriano formal de cuello alto, expresión seria e inteligente, iluminación suave de estudio, fondo neutro, encuadre centrado en rostro y hombros, estilo pictórico realista — NO fotografía (no existen fotografías de ella; usar estética de retrato pintado de época).",
  "consistency_mechanism": "InstantID + IPAdapter FaceID (weight 0.7) + ControlNet OpenPose + FaceDetailer — aplicado a las 22 generaciones (11 escenas × start/end) usando el reference_image anterior como ancla.",
  "sample_keyframe_calls": [
    { "scene_id": "scene_01", "frame": "start", "prompt": "<start_frame_prompt de scene_01>", "source": "instantid" },
    { "scene_id": "scene_01", "frame": "end", "prompt": "<end_frame_prompt de scene_01>", "source": "instantid" }
  ],
  "note": "Se repite el mismo patrón para las 11 escenas → 22 imágenes. scene_09 y scene_10 no requieren el rostro de Ada en cuadro (ver tabla de la etapa 2) — pueden generarse sin pasar por InstantID si el encuadre no incluye el personaje, ahorrando ese paso."
}
```

---

## [4] FLF2V — RunComfy / LTX-2.5 — payload simulado (no ejecutado; sin credenciales de RunComfy en este entorno)

Ejemplo real del objeto que `scripts/runcomfy_client.py` enviaría para `scene_01`:

```json
{
  "overrides": {
    "<NODE_ID_first_frame_loader>": { "inputs": { "image": "ada_lovelace/scene_01_start.png" } },
    "<NODE_ID_last_frame_loader>": { "inputs": { "image": "ada_lovelace/scene_01_end.png" } },
    "<NODE_ID_prompt_text>": { "inputs": { "text": "push-in lento, 35mm, luz tenue de ventana" } },
    "<NODE_ID_duration_or_length>": { "inputs": { "duration_seconds": 8 } }
  }
}
```

**Riesgo a vigilar en el piloto real:** scene_03, scene_06, scene_08 y scene_11 tienen el rostro de Ada en primer plano con movimiento ya elegido como "bajo riesgo" (estático) — son las que menos margen de error tienen si aparece drift, porque no hay un movimiento de cámara que lo disimule. Priorizar estas 4 en el piloto de 5-10 escenas.

---

## [5] Narración / Voz en Off — payload simulado (no ejecutado; sin credenciales de Fish Audio en este entorno)

```json
{
  "model": "s2.1-pro-free",
  "reference_id": "<voice_reference_id de catálogo del canal>",
  "format": "mp3",
  "text": "En 1843, una joven inglesa escribió el primer programa de la historia — para una máquina que nunca llegó a existir."
}
```

Texto total de narración del short (11 escenas): ~1,340 caracteres → dentro del límite de 10,000 caracteres por llamada del MCP server, y consistente con la estimación de costo previa (~$0 en `s2.1-pro-free`).

---

## [6] Ensamblaje — overrides de HyperFrames simulados (no ejecutado; sin entorno Node.js/FFmpeg disponible aquí)

```
data-composition-id="ada-lovelace-short"
scene_01.mp4  → data-start=0   data-duration=8
scene_02.mp4  → data-start=8   data-duration=8
scene_03.mp4  → data-start=16  data-duration=8
scene_04.mp4  → data-start=24  data-duration=8
scene_05.mp4  → data-start=32  data-duration=8
scene_06.mp4  → data-start=40  data-duration=8
scene_07.mp4  → data-start=48  data-duration=8
scene_08.mp4  → data-start=56  data-duration=8
scene_09.mp4  → data-start=64  data-duration=8
scene_10.mp4  → data-start=72  data-duration=8
scene_11.mp4  → data-start=80  data-duration=10
VO completo   → data-start=0   data-duration=90  (track-index 1)
```

---

## [7] QA / Checklist de Revisión — resultado del test

| Check | Resultado |
|---|---|
| Sync VO/video | N/A en este test (no hay media real) |
| Continuidad entre escenas | OK — `continuity_notes` de la etapa 2 forman una cadena coherente escena a escena |
| Consistencia de identidad | Pendiente de piloto real — identificadas 4 escenas de riesgo bajo-pero-crítico (ver etapa 4) |
| **Precisión histórica** | **Encontrado y corregido 1 error** antes de avanzar: la escena 5 afirmaba que el Motor Analítico se construyó — es falso, nunca se construyó. Corregido en la tabla de la etapa 2. Resto de afirmaciones verificadas: demo del Motor Diferencial (1833, Ada adolescente) ✓, notas sobre el Motor Analítico y el algoritmo de Bernoulli — "Nota G" (1843) ✓, muerte a los 36 años (1852) ✓, redescubrimiento de sus notas por B.V. Bowden (1953) ✓, lenguaje de programación Ada nombrado en su honor (1980) ✓ — se mantienen como dos hitos separados, no fusionados. |
| Claridad del mensaje de valores | OK — "ver más allá de tu tiempo, aunque nadie te crea" es concreto y aplicable, no solo biografía |
| Artefactos/glitches | N/A en este test |
| Duración | 90s exactos (10×8s + 10s) ✓ |

**Status: aprobado con nota** — el pipeline de contenido (etapas 1-3, 7) funciona correctamente end-to-end y el proceso de QA cumplió su función (atrapó un error histórico real antes de que llegara a producción). Falta validar las etapas 4-6 con credenciales reales.

---

## [8] Exportación + Publicación-Ready — output

```json
{
  "upload_bundle": {
    "title_options": [
      "Ella escribió el primer programa de la historia — y nadie le creyó",
      "La mujer que vio las computadoras 100 años antes de que existieran",
      "El algoritmo que esperó un siglo para ser entendido"
    ],
    "description": "En 1843, Ada Lovelace escribió las notas que hoy consideramos el primer programa de computadora — para una máquina que nunca se construyó en su vida. Esta es la historia de ver más allá de tu época, aunque el mundo tarde un siglo en alcanzarte.",
    "tags": ["historia", "mujeres en la ciencia", "Ada Lovelace", "valores", "resiliencia"]
  },
  "airtable_record": "no creado en este test — requiere AIRTABLE_API_KEY real"
}
```

*Nota: los títulos no fueron scoreados con tus herramientas vidIQ reales en este test — puedo correr `vidiq_score_title` sobre estas 3 opciones si quieres el paso completo.*
