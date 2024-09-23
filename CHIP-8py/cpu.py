import numpy as np
import pygame as pg

class chip8 ():
    def __init__(self):
        self.Memory = [] #4096 bit 512 byte len 0x1000 hex
        self.stack = [] ## 16 len 
        self.sp = 0
        self.pc = 0
        self.V = np.zeros(16, np.uint16)
        self.I = np.uint16(0)
        self.dt = 0
        self.st = 0


class OP_CO ():
    def __init__(self, chip):
        self.x = 0
        self.y = 0
        self.nn = 0
        self.n = 0
        self.kk = 0
        self.op_code = np.zeros(1, np.uint16)


class keys ():

    def __init__(self):
        dicKeys = {  ## key chip, key real
        pg.K_1: 1,
        pg.K_2: 2,
        pg.K_3: 3,
        pg.K_q: 4,
        pg.K_w: 5,
        pg.K_e: 6,
        pg.K_a: 7, 
        pg.K_s: 8, 
        pg.K_d: 9,
        pg.K_x: 0,
        pg.K_4: 12,
        pg.K_r: 13,
        pg.K_f: 14,
        pg.K_z: 10,
        pg.K_c: 11,
        pg.K_v: 15
    }

class sprites ():
    def __init__(self):
        fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, #0
            0x20, 0x60 ,0x20, 0x20, 0x70, #1 
            0xF0, 0x10, 0xF0, 0x80, 0xF0, #2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, #3
            0x90, 0x90, 0xF0, 0x10, 0x10, #4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, #5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, #6
            0xF0, 0x10, 0x20, 0x40, 0x40, #7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, #8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, #9
            0xF0, 0x90, 0xF0, 0x90, 0x90, #A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, #B
            0xF0, 0x80, 0x80, 0x80, 0xF0, #C
            0xE0, 0x90, 0x90, 0x90, 0xE0, #D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, #E
            0xF0, 0x80, 0xF0, 0x80, 0x80  #F
        ]