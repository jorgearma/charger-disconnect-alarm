# Alarma Anti-Robo para Laptop

Este script en Python está diseñado para evitar el robo de tu laptop cuando te encuentras en un lugar público, como una biblioteca o cafetería, y necesitas alejarte momentáneamente. Funciona activando una alarma sonora y enviando un correo de alerta cuando se detecta que el cargador ha sido desconectado.

## Características
- Detecta la desconexión del cargador de la laptop.
- Reproduce una alarma sonora hasta que el cargador sea reconectado.
- Envía una notificación por correo electrónico.
- Deshabilita las teclas de volumen para evitar que el ladrón silencie la alarma.
- Desactiva las opciones de apagado, suspensión y reinicio del sistema.

## Requisitos
- Python 3
- Librerías requeridas:
  - `smtplib`
  - `ssl`
  - `time`
  - `psutil`
  - `subprocess`
  - `os`
  - `email`
  - `dotenv`
- Cliente de correo Gmail (se requieren credenciales configuradas en un archivo `.env`).
- `mpv` instalado para reproducir el sonido de alarma.

## Instalación
1. Clona este repositorio o descarga el archivo.
2. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install psutil python-dotenv
   ```
3. Crea un archivo `.env` en el mismo directorio y añade las credenciales de tu cuenta de Gmail:
   ```env
   GMAIL_USER=tu_correo@gmail.com
   GMAIL_PASSWORD=tu_contraseña
   ```
4. Asegúrate de tener un archivo de audio de alarma en el mismo directorio con el nombre `alarm-26718.mp3` o modifica el script para usar otro sonido.

## Uso
Ejecuta el script con el siguiente comando:
```bash
python alarma.py
```
Una vez activado, si alguien desconecta el cargador de la laptop:
- Se activará la alarma sonora.
- Se enviará una notificación por correo.
- El sistema bloqueará las teclas de volumen y deshabilitará los botones de apagado, suspensión y reinicio.

Para detener el script, presiona `Ctrl + C`.

## Notas
- Para evitar que el sistema entre en suspensión, el script ejecuta un comando para deshabilitar la suspensión automática.
- Asegúrate de probar el script antes de usarlo en público.
- Puede ser necesario ejecutar el script con permisos de administrador en algunos sistemas.

## Licencia
Este proyecto es de código abierto y se distribuye bajo la licencia MIT.

