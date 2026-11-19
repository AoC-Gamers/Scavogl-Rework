# Trabajo en Scavogl-Rework

Consulta [el índice de documentación](docs/README.md) y
[la guía de compilación](docs/build/README.md) antes de editar.

- Conserva los IDs de Confogl, el orden de carga y descarga, los nombres de
  plugins y las rutas de Stripper, fuentes y recursos de SourceMod.
- Compila con el Makefile raíz. El mapa de producto en
  `scripts/package/package-map.json` declara los entrypoints. Genera y valida el ZIP con
  `make release` y `make validate-artifact`. Las salidas quedan en
  `.deps/`, `.build/` y `dist/`.
- Conserva autoría y licencias. Distingue compilación, validación offline y
  prueba en SRCDS. Los cambios remotos y el despliegue requieren autorización.
