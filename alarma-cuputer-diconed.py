import smtplib
import ssl
import time
import psutil
import subprocess
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Datos de Gmail desde las variables de entorno
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
ALARM_SOUND = "alarm-26718.mp3"

print("\U0001F512 Alarma anti-robo activada. Si desconectan la corriente, sonará la alarma.")

# Comando para evitar que el sistema entre en suspensión
def prevent_sleep():
    subprocess.run(["sudo", "systemctl", "mask", "sleep.target", "suspend.target", "hibernate.target", "hybrid-sleep.target"])

# Verificar el estado de la batería
def check_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return battery.power_plugged, battery.percent
        else:
            print("⚠️ No se pudo obtener el estado de la batería.")
            return False, None
    except Exception as e:
        print(f"Error al verificar el estado de la batería: {e}")
        return False, None

# Ejecutar la alarma en bucle
def play_alarm():
    if os.path.exists(ALARM_SOUND):
        subprocess.run(["mpv", "--no-terminal", "--volume=100", ALARM_SOUND])
    else:
        print(f"⚠️ El archivo de alarma '{ALARM_SOUND}' no se encuentra.")

# Enviar correo
def send_email():
    try:
        subject = "⚠️ ¡Alarma! Cargador desconectado"
        body = "Se ha desconectado el cargador. La alarma se ha activado."
        message = MIMEMultipart()
        message["From"] = GMAIL_USER
        message["To"] = GMAIL_USER
        message["Subject"] = Header(subject, 'utf-8')
        message.attach(MIMEText(body, "plain", "utf-8"))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, GMAIL_USER, message.as_string())
            print("Correo electrónico enviado a", GMAIL_USER)
    except Exception as e:
        print(f"Error al enviar correo: {e}")

# Bloquear el volumen
def disable_volume_keys():
    try:
        subprocess.run(["xmodmap", "-e", "keycode 122 = NoSymbol"])
        subprocess.run(["xmodmap", "-e", "keycode 123 = NoSymbol"])
        subprocess.run(["xmodmap", "-e", "keycode 124 = NoSymbol"])
        print("Teclas de volumen desactivadas.")
    except Exception as e:
        print(f"Error al desactivar teclas de volumen: {e}")

# Reactivar el volumen
def enable_volume_keys():
    try:
        subprocess.run(["xmodmap", "-e", "keycode 122 = XF86AudioLowerVolume"])
        subprocess.run(["xmodmap", "-e", "keycode 123 = XF86AudioRaiseVolume"])
        subprocess.run(["xmodmap", "-e", "keycode 124 = XF86AudioMute"])
        print("Teclas de volumen reactivadas.")
    except Exception as e:
        print(f"Error al reactivar teclas de volumen: {e}")

# Deshabilitar apagado desde GNOME
def disable_gnome_power_options():
    try:
        subprocess.run(["gsettings", "set", "org.gnome.desktop.session", "idle-delay", "0"], check=True)
        subprocess.run(["gsettings", "set", "org.gnome.settings-daemon.plugins.power", "power-button-action", "nothing"], check=True)
        print("Opciones de apagado en GNOME deshabilitadas.")
    except subprocess.CalledProcessError as e:
        print(f"Error al deshabilitar opciones de apagado en GNOME: {e}")

# Aplicar restricciones
disable_volume_keys()
disable_gnome_power_options()

try:
    while True:
        plugged, battery_percentage = check_battery_status()
        if not plugged:
            print("⚠️  ¡Batería desconectada! Activando alarma...")
            send_email()
            while not plugged:
                play_alarm()
                plugged, _ = check_battery_status()
            print("🔌 Batería reconectada. Alarma desactivada.")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nScript interrumpido por el usuario.")
finally:
    enable_volume_keys()
