import subprocess
import sys
import argparse


def colorize_output(line):
    if "Enter" in line:
        return f"\033[93m{line}\033[0m"  # Yellow
    elif "Generating" in line:
        return f"\033[92m{line}\033[0m"  # Green
    elif "error" in line.lower():
        return f"\033[91m{line}\033[0m"  # Red
    else:
        return line


def run_ssh_keygen():
    process = subprocess.Popen(
        ["ssh-keygen"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        while True:
            char = process.stdout.read(1)
            if char == "" and process.poll() is not None:
                break
            if char:
                sys.stdout.write(colorize_output(char))
                sys.stdout.flush()
    except KeyboardInterrupt:
        process.terminate()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Run ssh-keygen with optional arguments."
    )
    parser.add_argument(
        "ssh_keygen_args",
        nargs=argparse.REMAINDER,
        help="Arguments to pass to ssh-keygen",
    )
    args = parser.parse_args()

    def run_ssh_keygen_with_args():
        process = subprocess.Popen(
            ["ssh-keygen"] + args.ssh_keygen_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        try:
            while True:
                char = process.stdout.read(1)
                if char == "" and process.poll() is not None:
                    break
                if char:
                    sys.stdout.write(colorize_output(char))
                    sys.stdout.flush()
        except KeyboardInterrupt:
            process.terminate()

    run_ssh_keygen_with_args()
