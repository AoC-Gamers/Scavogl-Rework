# Autoría y licencias

| Componente | Procedencia y licencia documentada |
|---|---|
| `cfg/cfgogl/scav*/` y `cfg/stripper/scavogl/global_filters.cfg` | Adaptación de ScavOgl y de la base competitiva. Los metadatos de Google Code identifican GPLv3 para el proyecto ScavOgl original. Las cabeceras Confogl declaran CC BY-SA 3.0 y acreditan a Lechuga, Visor, Jahze, ProdigySim, Vintik, CanadaRox, Blade, Tabun, Jacob y Sir. El filtro se conserva según el historial local, con cambios hasta `d49f50c`. El filtro actual difiere de los filtros históricos de ScavOgl y HouseHse del archivo original. Su procedencia exacta y licencia específica están pendientes. |
| `scavenge_gamemode.sp`, `scavenge_rounds.sp`, `scavenge_readyup_meds.sp` y traducciones correspondientes | Lechuga. El historial de las fuentes registra `2b75478`, `6da66b8` y `985922f`. El código y las traducciones de autoría propia de estos tres plugins se ofrecen bajo GPL-3.0-only. El texto completo está en [LICENSE](LICENSE). |
| `l4d2_scav_gascan_selfburn.sp`, sus traducciones y `data/l4d2_scav_gascan_selfburn.cfg` | ratchetx y blueblur. Adaptación de la familia publicada en el repositorio GPLv3 de blueblur, incorporada en `c719965`. La revisión de origen consultada difiere de la copia local. |
| `scavenge_quick_end.sp` y sus traducciones | ProdigySim y blueblur. Adaptación de la familia publicada en el repositorio GPLv3 de blueblur, incorporada en `c719965`. La revisión de origen consultada difiere de la copia local. |
| `scavenge_no_starting_items.sp` y su gamedata | Forgetest. La fuente importada en `387a53e` coincide byte a byte con `15538264` de MoYu Server Stupid Plugins, con GPLv3 en esa revisión. La fuente se modificó posteriormente en Scavogl. La gamedata coincide con la del repositorio de origen consultado. |

Source Scramble es una dependencia GPLv3 de nosoop que instala la base de
L4D2-Competitive-Rework. Para compilar, Scavogl conserva una copia exacta
del `sourcescramble.inc` de la base en `0390482d`. El binario Linux
histórico de Scavogl correspondía al paquete oficial 0.7.1.1. Se retiró
esa copia del repositorio al adoptar la extensión que ya instala la base.

El ZIP excluye la extensión, los includes externos de Source Scramble,
Left4DHooks, Confogl, ReadyUp, BuiltinVotes y Colors, y `original_project.zip`.
Confogl, ReadyUp, BuiltinVotes, Left4DHooks y Stripper se requieren en
runtime. Se omite la gamedata `l4d2_fix_scvng_firsthit.txt`, cuyo plugin
salió del modo en `a338f2b`.

El ZIP de validación local incluye GPLv3 en `LICENSE` y CC BY-SA 3.0 en
`LICENSES/`. Para una publicación queda por verificar la revisión exacta de
las dos adaptaciones de blueblur y el alcance de las declaraciones para
los recursos de terceros, incluidos traducciones, datos y filtros.

- [ScavOgl de HouseHse](https://github.com/HouseHse/Scavogl/tree/a6b15cb646126532bf03b0e57fab7a3507237b8f)
- [Metadatos del proyecto ScavOgl en Google Code](https://storage.googleapis.com/google-code-archive/v2/code.google.com/scavogl/project.json)
- [Base competitiva](https://github.com/SirPlease/L4D2-Competitive-Rework)
- [Fuentes y GPLv3 de blueblur](https://github.com/blueblur0730/modified-plugins/tree/921a3ac5901bbd8e277bc8a683ae70614a3ffb09)
- [Fuentes y GPLv3 de Forgetest](https://github.com/Target5150/MoYu_Server_Stupid_Plugins/tree/155382641b02ff5ae269a6e073e93f080f6cc756)
- [Include de Source Scramble en la base competitiva](https://github.com/SirPlease/L4D2-Competitive-Rework/blob/0390482d48ee87ba16ecb39490dc6f235dbdc1e0/addons/sourcemod/scripting/include/sourcescramble.inc)
- [Paquete histórico Source Scramble 0.7.1.1](https://github.com/nosoop/SMExt-SourceScramble/releases/tag/0.7.1.1)
- [Licencia de Source Scramble 0.7.1.1](https://github.com/nosoop/SMExt-SourceScramble/blob/7754d0d5cf1b601a1961636439ed6f87b36dde8e/LICENSE)
