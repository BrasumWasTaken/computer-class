import pygame
from calc import calc
def find(lst, item):
    try:
        return lst.index(item)
    except ValueError:
        return -1
class Cursor:
    def __init__(self,pos,Color,sounds,controls,DMG,HEAL,DELAY,PUNISHMENT,Max):
        self.x=pos[0]
        self.y=pos[1]
        self.spawn=pos
        self.score=0
        self.controls=controls[1:]
        self.health=5
        self.color=Color
        self.inputText=""
        self.answer=0
        self.answerText=str(self.answer)
        self.redraw=True
        self.others=[]
        self.snd_buzz=sounds[0]
        self.snd_blip=sounds[1]
        self.snd_select=sounds[2]
        self.snd_hit=sounds[3]
        self.snd_die=sounds[4]
        self.max=Max
        self.dmg=DMG
        self.timer=0
        self.DELAY=DELAY
        self.punishment=PUNISHMENT
        self.HEAL=HEAL
        #special states
        self.state=0
        
        
        #special variables for gameplay
        self.numPressed=False #stores if a number has been pressed
        self.doingDecimal=False #stores if a decimal place has been pressed
    def clear(self):
        self.answer=0
        self.inputText=""
        self.health=5
        self.score=0
        self.x=self.spawn[0]
        self.y=self.spawn[1]
        self.answerText=""
        self.redraw=True
        self.numPressed=False
        self.doingDecimal=False
    #sets the volume of all loaded sounds
    def set_volume(self,volume):
    
        self.snd_buzz.set_volume(volume)
        self.snd_blip.set_volume(volume)
        self.snd_select.set_volume(volume)
    def warp(self,pos,frag=True):
        for player in self.others:
            if ((player.x==pos[0] and player.y==pos[1]) or (player.x==self.x and player.y==self.y)):
                player.die()
        self.x=pos[0]
        self.y=pos[1]
        
    def move(self,dirr,sound=""):
        positions=[]
        if player.state==2:
            self.snd_buzz.play()
            return
        for player in self.others:
            positions.append((player.x,player.y))
        if (self.x+dirr[0]>6 or self.x+dirr[0]<0) or (self.y+dirr[1]>4 or self.y+dirr[1]<0) or (find(positions,((self.x+dirr[0],self.y+dirr[1])))!=-1):
            if sound=="":
                self.snd_buzz.play()
            else:
                sound.play()
            return
        
            
        self.x=(self.x+dirr[0])
        self.y=(self.y+dirr[1])
        if sound=="":
            sound=self.snd_blip
        sound.play()
        #print("--")
        #print(self.x)
        #print(self.y)
    def ouch(self,dirr):
        
        self.health-=self.dmg
        if self.health>0:
            self.move((dirr[0]*-1,dirr[1]*-1),self.snd_hit)
            self.state=1
        else:
            
            self.die()
    def die(self):
        self.snd_die.play()
        self.score-=self.punishment
        self.health=0
        self.state=2
        self.timer=0
    def draw(self):
        tmpsurf=pygame.Surface((96,90))
        tmpsurf.fill((255,0,255))
        if self.state==0:
            pygame.draw.rect(tmpsurf,self.color,((0,0),(96,90)),3)
        elif self.state==1:
            tmpColor=[self.color[0]+255-17*self.timer,self.color[1]+255-17*self.timer,self.color[2]+255-17*self.timer]
            for i in range(0,3):
                if tmpColor[i]>255:
                    tmpColor[i]=255
                elif tmpColor[i]<0:
                    tmpColor[i]=0
            pygame.draw.rect(tmpsurf,tmpColor,((0,0),(96,90)),3)
            self.timer+=1
        elif self.state==2:
            tmpColor=[self.color[0]+125,self.color[1]+125,self.color[2]+125]
            for i in range(0,3):
                if tmpColor[i]>255:
                    tmpColor[i]=255
                elif tmpColor[i]<0:
                    tmpColor[i]=0
            pygame.draw.rect(tmpsurf,tmpColor,((0,0),(96,90)),3)
            self.timer+=1
        if self.timer==15 and self.state==1:
            self.timer=0
            self.state=0
        elif self.state==2 and self.timer>=self.DELAY:
            self.state=0
            self.timer=0
            self.warp((self.spawn[0],self.spawn[1]))
            self.health=self.max
        
        return tmpsurf
    def heal(self):
        if self.state!=2 and self.health!=self.max:
            self.health+=self.HEAL
    def update(self,event):
        self.answerText=str(self.answer)
        if self.state!=2:        
            if event.key==self.controls[0]:
                self.move((0,-1))
                return True
            elif event.key==self.controls[1]:
                self.move((0,1))
                return True
            elif event.key==self.controls[2]:
                self.move((-1,0))
                return True
            elif event.key==self.controls[3]:
                self.move((1,0))
                return True
            elif event.key==self.controls[4]:
                self.melee()
                return True
            elif event.key==self.controls[5]:
                self.select()
                return True
            return False
    def melee(self):
        positions=[]
        hitable=[]
        for player in self.others:
            positions.append((player.x,player.y,player))
        for position in positions:
            hitable.append([])
            for i in range(1,-2,-1):
                for j in range(1,-2,-1):
                    hitable[-1].append((position[0]+i,position[1]+j))
            hitable[-1].remove((position[0],position[1]))
            hitable[-1].append(player)
        for i in range(0,len(hitable)):
            for j in range(0,len(hitable[i])):
                if find(hitable[i],(self.x,self.y))!=-1:
                    hitable[i][-1].ouch((self.x-hitable[i][-1].x,self.y-hitable[i][-1].y))
                    break
        return
    def inputRender(self,font):
        renderText=self.inputText
        if(len(renderText)>44):
            renderText=renderText[len(renderText)-44::]
        return font.render(renderText,True,(0,0,0))
    def select(self):
        pos=(self.x,self.y)
        if pos==(6,0):
            self.inputText=""
            #self.answer=0
            self.answerText="0"
            self.redraw=True #flags the main loop that it needs to redraw the answer text
            self.doingDecimal=False
            self.numPressed=False
            self.snd_select.play()
            return
        if pos==(5,4):
            if(self.inputText==""):
                self.snd_buzz.play()
                return
            
            tmp2=self.inputText.upper()
            if(tmp2.find("ANS")!=-1):
               tmp=""
               for i in range(0,tmp2.find("ANS")):
                   tmp+=self.inputText[i]
               tmp+=str(self.answer)
               for i in range(tmp2.find("ANS")+3,len(self.inputText)):
                   tmp+=self.inputText[i]
               print(tmp)
            else:
                tmp=self.inputText
            
            try:
                self.answer=calc(tmp)
                self.answerText=str(self.answer)
            except Exception as e:
                raise e
                self.answer=0
                self.answerText=str(e.__class__.__name__)
            self.redraw=True
            self.snd_select.play()
            return
        if pos==(0,3):
            if self.inputText=="":
                self.snd_buzz.play()
                return
            spots=1
            if self.inputText[-1]==".":
                self.doingDecimal=False
            elif self.inputText[-1].isnumeric:
                self.numPressed=False
            elif self.inputText[-1].upper()=="S":
                spots=3
            self.inputText=self.inputText[0:len(self.inputText)-spots]
            self.snd_select.play()
            return
        elif pos==(1,4):
            self.inputText+="^"
            self.numPressed=False
            self.doingDecimal=False
            self.snd_select.play()
            return
        elif pos==(0,2):
            self.inputText+="!"
            self.numPressed=False
            self.doingDecimal=False
            self.snd_select.play()
            return
        elif pos==(4,4):
            self.doingDecimal=True
            self.inputText+="."
            self.snd_select.play()
            return
        calcbtns=[["RAD","DEG","!","(",")","%","AC"],
                  ["Inv","sin(","ln(","7","8","9","/"],
                  ["pi","cos(","log(","4","5","6","*"],
                  ["DEL","tan(","sqrt(","1","2","3","-"],
                  ["Ans","EXP","X^y","0",".","=","+"]]
        
        if(((self.y>=1 and self.y<=3) and (self.x>=3 and self.x<=5)) or (pos==(3,4))):
            if not self.numPressed or self.doingDecimal:
                self.numPressed=True
            else:
                self.snd_buzz.play()
                return
        else:
            self.doingDecimal=False
            self.numPressed=False
        self.inputText+=calcbtns[self.y][self.x]
        self.snd_select.play()
        return
        
