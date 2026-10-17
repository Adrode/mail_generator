import sys
import json
import struct
import traceback
from datetime import datetime
from pathlib import Path

script_dir = Path(__file__).resolve().parent

def read_message():
    raw_length = sys.stdin.buffer.read(4)

    if not raw_length:
        return None

    message_length = struct.unpack("=I", raw_length)[0]

    message = sys.stdin.buffer.read(message_length)

    return json.loads(message.decode("UTF-8"))

def send_message(message):
    encoded = json.dumps(message).encode("UTF-8")

    sys.stdout.buffer.write(
        struct.pack("=I", len(encoded))
    )

    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

message = read_message()

if message:
    response = {
        "ok": True,
        "stage": "complete",
        "error": None
    }

    try:
        response["stage"] = "import"

        from outlook_generator.create_outlook_template import generate_mail

        response["stage"] = "validate_html"

        html = message["message"]
        if not html:
            raise ValueError("No HTML was received")

        response["stage"] = "generate_mail"
        generate_mail(message["message"])

        response["stage"] = "complete"

    except Exception as error:
        response["ok"] = False
        response["error"] = str(error)

        with open(script_dir / "error_log.log", "a", encoding="UTF-8") as f:
            f.write(f"\n{datetime.now()} - ERROR:\n")
            f.write(traceback.format_exc())
            f.write("\n" + "-" * 60 + "\n")

    send_message(response)