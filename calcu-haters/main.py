import sys,pygame,os
from calc import calc
from victpopup import VictPopup
from random import random
from cursor import Cursor
import settings
import profile
def main():
    sets=settings.load(os.getcwd())
    prof=profile.load(os.getcwd()+"/"+sets[-2][0])
    MAXHEALTH, GOAL, MAXNUM, HEAL_DELAY, HEAL_AMOUNT, DAMAGE, DEATH_PUNISH, PUNISHMENT, SCORE_POINTS=prof
    HEAL_DELAY*=60
    SPAWNDELAY=3*60
    PUNISHMENT*=int(DEATH_PUNISH)
    pygame.mixer.pre_init(44100,-16,2,1024)
    pygame.init()
    pygame.font.init()
    
#    global size
    size=(1280,720)
#    global screen
    calcbtns=[["RAD","DEG","x!","(",")","%","AC"],
              ["Inv","sin","ln","7","8","9","/"],
              ["pi","cos","log","4","5","6","*"],
              ["DEL","tan","sqrt","1","2","3","-"],
              ["Ans","EXP","X^y","0",".","=","+"]]
    screen=pygame.display.set_mode(size)
    pygame.display.set_caption("Calcuhaters")
    screen.fill((255,0,0))
    running=True
#    global myStack

#    global clock
    clock=pygame.time.Clock()



    
    
    buzz=pygame.mixer.Sound(os.getcwd()+"/sounds/beep.wav")
    blip=pygame.mixer.Sound(os.getcwd()+"/sounds/blip.wav")
    select=pygame.mixer.Sound(os.getcwd()+"/sounds/select.wav")
    hit=pygame.mixer.Sound(os.getcwd()+"/sounds/hit.wav")
    die=pygame.mixer.Sound(os.getcwd()+"/sounds/dead.wav")
    point=pygame.mixer.Sound(os.getcwd()+"/sounds/point.wav")
    victory=pygame.mixer.Sound(os.getcwd()+"/sounds/victory.wav")

    sounds=[buzz,blip,select,hit,die]
    
    calcbtnFont=pygame.font.SysFont("Arial",36,True)
    calcInputFont=pygame.font.Font("font1.ttf",16)
    resultFont=pygame.font.SysFont("Arial",72,True)
    scoreFont=pygame.font.SysFont("Arial:",52,True)
    bg=pygame.Surface(size)

    bg.fill((150,150,150))
    
    pygame.draw.rect(bg,(100,100,100),((25,200),(1280-50,720-225))) #button bg
    count=0
    rowcount=0
    cursurf=pygame.Surface((1230,720-225))
    cursurf.set_colorkey((255,0,255))
    
    p1=Cursor((0,0),(255,0,0),sounds, sets[1],DAMAGE,HEAL_AMOUNT,SPAWNDELAY,PUNISHMENT,MAXHEALTH)
    p2=Cursor((6,0),(0,0,255),sounds, sets[2],DAMAGE,HEAL_AMOUNT,SPAWNDELAY,PUNISHMENT,MAXHEALTH)
    p1.set_volume(sets[0][0]*sets[0][2]/100)
    p2.set_volume(sets[0][0]*sets[0][2]/100)
    p1.others.append(p2)
    p2.others.append(p1)
    posSurf=pygame.Surface(size)
    posSurf.set_colorkey((255,0,255))
    posSurf.fill((255,0,255))

    srf1=pygame.Surface((400,200))
    srf2=pygame.Surface((400,200))

    srf1.fill((255,255,255))
    pygame.draw.rect(srf1,(255,0,0),((0,0),(400,200)),1)
    srf2.fill((255,0,0))
    
    tmp=scoreFont.render("Player 1 Wins!",True,(255,0,0))
    srf1.blit(tmp,(200-tmp.get_width()/2,100-tmp.get_height()/2))
    srf2.blit(scoreFont.render("Player 1 Wins!",True,(255,255,255)),(200-tmp.get_width()/2,100-tmp.get_height()/2))

    p1Popup=VictPopup(srf1.copy(),srf2.copy())

    srf1.fill((255,255,255))
    srf2.fill((0,0,255))
    
    srf1.blit(scoreFont.render("Player 2 Wins!",True,(0,0,255)),(200-tmp.get_width()/2,100-tmp.get_height()/2))
    srf2.blit(scoreFont.render("Player 2 Wins!",True,(255,255,255)),(200-tmp.get_width()/2,100-tmp.get_height()/2))

    p2Popup=VictPopup(srf1,srf2)

    for i in range(0,7):
        for j in range(0,5):
            if i==5 and j==4:
                r,g,b=(50,50,250)
            else:
                r,g,b=(150,150,150)
            pygame.draw.rect(bg,(r,g,b),((42+i*100,217+j*93),(95,88)))
    for i in range (0,7):
        for j in range(0,5):
            btn=calcbtns[j][i]
            btnsurf=calcbtnFont.render(btn,True,(255,255,255))
            bg.blit(btnsurf,(42+i*100+(95-btnsurf.get_width())/2,217+j*93+(88-btnsurf.get_height())/2))
    del btnsurf
    del calcbtnFont
    del i
    del j
    del srf1
    del srf2
    del count
    del rowcount
    
    pygame.draw.rect(bg,(175,175,175),((25,50),(500,100))) #player 1 screen
    pygame.draw.rect(bg,(175,175,175),((755,50),(500,100))) #player 2 screen
    pygame.draw.rect(bg,(255,255,255),((800,200+495/8*3),(455-63,495/4)))

    masterScoreSurf=pygame.Surface(size)
    masterScoreSurf.fill((100,100,100))
    masterScoreSurf.set_colorkey((100,100,100))
    
    p1ScoreSurf=scoreFont.render("Player 1 Score: 0",True,(255,0,0))
    
    masterScoreSurf.blit(p1ScoreSurf,(800,200+495/4-p1ScoreSurf.get_height()/2))
    p2ScoreSurf=scoreFont.render("Player 2 Score: 0",True,(0,0,255))
    masterScoreSurf.blit(p2ScoreSurf,(800,200+(495/4)*3-p2ScoreSurf.get_height()/2))
    goal=int(random()*MAXNUM)
    goalSurf=scoreFont.render("Goal: "+str(goal),True,(0,0,0))
    goalX=800+392/2-goalSurf.get_width()/2
    goalY=200+495/2-goalSurf.get_height()/2

    masterTick=0
    winner=0
    continuePrompt=pygame.Surface((720,100))
    continuePrompt.fill((0,75,0))
    scoreFont.set_italic(True)
    tmp=scoreFont.render("Press Any Key to play again...",True,(255,255,255))
    continuePrompt.blit(tmp,(360-tmp.get_width()/2,50-tmp.get_height()/2))
    scoreFont.set_italic(False)
    resetReady=False

    del tmp
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if winner==0:
                    p1.update(event)
                    p2.update(event)
                elif resetReady:
                    p1.clear()
                    p2.clear()
                    winner=0
                    resetReady=False
            elif event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                print(pos)
                posSurf.fill((255,0,255))
                pygame.draw.line(posSurf,(0,255,0),(0,pos[1]),(1280,pos[1]),1)
                pygame.draw.line(posSurf,(0,255,0),(pos[0],0),(pos[0],720),1)

        if p1.answer==goal:
            p1.score+=SCORE_POINTS
            masterScoreSurf=pygame.Surface((size))
            masterScoreSurf.fill((100,100,100))
            masterScoreSurf.set_colorkey((100,100,100))
            p1ScoreSurf=scoreFont.render("Player 1 Score: "+str(p1.score),True,(255,0,0))
            masterScoreSurf.blit(p1ScoreSurf,(800,200+495/4-p1ScoreSurf.get_height()/2))
            masterScoreSurf.blit(p2ScoreSurf,(800,200+(495/4)*3-p2ScoreSurf.get_height()/2))

            goal=int(random()*MAXNUM)
            goalSurf=scoreFont.render("Goal: "+str(goal),True,(0,0,0))
            goalX=800+392/2-goalSurf.get_width()/2
            goalY=200+495/2-goalSurf.get_height()/2
            point.play()
            
        elif p2.answer==goal:
            p2.score+=SCORE_POINTS
            masterScoreSurf=pygame.Surface((size))
            masterScoreSurf.fill((100,100,100))
            masterScoreSurf.set_colorkey((100,100,100))
            p2ScoreSurf=scoreFont.render("Player 2 Score: "+str(p2.score),True,(255,0,0))
            masterScoreSurf.blit(p1ScoreSurf,(800,200+495/4-p1ScoreSurf.get_height()/2))
            masterScoreSurf.blit(p2ScoreSurf,(800,200+(495/4)*3-p2ScoreSurf.get_height()/2))

            goal=int(random()*MAXNUM)
            goalSurf=scoreFont.render("Goal: "+str(goal),True,(0,0,0))
            goalX=800+392/2-goalSurf.get_width()/2
            goalY=200+495/2-goalSurf.get_height()/2
            point.play()

        if p1.state==2:
            masterScoreSurf=pygame.Surface((size))
            masterScoreSurf.fill((100,100,100))
            masterScoreSurf.set_colorkey((100,100,100))
            p1ScoreSurf=scoreFont.render("Player 1 Score: "+str(p1.score),True,(255,0,0))
            masterScoreSurf.blit(p1ScoreSurf,(800,200+495/4-p1ScoreSurf.get_height()/2))
            masterScoreSurf.blit(p2ScoreSurf,(800,200+(495/4)*3-p2ScoreSurf.get_height()/2))
        elif p2.state==2:
            masterScoreSurf=pygame.Surface((size))
            masterScoreSurf.fill((100,100,100))
            masterScoreSurf.set_colorkey((100,100,100))
            p2ScoreSurf=scoreFont.render("Player 2 Score: "+str(p2.score),True,(p2.color))
            masterScoreSurf.blit(p1ScoreSurf,(800,200+495/4-p1ScoreSurf.get_height()/2))
            masterScoreSurf.blit(p2ScoreSurf,(800,200+(495/4)*3-p2ScoreSurf.get_height()/2))


        if p1.score==GOAL and winner==0:
            winner=1
            tick=masterTick
            victory.play()
        elif p2.score==GOAL and winner==0:
            winner=2
            tick=masterTick
            victory.play()
        if masterTick%HEAL_DELAY==0:
            p1.heal()
            p2.heal()
        cursurf.fill((255,0,255))

        
        screen.blit(bg,(0,0))
        cursurf.blit(p1.draw(),(15+p1.x*100+2,15+p1.y*93))
        cursurf.blit(p2.draw(),(15+p2.x*100+2,15+p2.y*93))

        

        screen.blit(cursurf,(25,200))
        screen.blit(p1.inputRender(calcInputFont),(35,60))
        screen.blit(p2.inputRender(calcInputFont),(765,70))
        
        if(p1.redraw):
            p1RenderText=p1.answerText
            p1AnsSurf=resultFont.render(p1RenderText,False,(255,0,0))
            p1AnsX=515-p1AnsSurf.get_width()
            p1.redraw=False
        if(p2.redraw):
            p2RenderText=p2.answerText
            p2AnsSurf=resultFont.render(p2RenderText,False,(0,0,255))
            p2AnsX=1245-p2AnsSurf.get_width()
            p2.redraw=False
        screen.blit(posSurf,(0,0))    
        screen.blit(p1AnsSurf,(p1AnsX,70))
        screen.blit(p2AnsSurf,(p2AnsX,70))
        screen.blit(masterScoreSurf,(0,0))
        screen.blit(goalSurf,(goalX,goalY))
        if winner!=0:
            if winner==1:
                if ((masterTick-tick)%10==0):
                    p1Popup.flip()
                screen.blit(p1Popup.draw(),(640-p1Popup.draw().get_width()/2,360-p1Popup.draw().get_height()/2))
            elif winner==2:
                if ((masterTick-tick)%10==0):
                    p2Popup.flip()
                screen.blit(p2Popup.draw(),(640-p2Popup.draw().get_width()/2,360-p2Popup.draw().get_height()/2))
            if masterTick-tick>=120:
                
                screen.blit(continuePrompt,(640-continuePrompt.get_width()/2,600))
                resetReady=True

        masterTick+=1
        pygame.display.flip()
        
    pygame.quit()
main()
