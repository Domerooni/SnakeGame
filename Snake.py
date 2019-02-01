import pygame
import time
import random

pygame.init()
# this is the color combo: (red,green,blue) or (r,g,b)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (100,200,100)
blue = (0,0,255)

display_width = 600
display_height = 600

gameDisplay = pygame.display.set_mode((600,600))
pygame.display.set_caption('Snake')

pygame.display.update()

clock = pygame.time.Clock()

block_size = 30
FPS = 15


smallfont = pygame.font.SysFont("comicsansms", 10)
mediumfont = pygame.font.SysFont("comicsansms", 25)
largefont = pygame.font.SysFont("comicsansms", 50)

def score(score):
    text = smallfont.render("Apples eaten: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def game_intro():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(green)
        message_to_screen("Welcome to Snake", red, -50, size="large")
        message_to_screen("Eat the red apples", red, 50, size="medium")
        message_to_screen("Press C to play or Q to quit", red, 100, size="medium")
        pygame.display.update()
        clock.tick(5)

def snake(block_size, snakeList):
    for XnY in snakeList: 
        pygame.draw.rect(gameDisplay, black, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = mediumfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()
    

def message_to_screen(msg,color,y_displace=0,size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)
  #  screen_text = font.render(msg, True, color)
  #  gameDisplay.blit(screen_text, [display_width/5,display_height*2/3])

def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1
    
    # the round function here just ensures that the apple, like the snake
    # falls on a multiple of 30 and that there is no overlap
    randAppleX = round(random.randrange(0,display_width-block_size)/30.0)*30.0
    randAppleY =  round(random.randrange(0,display_height-block_size)/30.0)*30.0
    
    while not gameExit:
        
        while gameOver == True:
            gameDisplay.fill(green)
            message_to_screen("Game over", red, y_displace=-25, size = "large")
            message_to_screen("Press C to play again or Q to quit", red, 25, size = "medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

            if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
                gameOver = True
            

           # if event.type == pygame.KEYUP:
           #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
           #         lead_x_change = 0
           # this would make snake stop when we stopped pressing our key
                    
    # the lead_x_change keeps the snake moving once the keys aren't pressed
        lead_x += lead_x_change
        lead_y += lead_y_change
        

        gameDisplay.fill(green)
        AppleThickness = 30
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLength:
            del snakeList[0]
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        score(snakeLength-1)
        
        pygame.display.update()

        if lead_x + block_size > randAppleX and lead_x < randAppleX + AppleThickness:
            if lead_y + block_size > randAppleY and lead_y < randAppleY + AppleThickness:
                print("you ate the apple")
                randAppleX = round(random.randrange(0,display_width-block_size)/30.0)*30.0
                randAppleY = round(random.randrange(0,display_height-block_size)/30.0)*30.0
                snakeLength += 1
                
        clock.tick(FPS)
    pygame.quit()
    quit()
    
game_intro()
gameLoop()
