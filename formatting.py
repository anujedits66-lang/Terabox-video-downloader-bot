def format_bytes(size: int | str) -> str:
    try:
        b = int(size)
    except (ValueError, TypeError):
        return "Unknown size"

    if b == 0:
        return "0 B"

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.2f} {unit}"
        b /= 1024

    return f"{b:.2f} PB"
