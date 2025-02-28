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

def disable_volume_keys():
    try:
        subprocess.run(["xmodmap", "-e", "keycode 122 = NoSymbol"])
        subprocess.run(["xmodmap", "-e", "keycode 123 = NoSymbol"])

        subprocess.run(['sudo', 'systemctl', 'mask', 'poweroff.target'], check=True)
        
        print("Teclas de volumen desactivadas.")
    except Exception as e:
        print(f"Error al desactivar teclas de volumen: {e}")

def enable_volume_keys():
    try:
        subprocess.run(["xmodmap", "-e", "keycode 122 = XF86AudioLowerVolume"])
        subprocess.run(["xmodmap", "-e", "keycode 123 = XF86AudioRaiseVolume"])

        subprocess.run(['sudo', 'systemctl', 'unmask', 'poweroff.target'], check=True)
        
        print("Teclas de volumen reactivadas.")
    except Exception as e:
        print(f"Error al reactivar teclas de volumen: {e}")


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

def play_alarm_nonblocking():
    if os.path.exists(ALARM_SOUND):
        proc = subprocess.Popen(["mpv", "--no-terminal", "--volume=100", "--loop" , ALARM_SOUND])
        return proc
    else:
        print(f"⚠️ El archivo de alarma '{ALARM_SOUND}' no se encuentra.")
        return None

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

# Aplicar restricciones
disable_volume_keys()


try:
    while True:
        plugged, battery_percentage = check_battery_status()
        if not plugged:
            print("⚠️ ¡Batería desconectada! Activando alarma...")
            send_email()
            alarm_process = play_alarm_nonblocking()
            # Monitorear el estado de la batería mientras la alarma suena
            while not plugged:
                time.sleep(0.5)  # Verifica cada 0.5 segundos
                plugged, _ = check_battery_status()
                if plugged and alarm_process:
                    alarm_process.terminate()  # Terminar la alarma
                    alarm_process = None
                    break
            print("🔌 Batería reconectada. Alarma desactivada.")
            # Reactivar las teclas de volumen inmediatamente al reconectar el cargador
            enable_volume_keys()
        time.sleep(2)
except KeyboardInterrupt:
    print("\nScript interrumpido por el usuario.")
    enable_volume_keys()
