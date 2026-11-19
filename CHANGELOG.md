# Changelog

## [Unreleased]

### Cambiado

- La extensión Source Scramble se toma de L4D2-Competitive-Rework. El ZIP
  incluye el plugin que la usa y su gamedata.

### Corregido

- Stripper aplica los ajustes de recogida de armas cuerpo a cuerpo, objetos
  genéricos y píldoras por clase de entidad, como en ZoneMod.
- Los perfiles reducidos usan sus límites generales de comunes y prescinden
  de la carga del complemento de Cvars por mapa.
- Los cuatro perfiles de ScavOgl usan Plugin Manager al salir del modo.
- Durante el ready-up de Scavenge, los supervivientes ya no pueden recoger
  píldoras ni adrenalina mediante las rutas cubiertas por SDKHooks. La entrega
  de píldoras al iniciar la ronda conserva su configuración.

### Desarrollo

- Make y GitHub Actions compilan los plugins desde las fuentes y validan el
  ZIP con la configuración, los filtros y los recursos de Scavogl.
