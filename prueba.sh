#!/bin/bash

# Ruta del archivo de sonido (cámbiala si usas otro archivo)
ALARM_SOUND="$HOME/Desktop/alarm-26718.mp3"

# Verificar si 'mpv' está instalado
if ! command -v mpv &> /dev/null; then
    echo "Instalando mpv..."
    sudo apt install -y mpv
fi

# Archivo donde se encuentra el estado de la batería
BATTERY_STATUS="/sys/class/power_supply/BAT0/status"

# Mensaje inicial
echo "🔒 Alarma anti-robo activada. Si desconectan la corriente, sonará la alarma."


while true; do
    if [ -f "$BATTERY_STATUS" ]; then
        STATUS=$(cat "$BATTERY_STATUS")

        if [ "$STATUS" == "Discharging" ]; then
            echo "⚠️  ¡Batería desconectada! Activando alarma..."
            
            # Reproducir alarma en bucle hasta que se reconecte la corriente
            while [ "$(cat $BATTERY_STATUS)" == "Discharging" ]; do
                mpv --loop=inf alarm-26718.mp3


            done

            echo "🔌 Batería reconectada. Alarma desactivada."
        fi
    else
        echo "No se pudo detectar el estado de la batería."
        exit 1
    fi

    sleep 2  # Revisar cada 2 segundos
done
