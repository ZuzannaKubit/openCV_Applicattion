import json
from enum import IntEnum

class Vector3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class BlockType(IntEnum):
    Square = 0
    Circle = 1
    Triangle = 2

class BlockColor(IntEnum):
    Red = 0
    Blue = 1

class BlockData:
    def __init__(self, position, type, color):
        self.position = position
        self.type = type
        self.color = color

class BlockDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BlockData):
            return {"position": obj.position.__dict__, "type": obj.type, "color": obj.color}
        return json.JSONEncoder.default(self, obj)

# vector = Vector3(0.0, 0.5, 1.0)

# color = BlockColor.Red
# blockType = BlockType.Circle
# blockData = BlockData(vector, int(blockType),int(color))

# jsonStr = json.dumps(blockData, cls=BlockDataEncoder)

# print(jsonStr)