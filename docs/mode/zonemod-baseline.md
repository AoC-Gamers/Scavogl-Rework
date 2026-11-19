# Base de ZoneMod para ScavOgl

| Referencia | Valor |
| --- | --- |
| Base | [SirPlease/L4D2-Competitive-Rework](https://github.com/SirPlease/L4D2-Competitive-Rework) |
| Versión comparada | ZoneMod **v2.9.2b** |
| Revisión comparada | [`0390482d48ee87ba16ecb39490dc6f235dbdc1e0`](https://github.com/SirPlease/L4D2-Competitive-Rework/tree/0390482d48ee87ba16ecb39490dc6f235dbdc1e0/cfg/cfgogl) |
| Modo de destino | ScavOgl Rework **v2.4.1**, sobre Scavenge |

Los perfiles se compararon por tamaño. Las variantes reducidas heredan los CFG compartidos de su modo principal.

| Formato | ScavOgl | ZoneMod | Tiempo añadido por bidón |
| --- | --- | --- | --- |
| 4v4 | [`scavogl`](../../cfg/cfgogl/scavogl/confogl.cfg) | `zonemod` | 20 s |
| 3v3 | [`scav3v3`](../../cfg/cfgogl/scav3v3/confogl.cfg) | `zm3v3` | 20 s |
| 2v2 | [`scav2v2`](../../cfg/cfgogl/scav2v2/confogl.cfg) | `zm2v2` | 25 s |
| 1v1 | [`scav1v1`](../../cfg/cfgogl/scav1v1/confogl.cfg) | `zm1v1` | 25 s |

## Apagado sincronizado

Los cuatro perfiles pasan por el [CFG compartido de apagado](../../cfg/cfgogl/scavogl/confogl_off.cfg). Tras restablecer los ajustes de Confogl, el CFG ejecuta `pm_unload_plugins refresh`. Plugin Manager lo aporta la base. Se verificaron las cuatro cadenas de apagado en el ZIP local.

## Reglas propias de Scavenge

| Área | Comportamiento de ScavOgl |
| --- | --- |
| Objetivo y reloj | Los cuatro perfiles fijan `mp_gamemode scavenge`. Los bidones suman tiempo mediante `scavenge_score_bonus_time`. El modo omite el plugin de puntuación híbrida de Versus. |
| Mitades y cierre anticipado | [`scavenge_quick_end`](../../addons/sourcemod/scripting/scavenge_quick_end.sp) compara los tiempos y el resultado de la primera mitad para cerrar antes la segunda cuando se cumplen sus condiciones. `sm_time` muestra tiempos y puntuación de bidones. |
| Series y reinicio | [`scavenge_rounds`](../../addons/sourcemod/scripting/scavenge_rounds.sp) ofrece `sm_scavrounds` para votar 1, 3 o 5 rondas. El valor por defecto es 5 y el reinicio tras finalizar la serie está habilitado por defecto. |
| Clases y ScavHunters | [`scavenge_gamemode`](../../addons/sourcemod/scripting/scavenge_gamemode.sp) aplica límites de infectados según el tamaño. `sm_scavmode` permite votar entre ScavOgl y ScavHunters dentro del tamaño activo. ScavHunters modifica los límites de clase dentro de los cuatro perfiles Confogl. |
| Bidones fuera del área | [`l4d2_scav_gascan_selfburn`](../../addons/sourcemod/scripting/l4d2_scav_gascan_selfburn.sp) enciende los bidones al superar los límites definidos en su [archivo de datos para seis mapas](../../addons/sourcemod/data/l4d2_scav_gascan_selfburn.cfg). |
| Medicina | [`scavenge_no_starting_items`](../../addons/sourcemod/scripting/scavenge_no_starting_items.sp) retira kits y píldoras iniciales mediante Source Scramble de la base. [`scavenge_readyup_meds`](../scavenge_readyup_meds.md) bloquea recoger píldoras y adrenalina durante ready-up. |
| Jefes | Los cuatro perfiles fijan `sm_tank_can_spawn 0` y `sm_witch_can_spawn 0`. La [carga compartida](../../cfg/cfgogl/scavogl/shared_plugins.cfg) omite los plugins de jefes, sus votaciones y sus reglas por mapa de ZoneMod. |

## Límites de comunes

ScavOgl usa los límites generales de `z_common_limit` del `confogl.cfg` de cada perfil. En orden de 4v4 a 1v1 son 30, 18, 10 y 5. ScavOgl prescinde de `mapcvars.txt` y de la carga de `l4d_mapbased_cvars`. ZoneMod aplica ajustes por mapa en sus formatos reducidos.

## Pase de píldoras y adrenalina

ScavOgl usa `fix_pill_pass` de la base con `fix_pill_pass_reload 1`,
como ZoneMod. El ajuste habilita el pase por recarga. [Carga compartida](../../cfg/cfgogl/scavogl/shared_plugins.cfg) ·
[Ajustes compartidos](../../cfg/cfgogl/scavogl/shared_settings.cfg).

El bloqueo de recogida durante ReadyUp y el pase entre supervivientes
usan rutas distintas.

## Diferencias pendientes de revisión

| Área | Configuración vigente y punto pendiente |
| --- | --- |
| Datos de mapas | ScavOgl carece de `mapinfo.txt` y fija `confogl_itemtracking_mapspecific 0`. Queda por revisar si algún dato de mapa de ZoneMod es aplicable a Scavenge. |
| Stripper | Los 17 selectores de recogida del [filtro global](../../cfg/stripper/scavogl/global_filters.cfg) ya coinciden con ZoneMod y usan `classname`. Queda por revisar el resto de las diferencias en filtros globales y por mapa según su efecto en Scavenge. |
| Armas, objetos y balance | Los [ajustes compartidos](../../cfg/cfgogl/scavogl/shared_settings.cfg) conservan conversiones y atributos de armas distintos, `steady_boost` para infectados, godframes del Hunter de `1.8`, flags de infectados poco comunes de `55` y perdigón central en `0`. También difieren las reglas de retirada de objetos y los ajustes de aparición de píldoras. |

El bloqueo de recogida durante ready-up se comprobó en un servidor local. [Prueba de recogida](../scavenge_readyup_meds.md) · [Guía de compilación y distribución](../build/README.md).
