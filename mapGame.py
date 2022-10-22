#Pygame Program: CMU Map Locationfinder Game

# Import libraries
import sys, pygame, os, random, math
pygame.init()

#dimensions of window
width, height = 1512, 818
screen = pygame.display.set_mode([width, height])
screen.fill((255, 255, 255))

#display details
fontCali = pygame.font.SysFont("Calibri", 25)
borderW = 6 #width of rectangle card

#game locations
locations = ["Stever", "Tepper", "Baker", "CUC", "Mudge", "M. Gardens", "M. E-Tower",
             "Hunt", "GHC", "Doherty", "Porter", "Wean"]
visited = []

#user's circle information
colorcircle = (255,0,0)

def gameStart():
    drawCMUMap()
    newLocation() #start the game by generating a location

def drawCMUMap():
    CMUMap = pygame.image.load("CMU_Map.png")
    CMUMap = pygame.transform.scale(CMUMap, (width, height))
    screen.blit(CMUMap, pygame.Rect(0, 0, CMUMap.get_width(), CMUMap.get_height()))

def newLocation():
    location = int(random.random()*len(locations))
    while ((location in visited) and (len(visited) <=12)):
        location = int(random.random()*len(locations))
    visited.append(location)

def drawCard(red, green, blue):
    card = pygame.Rect(1200, borderW, width-(1200+borderW), 50)
    #border is a rectangle with larger dimensions underneath
    border = pygame.Rect(1200-borderW, 0, width-(1200-borderW), 50+2*borderW)
    pygame.draw.rect(screen, (red, green, blue), border)
    pygame.draw.rect(screen, (255, 255, 255), card)

def gamePlay():
    running = True # Run until user quits Pygame
    isFound = False #specific location is found
    gameOver = False #all locations found
    posx, posy = width//2, height//2
    location = visited[0]
    move_right, move_left, move_up, move_down = False, False, False, False
    score = 0 #user's number of correct locations
    
    while running:
        if (gameOver): #game is over
            drawCard(100, 100, 0)
            screen.blit(fontCali.render("Game Finished! Good Job!", 1, (0, 0, 0)),
                        pygame.Rect(1200+borderW, 2*borderW, width-(1200+2*borderW), 100-borderW))
            screen.blit(fontCali.render("Score: " + str(score), 1, (0, 0, 0)),
                        pygame.Rect(1200+borderW, 6*borderW, width-(1200+2*borderW), 100-borderW))    
        else: #event occurs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                #move in a direction if the key is held down
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_left = True
                    elif event.key == pygame.K_RIGHT:
                        move_right = True
                    #simultaneous horizontal/vertical mvt allowed
                    if event.key == pygame.K_UP:
                        move_up = True
                    elif event.key == pygame.K_DOWN:
                        move_down = True
                    #reset to center of window when location is found
                    elif event.key == pygame.K_SPACE and isFound:
                        if (len(visited)>=len(locations)): #all locations have been visited
                            gameOver = True
                            break
                        else:
                            posx = width//2
                            posy = height//2
                            #generate new index for location in list
                            newLocation()
                            location = visited[-1]
                            isFound = False
                #if key is not pressed anymore, stop circle's movement
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        move_right = False
                    elif event.key == pygame.K_LEFT:
                        move_left = False
                    if event.key == pygame.K_UP:
                        move_up = False
                    elif event.key == pygame.K_DOWN:
                        move_down = False
        
            if (move_right):
                posx = posx + 8
            elif (move_left):
                posx = posx - 8
            if (move_up):
                posy -= 8
            elif (move_down):
                posy += 8

            #redraw map using new location
            drawCMUMap()  
            circle = pygame.draw.circle(screen, colorcircle, (posx, posy), 10)

            if (not isFound):
                #text and design of displayed instruction card
                drawCard(255, 0, 0)
                instr = "Goal: Find " + locations[location]
                screen.blit(fontCali.render(instr, 1, (0, 0, 0)), pygame.Rect(1200+borderW, 2*borderW, width-(1200+2*borderW), 100-borderW))
            else: #displayed card when user has found location
                drawCard(100, 100, 0)
                screen.blit(fontCali.render("Nice Job! (SPACE for new).", 1, (0, 0, 0)), pygame.Rect(1200+borderW, 2*borderW, width-(1200+2*borderW), 100-borderW))

            screen.blit(fontCali.render("Score: " + str(score), 1, (0, 0, 0)), pygame.Rect(1200+borderW, 6*borderW, width-(1200+2*borderW), 100-borderW))    
            
            if (boundaries(posx, posy) == location and not isFound):
                score += 1
                drawCard(100, 100, 0)

                screen.blit(fontCali.render("Mission Complete!", 1, (0, 0, 0)), pygame.Rect(1200+borderW, 2*borderW, width-(1200+2*borderW), 100-borderW))
                isFound = True
                screen.blit(fontCali.render("Score: " + str(score), 1, (0, 0, 0)), pygame.Rect(1200+borderW, 6*borderW, width-(1200+2*borderW), 100-borderW))    
            # flip display
        pygame.display.flip()    

#returns index in location list if user's circle lands within specific coordinates
def boundaries(posx, posy):
    #Stever
    if (940 <= posx <= 950) and (240 <= posy <= 280):
        return 0
    #Tepper
    elif (710<=posx<=780) and (320<=posy<=400):
        return 1
    #Baker Hall
    elif (730<=posx<=840) and (670<=posy<=720):
        return 2
    #CUC
    elif (950<=posx<=1030) and (450<=posy<=570):
        return 3
    #Mudge
    elif (900<=posx<=950) and (180<=posy<=230):
        return 4
    #Morewood Gardens
    elif (890<=posx<=950) and (290<=posy<=350):
        return 5
    #E-Tower
    elif (880<=posx<=940) and (355<=posy<=390):
        return 6
    #Hunt
    elif (850<=posx<=900) and (710<=posy<=740):
        return 7
    #GHC
    elif (790<=posx<=840) and (465<=posy<=535):
        return 8
    #Doherty
    elif (780<=posx<=870) and (555<=posy<=625):
        return 9
    #Porter
    elif (655<=posx<=720) and (650<=posy<=705):
        return 10
    #Wean
    elif (685<=posx<=775) and (560<=posy<=605):
        return 11

def main():
    gameStart()
    gamePlay()

main()
