import tkinter as tk
import time
from tkinter import *
from PIL import Image, ImageTk
import random
import time
import os
import pygame


"""this is my final project for the amaizing free online course in the Codeinplace Stanford, where i met such awesome and inspiring people to guide me through! much thanks to my professors Chris, Mayahem and my section leader: Anwarul!'
,to generate the sounds and effect i used elevenlabs sound effects."""

#the constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
PLAYER_PLANE_SIZE = 100 #in pixels x and y axis.
ENEMY_PLANE_SIZE = 100


#the sound variable info
loop_track = True
pygame.mixer.init()
current_playback = None #a wave sound effect


def stop_song():
    pygame.mixer.music.stop()



def play_song(filename,Replay = True):
    global current_playback
    # Construct the sound path to a .wav sound file
    sound_path = os.path.join(os.getcwd(), 'sounds', filename)
    stop_song()
    # Load and play the new audio file
    if os.path.isfile(sound_path):
        if filename == 'collision.mp3':

            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(0)
            
            sound_path = os.path.join(os.getcwd(), 'sounds', 'sound_effect_3.wav')
        
            pygame.mixer.music.queue(sound_path, namehint="", loops=-1)
            
        else:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(-1 if Replay else 0)
            
       
        current_playback = filename
    else:
        print(f"File not found: {sound_path}")

    

#score system variables
score_text_display = None #the text representation in canvas of the score
score = 0

#number of lifes system variables
number_player_lifes = 3
player_lifes_image = []
player_lifes_obj = []

#enemy mobility variables

delay = [] #each enemy has its own speed independently
mobility = 20 #Mobility represents the amount of pixels the player's plane can turn in mid air.
enemy_mobility = 10 #base number for initial enemy speed

#incremental dificulty variables
incremental_enemy_speed = 0 
difficulty_level = 50

#important GLOBALS
start_game_text = None
player = None

#for the invencibility mechaniscs
first_runtime_secs = None

#intro
player_intro_image = None
player_intro_model = None

#player_image needs to be global to update for each "frame"
start_text = None
player_image = None
enemy_image = []

initial_x = None
initial_y = None
restricted_area = None
#the following code its for create a window/root, the part where differs from the Graphics canvas of Codeinplace editor, also its how you make loops in animation using function .after and the global .mainloop.

window = tk.Tk()
window.resizable(width=False, height=False)
window.title("SkyboundInPlace - Stanford")
window.geometry("1024x720")
canvas = None

def setup():
    global canvas,initial_x,initial_y,restricted_area
    canvas = tk.Canvas(window,width=SCREEN_WIDTH,height=SCREEN_HEIGHT)
    canvas.pack()
    #here its the position where the player starts
    initial_x = 0.3*SCREEN_WIDTH
    initial_y = SCREEN_HEIGHT/2


    #mobility and limitations of the players plane
    restricted_area =  mobility_area_plane(canvas)

   

#creating the helper functions




def create_transform_image(image_filename,size_x=PLAYER_PLANE_SIZE,size_y=PLAYER_PLANE_SIZE):
     #its will be a image of a player plane, but for now it will be a rectangular blue.
    
    #using some os propreties to find the current path and locate the images folder where its all images of the game
    image_path = os.path.join(os.getcwd(), "images", image_filename)
    image_player_id = Image.open(image_path)


    #resizing the image to the determinated size aka PLAYER_PLANE_SIZE.
    resized_image = image_player_id.resize((size_x, size_y), Image.Resampling.LANCZOS)
   
    return ImageTk.PhotoImage(resized_image)


def create_heart_display(canvas,filename):
    global player_lifes_obj,player_lifes_image
    #create a number of lifes for display on canvas.

    for i in range(number_player_lifes):
        player_lifes_image.append(create_transform_image(filename))
        player_lifes_obj.append(canvas.create_image((SCREEN_WIDTH*0.7 + 40*i,25),image=player_lifes_image[-1]))


def create_player_plane(canvas,position_x,position_y):
    
    global player_image
    player_image = create_transform_image('PLAYER_PLANE.png')
    return canvas.create_image(position_x, position_y, image=player_image)
     
def create_enemy_plane(canvas,position_x,position_y):

    """"function that creates the image of one enemy plane at the given position x,y"""

    global enemy_image
    
    enemy_image.append(create_transform_image('ENEMY_PLANE01.png'))

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
    
def move_down(event):
    position_player = canvas.coords(player)
    position_restricted_area = canvas.coords(restricted_area)

    #the condition in this case it will be the comparison of player y1 with y2 of both lists, index 1 and 3 respectively, while plane's y1 is less than y3 its fine
    if(position_player[1]+PLAYER_PLANE_SIZE/2<position_restricted_area[3]):
        canvas.move(player,0,mobility)
    
def move_left(event):
    position_player = canvas.coords(player)
    position_restricted_area = canvas.coords(restricted_area)
    #the condition in this case it will be the players x1  with the restricted_area x1, both index 0
    if(position_player[0]-PLAYER_PLANE_SIZE/2>position_restricted_area[0]):
        canvas.move(player,-mobility,0)
    
def move_right(event):
    position_player = canvas.coords(player)
    position_restricted_area = canvas.coords(restricted_area)
    #the condition in this case it will be the plane x1 with restricted_area x2 lists, index 0 and 2 respectively
    if(position_player[0]+PLAYER_PLANE_SIZE/2<position_restricted_area[2]):
        canvas.move(player,mobility,0)
        
def start_game(event):
    #until the window.bind(<x> not being press, the game doens't start)

    global start_game_text,player,score_text_display,player_intro_model,current_playback
    
    #buttom pressed
    play_song('start_game_pressed.mp3')
    time.sleep(1)
    #making sure <x> is pressed only once, for not simultanios spawn bug.
    if player is None:
        player = create_player_plane(canvas,initial_x,initial_y)




        #start song of gameplay
        play_song('sound_effect_3.wav')

        #number of enemies circulating '5'
        spawn_wave_enemies(canvas,5)
        create_heart_display(canvas,'life_player_heart.png')
        canvas.delete(player_intro_model)
        player_intro_model = None
        canvas.delete(start_game_text)
        
        #here we create our first display, it will be maintened by the update_text_function.
        score_text_display= canvas.create_text(100,20,fill="white",font="Times 20 italic bold",text=f'Score: {str(score)}')
    


def run_game():

    global player, start_game_text,number_player_lifes,player_intro_image,player_intro_model

    number_player_lifes = 3
    
    # until pressed x it will be the menu_screen
    
    
    canvas.create_rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,fill="black")
    
    player_intro_size = 300


    if not player_intro_model:
        player_intro_image = create_transform_image('PLAYER_PLANE.png',player_intro_size,player_intro_size)
        #must be global player_intro_image
        player_intro_model = canvas.create_image(0-player_intro_size/2,SCREEN_HEIGHT/2,image=player_intro_image)
        intro_animation(canvas,player_intro_model)



    start_game_text = canvas.create_text(SCREEN_WIDTH/2,SCREEN_HEIGHT*0.7,fill="white",font="Times 20 italic bold",text='press x to start the game!')



    play_song("SkyboundArcade.wav")

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
    window.bind('<x>',start_game)
    
    update_score_text()
    window.mainloop()


def main():
    #some differences from the lessons in the codeinplace compiler such as window and mainloop and the animation concepts that's uses .after and .coords from Canvas
    setup()
    run_game()


    
def update_score_text():
        canvas.itemconfigure(score_text_display, text=f'Score: {str(score)}')
        window.after(10, update_score_text)
   
def game_over():
    global player,score

    print('game over')
    play_song('game_over.mp3',False)
    time.sleep(3)
    player = None
    score = 0

    canvas.destroy()
    #returning to menu
    setup()
    run_game()



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

    move_animation(canvas,enemy_model,-enemy_mobility,0,velocity)


def is_invencible():
    global first_runtime_secs
    
    #if first_runtime is empty it will receive a value, else will not
    if not first_runtime_secs:
        play_song('collision.mp3')
        first_runtime_secs = time.time()



    current_runtime_secs = time.time()
    #giving 1 secs of invencibility

    time_elapsed = current_runtime_secs - first_runtime_secs
    if time_elapsed < 1:
        return False
    else:
        first_runtime_secs = None
        return True

def is_collided(plane_coords,plane2_coords):
    # given a coordinate of 
    delta_x = abs(plane2_coords[0] - plane_coords[0])
    delta_y = abs(plane2_coords[1] - plane_coords[1])
    
    
    if delta_x< PLAYER_PLANE_SIZE/4:
        if delta_y < PLAYER_PLANE_SIZE/4:
           
            #need to give invencibility for the player for 1 sec.
            return is_invencible()
        
    return False


def intro_animation(canvas,player_model):


    player_pos = canvas.coords(player_model)
    #print(player_pos)

    if player_pos:
        if player_pos[0]>SCREEN_WIDTH:
            canvas.move(player_model,-(SCREEN_WIDTH+300),0)
            canvas.after(100,intro_animation,canvas,player_model)
        else:
            canvas.move(player_model,20,0)
            canvas.after(100,intro_animation,canvas,player_model)



def move_animation(canvas,enemy_model,new_x_position,new_y_position,velocity):
        global score,incremental_enemy_speed,difficulty_level,player,number_player_lifes,player_lifes_obj #basicaly each enemy lap.
    
        enemy_position = canvas.coords(enemy_model)
        #here we use the move_animation to define our enemy movement, in this case from the greater x value until next to 0
        
        #the difficulty goes higher acompaning the score

        incremental_enemy_speed=int(difficulty_level*score)/SCREEN_WIDTH

        #print(f'important speed parameter: {new_x_position-incremental_enemy_speed}')


       
        player_pos = canvas.coords(player)
         #collision, when the player plane area intersect any enemy plane area, the life display should be reduced.
        
        if is_collided(player_pos,enemy_position):
  
            if player_lifes_obj:
                 canvas.delete(player_lifes_obj.pop())
            else:
                game_over()
            

        if(enemy_position[0]>0):
            #move different from moveto, it will specify the change in position regarding the earlier position.
            canvas.move(enemy_model,new_x_position-incremental_enemy_speed,new_y_position)
            #print(canvas.coords(enemy_model))
            canvas.after(velocity,move_animation,canvas,enemy_model,new_x_position,new_y_position,velocity)
        else:
            score +=1
            #print(score)
            #increses the difficulty as the score goes higher
                        

            #reset the x and y position of the enemyship
            aux = int(enemy_position[1]) #aux its being used to put the enemy y axis within canvas range plus the plane_size
            random_y_position = random.randint(-aux+PLAYER_PLANE_SIZE,SCREEN_HEIGHT-aux-PLAYER_PLANE_SIZE)
            canvas.move(enemy_model,+SCREEN_WIDTH,random_y_position)
            #print(canvas.coords(enemy_model))
            canvas.after(velocity,move_animation,canvas,enemy_model,new_x_position,new_y_position,velocity)
if __name__=="__main__":
    main()
