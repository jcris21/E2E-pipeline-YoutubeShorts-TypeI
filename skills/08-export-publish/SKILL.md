---
name: export-publish
description: Use when packaging an approved Type I short for upload — generating title/thumbnail via vidIQ, assembling metadata from the values library, and creating/updating the Airtable "videos" record linked to scripts, visual assets and audio assets. Eighth and final stage of the Type I pipeline.
---

# Exportación + Publicación-Ready + Airtable

## Cuándo usar este skill

Después de que `07-qa-checklist` apruebe el short.

## Input

```json
{
  "script_id": "string",
  "final_video": "path",
  "narrative_approach": "de 01-historytelling-design",
  "historical_figure": "string"
}
```

## Proceso

1. **Título y thumbnail**: generar vía tus herramientas vidIQ ya disponibles (`vidiq_generate_titles`, `vidiq_generate_thumbnail`, `vidiq_score_title`/`vidiq_score_thumbnail` para validar antes de fijar).
2. **Metadata**: título, descripción, tags — tomar la lección de valores de la tabla "values library" en Airtable como base de la descripción/CTA.
3. **Registro en Airtable** (9 tablas — `videos`, `scripts`, `visual assets`, `audio assets`, `performance metrics`, `expenses`, `research sources`, `production checklists`, `values library`):
   - Crear/actualizar registro en `videos` enlazando: el guion (`scripts`), los keyframes y clips generados (`visual assets`), la pista de VO (`audio assets`), y el resultado del checklist (`production checklists`).
   - Ver `scripts/airtable_sync.py` para una implementación de referencia — **ajustar nombres de campo a tu base real**; dado que ya usas el conector MCP de Airtable para gestión de base de datos, priorizar ese conector o el nodo nativo de Airtable en n8n sobre este script si están disponibles en el entorno de ejecución.
4. **Bundle final**: video + thumbnail + metadata, listo para subir.

## Output

```json
{
  "script_id": "string",
  "upload_bundle": {
    "video": "path",
    "thumbnail": "path",
    "title": "string",
    "description": "string",
    "tags": ["string"]
  },
  "airtable_record_id": "string"
}
```

## Fin del pipeline Tipo I

El short queda listo para publicación manual o automatizada (n8n) en el canal.
