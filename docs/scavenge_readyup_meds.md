# Protección de medicinas durante ready-up

Implementación local para el [issue #8](https://github.com/AoC-Gamers/Scavogl-Rework/issues/8).
**Estado: compilada; pendiente de validación en servidor.** No se ha reproducido
el fallo ni ejecutado la matriz de aceptación en juego. `competitive_dev` está
reservado para el trabajo de una extensión y no se modificó.

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
de píldoras o adrenalina, se aplica la misma condición de bloqueo; su ruta de
recogida y la conservación del stock siguen pendientes de pruebas en juego.

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
La salida normal del modo usa `pred_unload_plugins`.

El diagnóstico indica cliente, bot, entidad y classname,
sin limitar la frecuencia. Solo se ejecuta
con el plugin habilitado, en Scavenge y durante ready-up con ReadyUp disponible. Incluye las
entidades spawn identificadas como medicinas **si llegan al hook**. No instrumenta
`Use`, ni demuestra que un spawn no haya consumido stock.
Desactivar el diagnóstico al terminar.

## Compilación local

SourcePawn Compiler **1.12.0.7255**, includes SDK de esa distribución e includes
del repositorio: **sin errores ni advertencias**. El repositorio no dispone de
Makefile; se compiló directamente el entrypoint:

```bash
# Desde la raíz del repositorio; SM_SCRIPTING apunta al SDK Linux de SourceMod.
"$SM_SCRIPTING/spcomp" addons/sourcemod/scripting/scavenge_readyup_meds.sp \
  -iaddons/sourcemod/scripting/include -i"$SM_SCRIPTING/include" \
  -oaddons/sourcemod/plugins/optional/scavenge_readyup_meds.smx
```

El binario versionable se incluye en `plugins/optional`, siguiendo el repositorio.
También se compiló con los includes del checkout base
`L4D2-Competitive-Rework` (`0390482d48ee87ba16ecb39490dc6f235dbdc1e0`):
compilación exitosa con una advertencia de deprecación en su `halflife.inc`
(`CreateDialog`), externo a este cambio. El binario entregado usa el SDK indicado
arriba, sin esa advertencia.

## Validación pendiente

Registrar las versiones realmente instaladas de SourceMod, SDKHooks,
Left4DHooks, ReadyUp y `starting_items` antes de probar. El diagnóstico estático
se basó en `starting_items` 2.2.1 del checkout base: da píldoras al pasar a live
solo si el slot médico está vacío; ReadyUp pone `inReadyUp = false` antes de
emitir `OnRoundIsLive`.

Ejecutar en Dark Carnival Motel (`c2m1_highway`) y The Passing Port
(`c6m3_port`), primero sin protección y después con ella:

- T01–T04: píldoras, adrenalina, objetos caídos y spawns multiuso. Comprobar
  callbacks, inventario, entidad y stock antes/después; incorporar otra ruta
  de bloqueo únicamente si las pruebas la justifican.
- T05–T09: cuenta atrás, cancelación, entrega inicial al pasar a live y recogida,
  uso, paso y drop posteriores. Comparar el total de medicinas entre ambos casos.
- T10–T15: bots, otros equipos, recarga con clientes, ConVar deshabilitada,
  salida del modo, ReadyUp ausente/retirado, cambio de mapa y siguiente mitad.
- T16–T18: mapas sin medicinas, tamaños 1v1–4v4 y Hunters, latencia y spam de uso.

La compilación y el mensaje de diagnóstico no prueban la conservación del recurso.
No dar por resuelto el issue hasta verificar estos resultados en juego.
