# workflow_api.json — nota importante

**El archivo `ltx25_flf2v_workflow_api.template.json` en esta carpeta es un esqueleto/plantilla, no el grafo real de ComfyUI.**

No fue posible generar el `workflow_api.json` real de LTX-2.5 FLF2V porque ese archivo depende de:
- Los `class_type` exactos de los custom nodes de LTX-2.5 instalados en tu ComfyUI Cloud (varían según versión del paquete).
- Los IDs de nodo que asigna ComfyUI al armar el grafo (se generan al construirlo, no son predecibles de antemano).
- Los modelos/checkpoints específicos cargados en tu Deployment.

Inventar estos valores produciría un archivo que *parece* válido pero fallaría al ejecutarse — por eso no se incluye como si fuera el real.

## Cómo obtener el archivo real

1. En RunComfy, abre ComfyUI Cloud y construye manualmente el grafo LTX-2.5 FLF2V (nodo de carga de modelo LTX-2.5 → nodo FLF2V con inputs de `first_frame`/`last_frame`/`prompt`/`duration` → nodo de salida de video).
2. Prueba el grafo manualmente con una escena de ejemplo hasta que el resultado sea satisfactorio.
3. **Export (API)** → esto genera el `workflow_api.json` real, con los `class_type` e IDs correctos de tu grafo.
4. **Cloud Save** → empaqueta runtime, custom nodes y modelos en un contenedor reproducible.
5. **Deploy as Deployment** sobre GPU X-Large Plus (L40S).
6. Reemplaza `ltx25_flf2v_workflow_api.template.json` con el archivo exportado real, y usa `scripts/runcomfy_client.py` para las llamadas con `overrides` contra esa Deployment.

## Qué sí documenta la plantilla

`ltx25_flf2v_workflow_api.template.json` documenta la **forma esperada** del objeto `overrides` que se envía en cada llamada por escena, basada en el patrón documentado de RunComfy Serverless API — útil para saber qué construir en el cliente (`runcomfy_client.py`) incluso antes de tener el grafo real exportado.
