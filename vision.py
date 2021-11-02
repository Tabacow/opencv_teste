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
            'metamask-popup': 'assets/metamask-popup.png',
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

    def take_screenshot(self):
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return img_gray

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

    #def count_item_on_image(self, image=None, object=None):
    #    if image is None:
    #        if self.frame is None:
    #            self.refresh_frame()
#
    #        image = self.frame
    #    obj = cv2.imread(self.template[object],0)
    #    img = cv2.imread(self.template[image])
    #    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #    w, h = template.shape[::-1]
    #    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    #    threshold = 0.8
    #    loc = np.where( res >= threshold)
#
    #    f = set()
    #    
    #    for pt in zip(*loc[::-1]):
    #        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
#
    #        sensitivity = 100
    #        f.add((round(pt[0]/sensitivity), round(pt[1]/sensitivity)))
    #    return len(f)

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
