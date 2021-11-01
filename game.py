from os import startfile
import numpy as np
import time
import keyboard

class Game:

    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.state = 'not started'

    def run(self):
        while True:
            self.vision.refresh_frame()

            if (self.check_errors()):
                keyboard.press_and_release('F5')
                self.state = 'not started'

            if self.state == 'not started' and self.is_connect_screen():
                self.log('Connecting...')
                self.launch_player()
                self.state = 'connecting'

            if self.state == 'connecting' and self.is_select_wallet():
                self.log('Authorizing...')
                self.login_metamask()
                self.state = 'authorize'

            if self.state == 'authorize' and self.is_authorize():
                self.log('Authorized! Now Loading...')
                self.authorize_metamask()
                self.state = 'in menu'
            
            if self.state == 'in menu' and self.is_menu():
                self.log('in game menu, going to heroes...')
                self.open_heroes()
                self.state = 'heroes opened'

            if self.state == 'heroes opened' and self.is_on_hero_menu():
                self.log('in hero menu, scrolling down...')
                self.state = 'hero menu'

            if self.state == 'hero menu' and self.is_on_hero_menu():
                self.log('hero menu opened!')
                self.state = 'selecting heroes'

            if self.state == 'selecting heroes' and self.is_heroes_resting():
                self.log('scrolling...')
                self.send_heroes_to_work()
                self.state = 'lets go to work!'

            if self.state == 'lets go to work!' and self.is_on_hero_menu():
                self.log('selecting heroes...')
                self.exit_heroes()
                self.state = 'going to game'

            if self.state == 'going back to menu' and self.is_in_game():
                self.log('going back to menu...')
                self.from_game_to_menu()
                self.state = 'in menu'

            if self.state == 'going to game' and self.is_menu():
                self.log('going to game...')
                self.go_to_game()

            if(self.state == 'im on game' and self.is_new_map()):
                self.log('going to next map...')
                self.go_to_next_map()
                
            if(self.state == 'im on game' and self.is_in_game()):
                self.log('im gamming... >:(')
                time.sleep(3000)
                self.state = 'going back to menu'

            time.sleep(1)

#    def round_starting(self, player):
#        matches = self.vision.find_template('%s-health-bar' % player)
#        return np.shape(matches)[1] >= 1

    def launch_player(self):
        # Try multiple sizes of goalpost due to perspective changes for
        # different opponents
        scales = [1.2, 1.1, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97, 0.96, 0.95]
        matches = self.vision.scaled_find_template('connect-wallet', threshold=0.75, scales=scales)
        x = matches[1][0]
        y = matches[0][0]
        self.controller.move_mouse(x+60,y+20)
        self.controller.left_mouse_click()

        time.sleep(0.5)
    
    def login_metamask(self):
        matches = self.vision.find_template('metamask', threshold=0.9)
        x = matches[1][0]
        y = matches[0][0]
        self.controller.move_mouse(x+45,y+20)
        self.controller.left_mouse_click()
        time.sleep(0.2)

    def authorize_metamask(self):
            keyboard.press_and_release('tab')
            time.sleep(0.2)
            keyboard.press_and_release('tab')
            time.sleep(0.2)
            keyboard.press_and_release('tab')
            time.sleep(0.2)
            keyboard.press_and_release('enter')
            time.sleep(0.2)
    
    def open_heroes(self):
        matches = self.vision.find_template('heroes', threshold=0.9)
        x = matches[1][0]
        y = matches[0][0]
        self.controller.move_mouse(x,y)
        self.controller.left_mouse_click()
        time.sleep(0.2)

    def send_heroes_to_work(self):
        i=1
        while(i<=15):
            self.vision.refresh_frame()
            match_hero = self.vision.find_template_and_print(str(i), threshold=0.96)
            match_work = self.vision.find_template('work-off', threshold=0.90)
            if(np.shape(match_hero)[1] >= 1 and np.shape(match_work)[1] >= 1):
                x = match_work[1][0] + 10
                y = match_hero[0][0] + 10
                self.controller.move_mouse(x,y)
                time.sleep(0.2)
                self.controller.left_mouse_click()
                time.sleep(0.1)
                self.log("i found hero "+ str(i) + "!")
                i += 1
            self.controller.mouse_scroll(0,-100)
            time.sleep(0.1)
            self.controller.mouse_scroll(0,-100)
            time.sleep(0.1)
            self.controller.mouse_scroll(0,-100)
            time.sleep(0.1)
            self.controller.mouse_scroll(0,-100)
            time.sleep(0.1)

    def exit_heroes(self):
        matches = self.vision.find_template('exit-heroes', threshold=0.9)
        x = matches[1][0]
        y = matches[0][0]
        self.controller.move_mouse(x,y)
        time.sleep(0.4)
        self.controller.left_mouse_click()

    def go_to_game(self):
        matches = self.vision.find_template('game', threshold=0.8)
        
        x = matches[1][0]
        y = matches[0][0]
        self.controller.move_mouse(x+30,y+30)
        time.sleep(0.4)
        self.controller.left_mouse_click()

    def check_errors(self):
        match_unknown = self.vision.find_template('unknown', threshold=0.7)
        match_overloaded = self.vision.find_template('overloaded', threshold=0.7)
        is_error_unknown =  np.shape(match_unknown)[1] >= 1
        is_error_overloaded =  np.shape(match_overloaded)[1] >= 1
        return is_error_unknown or is_error_overloaded

    def from_game_to_menu(self):
        matches = self.vision.find_template('go-back', threshold=0.6)
        x = matches[1][0]
        y = matches[0][0]
        self.controller.move_mouse(x+20,y+20)
        time.sleep(0.4)
        self.controller.left_mouse_click()

    #def is_everyone_sleeping(self):
    #    blank_sleep = self.vision.count_item_on_image(object="blank-sleep")
    #    one_z = self.vision.count_item_on_image(object="one-z-sleep")
    #    two_z = self.vision.count_item_on_image(object="two-z-sleep")
    #    three_z = self.vision.count_item_on_image(object="three-z-sleep")
    #    total = blank_sleep + one_z + two_z + three_z
    #    self.log("i found " + str(total) + ' sleepyheads!') 
    #    return total == 15

    def go_to_next_map(self):
        matches = self.vision.find_template('new-map', threshold=0.6)
        x = matches[1][0]
        y = matches[0][0]
        self.controller.move_mouse(x+20,y+20)
        time.sleep(0.4)
        self.controller.left_mouse_click()

    def is_select_wallet(self):
        matches = self.vision.find_template('select-wallet', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def is_authorize(self):
        matches = self.vision.find_template('metamask-popup', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def is_heroes_resting(self):
        matches = self.vision.find_template('work-off', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def is_menu(self):
        matches = self.vision.find_template('game-screen', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def is_on_hero_menu(self):
        matches = self.vision.find_template('heroes-header', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def is_in_game(self):
        matches = self.vision.find_template('in-game-chest-and-options', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def is_connect_screen(self):
        matches = self.vision.find_template('connect-screen', threshold=0.9)
        return np.shape(matches)[1] >= 1
        
    def is_new_map(self):
        matches = self.vision.find_template('next-map', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
