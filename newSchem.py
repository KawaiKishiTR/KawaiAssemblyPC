import mcschematic

class cord:
    def __init__(self, x:int = None, y:int = None, z:int = None, value:tuple = None):
        if value!=None:
            self.value = value
        elif x!=None and y!=None and z!=None:
            self.value = (x, y, z)
        else:
            raise ValueError("not enough value")
    def copy(self):
        return cord(value=self.value)
    def __add__(self, other):
        if not isinstance(other, cord):
            raise ValueError (f"invalid type {type(other)}")
        return cord(value=tuple([self.value[x] + other.value[x] for x in range(3)]))
    def __sub__(self, other):
        if not isinstance(other, cord):
            raise ValueError (f"invalid type {type(other)}")
        return cord(value=tuple([self.value[x] - other.value[x] for x in range(3)]))
    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError (f"invalid type {type(other)}")
        return cord(value=tuple([other*x for x in self.value]))
    def __repr__(self):
        return f"{self.value}"
class direction:
    directions = {}
    def __init__(self, name:str, value:cord):
        self.name = name; self.value = value
        direction.directions[name] = self
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"{self.name} {self.value}"  
    def find_direction(char:str):
        for key,value in direction.directions.items():
            if char.lower() in key.lower():
                return value
    def _rotating(self, number:int,mod:int=4):
        return direction.directions[list(direction.directions.keys())[(list(direction.directions.keys()).index(self.name) + number)%mod]]
    @property
    def right(self):
        return self._rotating(1,4)
    @property
    def left(self):
        return self._rotating(3,4)
    @property
    def back(self):
        return self._rotating(2,4)
    
direction("north", cord(0, 0, -1))
direction("east", cord(1, 0, 0))
direction("south", cord(0, 0, 1))
direction("west", cord(-1, 0, 0))
direction("up", cord(0, 1, 0))
direction("down", cord(0, -1, 0))

def setInstructionMemory(file_name:str, schem:mcschematic.MCSchematic, MD:direction, start_pos:cord) -> None:
    #dosya okuma
    with open(file_name, 'r') as f:
        lines = [line.strip() for line in f]

    #eğer satır sayısı 1024 değilse sonuna ekleme yap
    while len(lines) < 1024:
        lines.append('0000000000000000')
    
    #1024 ün üzerinde ise hata yönlendir
    if len(lines) > 1024:
        raise ValueError("Too Long Code")

    #satırları tek tek işle
    for index, line in enumerate(lines):
        repeater_direction:direction = MD

        #eğer satır 16 uzunluğunda değilse hata yönlendir
        if len(line) != 16:
            raise ValueError(f"invalid data on line:{index}")

        #konum hesaplamaları
        pos = start_pos.copy()
        branchNo:int = index%16
        socketNo:int = index//16
        socket:int = socketNo%32
        isShifted:bool = bool(index %2)
        isReversed:bool = bool(socketNo//32)


        #yapılan hesaplamaya göre pozisyon hizalaması
        if isShifted:
            pos += MD.right.value
        if isReversed:
            pos += MD.value*2
            repeater_direction = repeater_direction.back
        pos += MD.value * 7 * branchNo
        pos += MD.right.value * 2 * socket
        for bitindex, char in enumerate(line):
            subpos:cord = pos + cord(0, -2*bitindex,0)
            if char == '1':
                schem.setBlock(tuple(subpos.value), f"minecraft:repeater[facing={repeater_direction.back.name}]")
            elif char == '0':
                schem.setBlock(tuple(subpos.value), "minecraft:purple_wool")
def resetFileRegister(schem:mcschematic.MCSchematic, MD:direction, start_pos:cord) -> None:
    for side in range(2):
        pos:cord = start_pos.copy()

        #sağ ve sol olarak ikiye böl
        if side:
            repeater_direction:direction = MD.right
            pos += MD.left.value
        else:
            repeater_direction:direction = MD.left
            pos += MD.right.value

        for column_id in range(15):
            column_top:cord = pos.copy()

            #sütun sütun böl
            if column_id%2:
                column_top += direction.directions["up"].value
            column_top += MD.value * (column_id*2)
            
            #her hücreyi sıfırla
            for bit in range(8):
                bit_pos:cord = column_top + direction.directions["down"].value*(bit*2)
                schem.setBlock(bit_pos.value, f"repeater[facing={repeater_direction.name},powered=false,locked=true]")
def resetCallStack(schem:mcschematic.MCSchematic, MD:direction, start_pos:cord) -> None:
    for stack in range(16):
        stack_pos = start_pos + MD.value * (3 * stack)
        for bit in range(10):
            bit_pos = stack_pos + direction.directions["down"].value * (2 * bit)

            schem.setBlock((bit_pos + MD.right.value).value, f"repeater[facing={MD.name},locked=true,powered=false]")
            schem.setBlock((bit_pos + MD.value).value, f"repeater[facing={MD.back.name},locked=true,powered=false]")
def resetProgramCounter(schem:mcschematic.MCSchematic, MD:direction, start_pos:cord) -> None:
    for bit in range(10):
        pos = start_pos + direction.directions["down"].value*(2*bit)
        schem.setBlock(pos.value, f"repeater[facing={MD.name},powered=false,locked=true]")
def resetMemory(schem:mcschematic.MCSchematic, MD:direction, start_pos:cord) -> None:#FIXME:
    resetFileRegister(schem, MD.left, cord(-8, -2, 3))
    resetFileRegister(schem, MD.left, cord(-24, -2, 3))
    resetFileRegister(schem, MD.left, cord(-40, -2, 3))
    resetFileRegister(schem, MD.left, cord(-56, -2, 3))
    resetFileRegister(schem, MD.right, cord(-8, -2, -3))
    resetFileRegister(schem, MD.right, cord(-24, -2, -3))
    resetFileRegister(schem, MD.right, cord(-40, -2, -3))
    resetFileRegister(schem, MD.right, cord(-56, -2, -3))
def resetFlags(schem:mcschematic.MCSchematic, MD:direction, start_pos:cord) -> None:
    schem.setBlock((start_pos + MD.right.value).value,f"repeater[facing={MD.name},powered=false,locked=true]")
    schem.setBlock((start_pos + MD.left.value).value,f"repeater[facing={MD.name},powered=false,locked=true]")



def main(file_name:str, version:mcschematic.Version,start_pos:cord = cord(0,0,0)):
    schem = mcschematic.MCSchematic()
    MD:direction = direction.find_direction("n")

    setInstructionMemory(file_name, schem, MD, start_pos + cord(0,-2,0))
    resetFileRegister(schem, MD.right, start_pos + cord(16,-12,15))
    resetProgramCounter(schem, MD.left, start_pos + cord(-13,-34,12))
    resetCallStack(schem, MD, start_pos + cord(-13,-37,-14))
    resetFlags(schem, MD, start_pos + cord(68,-8,28))

    file_name = file_name.replace("__binaryCode__", "__schems__", 1)
    path = file_name.split("\\")
    schem.save("\\".join(path[:-1]), path[-1].split(".")[0], version)


