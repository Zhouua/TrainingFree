import importlib
import json
import pathlib

from mcp.server.fastmcp import FastMCP

schema = json.loads(pathlib.Path("manifest.json").read_text())

cls_module = importlib.import_module("runner")
inst = getattr(cls_module, schema["impl_class_name"])()

mcp = FastMCP(schema["impl_class_name"])
for method in schema["impl_methods"]:
    mcp.add_tool(
        fn=getattr(inst, method),
        name=method,
    )

if __name__ == "__main__":
    mcp.run()
