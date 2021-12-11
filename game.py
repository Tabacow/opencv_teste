from os import startfile
import numpy as np
import time
import keyboard
import random
import cv2

class Game:

    def __init__(self, vision, controller, heroes):
        self.vision = vision
        self.controller = controller
        self.heroes = heroes
        self.state = 'no status'
        self.working_time = 0 # working_time is set on seconds!
        self.shift_count = 0
        self.current_working_heroes = 15 # how many heroes you have?
        self.failed_captchas_count = 0

    def run(self):
        while True:
            self.vision.refresh_frame()

            if (self.check_errors()):
                self.reset_game()

            if(self.state == 'no status'):
                self.state = self.get_initial_state()

            if(self.check_captcha_popup()):
                self.log("im solving the captcha, this is real hard cause im a robot, ok?")
                okay = self.resolve_captcha()
                self.failed_captchas_count += 1
                if(okay):
                    self.failed_captchas_count = 0
                print(self.failed_captchas_count)
            
            if self.state == 'not started' and self.is_connect_screen():
                self.log('Connecting...')
                self.launch_player()
                self.state = 'authorize'

            self.vision.refresh_frame()
            if(not (self.state == 'not started' or self.state=='authorize') and self.is_connect_screen()):
                self.log("im not supposed to be here")
                self.reset_game()

            if self.state == 'authorize' and self.is_authorize() and self.check_metamask_popup_check():
                self.log('Authorized! Now Loading...')
                self.authorize_metamask()
                self.state = 'in menu'

            #if self.state == 'authorize' and not self.is_authorize() and not self.check_metamask_popup_check():
            #    self.log('Let me search for the authorization popup...')
            #    self.search_for_authorize_metamask()
            
            if self.state == 'in menu' and self.is_menu():
                self.log('in game menu, going to heroes...')
                self.open_heroes()
                self.state = 'heroes opened'

            if self.state == 'heroes opened' and self.is_on_hero_menu():
                self.log('in hero menu opened sucessfully')
                self.state = 'hero menu'

            if self.state == 'hero menu' and self.is_on_hero_menu():
                self.log('hero menu opened!')
                self.state = 'selecting heroes'

            if self.state == 'selecting heroes' and self.is_heroes_resting():
                self.log('selecting heroes...')
                okay = self.send_heroes_to_work()
                if(okay):
                    self.state = 'lets go to work!'
                if(not okay):
                    self.reset_game()
#
            if self.state == 'lets go to work!' and self.is_on_hero_menu():
                self.log('selecting heroes...')
                self.exit_heroes()
                self.state = 'going to game'
#
            if self.state == 'going back to menu' and self.is_in_game():
                self.log('going back to menu...')
                self.from_game_to_menu()
                self.state = 'in menu'
#
            if self.state == 'going back to menu' and not self.is_in_game():
                self.log("something went wrong, reseting...")
                self.reset_game()
#
            if self.state == 'going to game' and self.is_menu():
                self.log('going to game...')
                self.go_to_game()
                self.state = 'im on game'
#
            if(self.state == 'im on game' and self.is_new_map()):
                self.log('going to next map...')
                self.go_to_next_map()
                
            if(self.state == 'im on game' and self.is_in_game()):
                self.log('im gamming... >:(')
                self.counting_work_time()
                if(self.working_time == 0 ):
                    self.heroes.change_all_to_false()
                    self.heroes.print_hero_status()
                    self.state = 'going back to menu'
#
            time.sleep(1)



    def launch_player(self):
        # Try multiple sizes of goalpost due to perspective changes for
        # different opponents
        scales = [1.2, 1.1, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97, 0.96, 0.95]
        matches = self.vision.scaled_find_template('connect-wallet', threshold=0.75, scales=scales)
        if(np.shape(matches)[1] >= 1):
            x = matches[1][0] + self.add_x_random_movement()
            y = matches[0][0] + self.add_y_random_movement()
            self.controller.move_mouse(x+60,y+20)
            time.sleep(0.2)
            self.controller.left_mouse_click()
            time.sleep(0.5)
    
    def login_metamask(self):
        matches = self.vision.find_template('metamask', threshold=0.8)
        if(np.shape(matches)[1] >= 1):
            x = matches[1][0] + self.add_x_random_movement()
            y = matches[0][0] + self.add_y_random_movement()
            self.controller.move_mouse(x+45,y+20)
            time.sleep(0.2)
            self.controller.left_mouse_click()
            time.sleep(0.2)
        else:
            matches = self.vision.find_template('metamask-dark', threshold=0.8)
            if(np.shape(matches)[1] >= 1):
                x = matches[1][0] + self.add_x_random_movement()
                y = matches[0][0] + self.add_y_random_movement()
                self.controller.move_mouse(x+45,y+20)
                time.sleep(0.2)
                self.controller.left_mouse_click()
                time.sleep(0.2)
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

    def search_for_authorize_metamask(self):
        match = self.vision.find_template('metamask-popup-right-side', threshold=0.9)
        if(np.shape(match)[1] >= 1):
                x = match[1][0] + self.add_x_random_movement()
                y = match[0][0] + self.add_y_random_movement()
                self.controller.move_mouse(x+45,y+20)
                time.sleep(0.2)
                self.controller.left_mouse_click()
                time.sleep(0.2)

    def open_heroes(self):
        matches = self.vision.find_template('heroes', threshold=0.9)
        x = matches[1][0] + self.add_x_random_movement()
        y = matches[0][0] + self.add_y_random_movement()
        self.controller.move_mouse(x,y)
        time.sleep(0.2)
        self.controller.left_mouse_click()
        time.sleep(0.2)

    def counting_work_time(self):
        time_period = 60
        self.working_time = self.working_time - time_period
        time.sleep(time_period)
        self.log("there is still " + str(self.working_time/time_period) + " minutes left...")
        self.shift_count += 1
        if((self.shift_count % 5) == 0):
            if(self.check_errors() or not self.is_in_game):
                self.reset_game()
                return
            self.from_game_to_menu()
            time.sleep(3)
            self.vision.refresh_frame()
            
            self.state = "going to game"
            
  
    def send_heroes_to_work(self):
        self.log("now im selecting heroes...")
        self.vision.refresh_frame()
        match = self.vision.find_template('heroes-header', threshold=0.95)
        x = match[1][0] + 75 + self.add_x_random_movement()
        y = match[0][0] + 75 + self.add_y_random_movement()
        self.controller.move_mouse(x,y)
        time.sleep(0.2)
        scroll = 0
        okay = True
        while(not self.heroes.is_all_heroes_working() and self.is_on_hero_menu()):
            okay = self.find_heroes_in_vision()
            if(not okay):
                return okay
            while(scroll < 20):
                self.controller.mouse_scroll(0,-1)
                time.sleep(0.1)
                scroll += 1
            scroll = 0
        self.log("found all heroes...")
        return okay


    def find_heroes_in_vision(self):
        hero_count = 1
        while(hero_count <= self.current_working_heroes):
            self.vision.refresh_frame()
            if (self.check_errors()):
                self.log("SOMETHING WENT WRONG, IM GOING TO RESET!")
                return False
                
            self.log("looking for hero " + str(hero_count))
            match_hero = self.vision.find_template(str(hero_count), threshold=0.95)
            if(np.shape(match_hero)[1] >= 1):
                match_work = self.vision.find_template('work-off', threshold=0.8)
                if(not np.shape(match_work)[1] >= 1):
                    match_work = self.vision.find_template('work-on', threshold=0.8)
                if(np.shape(match_work)[1] >= 1):
                    x = match_work[1][0] + 10 + self.add_x_random_movement()
                    y = match_hero[0][0] + 10 + self.add_y_random_movement()
                    self.controller.move_mouse(x,y)
                    time.sleep(0.2)
                    self.controller.left_mouse_click()
                    time.sleep(1)
                else:
                    self.log("hmmm... weird. Call Mr Tobacco if the game crashes")
                    self.log("im proceeding, maybe the hero will work as he should")
                self.heroes.change_status(hero_count, True)
                self.log("found hero " + str(hero_count))
            hero_count += 1
            time.sleep(0.1)
        self.heroes.print_hero_status()
        return True

        


    def exit_heroes(self):
        matches = self.vision.find_template('exit-heroes', threshold=0.9)
        x = matches[1][0] + self.add_x_random_movement()
        y = matches[0][0] + self.add_y_random_movement()
        self.controller.move_mouse(x,y)
        time.sleep(0.4)
        self.controller.left_mouse_click()

    def go_to_game(self):
        if(self.working_time == 0):
            self.working_time = 3300
            self.shift_count = 0
        else:
            self.log("there is still " + str(self.working_time) + " seconds of working time left!!!")
        matches = self.vision.find_template('game', threshold=0.6)
        if(self.check_errors() or not self.is_menu()):
                self.reset_game()
                return
        x = matches[1][0] + self.add_x_random_movement()
        y = matches[0][0] + self.add_y_random_movement()
        self.controller.move_mouse(x+30,y+30)
        time.sleep(0.4)
        self.controller.left_mouse_click()

    def check_errors(self):
        self.vision.refresh_frame()
        match_unknown = self.vision.find_template('unknown', threshold=0.7)
        match_overloaded = self.vision.find_template('overloaded', threshold=0.7)
        match_abnormal_disconection = self.vision.find_template('abnormal-disconection', threshold=0.7)
        match_socket_1 = self.vision.find_template('socket-1', threshold=0.7)
        match_manual = self.vision.find_template('manual', threshold=0.7)
        match_communication_error = self.vision.find_template('communication-error', threshold=0.7)
        connection_error = self.vision.find_template('communication-error', threshold=0.7)
        is_error_unknown =  np.shape(match_unknown)[1] >= 1
        is_error_overloaded =  np.shape(match_overloaded)[1] >= 1
        is_error_abnormal_disconetion =  np.shape(match_abnormal_disconection)[1] >= 1
        is_error_socket_1 =  np.shape(match_socket_1)[1] >= 1
        is_error_manual =  np.shape(match_manual)[1] >= 1
        is_error_communication_error =  np.shape(match_communication_error)[1] >= 1
        is_connection_error = np.shape(connection_error)[1] >= 1
        failed_captcha = False
        if(self.failed_captchas_count >= 3):
            failed_captcha = True
            self.failed_captchas_count = 0
        return is_error_unknown or is_error_overloaded or is_error_abnormal_disconetion or is_error_socket_1 or is_error_manual or is_error_communication_error or is_connection_error or failed_captcha

    def from_game_to_menu(self):
        matches = self.vision.find_template('go-back', threshold=0.6)
        if(np.shape(matches)[1] >= 1):
            x = matches[1][0] + self.add_x_random_movement()
            y = matches[0][0] + self.add_y_random_movement()
            self.controller.move_mouse(x+20,y+20)
            time.sleep(0.4)
            self.controller.left_mouse_click()

    def go_to_next_map(self):
        matches = self.vision.find_template('new-map', threshold=0.6)
        x = matches[1][0] + self.add_x_random_movement()
        y = matches[0][0] + self.add_y_random_movement()
        self.controller.move_mouse(x+20,y+20)
        time.sleep(0.4)
        self.controller.left_mouse_click()

    def resolve_captcha_old(self): #captcha resolver from when the captcha was a jigglesaw piece
        self.vision.refresh_frame()
        ROI = self.vision.find_jigsaw()
        time.sleep(0.2)
        if(not np.shape(ROI)[1] >= 1): #if ROI is not found, reset
            self.reset_game()
            return
        pieces_start_pos = self.vision.find_template_by_generated_template(template=ROI,threshold=0.5)
        if(not np.shape(pieces_start_pos)[1] >= 1): #if pieces_start_pos is not found, reset
            self.reset_game()
            return
        self.vision.refresh_frame()
        contour_result = self.vision.find_contour()
        self.vision.refresh_frame()
        slider_start_pos = self.vision.find_template('slider', threshold=0.92)
        if(not np.shape(slider_start_pos)[1] >= 1): #if slider_start_pos is not found, reset
            self.reset_game()
            return
        x_start = slider_start_pos[1][0] + self.add_x_random_movement(x0 = 0, x = 5)
        y_start = slider_start_pos[0][0] + self.add_y_random_movement(y0 = 0, y = 3)
        time.sleep(0.2)
        self.controller.move_mouse(x_start,y_start)
        time.sleep(0.2)
        self.vision.refresh_frame()
        piece_start = pieces_start_pos[1][0]+25
        piece_middle  = contour_result[0]
        slider_start = x_start
        self.controller.move_mouse(slider_start,y_start)
        time.sleep(0.3)
        self.controller.left_mouse_press()

        threshold = abs(piece_start - piece_middle)
        repeated_value=0
        repeated_value_count=0
        success = True
        while(threshold>=2):
            self.vision.refresh_frame()
            pieces_start_pos = self.vision.find_template_by_generated_template(template=ROI,threshold=0.4)
            piece_start = pieces_start_pos[1][0]+25
            threshold = abs(piece_start - piece_middle)
            print("distance to my trajectory: "+str(threshold))
            self.controller.move_mouse(slider_start,y_start)
            slider_start += 1 + random.randint(0,1)
            y_start += random.randint(-2,2)
            if(repeated_value==threshold):
                repeated_value_count+=1
            else:
                repeated_value_count=0
            if(repeated_value_count >= 6):
                success = False
                break
            repeated_value = threshold
        
        time.sleep(1)
        if(self.check_captcha_popup()):
            success = False
        if(success):
            self.failed_captchas_count = 0

        self.controller.left_mouse_release()
        #self.controller.move_mouse(slider_awnser,y_start)
        time.sleep(0.2)
        #self.controller.left_mouse_release()

    def resolve_captcha(self):
        self.vision.refresh_frame()
        slider_start_pos = self.vision.find_template('slider', threshold=0.80)
        number_sequence = self.vision.find_number_sequence()
        if(not np.shape(slider_start_pos)[1] >= 1): #if slider_start_pos is not found, reset
            self.reset_game()
            return
        x_start = slider_start_pos[1][0] + 10
        y_slider = slider_start_pos[0][0] + 10
        self.controller.move_to_with_randomness(x_start+10,y_slider+10, 0.5)
        time.sleep(0.1)
        self.controller.left_mouse_press()
        time.sleep(0.1)
        self.controller.move_to_with_randomness(x_start+400,y_slider, 0.5)
        time.sleep(1)
        self.vision.refresh_frame()
        
        slider_end_pos = self.vision.find_template('slider', threshold=0.80)
        x_end = slider_end_pos[1][0] + 10
        time.sleep(1)

        self.controller.move_to_with_randomness(x_start,y_slider, 0.5)
        time.sleep(0.1)
        # variação do slider
        delta_x = abs(x_start - x_end)
        # Determinando as posições chave do slider
        first_position  =   x_start
        second_position =   x_start + delta_x*0.25
        third_position  =   x_start + delta_x*0.5
        fourth_position =   x_start + delta_x*0.75
        fifth_position  =   x_end

        positions = [first_position, second_position, third_position, fourth_position, fifth_position]
        
        print(positions)

        mouse_x_movement = x_start
        mouse_y_movement = y_slider
        
        

        for position in positions:
            print(position)
            threshold = abs(mouse_x_movement - position)
            while(threshold>=2):
                mouse_x_movement += 1 + self.add_x_random_movement(x0 = 0, x = 1)
                mouse_y_movement += self.add_y_random_movement(y0 = -1, y = 1)
                threshold = abs(mouse_x_movement - position)
                time.sleep(0.025)
                self.controller.move_mouse(mouse_x_movement,mouse_y_movement)

            time.sleep(1)
            
            counter= 0

            check_tries = []
            while(counter < 5):
                self.vision.refresh_frame()
                crooked_number_sequence = self.vision.find_captcha_crooked_numbers(number_sequence)
                if(crooked_number_sequence == None):
                    counter += 1
                    continue
                check_array = self.is_correct_number_order_by_position(number_sequence, crooked_number_sequence)
                found = self.is_correct_number_order(number_sequence, crooked_number_sequence)

                
                if(np.all(check_array)):
                    self.log("looks like i did it guys")
                    self.controller.left_mouse_release()
                    time.sleep(1)
                    return True
                else:
                    self.log("not this one...")
                counter += 1
                print(counter)
                time.sleep(0.1)
                check_tries.append(check_array)

        self.controller.left_mouse_release()
        self.log("i coulnt make it :(")
        return False

        
    def is_correct_number_order(self, numbers, crooked_numbers): #(pergunta)
        first_number_is_equal = (numbers[0][0] == crooked_numbers[0][0])
        second_number_is_equal = (numbers[1][0] == crooked_numbers[1][0])
        third_number_is_equal = (numbers[2][0] == crooked_numbers[2][0])
        return first_number_is_equal and second_number_is_equal and third_number_is_equal
        
    def is_correct_number_order_by_position(self, numbers, crooked_numbers): #(pergunta)
        first_number_is_equal = (numbers[0][0] == crooked_numbers[0][0])
        second_number_is_equal = (numbers[1][0] == crooked_numbers[1][0])
        third_number_is_equal = (numbers[2][0] == crooked_numbers[2][0])
        return [first_number_is_equal, second_number_is_equal, third_number_is_equal]

    def get_initial_state(self):
        self.log("getting initial state...")
        if(self.working_time > 0):
            self.log("there is still game time")
            return "going to game"
        else:
            if(self.is_connect_screen()):
                self.log("not started? no problem! starting...")
                return "not started"
            if(self.is_menu()):
                self.log("hmm the menu? can i get some spaghetti and meatballs?")
                return "in menu"
            if(self.is_on_hero_menu()):
                self.log("heroes menu? lets send em to work!")
                return "hero menu"
            if(self.is_in_game()):
                self.log("looks like you're in the game, thats not allowed >:(, im going back to the menu!")
                return "going back to menu"
    
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

    def check_metamask_popup_check(self):
        matches = self.vision.find_template('metamask-popup-check', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def check_bomb_crypto_logo(self):
        matches = self.vision.find_template('bomb-crypto-logo', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def check_captcha_popup(self):
        matches = self.vision.find_template('are_you_a_robot', threshold=0.9)
        return np.shape(matches)[1] >= 1

    def add_x_random_movement(self, x0 = 0, x = 30):
        result = random.randint(x0, x)
        return result

    def add_y_random_movement(self, y0 = 0, y = 20):
        result = random.randint(y0, y)
        return result
    
    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))

    def reset_game(self):
        keyboard.press_and_release('ctrl+r')
        self.state = 'not started'