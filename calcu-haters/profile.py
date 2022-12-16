import pygame
from os import path, remove
#from os import getcwd
def has(string,i):
    return bool(string.find(i)+1)
def load(file):
    corrupt=False
    try:
        infile=open(file,"r")
    except FileNotFoundError:
        corrupt=True
    except Exception as e:
        raise e
    baseout=["","","","","","","","",""]
    out=["","","","","","","","",""]
    if not corrupt:

        for line in infile:
            if line[0]=="#" or line[0]=="\n":
                continue
            value=line[(line.find("=")+1):]
            if has(line, "MAX"):
                if has(line, "NUM"):
                    out[2]=int(value)
                elif has(line, "H"):
                    out[0]=int(value)
            elif has(line, "HEAL"):
                if has(line, "DE"):
                    out[3]=int(value)
                elif has(line,"AM"):
                    out[4]=int(value)
            elif has(line, "PUN"):
                if has(line, "D"):
                    out[6]=bool(int(value))
                elif has(line,"MENT"):
                    out[7]=int(value)
            elif has(line,"DAM"):
                out[5]=int(value)
            elif has(line,"SUM"):
                out[1]=int(value)
            elif has(line,"SCO"):
                out[8]=int(value)
            else:
                corrupt=True
                break
        infile.close()
    for i in range(0,len(out)):
        if out[i]==baseout[i]:
            corrupt=True
            break
    if corrupt:
        if path.exists(file):
            remove(file)
        writeDefault(file)
        out=load(file)
    return out
        
def writeDefault(file):
    print("corrupted, resetting...")
    infile=open(file,"x")
    infile.writelines(
                      "MAX_HP=5\n"
                      "WINNING_SUM=100\n"
                      "MAXNUM=1000\n"
                      "HEAL_DELAY=5\n"
                      "HEAL_AMOUNT=1\n"
                      "DAMAGE=1\n\n"
                      "#1 or more is ON, 0 or less is OFF\n"
                      "DEATH_PUNISH=1\n\n"
                      "PUNISHMENT=-5\n"
                      "SCORE_POINTS=10\n"
                      )
    infile.close()
#print(load(getcwd()+"/myProfile.prf"))
