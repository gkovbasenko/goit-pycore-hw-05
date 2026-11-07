def parse_input(user_input):
    parts = user_input.split()
    if not parts:
        return "",
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return cmd, *args