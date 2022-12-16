import pygame
from os import path, remove
#from os import getcwd
#opens the settings.ini file and parses the values for main() to handle

#takes a string representing the cwd, meaning I only call the OS module once. 

#returns a 2D array with up to 6 elements
#0: sound settings and valuestick configuration
#1: player 1 controls*
#2: player 2 controls*
#3: player 3 controls*
#4: player 4 controls*
#5: profile
#6: corruption**

#*because representation of bindings for P3 and P4 aren't certain, the function
#adds an int to the start of each control array, ranging from 101 to 104,
#depending on the player. The numbers are so high as to not conflict
#with the volume values

#**This is just a 

def load(cwd):
    corrupt=False
    try:
        infile=open(cwd+"/settings.ini","r")
    except FileNotFoundError:
        corrupt=True
    except Exception as e:
        raise e
    keymap={
        #Row 1: Function Keys
        "F1":pygame.K_F1,
        "F2":pygame.K_F1,
        "F3":pygame.K_F1,
        "F4":pygame.K_F1,
        "F5":pygame.K_F1,
        "F6":pygame.K_F1,
        "F7":pygame.K_F1,
        "F8":pygame.K_F1,
        "F9":pygame.K_F1,
        "F10":pygame.K_F1,
        "F11":pygame.K_F1,
        "F12":pygame.K_F1,
        "F13":pygame.K_F1,
        "F14":pygame.K_F1,
        "F15":pygame.K_F1,

        #Row 2:Tidle -Backspace

        "TILDE":pygame.K_BACKQUOTE,
        "1":pygame.K_1,
        "2":pygame.K_2,
        "3":pygame.K_3,
        "4":pygame.K_4,
        "5":pygame.K_5,
        "6":pygame.K_6,
        "7":pygame.K_7,
        "8":pygame.K_8,
        "9":pygame.K_9,
        "0":pygame.K_0,
        "-":pygame.K_MINUS,
        "=":pygame.K_EQUALS,
        "BACKSPACE":pygame.K_BACKSPACE,

        #Row 3: Tab - \

        "Q":pygame.K_q,
        "W":pygame.K_w,
        "E":pygame.K_e,
        "R":pygame.K_r,
        "T":pygame.K_t,
        "Y":pygame.K_y,
        "U":pygame.K_u,
        "I":pygame.K_i,
        "O":pygame.K_o,
        "P":pygame.K_p,
        "OPEN_BRACKET":pygame.K_LEFTBRACKET,
        "CLOSED_BRACKET":pygame.K_RIGHTBRACKET,
        "BACKSLASH":pygame.K_BACKSLASH,

        #Row 5: Capslock - Enter

        "CAPSLOCK":pygame.K_CAPSLOCK,
        "A":pygame.K_a,
        "S":pygame.K_s,
        "D":pygame.K_d,
        "F":pygame.K_f,
        "G":pygame.K_g,
        "H":pygame.K_h,
        "J":pygame.K_j,
        "K":pygame.K_k,
        "L":pygame.K_l,
        ";":pygame.K_SEMICOLON,
        "'":pygame.K_QUOTE,
        "RETURN":pygame.K_RETURN,

        #Row 6: LShift-Rshift
        "LSHIFT":pygame.K_LSHIFT,
        "Z":pygame.K_z,
        "X":pygame.K_x,
        "C":pygame.K_c,
        "V":pygame.K_v,
        "B":pygame.K_b,
        "N":pygame.K_n,
        "M":pygame.K_m,
        "COMMA":pygame.K_COMMA,
        "PERIOD":pygame.K_PERIOD,
        "QUESTION":pygame.K_QUESTION,
        "RSHIFT":pygame.K_RSHIFT,

        #Row 7: LCtrl - RCtrl
        "LCTRL":pygame.K_LCTRL,
        "LALT":pygame.K_LALT,
        "SPACE":pygame.K_SPACE,
        "RALT":pygame.K_RALT,
        "RCTRL":pygame.K_RCTRL,

        #navigation keys
        "INS":pygame.K_INSERT,
        "HOME":pygame.K_HOME,
        "PGUP":pygame.K_PAGEUP,
        "DEL":pygame.K_DELETE,
        "END":pygame.K_END,
        "PGDOWN":pygame.K_PAGEDOWN,
        
        #arrow keys
        "UP":pygame.K_UP,
        "DOWN":pygame.K_DOWN,
        "LEFT":pygame.K_LEFT,
        "RIGHT":pygame.K_RIGHT,

        #numpad keys
        "K_DIVIDE":pygame.K_KP_DIVIDE,
        "K_MULTIPLY":pygame.K_KP_MULTIPLY,
        "K_MINUS":pygame.K_KP_MINUS,
        "K_PLUS":pygame.K_KP_PLUS,
        "K_9":pygame.K_KP_9,
        "K_8":pygame.K_KP_8,
        "K_7":pygame.K_KP_7,
        "K_6":pygame.K_KP_6,
        "K_5":pygame.K_KP_5,
        "K_4":pygame.K_KP_4,
        "K_3":pygame.K_KP_3,
        "K_2":pygame.K_KP_2,
        "K_1":pygame.K_KP_1,
        "K_0":pygame.K_KP_0,
        "K_PERIOD":pygame.K_KP_PERIOD,
        "K_RETURN":pygame.K_KP_ENTER
        }
    baseout=[
            ["","","","","","",""],
            ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
            ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
            ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
            ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
            [""],
            [False]
            ]
    out=[
        ["","","","","","",""],
        ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
        ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
        ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
        ["UP","DOWN","LEFT","RIGHT","ENTER","PUNCH"],
        [""],
        [False]
        ]

    if not corrupt:
        player3=False
        player4=False
        for line in infile:
            if line[0]=="#":
                continue
            line=line.strip("\n")
            value=line[(line.find("=")+1):]
            if line.find("MA")!=-1:
                out[0][0]=int(value)
            elif line.find("MU")!=-1:
                out[0][1]=int(value)
            elif line.find("SO")!=-1:
                out[0][2]=int(value)
            elif line.find("PR")!=-1:
                out[5][0]=value
            
            elif line.find("P1")!=-1:
                tag=line[(line.find("_")+1):(line.find("="))]
                if tag=="JOY":
                    out[0][3]=bool(int(value))
                else:
                    out[1][(out[1].index(tag))]=keymap[value]

            elif line.find("P2")!=-1:
                tag=line[(line.find("_")+1):(line.find("="))]
                if tag=="JOY":
                    out[0][4]=bool(int(value))
                else:
                    out[2][(out[2].index(tag))]=keymap[value]

            elif line.find("P3")!=-1:
                tag=line[(line.find("_")+1):(line.find("="))]
                if tag=="JOY":
                    out[0][5]=bool(int(value))
                else:
                    player3=True
                    out[3][(out[3].index(tag))]=keymap[value]

            elif line.find("P4")!=-1:
                tag=line[(line.find("_")+1):(line.find("="))]
                if tag=="JOY":
                    out[0][6]=bool(int(value))
                else:
                    player4=True
                    out[4][(out[4].index(tag))]=keymap[value]
        infile.close()
        del infile
        if not player4:
            del out[4]
            del baseout[4]

        if not player3:
            del out[3]
            del baseout[3]
    for i in range(0,len(out)):
        if len(baseout[i])!=len(out[i]):
                corrupt=True
        if corrupt:
            if path.exists(cwd+"/settings.ini"):
                remove(cwd+"/settings.ini")
            writeDefault(cwd)
            out=settingsLoad(cwd)
            break
        for j in range(0,len(baseout[i])):
            test1=out[i][j]
            test2=baseout[i][j]
            if out[i][j]==baseout[i][j]:
                corrupt=True
                break
    
    out[-1][0]=corrupt
    try:
        out[1].index(101)
    except ValueError:
        out[1].insert(0,101)

    try:
        out[2].index(102)
    except ValueError:
        out[2].insert(0,102)

    if player3:
        try:
            out[3].index(103)
        except ValueError:
            out[3].insert(0,103)
    if player4:
        try:
            out[4].index(104)
        except ValueError:
            out[4].insert(0,104)
    return out
            
#handles broken/missing settings files
def writeDefault(cwd):
    #delete the "bad" file if it exists
    if os.path.exists(cwd+"/settings.ini"):
        os.remove(cwd+"/settings.ini")
    #write the base file
    infile=open(cwd+"/settings.ini","x")
    infile.write("MASTER=100\n"
                 "MUSIC=42\n"
                 "SOUND=51\n"
                 "P1_JOY=0\n"
                 "P2_JOY=0\n"
                 "P3_JOY=0\n"
                 "P4_JOY=0\n"
                 "###PLAYER1###\n"
                 "P1_UP=UP\n"
                 "P1_DOWN=DOWN\n"
                 "P1_LEFT=LEFT\n"
                 "P1_RIGHT=RIGHT\n"
                 "P1_ENTER=RSHIFT\n"
                 "P1_PUNCH=RCTRL\n"
                 "###PLAYER2###\n"
                 "P2_UP=W\n"
                 "P2_DOWN=S\n"
                 "P2_LEFT=A\n"
                 "P2_RIGHT=D\n"
                 "P2_ENTER=SPACE\n"
                 "P2_PUNCH=LSHIFT\n"
                 "PROFILE=myProfile.prf")
    infile.close()

#print(settingsLoad(getcwd()))
