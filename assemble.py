#settings
comment_symbol = "//"


#static syntax sets
opcodes = ['nop', 'hlt', 'add', 'sub', 'nor', 'and', 'xor', 'rsh', 'ldi', 'adi', 'jmp', 'brh', 'cal', 'ret', 'lod', 'str']
registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
ports = ['pixel_x', 'pixel_y', 'draw_pixel', 'clear_pixel', 'load_pixel', 'buffer_screen', 'clear_screen_buffer', 
         'write_char', 'buffer_chars', 'clear_chars_buffer', 'show_number', 'clear_number', 'signed_mode', 'unsigned_mode', 'rng', 'controller_input']
letters = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '!', '?']


def main(file_name:str):
    result = []

    #create symbol table
    symbols = {}
    [symbols.update({f"{symbol}":index}) for index, symbol in enumerate(opcodes)]
    [symbols.update({f"{symbol}":index}) for index, symbol in enumerate(registers)]
    [symbols.update({f"{symbol}":index+240}) for index, symbol in enumerate(ports)]
    [symbols.update({f"'{symbol}'":index}) for index, symbol in enumerate(letters)]
    [symbols.update({f'"{symbol}"':index}) for index, symbol in enumerate(letters)]

    #add conditions to table
    conditions = [
        ['eq', 'ne', 'ge', 'lt'],
        ['=', '!=', '>=', '<'],
        ['z', 'nz', 'c', 'nc'],
        ['zero', 'notzero', 'carry', 'notcarry']
                  ]
    [[symbols.update({f"{symbol}":index}) for index, symbol in enumerate(condition)] for condition in conditions]

    #function tools
    def resolve(word):
        if word[0] in "-0123456789":
            return int(word,0)
        if symbols.get(word) is None:
            exit(f"Could not resolve {word}")
        return symbols[word]
    
    #read file
    with open(file_name,"r") as f:
        lines = [line.strip().lower() for line in f.readlines()]

    #clean Comments
    lines = [line if comment_symbol not in line else line.split(comment_symbol)[0].strip() for line in lines if line.split(comment_symbol)[0].strip() != ""]

    #variable
    pc:int = 0
    instructions:list = []

    #handle vars and labels
    for line in lines:
        words = [word.lower() for word in line.split()]
        if words[0] == "define":
            symbols[words[1]] = int(words[2])
        elif words[0][0] == ".":
            symbols[words[0]] = pc
            if len(words) > 1:
                pc += 1
                instructions.append(words[1:])
        else:
            pc+=1
            instructions.append(words)
    for pc, words in enumerate(instructions):
        #resolve pseudo-instructions
        match words[0]:
            case "cmp":
                words = ["sub", words[1], words[2], registers[0]]
            case "mov":
                words = ["add", words[1], registers[0], words[2]]
            case "lsh":
                words = ["add", words[1], words[1], words[2]]
            case "inc":
                words = ["adi", words[1], "1"]
            case "dec":
                words = ["adi", words[1], "-1"]
            case "not":
                words = ["nor", words[1], registers[0], words[2]]
            case "neg":
                words = ["sub", registers[0], words[1], words[2]]
        
        #lod/str optional offset
        if words[0] in ["lod", "str"] and len(words) == 3:
            words.append("0")

        #space special case
        if words[-1] in ["'", '"'] and words[-2] in ["'", '"']:
            words[-1] = "' '"
        
        #translate
        opcode = words[0]
        binary = symbols[opcode] << 12
        words = [resolve(word) for word in words]
        
        exit(f"Incorrect number of operands for {opcode} on line {pc}") if opcode in ["nop", "hlt", "ret"] and len(words) != 1 or opcode in ["jmp", "cal"] and len(words) != 2 or opcode in ["rsh", "ldi", "adi", "brh"] and len(words) != 3 or opcode in ["add", "sub", "nor", "and", "xor", "lod", "str"] and len(words) != 4 else ...

        #reg A
        if opcode in ["add", "sub", "nor", "and", "xor", "rsh", "ldi", "adi", "lod", "str"]:
            if words[1] != (words[1] % 16):
                exit(f'Invalid reg number on {pc}')
            binary |= (words[1] << 8)
        
        #reg B
        if opcode in ["add", "sub", "nor", "and", "xor", "lod", "str"]:
            if words[2] != (words[2] % 16):
                exit(f'Invalid reg number on {pc}')
            binary |= (words[2] << 4)
        
        #reg C
        if opcode in ["add", "sub", "nor", "and", "xor", "rsh"]:
            if words[-1] != (words[-1] % 16):
                exit(f'Invalid reg number on {pc}')
            binary |= words[-1]

        #Immadiate
        if opcode in ["ldi", "adi"]:
            if 255 > words[2] < -128:
                exit(f"number must be between -128 and 255 not {words[2]} error on line {pc}")
            binary |= words[2] & 255

        # Instruction memory address
        if opcode in ['jmp', 'brh', 'cal']:
            if words[-1] != (words[-1] % 1024):
                exit(f'memory adress must be between 0 and 1024 not {words[-1]} error on line {pc}')
            binary |= words[-1]

        # Condition
        if opcode in ['brh']:
            if words[1] != (words[1] % 4):
                exit(f'Invalid condition for {opcode} on line {pc}')
            binary |= (words[1] << 10)

        #offset
        if opcode in ["lod", "str"]:
            if 7 > words[3] < -8 :
                exit(f'offset must be between -8 and 15 not {words[3]} error on line {pc}')
            binary |= words[3] & 15

        #save binary lines
        result.append(bin(binary)[2:].rjust(16, '0')+"\n")
    #write lines to file
    with open(file_name.replace("programs","__binaryCode__",1), "w") as f:
        f.writelines(result)
