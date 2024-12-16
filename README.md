# Needlr

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![image](https://img.shields.io/pypi/v/uv.svg)](https://pypi.python.org/pypi/uv)
[![image](https://img.shields.io/pypi/l/uv.svg)](https://pypi.python.org/pypi/uv)
[![image](https://img.shields.io/pypi/pyversions/uv.svg)](https://pypi.python.org/pypi/uv)

Needlr is a Python SDK package for working with Microsoft Fabric. It provides a simple way to use the Microsoft Fabric APIs and includes several utilities for Workspace item management. Needlr is designed to be easy to use and flexible, allowing you to quickly build custom solutions for your business needs.

## Features

- Easy to use client for all Microsoft Fabric APIs
- Complete documentation
- Out-of-the-box examples to help you get started
- Complete Pytests Test for all modules

## Installation

To install Needlr, use pip:

```bash
pip install needlr
```

## Quick Start

Here's a quick example to get you started:

```python
from needlr import auth, FabricClient

#Some sample variables
wsname = ""
mirrored_ws_id =""
semantic_model_ws_id = ""
semantic_model_to_delete_id = ""


# Fabric CLient with Interactive Auth
fr = FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

# Print WOrkspace List
for ws in fr.workspace.ls():
    print(ws.name)

# Create a new workspace
ws = fr.workspace.create(display_name=wsname, 
                         capacity_id="", 
                         description="")
print(ws)

# Create a new Warehouse    
wh = fr.warehouse.create(workspace_id=ws.id, 
                         display_name="", 
                         description="")
print(wh)
```

## Documentation

Full documentation is available at [https://needlr.co](https://needlr.co).

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](https://github.com/microsoft/needlr/blob/main/CONTRIBUTING.md) file for guidelines.

## License

This project is licensed under the MIT License. Review the [LICENSE](https://github.com/microsoft/needlr/blob/main/LICENSE) file for more details.

## Acknowledgements

Inspired by the capabilities of Microsoft Fabric

Special thanks to the open-source community

## Contact

For questions or feedback, please reach out to [Tonio Lora](tonio.lora@outlook.com).
