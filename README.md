# Scavogl Rework v2.4.0

[EN] [translation](https://translate.google.com/translate?sl=es&tl=en&u=https://github.com/AoC-Gamers/scavogl_rework)

Scavogl Rework es una configuración competitiva para Left 4 Dead 2, diseñada para mejorar y estructurar el modo Scavenge en un entorno más equilibrado y competitivo.

## Características

### General
- Basado en ZoneMod y otras configuraciones competitivas.
- Bloqueo de recogida de píldoras y adrenalina durante ready-up de Scavenge, comprobado en un servidor local.

### Scavogl 2v2 y 1v1
- Incrementa el tiempo de bonificación por puntuación en Scavenge de 20 a 25 segundos.

### ScavHunter (4v4, 3v3, 2v2, 1v1)
- Mantienen las mismas características que la configuración base, pero se limitan a solo Hunters.
- Solo permite el uso de Hunters como Infectados Especiales.

## Instalación
1. Scavogl Rework requiere el proyecto base [L4D2-Competitive-Rework](https://github.com/SirPlease/L4D2-Competitive-Rework). Descárgalo e instálalo primero.
2. Con GNU Make y Python 3.10 o posterior, genera el ZIP local con `make deps-smx`, `make build-smx` y `make release`.
3. Copia las rutas `cfg/` y `addons/sourcemod/` declaradas dentro del ZIP a `left4dead2/` en el servidor.
4. Verifica los proveedores indicados en [NOTICES.md](NOTICES.md) y registra el modo como se muestra abajo.

Source Scramble viene con la base de L4D2-Competitive-Rework. Scavogl
usa esa instalación para `scavenge_no_starting_items`.

## Configuración

### Agregar modo de juego
Para habilitar *Scavogl Rework* en las votaciones del servidor, edita el archivo `addons/sourcemod/configs/matchmodes.txt` y agrega:

```plaintext
"MatchModes"
{
    "ScavOgl Rework Configs"
    {
        "scavogl"
        {
            "name" "ScavOgl Rework"
        }
        "scav3v3"
        {
            "name" "3v3 ScavOgl"
        }
        "scav2v2"
        {
            "name" "2v2 ScavOgl"
        }
        "scav1v1"
        {
            "name" "1v1 ScavOgl"
        }
    }
}
```
Luego, reinicia el servidor para aplicar los cambios.

## Contribuciones
Gracias por tu interés en contribuir a *Scavogl Rework*, Puedes reportar problemas o sugerir mejoras a través de la [página de issues](https://github.com/AoC-Gamers/scavogl_rework/issues) o enviando un *pull request* en el [repositorio de GitHub](https://github.com/AoC-Gamers/scavogl_rework/pulls).

## Licencias y autoría

Las configuraciones de Confogl declaran CC BY-SA 3.0. Consulta
[NOTICES.md](NOTICES.md) para la procedencia, licencias de los plugins
y componentes pendientes de confirmar.

# Copyright
*Scavogl Rework* es es una adaptación de "ScavOgl".
Todos los complementos y códigos acondicionados son de sus respectivos autores.
```
- https://github.com/SirPlease/L4D2-Competitive-Rework
- https://github.com/HouseHse/Scavogl
- https://code.google.com/archive/p/scavogl/
- https://github.com/Target5150/MoYu_Server_Stupid_Plugins/
- https://github.com/blueblur0730/modified-plugins
```

