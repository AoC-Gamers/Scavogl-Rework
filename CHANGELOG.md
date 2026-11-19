# Changelog

## [2.4.0] - 2026-11-19

### Añadido

- `scavenge_readyup_meds` bloquea la recogida de píldoras y adrenalina
  durante ReadyUp. La entrega de píldoras al iniciar la ronda conserva su
  configuración. Queda pendiente la prueba en SRCDS.

### Cambiado

- La extensión Source Scramble se toma de L4D2-Competitive-Rework. El ZIP
  incluye el plugin que la usa y su gamedata.

### Corregido

- Stripper aplica los ajustes de recogida de armas cuerpo a cuerpo, objetos
  genéricos y píldoras por clase de entidad, como en ZoneMod.
- Los perfiles reducidos usan sus límites generales de comunes y prescinden
  de la carga del complemento de Cvars por mapa.
- Los cuatro perfiles de ScavOgl usan Plugin Manager al salir del modo.
- Los plugins gestionan la limpieza de bidones y el cierre de ronda mediante
  eventos de Scavenge. El reinicio tras finalizar la serie cancela cualquier
  temporizador anterior.

### Desarrollo

- Make y GitHub Actions compilan los plugins desde las fuentes y validan el
  ZIP con la configuración, los filtros y los recursos de Scavogl.
