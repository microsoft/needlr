class FabricItem():
    def __init__(self, display_name:str, type_name:str, definition:dict=None, description:str=None) -> None:
        self._displayName = display_name
        self._type = type_name
        self._definition = definition
        self._description = description

    def to_json(self):
        return {
            "displayName": self._displayName,
            "type": self._type,
            "definition": self._definition,
            "description": self._description
        }