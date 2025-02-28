# Anti-Theft Alarm for Laptop

This Python script is designed to prevent laptop theft when you are in a public place, such as a library or café, and need to step away momentarily. It works by activating a loud alarm and sending an alert email when it detects that the charger has been unplugged.

## Features
- Detects laptop charger disconnection.
- Plays a loud alarm sound until the charger is reconnected.
- Sends a notification email.
- Disables volume keys to prevent the thief from silencing the alarm.
- Disables shutdown, sleep, and restart options.

## Requirements
- Python 3
- Required libraries:
  - `smtplib`
  - `ssl`
  - `time`
  - `psutil`
  - `subprocess`
  - `os`
  - `email`
  - `dotenv`
- Gmail client (credentials must be set up in a `.env` file).
- `mpv` installed to play the alarm sound.

## Installation
1. Clone this repository or download the file.
2. Install the necessary dependencies by running:
   ```bash
   pip install psutil python-dotenv
   ```
3. Create a `.env` file in the same directory and add your Gmail account credentials:
   ```env
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASSWORD=your_password
   ```
4. Make sure you have an alarm audio file in the same directory named `alarm-26718.mp3` or modify the script to use a different sound.

## Usage
Run the script with the following command:
```bash
python alarma-cuputer-diconed.py
```
Once activated, if someone disconnects the laptop charger:
- The alarm sound will be triggered.
- A notification email will be sent.
- The system will lock volume keys and disable shutdown, sleep, and restart buttons.

To stop the script, press `Ctrl + C`.

## Notes
- To prevent the system from going into sleep mode, the script runs a command to disable automatic suspension.
- Make sure to test the script before using it in public.
- Running the script with administrator privileges may be required on some systems.
- The physical power button (forced shutdown) remains active.
- For greater effectiveness, run the script in the background in a minimized shell; an average thief will not know how to disable it.
- Before running the script, increase the volume to the maximum level to ensure the alarm is as loud as possible.

## License
This project is open-source and distributed under the MIT license.

