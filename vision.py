import cv2
from mss import mss
from PIL import Image
import numpy as np

class Vision:
    def __init__(self):
        self.static_templates = {
            'characters-actions': 'assets/characters-actions.png',
            'connect-wallet': 'assets/connect-wallet.png',
            'exit-heroes': 'assets/exit-heroes.png',
            'game-screen': 'assets/game-screen.png',
            'go-back': 'assets/go-back.png',
            'metamask': 'assets/metamask.png',
            'metamask-dark': 'assets/metamask-dark.png',
            'metamask-popup': 'assets/metamask-popup.png',
            'metamask-popup-check': 'assets/metamask-popup-check.png',
            'select-wallet': 'assets/select-wallet.png',
            'heroes': 'assets/heroes.png',
            'rest-on': 'assets/rest-on.png',
            'rest-off': 'assets/rest-off.png',
            'work-on': 'assets/work-on.png',
            'work-off': 'assets/work-off.png',
            'energy-full': 'assets/energy-full.png',
            'heroes-header': 'assets/heroes-header.png',
            'game': 'assets/game.png',
            'in-game-chest-and-options': 'assets/in-game-chest-and-options.png',
            'connect-screen' : 'assets/connect-screen.png',
            'unknown': 'assets/errors/unknown.png',
            'overloaded': 'assets/errors/overloaded.png',
            'new-map':'assets/new-map.png',
            'next-map':'assets/next-map.png',
            'bomb-crypto-logo' : 'assets/bomb-crypto-logo.png',
            'abnormal-disconection' : 'assets/errors/abnormal-disconection.png',
            'communication-error' : 'assets/errors/communication-error.png',
            'socket-1': 'assets/errors/socket-1.png',
            'manual': 'assets/errors/manual.png',
            'connection-error': 'assets/connection-error.png',
            '1': 'assets/heroes/1.png',
            '2': 'assets/heroes/2.png',
            '3': 'assets/heroes/3.png',
            '4': 'assets/heroes/4.png',
            '5': 'assets/heroes/5.png',
            '6': 'assets/heroes/6.png',
            '7': 'assets/heroes/7.png',
            '8': 'assets/heroes/8.png',
            '9': 'assets/heroes/9.png',
            '10': 'assets/heroes/10.png',
            '11': 'assets/heroes/11.png',
            '12': 'assets/heroes/12.png',
            '13': 'assets/heroes/13.png',
            '14': 'assets/heroes/14.png',
            '15': 'assets/heroes/15.png',
            '0_captcha' : 'assets/captcha/0.png',
            '1_captcha' : 'assets/captcha/1.png',
            '2_captcha' : 'assets/captcha/2.png',
            '3_captcha' : 'assets/captcha/3.png',
            '4_captcha' : 'assets/captcha/4.png',
            '5_captcha' : 'assets/captcha/5.png',
            '6_captcha' : 'assets/captcha/6.png',
            '7_captcha' : 'assets/captcha/7.png',
            '8_captcha' : 'assets/captcha/8.png',
            '9_captcha' : 'assets/captcha/9.png',
            '0_crooked' : 'assets/captcha/0_crooked.png',
            '1_crooked' : 'assets/captcha/1_crooked.png',
            '2_crooked' : 'assets/captcha/2_crooked.png',
            '3_crooked' : 'assets/captcha/3_crooked.png',
            '4_crooked' : 'assets/captcha/4_crooked.png',
            '5_crooked' : 'assets/captcha/5_crooked.png',
            '6_crooked' : 'assets/captcha/6_crooked.png',
            '7_crooked' : 'assets/captcha/7_crooked.png',
            '8_crooked' : 'assets/captcha/8_crooked.png',
            '9_crooked' : 'assets/captcha/9_crooked.png',
            '0_crooked_mask' : 'assets/captcha/0_crooked_mask.png',
            '1_crooked_mask' : 'assets/captcha/1_crooked_mask.png',
            '2_crooked_mask' : 'assets/captcha/2_crooked_mask.png',
            '3_crooked_mask' : 'assets/captcha/3_crooked_mask.png',
            '4_crooked_mask' : 'assets/captcha/4_crooked_mask.png',
            '5_crooked_mask' : 'assets/captcha/5_crooked_mask.png',
            '6_crooked_mask' : 'assets/captcha/6_crooked_mask.png',
            '7_crooked_mask' : 'assets/captcha/7_crooked_mask.png',
            '8_crooked_mask' : 'assets/captcha/8_crooked_mask.png',
            '9_crooked_mask' : 'assets/captcha/9_crooked_mask.png',
            '0_mask' : 'assets/captcha/0_mask.png',
            '1_mask' : 'assets/captcha/1_mask.png',
            '2_mask' : 'assets/captcha/2_mask.png',
            '3_mask' : 'assets/captcha/3_mask.png',
            '4_mask' : 'assets/captcha/4_mask.png',
            '5_mask' : 'assets/captcha/5_mask.png',
            '6_mask' : 'assets/captcha/6_mask.png',
            '7_mask' : 'assets/captcha/7_mask.png',
            '8_mask' : 'assets/captcha/8_mask.png',
            '9_mask' : 'assets/captcha/9_mask.png',
            'slider': 'assets/slider.png',
            'are_you_a_robot': 'assets/are_you_a_robot.png',
            'blank-sleep': 'assets/sleep/blank-sleep.png',
            'one-z': 'assets/sleep/one-z.png',
            'two-z': 'assets/sleep/two-z.png',
            'three-z': 'assets/sleep/three-z.png',
            #'': 'assets/.png',
        }

        self.templates = { k: cv2.imread(v, 0) for (k, v) in self.static_templates.items() }

        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.screen = mss()

        self.frame = None

    def take_screenshot(self, type='grey'):
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        if(type=='grey'):
            img_res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if(type=='hsv'):
            img_res = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return img_res

    def get_image(self, path):
        return cv2.imread(path, 0)

    def bgr_to_rgb(self, img):
        b,g,r = cv2.split(img)
        return cv2.merge([r,g,b])

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def match_template(self, img_grayscale, template, threshold=0.9):
        """
        Matches template image in a target grayscaled image
        """

        res = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    def find_contour(self, image=None):
        
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame
        self.refresh_frame
        img_gray = image
        img_gray = cv2.GaussianBlur(img_gray,(5,5),0)
        img_gray = cv2.bilateralFilter(img_gray,30,10,40)

        

        ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img_gray, contours, -1, (0,255,75), 1)
        hsv = self.take_screenshot(type='hsv')
        hsv = cv2.GaussianBlur(hsv,(5,5),0)
        mask = cv2.inRange(hsv, (0, 0, 100), (255, 5, 255))


        

        cv2.line(mask, (0, 1080), (1920, 1080), (0,0,0), 700)
        cv2.line(mask, (0, 0), (1920, 0), (0,0,0), 750)
        cv2.line(mask, (0, 0), (0, 1080), (0,0,0), 100)
        cv2.line(mask, (1920, 0), (1920, 1080), (0,0,0), 300)

        kernel = np.ones((3,3),np.uint8)
        final = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        mask_contours, mask_hierarchy= cv2.findContours(final.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sorted_contours= sorted(mask_contours, key=cv2.contourArea, reverse= True)
        largest_item= sorted_contours[0]
        mask_contours = cv2.drawContours(img_gray, largest_item,  -1, (0,255,75),5)

        
        moment = cv2.moments(sorted_contours[0])
        x = int(moment["m10"] / moment["m00"])
        y = int(moment["m01"] / moment["m00"])

        cv2.imwrite('mask.png', mask)
        cv2.imwrite('img_grey.png', img_gray)

        return [x, y]

    
    def show_image(self, image):
        cv2.imshow('image',image)
        c = cv2.waitKey()
        if c >= 0 : return -1
        return 0

    def captcha_image_processing(self, name):
        img_gray = self.templates[name]
        img = cv2.GaussianBlur(img_gray,(9,9),0)
        img = cv2.bilateralFilter(img,30,10,40)
        cv2.imwrite('gaussian_blur_2.png', img)


    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def find_template_by_generated_template(self, template, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame
        return self.match_template(
            image,
            template,
            threshold
        )

    def find_template_and_print(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame
        cv2.imwrite('res.png',image)
        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def find_jigsaw_contours(self):
        return self.find_contour()
        #self.find_contour('jigsaw')

    def find_captcha_crooked_numbers(self, numbers, image=None):
        scales = [1.2, 1.1, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97, 0.96, 0.95] 
        first = self.scaled_find_template(name=(str(numbers[0][0]) + '_crooked_mask'), threshold=0.45, scales=scales) #gets position of template
        second = self.scaled_find_template(name=(str(numbers[1][0]) + '_crooked_mask'), threshold=0.45, scales=scales) #gets position of template
        third = self.scaled_find_template(name=(str(numbers[2][0]) + '_crooked_mask'), threshold=0.45, scales=scales) #gets position of template
        
        if(np.shape(first)[1] >= 1 and np.shape(second)[1] >= 1 and np.shape(third)[1] >= 1):
            crooked_numbers_unsorted = [[numbers[0][0], first[1][0]], [numbers[1][0], second[1][0]], [numbers[2][0], third[1][0]]] #creates an array similiar to the numbers array
            sorted_crooked_numbers = self.sort_number_order(crooked_numbers_unsorted)
            if(self.is_correct_number_order(numbers, sorted_crooked_numbers)):
                return True
        return False


    def is_correct_number_order(self, numbers, crooked_numbers): #(pergunta)
        first_number_is_equal = (numbers[0][0] == crooked_numbers[0][0])
        second_number_is_equal = (numbers[1][0] == crooked_numbers[1][0])
        third_number_is_equal = (numbers[2][0] == crooked_numbers[2][0])
        return first_number_is_equal and second_number_is_equal and third_number_is_equal

    def find_number_sequence(self, image=None):
        #------------------------------Parte de tratamento da imagem------------------------------
        self.refresh_frame()
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame
        
        #------------------------------Parte de tratamento da imagem------------------------------

        count = 0
        number_1 = None
        number_2 = None
        number_3 = None
        number_1_done = False #check se o número foi achado
        number_2_done = False #check se o número foi achado
        number_3_done = False #check se o número foi achado
        
        while(number_1 == None or number_2 == None or number_3 == None): #Repete o processo até achar os 3 números
            while(count<=9): #Como só existem números diferentes nos captchas, isso funciona, caso troquem, o código necessitará adaptação
                print(count)
                template_name = str(count)+'_mask'
                match = self.find_template(name=template_name, image=image, threshold=0.75)
                if(np.shape(match)[1] >= 1):
                    x = match[1][0]
                    if(count==1):
                        cv2.line(image, (x, 0), (x+50, 1080), (0,0,0), 35)#Passa uma linha preta em cima do número achado na mask
                    else:
                        cv2.line(image, (x, 0), (x+50, 1080), (0,0,0), 50)
                    if(not number_1_done):
                        number_1 = [count,x]
                        print(number_1)
                        break

                    if(not number_2_done):
                        number_2 = [count,x]
                        print(number_2)
                        break

                    if(not number_3_done):
                        number_3 = [count,x]
                        print(number_3)
                        break

                count+=1
            count = 0
            if(number_1!=None): #check se o número foi achado
                number_1_done = True

            if(number_2!=None): #check se o número foi achado
                number_2_done = True

            if(number_3!=None): #check se o número foi achado
                number_3_done = True
                
        unsorted_numbers = [number_1, number_2, number_3]

        sorted_numbers = self.sort_number_order(unsorted_numbers)
        
        return sorted_numbers
    
    
    def sort_number_order(self, number_array): #algoritmo simples pra ordenar array
        number_array.sort(key = lambda x: x[1])
        return number_array

    def find_jigsaw(self,image=None):
        
        if image is None:
            if self.frame is None:
                self.refresh_frame()
            image = self.frame
        match = self.find_template_and_print(name='are_you_a_robot', threshold=0.9)        
        img = image.copy()
        rx = match[1][0]
        ry = match[0][0]



        w = 64
        h = 200
        x_offset = -20
        y_offset = 65

        y = ry + y_offset
        x = rx + x_offset

        
        #TODO tirar um poco de cima

        original = image.copy()
        cropped = img[ y : y + h , x: x + w]
        blurred = cv2.GaussianBlur(cropped, (3, 3), 0)
        canny = cv2.Canny(blurred, 120, 255, 1)
        kernel = np.ones((5,5),np.uint8)
        dilate = cv2.dilate(canny, kernel, iterations=1)

        # Find contours
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # Iterate thorugh contours and filter for ROI
        image_number = 0
        for c in cnts:
            xc,yc,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x+xc, y+yc), (x+xc + w, y+yc + h), (36,255,12), 2)
            ROI = original[y+yc:y+yc+h, x+xc:x+xc+w]
            image_number += 1
        

        return ROI


    def findPuzzlePieces(self, result, piece_img, threshold=0.8):
        piece_w = piece_img.shape[1]
        piece_h = piece_img.shape[0]
        yloc, xloc = np.where(result >= threshold)
    

        r= []
        for (piece_x, piece_y) in zip(xloc, yloc):
            r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
            r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
    
    
        r, weights = cv2.groupRectangles(r, 1, 0.2)
        
        if len(r) < 1:
            print('threshold = %.3f' % threshold)
            return self.findPuzzlePieces(result, piece_img,threshold-0.01)
    
        if len(r) == 1:
            print('match')
            return r
    
        if len(r) > 1:
            print('overshoot by %d' % len(r))
            cv2.imwrite('overshoot.png', result)
            cv2.imwrite("debug.png", self.frame)
            return r


    def getRightPiece(self, puzzle_pieces):
        xs = [row[0] for row in puzzle_pieces]
        index_of_right_rectangle = xs.index(max(xs))

        right_piece = puzzle_pieces[index_of_right_rectangle]
        return right_piece

    def getLeftPiece(self, puzzle_pieces):
        xs = [row[0] for row in puzzle_pieces]
        index_of_left_rectangle = xs.index(min(xs))

        left_piece = puzzle_pieces[index_of_left_rectangle]
        return left_piece

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        initial_template = self.templates[name]
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
            matches = self.match_template(
                image,
                scaled_template,
                threshold
            )
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def refresh_frame(self):
        self.frame = self.take_screenshot()
