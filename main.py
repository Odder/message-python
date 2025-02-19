import subprocess
import sys
import os
import time


def start_process(cwd):
    return subprocess.Popen([sys.executable, "main.py"], cwd=cwd)


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Start the three services.
    qs_dir = os.path.join(root_dir, "queue_service")
    print("Starting queue_service...")
    qs_proc = start_process(qs_dir)
    time.sleep(1)

    fr_dir = os.path.join(root_dir, "file_reader")
    print("Starting file_reader...")
    fr_proc = start_process(fr_dir)
    time.sleep(1)

    fw_dir = os.path.join(root_dir, "file_writer")
    print("Starting file_writer...")
    fw_proc = start_process(fw_dir)
    time.sleep(1)

    print("All services started.")
    print("Enter commands in the format: <input_file> <output_file>")

    try:
        while True:
            cmd = input("Enter command: ").strip()
            if cmd.lower() == "exit":
                break

            command_file = os.path.join(root_dir, "command.txt")
            with open(command_file, "w", encoding="ascii") as f:
                f.write(cmd)
            print("Command sent. Waiting for processing...")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    print("Terminating services...")
    fr_proc.terminate()
    fw_proc.terminate()
    qs_proc.terminate()
    fr_proc.wait()
    fw_proc.wait()
    qs_proc.wait()
    print("All services terminated.")


if __name__ == '__main__':
    main()
