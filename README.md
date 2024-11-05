# Needlr

![Textual splash image](https://raw.githubusercontent.com/Textualize/textual/main/imgs/textual.png)

[![Discord](https://img.shields.io/discord/1026214085173461072)](https://discord.gg/Enf6Z3qhVr)

Needlr is a Python SDK package for working with Microsoft Fabric. It provides a simple way to use the Microsoft Fabric APIs and includes several utilities for Workspace item management. Needlr is designed to be easy to use and flexible, allowing you to quickly build custom solutions for your business needs.

## Features

- Easy to use client for all Microsoft Fabric APIs
- Complete documentation
- Out-of-the-box examples to help you get started
- Complete Pytests Test for all modules

## Local Environment Setup for Developers

1. [Install uv to your local machine](https://docs.astral.sh/uv/getting-started/installation/)
2. Post-installation, either restart your system or run the commands to set the $Path variable.
3. To test that `uv` works, in an IDE of your choice, open "Terminal" and select *Command Prompt*.
4. In that *Command Prompt*, type in `uv` and press *Enter*.
5. Now that `uv` has been installed and set up, create a virtual environment by running the following command:
`uv venv venv`.
6. Then, activate the virtual environment:
`venv\Scripts\activate`
7. After activating the virtual environment, install the required package dependencies:
`uv pip install -r pyproject.toml`
8. When all dependencies have been installed to the virtual environment, the virtual environment setup is complete.

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
wsname = 'TONIO_WS_TEST_1'
mirrored_ws_id ="27018a3b-d0ad-4925-9757-b09132484480"
semantic_model_ws_id = "e951d4bf-eb6b-4973-8b38-560d91ba57db"
semantic_model_to_delete_id = "d3735118-8aa6-4a76-8033-ea37966e0879"


# Fabric CLient with Interactive Auth
fr = FabricClient(auth=auth.FabricInteractiveAuth(scopes=['https://api.fabric.microsoft.com/.default']))

# Print WOrkspace List
for ws in fr.workspace.ls():
    print(ws.name)

# Create a new workspace
ws = fr.workspace.create(display_name=wsname, 
                         capacity_id='982748D8-27A1-4CC2-A227-F166GF45ABB8', 
                         description='test')
print(ws)

# Create a new Warehouse    
wh = fr.warehouse.create(workspace_id=ws.id, 
                         display_name='New_Warehouse', 
                         description='test')
print(wh)
```

## Documentation

Full documentation is available at [http://needlr.co].

## Contributing

Contributions are welcome! Please read the CONTRIBUTING.md file for guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

Inspired by the capabilities of Microsoft Fabric

Special thanks to the open-source community

## Contact

For questions or feedback, please reach out to [tonio.lora@outlook.com].
