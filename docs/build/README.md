# Compilación y distribución

Se requiere GNU Make y Python 3.10 o posterior.

```sh
make deps-smx
make build-smx
make validate-modes
make package-modes
make release
make validate-artifact
```

`deps-smx` descarga el compilador y los includes de SourceMod en `.deps/smx/`.
`SOURCEMOD_VERSION` selecciona la rama del SDK y su valor predeterminado es
`1.12`. Se puede usar un SDK instalado con `make build-smx SPCOMP=/ruta/a/spcomp`.
Las rutas de Make se resuelven desde el repositorio.

`build-smx` compila los entrypoints del
[mapa de producto](../../scripts/package/package-map.json) con los includes
del SDK y los versionados por el modo. Genera los plugins bajo
`.build/smx/addons/sourcemod/plugins/optional/` y el diagnóstico en
`.build/build-smx-compile.log`.

## Paquete local

- `validate-modes` revisa archivos seleccionados, destinos de `exec`, el árbol
  de Stripper y las llamadas de carga de los plugins propios.
- `package-modes` valida la compilación y prepara `.build/package-modes/`.
  Compara las huellas de las fuentes, los includes locales y los SMX con el
  registro creado por `build-smx`.
- `release` prepara el staging y genera `dist/release/scavogl-rework-local.zip`.
- `validate-artifact` verifica los nombres y bytes del ZIP contra los archivos
  actuales y la compilación. Pasa el mismo `RELEASE_BASENAME` a `release` y
  `validate-artifact` para usar otro nombre.

Las variantes seleccionables son scavogl, scav1v1, scav2v2 y scav3v3. El ZIP lleva la configuración
del modo, plugins recompilados, fuentes, recursos seleccionados y los
[avisos de autoría y licencia](../../NOTICES.md). El registro interno de
compilación queda en `.build/smx/`.

## Dependencias y verificación

En la copia revisada de L4D2-Competitive-Rework (`0390482d`) se encontraron
los 96 plugins externos referenciados por las configuraciones de carga.
`cvar_tracking.cfg` está en esa base. `confogl_rates.cfg` y
`confogl_personalize.cfg` se deben verificar en el perfil del servidor.

Verifica BuiltinVotes y Left4DHooks, incluida la gamedata
`left4dhooks.l4d2.txt`. La gamedata histórica `l4d2_fix_scvng_firsthit.txt`
queda fuera del paquete porque su plugin se retiró.

### Source Scramble

| Ruta o componente | Responsabilidad |
|---|---|
| `addons/sourcemod/scripting/include/sourcescramble.inc` | Include de compilación copiado byte a byte de [L4D2-Competitive-Rework en `0390482d`](https://github.com/SirPlease/L4D2-Competitive-Rework/blob/0390482d48ee87ba16ecb39490dc6f235dbdc1e0/addons/sourcemod/scripting/include/sourcescramble.inc). |
| `addons/sourcemod/plugins/optional/scavenge_no_starting_items.smx` | Plugin que Confogl carga para Scavogl y que requiere la extensión en runtime. |
| `addons/sourcemod/gamedata/scavenge_no_starting_items.txt` | Gamedata que acompaña al plugin en el ZIP del modo. El plugin aplica y revierte el cambio al cargarse y descargarse. |
| `sourcescramble.ext.so` o `sourcescramble.ext.dll` | Extensión compartida que instala la base de L4D2-Competitive-Rework. |

El ZIP de Scavogl contiene el plugin y su gamedata. El include se usa en
la compilación y la extensión se instala con la base. Scavogl administra
su parche directamente y puede funcionar sin `sourcescramble_manager.smx`.

En SRCDS, verifica que la extensión de la base aparezca en `sm exts list`.
Carga Scavogl y confirma la retirada de los objetos iniciales. Después
cambia de modo y comprueba que el comportamiento inicial se haya restaurado.

La aceptación en SRCDS requiere comprobar la activación, el inicio de ronda,
el cambio de modo y la restauración de cvars. La validación offline cubre
el contenido del paquete. Los pendientes para una publicación se registran
en `NOTICES.md`.

## GitHub Actions

El [workflow de compilación](../../.github/workflows/sourcemod-build.yml)
ejecuta los siguientes jobs en orden:

| Job | Operación |
|---|---|
| `deps-smx` | Valida `SOURCEMOD_VERSION` y prepara el SDK con `make deps-smx` cuando falta en la caché. |
| `build-smx` | Restaura el SDK preparado y ejecuta `make build-smx` con `spcomp64`. Entrega los SMX y el registro de compilación al job siguiente. |
| `package` | Descarga la compilación de la misma revisión Git y ejecuta `make validate-modes`, `make release` y `make validate-artifact`. Sube el ZIP con el SHA de la ejecución en el nombre. |

La caché distingue la rama del SDK, el sistema, la arquitectura y el
código de preparación de dependencias. La publicación de releases se
gestiona por separado.
