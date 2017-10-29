import sys
import pygame
from pygame.locals import *
import threading
from Craft import CraftClient
import time;
from pykeyboard import PyKeyboard

### init game window ###
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
WIDTH = 800
HEIGHT = 600
DELAY_TIME = 0.05
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


### keyboard value table ###
key_match = {K_a:"a",K_b:"b",K_c:"c",K_d:"d",K_e:"e",K_f:"f",K_g:"g",K_h:"h",K_i:"i",K_j:"j",K_k:"k",K_l:"l",K_m:"m",K_n:"n",K_o:"o",K_p:"p",K_q:"q",K_r:"r",K_s:"s",K_t:"t",K_u:"u",K_v:"v",K_w:"w",K_x:"x",K_y:"y",K_z:"z"}

sum_of_delta =[] ### store the delta value from turning the crown
key_in_word = '' ### store the keyboard value

### init the auto-pressing package ###
keyboard = PyKeyboard()

### draw the text on the window ###
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

### object_1 ###
def message_display(text):
    largeText = pygame.font.SysFont('Calibri',60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    windowSurface.blit(TextSurf, TextRect)

### object_2 ###
def message_display_2(text):
    largeText = pygame.font.SysFont('Calibri',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((WIDTH/2),(HEIGHT/3))
    windowSurface.blit(TextSurf, TextRect)

### show the text ###
def show():
	windowSurface.fill((0,0,0))
	message_display_2('You are choosing "'+key_in_word+'"')
	message_display('For hitting '+str(abs(sum(sum_of_delta)))+' times')
	pygame.display.update()
	time.sleep(DELAY_TIME)

### get the total delta from the rotation ###
def get_sum_of_delta():
	return sum(sum_of_delta)

### auto press n-times while n = total_delta ###
def auto_press_key():
	for i in range(abs(get_sum_of_delta())):
		keyboard.tap_key(key_in_word)
		print (key_in_word," (",i+1,")")
		time.sleep(DELAY_TIME)

### the handle of the crown event ###
def handleCraftEvent(event):
	if event['message_type'] == 'crown_turn_event':
		if event['delta'] < 0:
			sum_of_delta.append(event['delta'])
			get_sum_of_delta()
		if event['delta'] > 0:
			sum_of_delta.append(event['delta'])
			get_sum_of_delta()
	if event['message_type'] == 'crown_touch_event' and event['touch_state'] ==1 :
		print ('Choose how many times you want to auto-hitting')
	if event['message_type'] == 'crown_touch_event' and event['touch_state'] ==0 :
		show()
		auto_press_key()
		sum_of_delta.clear()

if __name__ == "__main__":

    craft = CraftClient()
    craft.connect("Python.app", "")
    craft.registerEventHandler(handleCraftEvent)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
            	### if receive key events , then show what it receive ###
                if event.key in key_match:
                	key_in_word = key_match[event.key]
                	show()