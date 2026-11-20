# Cola de revisión QA — mockup

UI de la etapa [7] (`skills/07-qa-checklist/`): panel para revisar en lote los shorts que
llegan a QA, con filtros por estado y acciones de aprobar/rechazar/regenerar etapa.

**Versión viva (interactiva):** https://claude.ai/artifact/QpfQhEjPNeTUVfctFx4Up8

`Main.dc.html` y `canvas.json` son el código fuente de ese artifact (formato Claude
Design-canvas). Están aquí para que el diseño quede versionado junto al resto del
pipeline, no para que se ejecuten sueltos fuera de Claude.

## Qué muestra

- 5 tiles de resumen (total del lote, pendiente, en producción, rechazado, aprobado).
- Tabs filtrables por estado.
- Tarjetas por short: figura histórica, etapa actual (1-8), estado con color, nota del
  hallazgo de QA, y botones contextuales — "Aprobar"/"Rechazar" si está pendiente,
  "Regenerar etapa N" si fue rechazado.

## Estado actual — qué falta para que sea real

Este mockup usa **datos de muestra hardcodeados** en el `constructor()` del componente
(8 shorts ilustrativos, incluyendo el caso real de Ada Lovelace del `test-run-ada-lovelace.md`
de la raíz del paquete). Dos piezas quedan pendientes antes de operar con él en producción:

1. **Datos reales desde Airtable** — reemplazar `this.state.items` por una lectura de las
   tablas `videos` / `production checklists` vía el conector MCP de Airtable (o
   `scripts/airtable_sync.py` como respaldo), en vez de la lista fija actual.
2. **Acciones con efecto real** — los botones `approve()`, `reject()` y `regenerate()`
   hoy solo llaman `this.setState(...)` localmente. Para que "Regenerar etapa N" dispare
   de verdad la etapa correspondiente del pipeline, hay que conectarlos a tu
   orquestador (n8n, un script, o lo que estés usando — ver nota sobre n8n en
   `skills/07-qa-checklist/SKILL.md`: es una opción de orquestación, no una dependencia
   dura del contrato de ningún skill).

Hasta que esas dos piezas estén conectadas, trátalo como prototipo de UX para validar la
forma del flujo, no como la cola de revisión operativa.
