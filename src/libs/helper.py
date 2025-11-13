import shutil

def center_text(text: str) -> str:
    """Return text roughly centered in terminal width."""
    width = shutil.get_terminal_size().columns
    padding = max((width - len(text)) // 2, 0)
    return " " * padding + text