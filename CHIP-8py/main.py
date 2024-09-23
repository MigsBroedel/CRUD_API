
import pygame as pg
import numpy as np
import cpu
from numpy import random




chip = cpu.chip8()
op = cpu.OP_CO(chip)
key = cpu.keys()
sprites = cpu.sprites()

HEIGHT = 32
WIDTH = 64
pixel_size = 10
buffer_display = [[0 for _ in range(64)] for _ in range(32)]
# tela de 8 por 8



def main():
    init_chip(chip)
    data = ROMCHARG(chip.Memory)
    chip.Memory = np.frombuffer(data, dtype=np.uint8)

    screen = pg.display.set_mode(((WIDTH * pixel_size), (HEIGHT * pixel_size))) # create a display with the size difined before
    clock = pg.time.Clock() # define a clock to measure the time, control some functions
    screen.fill(pg.Color(0, 0, 255))
    Running = True
    nun = 0

    while (Running == True):
        for event in pg.event.get():
        # Verifica se o usuário fechou a janela
            if event.type == pg.QUIT:
                pg.quit()
                Running = False
        fetch_opcde(screen, chip, op, nun)
        timer(chip)
        clock.tick(60)
        pg.display.flip()
        nun += 1
        #if nun == 30:
         #   Running = False
            
        
    

def ROMCHARG (Memory):
    #path = input("Rom path:")
    with open("./ROMS/IBM.ch8", 'rb') as file:
        data = file.read()
        return data
        
        

def fetch_opcde (screen, chip, op, nun): ## int type broo #some error with data types and lenghts
# pegar x, y, nnn e outros, além de verificar um op code, depois programar sua saída
    
    byte1 = chip.Memory[(chip.pc) % len(chip.Memory)]
    byte2 = chip.Memory[(chip.pc + 1) % len(chip.Memory)]
    byte1s = int(byte1) << 8 # int() vai setar a variavel para 16 bits ao invez de 8, podendo assim fazer o shift e juntar as 2 variaveis
    byte2s = int(byte2)
    if byte1s | byte2s != 0:
        op.op_code = byte1s | byte2s ## here, we get the op code, the most high 4 bits of 1 8 bits data, and the same with the next, but the lowest in case
        print(f"Byte 1: {byte1:02X}, Byte 2: {byte2:02X}, Opcode: {op.op_code:04X}")
        op.x = byte1 & 0x0F # & - substituir, if match = match value, else = 0
        op.y = (byte2 >> 4) & 0x0F
        op.n = byte2 & 0x0F
        op.kk = byte2
        op.nnn = ((byte1 & 0x0F) << 8) | byte2
        translate_opcode(screen, chip, op)
        #print(op.x)
        #print(op.y)

    chip.pc+=2

    
    
    

    return op.op_code


    

    
    
def translate_opcode (screen, chip, op): # notas opcode - V -> registrador, x base 1, y mais high, ou seja, quando for verificar fazer y - 15, para ler como um byte padrão e não como o conjunto mais alto
    
    if op.op_code != 0:
        if ((op.op_code & 0xF000) == 0):
            if (op.n == 0):
                screen.fill((0, 0, 0,))
                print("Clear")

            if (op.n == 14):
                chip.sp -= 1
                
        elif ((op.op_code & 0xF000) == 0x1000):
            chip.pc = op.nnn
        elif ((op.op_code & 0xF000) == 0x2000):
            chip.sp += 1
            stackadd(chip, chip.pc)
            chip.pc = op.nnn
        elif ((op.op_code & 0xF000) == 0x3000): # o valor do segundo bit na ordem dos reg == kk, if true, pc += 2
            if chip.V[op.x] == op.kk:
                chip.pc += 2
        elif ((op.op_code & 0xF000) == 0x4000): # o valor do segundo bit na ordem dos reg != kk, if true, pc += 2
            if chip.V[op.x] != op.kk:
                chip.pc += 2
        elif ((op.op_code & 0xF000) == 0x5000):
            if (chip.V[op.x] != chip.V[op.y - 15]):
                chip.pc += 2
        elif ((op.op_code & 0xF000) == 0x6000):
            chip.V[op.x] = op.kk
        elif ((op.op_code & 0xF000) == 0x7000):
            chip.V[op.x] += op.kk
        elif ((op.op_code & 0xF000) == 0x8000): #grupo dos 8
            if (op.n == 0x0):
                chip.V[op.x] = chip.V[op.y] ## VErificar tamanho dos op mini codes, pra verificar certo no hex mongol
            elif (op.n == 0x1):
                Vx = chip.V[op.x]
                Vy = chip.V[op.y]
                nu = Vx | Vy
                chip.V[op.x] = nu                
            elif (op.n == 0x2):
                Vx = chip.V[op.x]
                Vy = chip.V[op.y]
                nu = Vx & Vy
                chip.V[op.x] = nu
            elif (op.n == 0x3):
                Vx = chip.V[op.x]
                Vy = chip.V[op.y]
                nu = Vx ^ Vy
                chip.V[op.x] = nu
            elif (op.n == 0x4):
                Vx = chip.V[op.x]
                Vy = chip.V[op.y]
                nu = Vx + Vy
                if (nu > 255):
                    chip.V[0xF] = 1
                else: 
                    chip.V[0xF] = 0
                chip.V[op.x] = nu & 0xF0
            elif (op.n == 0x5):
                Vx = chip.V[op.x]
                Vy = chip.V[op.y]
                if (Vx > Vy):
                    chip.V[0xF] = 1
                else:
                    chip.V[0xF] = 0
                nu = Vx - Vy
                chip.V[op.x] = nu
            elif (op.n == 0x6):
                Vx = chip.V[op.x]
                ld = Vx & 0x01
                if ld == 1:
                    chip.V[0xF] = 1
                else:
                    chip.V[0xF] = 0
                chip.V[op.x] = Vx / 2
            elif (op.n == 0x7):
                Vx = chip.V[op.x]
                Vy = chip.V[op.y]
                if Vy > Vx:
                    chip.V[0xF] = 1
                else: 
                    chip.V[0xF] = 0
                nu = Vy - Vx
                chip.V[0xF] = nu
            elif (op.n == 0xD):
                Vx = chip.V[op.x]
                hd = (Vx >> 7) & 0x01
                if hd == 1:
                    chip.V[0xF] = 1
                else:
                    chip.V[0xF] = 0
                chip.V[op.x] = Vx * 2
        elif ((op.op_code & 0xF000) == 0x9000):
            Vx = chip.V[op.x]
            Vy = chip.V[op.y]
            if Vx != Vy:
                chip.pc += 2
        elif ((op.op_code & 0xF000) == 0xA000):
            chip.I = op.nnn
        elif ((op.op_code & 0xF000) == 0xB000):
            chip.pc = op.nnn + chip.V[0]
        elif ((op.op_code & 0xF000) == 0xC000):
            Vx = chip.V[op.x]
            nu = random.randint(0, 255)
            nu &= 0x0F
            chip.V[op.x] = nu & op.kk
        elif ((op.op_code & 0xF000) == 0xD000):
            print("draw")
            Vx = chip.V[op.x] & 63
            Vy = chip.V[op.y] & 31
            for n in range(op.n):
                spr = chip.Memory[chip.I+n]
                y = (Vy + n) % 32 # REVISE        #DRAWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
                for y in range(8):
                        x = (Vx + y) % 64
                        spr = spr & (0x80 >> y)
                        screen_px = buffer_display[y][x]
                        if spr:
                            if screen_px == 1:
                                chip.V[0xF] = 1
                            buffer_display[y][x] ^= 1

                        if buffer_display[y][x] == 1:
                            color = (255, 255, 255)
                        elif buffer_display[y][x] == 0: # just eskeleton, its not right yet, still missing data info, how pull bytes, how they influentes the buffer, its 8 bits not 1, and maybe sprites coding
                            color = (0, 0, 0)
            
                        pg.draw.rect(screen, color, pg.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            pg.display.update()

        elif ((op.op_code & 0xF000) == 0xE000):
            if (op.n == 0xE):
                Vx = chip.V[op.x]
                e = pg.event.get()
                if e.type == pg.KEYDOWN:
                    keypressed = e.key
                    if keypressed == Vx:
                        pc += 2
            elif (op.n == 0x1):
                Vx = chip.V[op.x]
                e = pg.event.get()
                keypressed = e.key
                if keypressed != Vx:
                    pc += 2
        elif ((op.op_code & 0xF000) == 0xF000):
            if (op.kk == 0x07):
                chip.V[op.x] = chip.dt
            elif (op.kk == 0x0A):
                i = 0
                while i == 0:
                    pg.time.wait(1000)
                    e = pg.event.get()
                    if e.type == pg.KEYDOWN:
                        if e == key.keys():
                            i = 1
                        else: i = 0
                    else:
                        i = 0

            elif (op.kk == 0x15):
                Vx = chip.V[op.x]
                chip.dt = Vx
            elif (op.kk == 0x18):
                Vx = chip.V[op.x]
                chip.st = Vx
            elif (op.kk == 0x1E):
                Vx = chip.V[op.x]
                nu = Vx + chip.I
                I = nu
            elif (op.kk == 0x29):
                Vx = chip.V[op.x]
                for i in range(15):
                    if sprites[i * 5] == Vx:
                        chip.I = i * 5

            elif (op.kk == 0x33):
                Vx = chip.V[op.x]
                chip.Memory[chip.I] = int(Vx/100)
                chip.Memory[chip.I + 1] = int(((Vx % 100) - Vx % 10) / 10)
                chip.Memory[chip.I + 2] = (Vx % 10)

            elif (op.kk == 0x55):
                for i in len(chip.V):
                    chip.Memory[chip.I + i] = chip.V[i]
            elif (op.kk == 0x65):
                for i in len(chip.V):
                    chip.V[i] = chip.Memory[chip.I + i] 

            
            


def timer (chip):
    if chip.dt > 0:
        chip.dt -= 1

    if chip.st > 0:
        chip.st -= 1
        if chip.st == 0:
            print("beep!")
#            pg.mixer.music.play()


            
                








def stackadd (chip, n):
    if (len(chip.stack) < 16):
        chip.stack.append(n)
    else:
        chip.stack[0] = chip.stack[1:]# talvez de merda, não sei a ordem de implementação dos elementos, do mais recente pro mais velho, do menor pro maior, por enquanto o TOPO da stack é o [16]!
        chip.stack.append(n)

def init_chip (chip):
    chip.pc = 0x200
    chip.op_code = np.zeros(1, dtype=np.uint16)
    chip.Memory = np.zeros(4096, dtype=np.uint8)
    chip.dt = 60
    chip.st = 30
    #pg.mixer.music.load("")



if (__name__ == "__main__"):
    main()
