import re


def clean_text(raw_text):
    if raw_text is None:
        return ""

    text = str(raw_text)
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\r", "\n")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "".join(ch for ch in text if ch.isprintable() or ch in "\n\t")
    text = text.replace("\t", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<=[A-Za-z0-9])\n(?=[A-Za-z0-9])", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()
