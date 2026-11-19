# Trabajo en Scavogl-Rework

Consulta [el índice de documentación](docs/README.md) y
[la guía de compilación](docs/build/README.md) antes de editar.

- Conserva los IDs de Confogl, el orden de carga y descarga, los nombres de
  plugins y las rutas de Stripper, fuentes y recursos de SourceMod.
- Compila con el Makefile raíz. El mapa de producto en
  `scripts/package/package-map.json` declara los entrypoints. Genera y valida el ZIP con
  `make release` y `make validate-artifact`. Las salidas quedan en
  `.deps/`, `.build/` y `dist/`.
- Conserva autoría y licencias. Los cambios remotos y el despliegue requieren autorización.

## Actualizar la base de ZoneMod

1. Toma la versión, el SHA y los pares de perfiles de la
   [referencia técnica](docs/mode/zonemod-baseline.md). Compara la revisión
   registrada con la candidata. Sigue los `exec` de cada tamaño y revisa
   los cambios de Plugin Manager, ReadyUp, Stripper y demás proveedores.
2. Compara la nueva base con los cuatro perfiles de ScavOgl y su
   configuración compartida. Aplica los cambios acordados y conserva la
   puntuación por bidones, las mitades, la serie y las reglas de ScavHunters.
   Revisa el efecto en Scavenge antes de incorporar datos de mapas, filtros
   o reglas de Versus. Ajusta el mapa de producto si cambian los recursos
   instalables o sus referencias externas.
3. Ejecuta `make validate-modes`, `make release` y `make validate-artifact`.
   Si falta una compilación válida o cambian fuentes o includes, sigue la
   guía de compilación y ejecuta `make build-smx` antes de empaquetar.
   Actualiza la revisión y el alcance de la
   sincronización en la referencia técnica y anota los cambios de
   comportamiento en el changelog.
