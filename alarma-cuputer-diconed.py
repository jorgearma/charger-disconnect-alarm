import os
import time
import psutil
import subprocess

# Ruta del archivo de sonido (cámbiala si usas otro archivo)
ALARM_SOUND = "alarm-26718.mp3"

# Mensaje inicial
print("🔒 Alarma anti-robo activada. Si desconectan la corriente, sonará la alarma.")

# Comando para evitar que el sistema entre en suspensión
def prevent_sleep():
    subprocess.run(["sudo", "systemctl", "mask", "sleep.target", "suspend.target", "hibernate.target", "hybrid-sleep.target"])

# Verificar el estado de la batería
def check_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return battery.power_plugged, battery.percent
    return False, None

# Ejecutar la alarma en bucle
def play_alarm():
    subprocess.run(["mpv", "--no-terminal", ALARM_SOUND])
while True:
    plugged, battery_percentage = check_battery_status()

    if not plugged:  # Si la batería está desconectada
        print("⚠️  ¡Batería desconectada! Activando alarma...")
        while not plugged:  # Reproducir la alarma hasta que se reconecte
            play_alarm()
            plugged, _ = check_battery_status()
        print("🔌 Batería reconectada. Alarma desactivada.")
    
    time.sleep(2)  # Revisar cada 2 segundos