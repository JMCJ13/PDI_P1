#Importacion de librerias a utilizar
import cv2
import imutils
import turtle
import math
import random
import time


#Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
	border_pen.fd(600)
	border_pen.lt(90)
border_pen.hideturtle()	


#Set the score to 0
score = 0

#Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("classic") #############
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

#Choose a number of enemies
number_of_enemies = 5
#Create an empty list of enemies
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
	#Create the enemy
	enemies.append(turtle.Turtle())
    
for enemy in enemies:
	enemy.color("red")
	enemy.shape("circle")###########
	enemy.penup()
	enemy.speed(0)
	x = random.randint(-200, 200)
	y = random.randint(100, 250)
	enemy.setposition(x, y)

enemyspeed = 2


#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

#Define bullet state
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"


#Move the player left and right
def move_left():
	x = player.xcor()
	x -= playerspeed
	if x < -280:
		x = - 280
	player.setx(x)
	
def move_right():
	x = player.xcor()
	x += playerspeed
	if x > 280:
		x = 280
	player.setx(x)
	
def fire_bullet():
	#Declare bulletstate as a global if it needs changed
	global bulletstate
	if bulletstate == "ready":
		bulletstate = "fire"
		#Move the bullet to the just above the player
		x = player.xcor()
		y = player.ycor() + 10
		bullet.setposition(x, y)
		bullet.showturtle()

def isCollision(t1, t2):
	distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
	if distance < 15:
		return True
	else:
		return False
    
#Funcion para cerrar el juego 
def Close_all():
    cap.release()
    cv2.destroyAllWindows()
    wn.clear()
    turtle.write("Game Over", move = False, align = "center", font = ("Arial", 30, "normal"))
    time.sleep(3)
    wn._delete("all")
    wn.bye()
    #exit()
    
    '''
def iniciar_mano():
    bg = cv2.cvtColor(frameAux,cv2.COLOR_BGR2GRAY)
    '''
    
def rec_acciones():
    # Determinar la región de interés
    ROI = frame[5:350,200:635]
    grayROI = cv2.cvtColor(ROI,cv2.COLOR_BGR2GRAY)
    
    # Región de interés del fondo de la imagen
    bgROI = bg[5:350,200:635]
    
    dif = cv2.absdiff(grayROI,bgROI)
    _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
    th = cv2.medianBlur(th, 7)
    
    # Encontrando los contornos de la imagen binaria
    cnts, _ = cv2.findContours(th,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:1]
    cv2.drawContours(ROI, cnts, 0, (0,255,0),1)
    
    for cnt in cnts:

        # Encontrar el centro del contorno
        M = cv2.moments(cnt)
        if M["m00"] == 0: M["m00"]=1
        x = int(M["m10"]/M["m00"])
        y = int(M["m01"]/M["m00"])
        cv2.circle(ROI,tuple([x,y]),5,(0,255,0),-1)
        
        # Punto más alto del contorno
        ymin = cnt.min(axis=1)
        cv2.circle(ROI,tuple(ymin[0]),5,color_ymin,-1)
        
        # Contorno encontrado a través de cv2.convexHull
        hull1 = cv2.convexHull(cnt)
        cv2.drawContours(ROI,[hull1],0,color_contorno,2)
    
    if (x<150): move_left()
    if (x>285): move_right()
    if (abs(y-ymin[0][1])>100): fire_bullet()
    else: print("disparar")
    
def rec_acciones():
    # Determinar la región de interés
    ROI = frame[5:350,200:635]
    grayROI = cv2.cvtColor(ROI,cv2.COLOR_BGR2GRAY)
    
    # Región de interés del fondo de la imagen
    bgROI = bg[5:350,200:635]
    
    dif = cv2.absdiff(grayROI,bgROI)
    _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
    th = cv2.medianBlur(th, 7)
    
    # Encontrando los contornos de la imagen binaria
    cnts, _ = cv2.findContours(th,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:1]
    cv2.drawContours(ROI, cnts, 0, (0,255,0),1)
    
    for cnt in cnts:

        # Encontrar el centro del contorno
        M = cv2.moments(cnt)
        if M["m00"] == 0: M["m00"]=1
        x = int(M["m10"]/M["m00"])
        y = int(M["m01"]/M["m00"])
        cv2.circle(ROI,tuple([x,y]),5,(0,255,0),-1)
        
        # Punto más alto del contorno
        ymin = cnt.min(axis=1)
        cv2.circle(ROI,tuple(ymin[0]),5,color_ymin,-1)
        
        # Contorno encontrado a través de cv2.convexHull
        hull1 = cv2.convexHull(cnt)
        cv2.drawContours(ROI,[hull1],0,color_contorno,2)
    
    if (x<150): move_left()
    if (x>285): move_right()
    if (abs(y-ymin[0][1])<100): fire_bullet()
    else: print("disparar")
    
    


#Create keyboard bindings
turtle.listen()
#turtle.onkey(move_left, "Left")
#turtle.onkey(move_right, "Right")
#turtle.onkey(fire_bullet, "space")
turtle.onkey(Close_all, "Escape")

#Start videocapture with cv2
cap = cv2.VideoCapture(0,cv2.CAP_MSMF)
bg = None
color_contorno = (0,255,0)
color_ymin = (0,130,255)
color_zona1 = (0,255,255)
color_zona2 = (0,0,255)


#Main loop for the game
while True:
    
    ret, frame = cap.read()
    if ret == False: break

    # Redimensionar la imagen para que tenga un ancho de 640
    frame = imutils.resize(frame,width=640)
    frame = cv2.flip(frame,1)
    frameAux = frame.copy()
    
    cv2.rectangle(frame,(200-1,5-1),(635+1,350+1),color_zona1,1)
    cv2.rectangle(frame,(200,5),(350,350),color_zona2,1)
    cv2.rectangle(frame,(485,5),(635,350),color_zona2,1)
    
    if bg is not None: rec_acciones()
        
    for enemy in enemies:
        #Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        
        #Move the enemy back and down
        if enemy.xcor() > 280:
            #Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            #Change enemy direction
            enemyspeed *= -1
        
        if enemy.xcor() < -280:
            #Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            #Change enemy direction
            enemyspeed *= -1
            
            
        #Check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            #Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            #Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            #Update the score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
            
        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print ("Game Over")
            break
    
    #Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)
    
    #Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    
    cv2.imshow('Frame',frame)
    
    k = cv2.waitKey(20)
    if k == ord('i'):
        bg = cv2.cvtColor(frameAux,cv2.COLOR_BGR2GRAY)

    


