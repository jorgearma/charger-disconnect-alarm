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

# Mensaje inicial
print("🔒 Alarma anti-robo activada. Si desconectan la corriente, sonará la alarma.")

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
    if os.path.exists(ALARM_SOUND):  # Verificar si el archivo existe
        subprocess.run(["mpv", "--no-terminal", "--volume=100", ALARM_SOUND])
    else:
        print(f"⚠️ El archivo de alarma '{ALARM_SOUND}' no se encuentra.")

# Función para enviar correo usando Gmail
def send_email():
    try:
        subject = "⚠️ ¡Alarma! Cargador desconectado"
        body = "Se ha desconectado el cargador. La alarma se ha activado."
        
        # Crear el mensaje MIME
        message = MIMEMultipart()
        message["From"] = GMAIL_USER
        message["To"] = GMAIL_USER
        message["Subject"] = Header(subject, 'utf-8')  # Codificación de UTF-8 en el asunto
        message.attach(MIMEText(body, "plain", "utf-8"))

        # Configurar la conexión segura
        context = ssl.create_default_context()

        # Conectar al servidor de Gmail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, GMAIL_USER, message.as_string())  # Enviar correo a ti mismo
            print("Correo electrónico enviado a", GMAIL_USER)

    except smtplib.SMTPException as e:
        print(f"Error de SMTP al enviar correo: {e}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

# Bloquear el volumen y deshabilitar las teclas de volumen
def disable_volume_keys():
    try:
        subprocess.run(["xmodmap", "-e", "keycode 122 = NoSymbol"])  # Desactiva bajar volumen
        subprocess.run(["xmodmap", "-e", "keycode 123 = NoSymbol"])  # Desactiva subir volumen
        subprocess.run(["xmodmap", "-e", "keycode 124 = NoSymbol"])  # Desactiva silenciar
        print("Teclas de volumen desactivadas.")
    except Exception as e:
        print(f"Error al desactivar teclas de volumen: {e}")

# Reactivar las teclas de volumen
def enable_volume_keys():
    try:
        subprocess.run(["xmodmap", "-e", "keycode 122 = XF86AudioLowerVolume"])  # Reactiva bajar volumen
        subprocess.run(["xmodmap", "-e", "keycode 123 = XF86AudioRaiseVolume"])  # Reactiva subir volumen
        subprocess.run(["xmodmap", "-e", "keycode 124 = XF86AudioMute"])         # Reactiva silenciar
        print("Teclas de volumen reactivadas.")
    except Exception as e:
        print(f"Error al reactivar teclas de volumen: {e}")

# Deshabilitar los botones de apagado, suspensión y reinicio
def disable_shutdown_suspend_restart():
    try:
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.lockdown', 'disable-power-off', 'false'], check=True)
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.lockdown', 'disable-suspend', 'false'], check=True)
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.lockdown', 'disable-restart', 'true'], check=True)
        print("Botones de apagado, suspensión y reinicio deshabilitados.")
    except subprocess.CalledProcessError as e:
        print(f"Error al deshabilitar botones: {e}")

# Reactivar los botones de apagado, suspensión y reinicio
def enable_shutdown_suspend_restart():
    try:
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.lockdown', 'disable-power-off', 'true'], check=True)
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.lockdown', 'disable-suspend', 'true'], check=True)
        subprocess.run(['gsettings', 'set', 'org.gnome.desktop.lockdown', 'disable-restart', 'false'], check=True)
        print("Botones de apagado, suspensión y reinicio reactivados.")
    except subprocess.CalledProcessError as e:
        print(f"Error al reactivar botones: {e}")

# Bloquear el volumen y deshabilitar las teclas de volumen
disable_volume_keys()

# Deshabilitar botones de apagado, suspensión y reinicio
disable_shutdown_suspend_restart()

try:
    while True:
        plugged, battery_percentage = check_battery_status()

        if not plugged:  # Si la batería está desconectada
            print("⚠️  ¡Batería desconectada! Activando alarma...")
            send_email()  # Enviar el correo
            while not plugged:  # Reproducir la alarma hasta que se reconecte
                play_alarm()
                plugged, _ = check_battery_status()
            print("🔌 Batería reconectada. Alarma desactivada.")
        
        time.sleep(2)  # Revisar cada 2 segundos para evitar uso excesivo de CPU
except KeyboardInterrupt:
    print("\nScript interrumpido por el usuario.")
finally:
    # Reactivar las teclas de volumen al finalizar
    enable_volume_keys()

    # Reactivar los botones de apagado, suspensión y reinicio
    enable_shutdown_suspend_restart()
