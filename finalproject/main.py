import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random
import time
import os
"""this is my final project for the amaizing free online course in the Codeinplace Stanford, where i met such awesome and inspiring people to guide me through! much thanks to my professors Chris, Mayahem and [name of the other one] and section leader: Anwarul!'
,to generate the sounds and effect i used elevenlabs sound effects."""


#the constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
PLAYER_PLANE_SIZE = 100 #in pixels x and y axis.
ENEMY_PLANE_SIZE = 100


#the painel info

score_text_display = None
score = 0
number_player_lifes = 3
delay = []
mobility = 20 #Mobility represents the amount of pixels the player's plane can turn in mid air.
enemy_mobility = 10
incremental_enemy_speed = 0
difficulty_level = 50
start_game_text = None
player = None
pressed_start_buttom = []


#player_image needs to be global to update for each "frame"
start_text = None
player_image = None
enemy_image = []

#we create a window
window = tk.Tk()
window.title("SkyboundInPlace - Stanford")
window.geometry("1024x720")
canvas = tk.Canvas(window,width=SCREEN_WIDTH,height=SCREEN_HEIGHT)
canvas.pack()



    

#creating the helper functions


def create_player_plane(canvas,position_x,position_y):
    #its will be a image of a player plane, but for now it will be a rectangular blue.
    global player_image
   
    #using some os propreties to find the current path and locate the images folder where its all images of the game
    image_path = os.path.join(os.getcwd(), "images", "PLAYER_PLANE.png")
    image_player_id = Image.open(image_path)


    #resizing the image to the determinated size aka PLAYER_PLANE_SIZE.
    resized_image = image_player_id.resize((PLAYER_PLANE_SIZE, PLAYER_PLANE_SIZE), Image.Resampling.LANCZOS)
    player_image = ImageTk.PhotoImage(resized_image)
    
    return canvas.create_image(position_x, position_y, image=player_image)
     
def create_enemy_plane(canvas,position_x,position_y):

    """"function that creates the image of one enemy plane at the given position x,y"""

    global enemy_image
    
    enemy_image_path = os.path.join(os.getcwd(),"images","ENEMY_PLANE01.png")
    enemy_image_id = Image.open(enemy_image_path)
    resize_enemy_image = enemy_image_id.resize((ENEMY_PLANE_SIZE,ENEMY_PLANE_SIZE),Image.Resampling.LANCZOS)
    
    enemy_image.append(ImageTk.PhotoImage(resize_enemy_image))

    return canvas.create_image(position_x,position_y, image=enemy_image[-1])

def mobility_area_plane(canvas):
    ''''here we place a rectangle to delimitate the movement of the plane'''
    margin = 20

    x_left = 0 + margin
    y_top = 0 + margin 
    x_right = SCREEN_WIDTH *0.5 - margin
    y_bottom = SCREEN_HEIGHT - margin


    return canvas.create_rectangle(x_left,y_top,x_right,y_bottom)

def move_up(event):
    position_player = canvas.coords(player)
    position_restricted_area = canvas.coords(restricted_area)
    #gets the position some element, in this case the player image as a list [x1,y1] representing the central point of the image

    #here we create a condition where cannot pass to the outside restricted area by not allowing to move if the player y1 are greater than y1 of the restricted area .
    if(position_player[1]-PLAYER_PLANE_SIZE/2>position_restricted_area[1]):
        canvas.move(player,0,-mobility)
        print(position_player)
def move_down(event):
    position_player = canvas.coords(player)
    position_restricted_area = canvas.coords(restricted_area)

    #the condition in this case it will be the comparison of player y1 with y2 of both lists, index 1 and 3 respectively, while plane's y1 is less than y3 its fine
    if(position_player[1]+PLAYER_PLANE_SIZE/2<position_restricted_area[3]):
        canvas.move(player,0,mobility)
        print(position_player)
def move_left(event):
    position_player = canvas.coords(player)
    position_restricted_area = canvas.coords(restricted_area)
    #the condition in this case it will be the players x1  with the restricted_area x1, both index 0
    if(position_player[0]-PLAYER_PLANE_SIZE/2>position_restricted_area[0]):
        canvas.move(player,-mobility,0)
        print(position_player)
def move_right(event):
    position_player = canvas.coords(player)
    position_restricted_area = canvas.coords(restricted_area)
    #the condition in this case it will be the plane x1 with restricted_area x2 lists, index 0 and 2 respectively
    if(position_player[0]+PLAYER_PLANE_SIZE/2<position_restricted_area[2]):
        canvas.move(player,mobility,0)
        
#here its the position where the player starts
initial_x = 0.3*SCREEN_WIDTH
initial_y = SCREEN_HEIGHT/2


#mobility and limitations of the players plane
restricted_area =  mobility_area_plane(canvas)

def start_game(event):
    #until the window.bind(<x> not being press, the game doens't start)

    global start_game_text,player,score_text_display
    player = create_player_plane(canvas,initial_x,initial_y)
    spawn_wave_enemies(canvas,5)
    canvas.delete(start_game_text)
    
    #here we create our first display, it will be maintened by the update_text_function.

    score_text_display= canvas.create_text(100,20,fill="white",font="Times 20 italic bold",text=f'Score: {str(score)}')
    window.unbind(pressed_start_buttom[-1])



def main():
    #some differences from the lessons in the codeinplace compiler such as window and mainloop and the animation concepts that's uses .after and .coords from Canvas
    global player, start_game_text,pressed_start_buttom


    background = canvas.create_rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,fill="black")
    start_game_text = canvas.create_text(SCREEN_WIDTH/2,SCREEN_HEIGHT*0.7,fill="white",font="Times 20 italic bold",text='press x to start the game!')

    #controls
    #.bind function its to associate the keyboard input with some function in this case the ones for mobility of the player
    window.bind("<Up>",move_up)
    window.bind("<w>",move_up)
    window.bind("<Down>",move_down)
    window.bind("<s>",move_down)
    window.bind("<Left>",move_left)
    window.bind("<a>",move_left)
    window.bind("<Right>",move_right)
    window.bind("<d>",move_right)
    
    #storing the indentifier of the bound in a list called pressed_start_buttom

    pressed_start_buttom.append(window.bind("<x>",start_game))
    
    update_score_text()
    window.mainloop()
   
    #testing player position
    

def update_score_text():
    try:
        canvas.itemconfigure(score_text_display, text=f'Score: {str(score)}')
        window.after(10, update_score_text)
    except StopIteration:
        pass


def spawn_one_enemy(canvas):
    random_vertical_enemy_position = random.randint(0,SCREEN_HEIGHT)

    enemy = create_enemy_plane(canvas,SCREEN_WIDTH*0.9,random_vertical_enemy_position)
    from_right_to_left(canvas,enemy,20)

   
def spawn_wave_enemies(canvas, enemy_max_quantity):
    count_enemies = 0
    enemies = []
    
    while count_enemies < enemy_max_quantity:
        random_y_position = random.randint(0,SCREEN_HEIGHT)

        # velocity represents the speed of the enemy flee, by the wainting time between each frame in ms of .after canvas function
        delay.append(random.randint(10,20))
        velocity = delay[count_enemies]
        enemies.append(create_enemy_plane(canvas,SCREEN_WIDTH*0.9,random_y_position))
        from_right_to_left(canvas,enemies[count_enemies],velocity)
        count_enemies+=1
    


def from_right_to_left(canvas,enemy_model,velocity):

    #todo test with one enemy- collision
    



    move_animation(canvas,enemy_model,-enemy_mobility,0,velocity)



def move_animation(canvas,enemy_model,new_x_position,new_y_position,velocity):
        global score,incremental_enemy_speed,difficulty_level,player #basicaly each enemy lap.
    
        enemy_position = canvas.coords(enemy_model)
        #here we use the move_animation to define our enemy movement, in this case from the greater x value until next to 0
        
        #the difficulty goes higher acompaning the score

        incremental_enemy_speed=int(difficulty_level*score)/SCREEN_WIDTH

        print(f'important speed parameter: {new_x_position-incremental_enemy_speed}')


        #collision
        player_pos = canvas.coords(player)
        if int(player_pos[0])+PLAYER_PLANE_SIZE == int(enemy_position[0]) - ENEMY_PLANE_SIZE:
            score=0

        if(enemy_position[0]>0):
            #move different from moveto, it will specify the change in position regarding the earlier position.
            canvas.move(enemy_model,new_x_position-incremental_enemy_speed,new_y_position)
            #print(canvas.coords(enemy_model))
            canvas.after(velocity,move_animation,canvas,enemy_model,new_x_position,new_y_position,velocity)
        else:
            score +=1
            print(score)
            #increses the difficulty as the score goes higher
                        

            #reset the x and y position of the enemyship
            aux = int(enemy_position[1]) #aux its being used to put the enemy y axis within canvas range plus the plane_size
            random_y_position = random.randint(-aux+PLAYER_PLANE_SIZE,SCREEN_HEIGHT-aux-PLAYER_PLANE_SIZE)
            canvas.move(enemy_model,+SCREEN_WIDTH,random_y_position)
            #print(canvas.coords(enemy_model))
            canvas.after(velocity,move_animation,canvas,enemy_model,new_x_position,new_y_position,velocity)
if __name__=="__main__":
    main()