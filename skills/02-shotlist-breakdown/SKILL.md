---
name: shotlist-breakdown
description: Use when breaking an approved 90-second historical-figure script into an 11-scene (8s each) shot list in two prompt levels — a quick descriptive draft (v1) for human review/correction, and a solid cinematic text-to-image prompt (v2) generated only after v1 is approved — plus narration text, camera movement, continuity notes, and engagement-maximizing variation suggestions per scene. Second stage of the Type I pipeline.
---

# Shot-List / Desglose de Escenas

## Cuándo usar este skill

Después de aprobar el guion de `01-historytelling-design`, antes de generar keyframes.

## Input

```json
{
  "script_id": "string",
  "script_text": "string",
  "emotional_beat_map": []
}
```

## Parámetros fijos (decisiones congeladas del diseño)

- **Duración estándar: 90s → 11 escenas de 8s** (90 / 8 ≈ 11.25; la última escena puede ajustarse a ~6-8s para cerrar exacto en 90s).
- **Segmentación: 1 generación FLF2V de 8s por escena** (no se divide en 2 de 4s). LTX-2.5 soporta hasta 20s por generación en modo Fast, así que 8s está cómodamente dentro de rango.
- **Dos niveles de prompt por frame (v1 descriptivo / v2 imagen), nunca uno solo.** v2 nunca se genera sin que v1 haya sido aprobado primero — ver "Proceso" y "Gate" abajo.

## Proceso

### Fase A — Shot-list descriptivo (v1)

1. Partir el guion en N escenas de 8s según el `emotional_beat_map`.
2. Para cada escena, generar:
   - `scene_id` (ej. `scene_01` … `scene_11`)
   - `narration_text` — línea de VO exacta para esa escena
   - `start_frame_prompt_v1` / `end_frame_prompt_v1` — descripción visual **breve y legible** (pose, iluminación, encuadre, vestuario) pensada para lectura y corrección rápida, no para el motor de imagen
   - `camera_movement` — lenguaje cinemático por defecto para esa escena
   - `continuity_notes` — el end-frame de la escena N debe enlazar visualmente con el start-frame de la escena N+1 (misma locación/ángulo aproximado si la transición es continua, o corte deliberado si no lo es)
3. **Generar `variant_suggestions`** por escena: 2-3 alternativas de `camera_movement`/pacing/encuadre pensadas para maximizar engagement (ej. push-in lento vs. pan lateral vs. corte estático). Reglas:
   - En escenas con el rostro del personaje en primer plano, **priorizar movimientos simples** (push-in lento, encuadre estático) — los movimientos grandes aumentan el riesgo de drift de identidad en la etapa FLF2V (ver nota de riesgo en `03-keyframe-generation` y `04-flf2v-runcomfy`).
   - Reservar movimientos más dramáticos para tomas amplias, de ambiente, o sin el rostro como foco principal.
4. Selección de variante: manual (tú) o vía heurística de scoring (ej. integración futura con vidIQ) — no bloqueante para continuar el pipeline; si no hay selección explícita, usar la variante por defecto marcada en el shot-list.
5. Presentar el shot-list v1 completo (las 11 filas) para revisión humana — tabla compacta, fácil de leer y corregir.

### 🔒 Gate — aprobación de v1 antes de expandir a v2

**No generar v2 hasta que v1 esté aprobado**, escena por escena o en bloque. Si se pide una corrección sobre v1, se aplica y se vuelve a presentar — v2 nunca se construye sobre un v1 no confirmado, porque heredaría el error y encarecería la corrección (v2 es más largo y más caro de regenerar/revisar).

### Fase B — Expansión a prompt de imagen (v2), solo escenas v1=Approved

1. Definir (una sola vez por short, no por escena) el **`cinematic_style_reference`**: el ancla visual compartida por las 11 escenas para que el short se vea como una sola pieza coherente. Incluye explícitamente:
   - Lenguaje de lente/encuadre (ej. "35mm, profundidad de campo media, retrato fotográfico")
   - Esquema de iluminación (ej. "iluminación de tres puntos, luz cálida direccional, sombras suaves")
   - Paleta / color grade (ej. "paleta desaturada, tonos sepia-fríos, contraste cinematográfico moderado")
   - Textura / film stock (ej. "grano de película fino, piel con textura realista, sin aspecto plástico/3D")
   - Un ancla de identidad repetible (vestuario, edad aparente, rasgos) para reforzar consistencia junto con InstantID — InstantID fija el rostro, pero el texto repetido ayuda a fijar vestuario/entorno/iluminación, que InstantID no controla.
2. Para cada escena con `v1_status = Approved`, construir `start_frame_prompt_v2` / `end_frame_prompt_v2` concatenando:
   `{cinematic_style_reference} + {detalle específico de la escena, expandido desde v1_prompt con más densidad de detalle visual} + {camera_movement/encuadre de esa escena} + {boosters de calidad: "fotorrealista, alta definición, iluminación cinematográfica, detalle de piel realista, composición de cine"}`
   — v2 es siempre más largo, más técnico y más denso que v1; v1 nunca se trunca ni se reemplaza, ambos quedan guardados.
3. Marcar `v2_status = Draft` al generarlo; pasa a `Approved` tras revisión humana de la imagen resultante (o del prompt, si se revisa antes de generar).
4. Solo los prompts `v2` se envían al grafo ComfyUI/InstantID de `03-keyframe-generation` — `v1` es memoria de trabajo y trazabilidad, nunca input directo del motor de imagen.

## Dónde se guarda

Las 11 filas (una por escena) se escriben en la tabla **`Shot List`** de Airtable (base "Faceless Youtube Channel"), enlazada al registro de `Videos` correspondiente — no en un archivo suelto. Campos: `Scene ID`, `Video` (link), `Narration Text`, `Duration Seconds`, `Camera Movement Selected`, `Variant Suggestions`, `Continuity Notes`, `Start/End Frame Prompt - Descriptive (v1)`, `V1 Status`, `Cinematic Style Reference`, `Start/End Frame Prompt - Image/T2I (v2)`, `V2 Status`, `Notes`. Si Airtable no está disponible, degradar a JSON local y decirlo explícitamente — nunca bloquear el pipeline por eso.

## Output

```json
{
  "script_id": "string",
  "cinematic_style_reference": "string — ancla de estilo compartida por las 11 escenas, definida una vez",
  "scenes": [
    {
      "scene_id": "scene_01",
      "narration_text": "string",
      "start_frame_prompt_v1": "string — descriptivo, lectura rápida",
      "end_frame_prompt_v1": "string — descriptivo, lectura rápida",
      "v1_status": "Draft | Needs Revision | Approved",
      "start_frame_prompt_v2": "string | null — imagen/T2I, solo si v1_status = Approved",
      "end_frame_prompt_v2": "string | null — imagen/T2I, solo si v1_status = Approved",
      "v2_status": "Not Generated | Draft | Approved",
      "camera_movement": "string — variante seleccionada",
      "variant_suggestions": [
        { "label": "push-in lento", "camera_movement": "string", "risk_level": "bajo" },
        { "label": "pan lateral", "camera_movement": "string", "risk_level": "medio" }
      ],
      "continuity_notes": "string",
      "duration_seconds": 8
    }
  ]
}
```

## Siguiente etapa

→ `03-keyframe-generation` (consume únicamente `start_frame_prompt_v2` / `end_frame_prompt_v2` de las escenas con `v2_status = Approved`)
