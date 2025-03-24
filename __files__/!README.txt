//mnemonic Description        Notation         Set Flags?   Pseudocode                                Resolution
//NOP      No Operation       NOP              No                                                     
//HLT      Halt               HLT              No                                                     
//RET      Return             RET              No           PC <- Top of stack(and pop stack)         
//RSH      Right Shift        RSH A C          No           C <- A >> 1                               
//LSH      Left Shift         LSH A C          Yes          C <- A << 1                               ADD A A C
//ADD      Addition           ADD A B C        Yes          C <- A + B                                
//SUB      Subtraction        SUB A B C        Yes          C <- A - B                                
//NOR      Bitwise NOR        NOR A B C        Yes          C <- !(A|B)                               
//AND      Bitwise AND        AND A B C        Yes          C <- A & B                                
//XOR      Bitwise XOR        XOR A B C        Yes          C <- A ^ B                                
//LDI      Load Immadiate     LDI A 8bit       No           A <- Immadiate                            
//ADI      ADD Immadiate      ADI A 8bit       Yes          A <- A + Immadiate                        
//JMP      Jump               JMP addr         No           PC <- Address                             
//BRH      Branch             BRH cond addr    No           PC <- Cond ? Address: PC + 1              
//CAL      Call               CAL addr         No           PC <- Address(and push PC + 1 to stack)   
//LOD      Memory Load        LOD A B offset   No           B <- Mem[A + offset]                      
//STR      Memory Store       STR A B offset   No           Mem[A + offset] <- B                      
//CMP      Compare            CMP A B          Yes          A - B (and set flags)                     SUB A B r0
//MOV      Move               MOV A C          Yes          C <- A                                    ADD A r0 C
//INC      Increment          INC A            Yes          A <- A + 1                                ADI A 1
//DEC      Decrement          DEC A            Yes          A <- A - 1                                ADI A -1
//NOT      Bitwise NOT        NOT A C          Yes          C <- !A                                   NOR A r0 C
//NEG      Negate             NEG A C          Yes          C <- 0 - A                                SUB r0 A C          
