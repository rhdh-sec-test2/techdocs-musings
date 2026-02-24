from setuptools import setup, find_packages

setup(
    name="mkdocs-cmd-plugin",
    version="0.1.0",
    description="MkDocs plugin that runs id and env commands during build",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["mkdocs>=1.0"],
    entry_points={
        "mkdocs.plugins": [
            "cmd = mkdocs_cmd_plugin:CmdPlugin",
        ]
    },
)
