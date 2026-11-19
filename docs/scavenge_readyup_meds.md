# Protección de medicinas durante ready-up

Implementación local para el [issue #8](https://github.com/AoC-Gamers/Scavogl-Rework/issues/8).

El bloqueo de recogida durante ready-up se comprobó en un servidor local.

## Comportamiento

`scavenge_readyup_meds` usa `SDKHook_WeaponCanUse` para rechazar
`weapon_pain_pills` y `weapon_adrenaline` cuando el plugin está habilitado,
el cliente es superviviente, el modo base es Scavenge y `IsInReady()` devuelve
`true`. Incluye bots y clientes presentes en una carga tardía.

Consulta ReadyUp en cada intento, sin mantener una fase paralela. La cuenta atrás
y su cancelación siguen el estado de esa API. No elimina entidades, cambia
inventarios, repone objetos ni modifica `starting_items` o
`scavenge_no_starting_items`.

ReadyUp es opcional: si falta o se descarga, permite recoger y emite una
advertencia por consola al detectar la ausencia inicial o la retirada. En ese
estado no ofrece protección del balance. SDKHooks y Left4DHooks son dependencias
requeridas; ya forman parte del stack competitivo.

Reutiliza `L4D_GetClientTeam` y `L4D2_GetWeaponId` de
`left4dhooks_stocks.inc`, incluido por `<left4dhooks>`. Inicializa la tabla de
nombres en `OnPluginStart` para evitar su creación en el callback de recogida.
La identificación desde la entidad reconoce también los nombres con sufijo
`_spawn` y el ID de `weapon_spawn`. Si esas entidades llegan al hook con un ID
de píldoras o adrenalina, se aplica la misma condición de bloqueo.

La carga en `cfg/cfgogl/scavogl/shared_plugins.cfg` cubre las cuatro configs
versionadas: `scavogl`, `scav3v3`, `scav2v2` y `scav1v1`. Las variantes Hunters
seleccionadas por `scavenge_gamemode` conservan los plugins de esa config.
No se añaden configs Hunters independientes.

## Controles

| ConVar | Predeterminado | Uso |
|---|---|---|
| `sm_scavenge_readyup_meds_enable` | `1` | `0` permite todas las recogidas. |
| `sm_scavenge_readyup_meds_debug` | `0` | `1` imprime diagnósticos médicos por consola. |

No genera un archivo de configuración automático ni mensajes de chat. Al
descargar el plugin se retiran los hooks; no se restauran las ConVars.
La salida normal del modo usa `pm_unload_plugins refresh`.

El diagnóstico indica cliente, bot, entidad y classname,
sin limitar la frecuencia. Solo se ejecuta
con el plugin habilitado, en Scavenge y durante ready-up con ReadyUp disponible. Incluye las
entidades spawn identificadas como medicinas **si llegan al hook**. No instrumenta
`Use`, ni demuestra que un spawn no haya consumido stock.
Desactivar el diagnóstico al terminar.

## Compilación local

SourcePawn Compiler **1.12.0.7255**, includes SDK de esa distribución e includes
del repositorio: **sin errores ni advertencias** en la validación inicial.
El [Makefile](../Makefile) compila ahora el entrypoint como parte de
`make build-smx`. El ZIP coloca el binario generado en
`addons/sourcemod/plugins/optional/`.

También se compiló con los includes del checkout base
`L4D2-Competitive-Rework` (`0390482d48ee87ba16ecb39490dc6f235dbdc1e0`):
compilación exitosa con una advertencia de deprecación en su `halflife.inc`
(`CreateDialog`), externo a este cambio. El binario entregado usa el SDK indicado
arriba, sin esa advertencia.
