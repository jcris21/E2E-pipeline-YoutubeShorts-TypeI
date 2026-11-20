# Pipeline Tipo I — Faceless YC

Exportación a formato de carpetas/skills para VS Code del pipeline end-to-end de Shorts Tipo I, derivado del diseño aprobado (`type-i-shorts-pipeline-design.md`).

**Ruta de generación:** RunComfy (Serverless API / ComfyUI) · LTX-2.5 · GPU L40S (X-Large Plus) · FLF2V

## Decisiones congeladas del diseño

| # | Decisión | Resuelto |
|---|---|---|
| 1 | Duración estándar | 90s (≈11 escenas de 8s) |
| 2 | Segmentación por escena | 1 FLF2V de 8s, con sugerencias de variación de movimiento/pacing |
| 3 | Consistencia de personaje | InstantID + IPAdapter FaceID + ControlNet + FaceDetailer (ComfyUI/RunComfy), con bypass para imágenes externas |
| 4 | TTS/voz | Fish Audio `s2.1-pro-free`, voz de catálogo |
| 5 | Ensamblaje | HyperFrames + plantilla `/general-video` |

## Estructura

```
type-i-shorts-pipeline/
├── skills/                          # un SKILL.md por etapa (formato Anthropic, estilo /mnt/skills)
│   ├── 01-historytelling-design/
│   ├── 02-shotlist-breakdown/
│   ├── 03-keyframe-generation/
│   ├── 04-flf2v-runcomfy/
│   ├── 05-voiceover-tts/
│   ├── 06-assembly-hyperframes/
│   ├── 07-qa-checklist/
│   └── 08-export-publish/
├── workflows/
│   ├── ltx25_flf2v_workflow_api.template.json   # ESQUELETO — ver workflows/README.md
│   └── README.md                                 # cómo obtener el archivo real desde RunComfy
├── scripts/
│   ├── runcomfy_client.py           # llamadas a la Deployment con overrides por escena
│   ├── fish_audio_client.py         # respaldo directo-a-API para TTS (preferir MCP si está disponible)
│   ├── airtable_sync.py             # respaldo directo-a-API para Airtable (preferir conector MCP/n8n)
│   └── hyperframes/
│       ├── template_general_video.html   # plantilla validada con un render real (ver test-run-ada-lovelace.md)
│       ├── abrir-studio.cmd               # lanza HyperFrames Studio (preview en vivo + edición) — Windows
│       └── abrir-studio.sh                # idem, macOS/Linux
└── ui/
    └── qa-review-queue/              # mockup de la cola de revisión de la etapa [7]
        ├── Main.dc.html               # fuente del artifact (Claude Design-canvas)
        ├── canvas.json
        └── README.md                  # qué muestra y qué falta para conectarlo a datos reales
```

**Nota sobre `ui/`:** es un mockup interactivo (datos de muestra, acciones solo en estado
local) — ver `ui/qa-review-queue/README.md` para la versión viva y lo que falta para
hacerlo real.

## Cómo usar esto

1. Copia esta carpeta a tu convención de `/mnt/skills` (o donde organices tus skills packages).
2. Cada carpeta en `skills/` es un skill independiente con inputs/outputs tipados — puedes correrlas sueltas, re-ejecutar una sola si falla, o encadenarlas en n8n según tu stack de automatización existente.
3. **Antes de producir en volumen**, hay dos pasos manuales obligatorios que ningún script reemplaza:
   - **`workflows/`**: construir y exportar el grafo real de LTX-2.5 FLF2V desde tu canvas de ComfyUI Cloud en RunComfy (ver `workflows/README.md`).
   - **Piloto de 5-10 escenas** (descrito en `skills/04-flf2v-runcomfy/SKILL.md`): validar throughput/costo real en L40S y, específicamente, que no haya drift de identidad dentro de los clips generados — no solo que los keyframes coincidan.
4. Los tres scripts en `scripts/` son implementaciones de referencia, no código probado en producción — cada uno indica en su docstring qué verificar (nombres de campo de Airtable, endpoints de API, IDs de nodo de ComfyUI) antes de correrlos contra tus cuentas reales.

## Qué no se inventó

Dos piezas dependen de acceso directo a tus entornos (RunComfy Cloud, tu base Airtable real) que no están disponibles aquí, así que se documentaron como plantillas a completar en vez de fabricar valores falsos:
- El `workflow_api.json` real de LTX-2.5 FLF2V (IDs de nodo y `class_type` exactos).
- Los nombres de campo reales de tus 9 tablas en Airtable (solo se conocían los nombres de las tablas, no sus columnas).
