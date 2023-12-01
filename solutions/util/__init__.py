import os


def read_input(day):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, f"../../inputs/{day:02d}.txt")
    lines = None
    with open(abs_file_path, 'r') as file:
        lines = file.read().split("\n")
    if lines[-1].strip() == "":
        return lines[:-1]
    return lines
