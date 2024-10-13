"""
This represent a key value pair within bucket
"""
class MapEntry:
    def __init__(self, key: str, value) -> None:
        self.key = key
        self.value = value
    
    def __eq__(self, value: object) -> bool:
        pass