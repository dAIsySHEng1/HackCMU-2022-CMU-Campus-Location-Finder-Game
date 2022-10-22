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
boundaryCoords = [
            [(940,950),(240,280)],
            [(710,780),(320,400)],
            [(730,840),(670,720)],
            [(950,1030),(450,570)],
            [(900,950),(180,230)],
            [(890,950),(290,350)],
            [(880,940),(355,390)],
            [(850,900),(710,740)],
            [(790,840),(465,535)],
            [(780,870),(555,625)],
            [(655,720),(650,705)],
            [(685,775),(560,605)]
            ]
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
            break
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
    for index in range(len(boundaryCoords)):
        lstCoord = boundaryCoords[index]
        x1,x2 = lstCoord[0]
        y1,y2 = lstCoord[1]
        if (x1 <= posx <= x2) and (y1 <= posy <= y2):
            return index
        
def main():
    gameStart()
    gamePlay()
    pygame.quit()

main()
