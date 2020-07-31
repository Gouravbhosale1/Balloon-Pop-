# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 12:48:59 2020

@author: gourav
"""
  
import math
import random
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.ticker

import pygame
import sys
from pygame import mixer


# Intialize the pygame
pygame.init()


# Create the screen for game
Screen = pygame.display.set_mode((800,600))

# Set Background
Background = pygame.image.load("Background.jpg")

# Background Sound
pygame.mixer.music.load('Happy_Dreams.mp3')
pygame.mixer.music.play(-1)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34,139,34)
MAROON = (128,0,0)
BLUE = (0,0,139)

# Caption And Icon
pygame.display.set_caption("Ballon Pop")
Icon = pygame.image.load("Icon_img.png")
pygame.display.set_icon(Icon)

# Input text
Input_text_font = pygame.font.Font('freesansbold.ttf',32)
text = ''
Start_text_font = pygame.font.Font('freesansbold.ttf',20)

# Variables for CSV
counter = -1
count = 0
flag = False

# Scores Variables
Score_Value = 0
score_font = pygame.font.Font('freesansbold.ttf',32)
textX = 10  
textY = 10

# Game Over & Leaderboard
Game_over_font = pygame.font.Font('freesansbold.ttf',64)
rank_font = pygame.font.Font('freesansbold.ttf',32)
leaderboard_font = pygame.font.Font('freesansbold.ttf',20)
leaderboard_rank_font = pygame.font.Font('freesansbold.ttf',16)
leaderboard_name_font = pygame.font.Font('freesansbold.ttf',16)
leaderboard_name_font = pygame.font.Font('freesansbold.ttf',16)

# Player
Player_Image = pygame.image.load("Knife.png")
PlayerX = 370
PlayerY = 80
PlayerX_change = 0

# Ballon
Ballon_Image = []
BallonX = []
BallonY = []
BallonX_change = []
BallonY_change = []
number_of_ballons = 20

for i in range(number_of_ballons):
    Ballon_Image.append(pygame.image.load("balloon.png"))
    BallonX.append(random.randint(0, 736))
    BallonY.append(random.randint(650, 700))
    BallonY_change.append(1)

# Knife logo blit
def player(x,y):
    Screen.blit(Player_Image,(x,y))

# Balloon logo blit
def ballon(x,y,i):
    Screen.blit(Ballon_Image[i],(x,y))
        
# Find Collision Occured 
def isCollision(BallonX, BallonY, PlayerX, PlayerY):
    Distance = math.sqrt(math.pow(BallonX - PlayerX, 2) + (math.pow(BallonY - PlayerY, 2)))
    if Distance < 55:
        return True
    else:
        return False

# Take user Input   
def UserInput():
    
    # Textbox
    Screen.blit(Background,(0,0))
    box = pygame.Rect(275, 300, 140, 35)
    Input_text = Input_text_font.render("Enter Your Name", True, (MAROON))
    Screen.blit(Input_text, (250, 250))
    inactive_color = pygame.Color(255,255,255)
    active_color = pygame.Color(124,252,0)
    color = inactive_color
    
    # Start Button
    button = pygame.Rect(330, 350, 80, 40)
    pygame.draw.rect(Screen,GREEN, button)
    Start_text = Start_text_font.render("Start", True, (BLACK))
    Screen.blit(Start_text, (346, 360))

    active = False
    global text 

    done = False


    while not done:
        # exit clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                
            # Mouse clicked on input box
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                    
                if event.button == 1:
                    if button.collidepoint(event.pos):
                        done = True
                    
                # Change the current color of the input box.
                color = active_color if active else inactive_color
            
            # Name Typing
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        Screen.blit(Background,(0,0))
                        box = pygame.Rect(275, 300, 140, 35)
                        Screen.blit(Input_text, (250, 250))
                        pygame.draw.rect(Screen,GREEN, button)
                        Screen.blit(Start_text, (346, 360))
                    else:
                        text += event.unicode
                
        # Render the current text.
        txt_surface = font.render(text, True, color)

        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        box.w = width

        # Blit the text
        Screen.blit(txt_surface, (box.x+5, box.y+5))
     
        # Blit the input_box rect.
        pygame.draw.rect(Screen, color, box, 2)
        pygame.display.flip()

   
# Blit score on screen  
def show_score(x, y):
    score = score_font.render("Score : " + str(Score_Value), True, (MAROON))
    Screen.blit(score, (x, y))

# Blit graph on screen   
def show_graph():
    global Player_df
    Player_df.plot(x ='Rank', y='Score', kind = 'line')
    locator = matplotlib.ticker.MultipleLocator(2)
    plt.gca().xaxis.set_major_locator(locator)
    formatter = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.scatter(rank_print(), Player_df['Score'][rank_print()-1], marker = '.',c = 'g')
    plt.text(rank_print()-0.1,Player_df['Score'][rank_print()-1]+0.7,'Your rank',fontsize = 12)
    plt.xlabel('Rank')
    plt.ylabel('Score')
    plt.savefig('graph.jpg',dpi=55)
    plt.show()

# Blit game over on screen
def game_over_text():
    global PlayerY
    global text
    global Player_df
    global count

    if(count == 0):
        CSV_Check()
        UpdateCSV()
        count = 1
    rank_print()
    LeaderBoard()
    
    Game_over_text = Game_over_font.render("GAME OVER", True, (MAROON))
    Screen.blit(Game_over_text, (200, 150))
    # Graph Image
    Graph = pygame.image.load("graph.jpg")
    Screen.blit(Graph, (30,300))
    PlayerY = 1000

# Blit rank of the current player 
def rank_print():      
        counter_end = 0
        for name1 in Player_df['Name']:
            counter_end +=1
            if name1==text:
                rank_text = rank_font.render("Your Rank Is : " + str(counter_end),True, (MAROON))
                Screen.blit(rank_text, (215, 230))
                return counter_end

# Blit top 5 players on screen
def LeaderBoard():
    global Player_df
    rankx = 580
    ranky = 340
    namesx = 605
    namesy = 340
    scoresx = 700
    scoresy = 340
    global flag
    global Score_Value
    global text
    i = 0
    Player_count = Player_df['Rank'].count()
    leaderboard_text = leaderboard_font.render("Top Five Players",True, (MAROON))
    Screen.blit(leaderboard_text, (580,300))
    if Player_count>=5:
        for i in range(0,5):
            leaderboard_rank_text = leaderboard_rank_font.render(str(Player_df['Rank'][i]),True, (MAROON))
            Screen.blit(leaderboard_rank_text, (rankx, ranky))
            leaderboard_rank_text = leaderboard_rank_font.render(str(Player_df['Name'][i]),True, (MAROON))
            Screen.blit(leaderboard_rank_text, (namesx, namesy))
            leaderboard_rank_text = leaderboard_rank_font.render(str(Player_df['Score'][i]),True, (MAROON))
            Screen.blit(leaderboard_rank_text, (scoresx, scoresy))
            ranky += 30
            namesy += 30
            scoresy += 30
    else:
        for i in range(0,Player_count):
            leaderboard_rank_text = leaderboard_rank_font.render(str(Player_df['Rank'][i]),True, (MAROON))
            Screen.blit(leaderboard_rank_text, (rankx, ranky))
            leaderboard_rank_text = leaderboard_rank_font.render(str(Player_df['Name'][i]),True, (MAROON))
            Screen.blit(leaderboard_rank_text, (namesx, namesy))
            leaderboard_rank_text = leaderboard_rank_font.render(str(Player_df['Score'][i]),True, (MAROON))
            Screen.blit(leaderboard_rank_text, (scoresx, scoresy))
            ranky += 30
            namesy += 30
            scoresy += 30
        

# Blit time left
def time_left():
    # Use python string formatting to format in leading zeros
    output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
 
    text = font.render(output_string, True, MAROON)
    Screen.blit(text, [530, 10]) 
    
# CSV file check    
Player_df = pd.DataFrame(columns = ['Rank','Name','Score','Date'],index=None)
def CSV_Check():
    global Player_df
    if os.path.isfile('./Player_Data.csv'):
        Player_df = pd.read_csv('Player_Data.csv')
    else:
        Player_df.to_csv('Player_Data.csv',index=None)


# Update data in CSV
def UpdateCSV():
    global Score_Value
    global text
    global Player_df
    global flag

    
    counter = -1
    # For old player score
    for n in Player_df['Name']:
        counter +=1
        if n==text:
            flag = True
            if Score_Value > Player_df['Score'][counter]:
                Player_df['Score'][counter]=Score_Value

    # new player score            
    if flag == False:
        new_player_df=pd.DataFrame({'Rank':[Player_df['Rank'].count()+1],'Name':[text],'Score':[Score_Value],'Date':[pd.to_datetime('today').strftime("%m/%d/%Y")]})
        Player_df = Player_df.append(new_player_df)
        
    Player_df.sort_values(["Score"], axis=0, ascending=False, inplace=True) 
    Player_df['Rank'] = Player_df['Rank'].sort_values(ascending=True).values
    Player_df.to_csv('Player_Data.csv',index=None)
    Player_df = pd.read_csv('Player_Data.csv')
    print(Player_df)
    show_graph()



# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
font = pygame.font.Font('freesansbold.ttf',32)
 
frame_count = 0
frame_rate = 60
start_time = 80                                              
        
# Game Loop
Counter = 0
Current = True

while Current:
    # RGB = Red, Green, Blue
    Screen.fill((WHITE))
    
    # Background Image
    Screen.blit(Background, (0, 0))
    
    if Counter == 0:
        Name = UserInput()
        Counter = 1
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Current = False
            
         # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
    
            if event.key == pygame.K_LEFT:
                PlayerX_change = -10
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_change = 0
     
    #Player Movement And Boundary Set           
    PlayerX += PlayerX_change
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736  
    

 
    # --- Timer going down ---
    # --- Timer going up ---
    # Calculate total seconds
    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0
 
    # Divide by 60 to get total minutes
    minutes = total_seconds // 60
 
    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60
 
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    frame_count += 1
 
    # Limit frames per second
    clock.tick(frame_rate)
    # Ballon Loop
    for i in range(number_of_ballons):
        
    # Game Over
        if  minutes <= 0 and seconds <= 0 :
            game_over_text()
            break
            

        
    #Ballon Movement And Boundary Set
        BallonY[i] -= BallonY_change[i]
        if BallonY[i] <= 0:
            BallonY[i] = 650

        
            
        # Collision Detection
        Collision = isCollision(BallonX[i], BallonY[i], PlayerX, PlayerY)
        if Collision:
            pop_sound = pygame.mixer.Sound('balloon-burst.wav')
            pop_sound.play()
            Score_Value += 1
            BallonY_change[i] += 0.6
            BallonX[i] = random.randint(0, 736)
            BallonY[i] = random.randint(650, 700)
        
        ballon(BallonX[i], BallonY[i], i)
                
    player(PlayerX, PlayerY)
    show_score(textX, textY)
    time_left()
    pygame.display.update()    

pygame.display.quit()
pygame.quit()

        
        
        
    