import io
import random
import json
from PIL import Image
from loguru import logger
import time
import os

with open("config/trigger.json", encoding='UTF-8') as f:
    triggers_json = json.load(f)

class ImageTriggers:
    def __init__(self, open_chest, requested_card, open_PR=False, debug=False):
        self.open_chest = open_chest
        self.open_PR = open_PR
        self.requested_card = requested_card
        self.debug = debug

        self.triggers = {
            '_cheakTimeInBatlle': self._cheakTimeInBatlle,
            '_getNumeberCrown': self._getNumeberCrown,
            '_getTriggerOpenChest': self._getTriggerOpenChest,
            '_getTriggerOpenedChest': self._getTriggerOpenedChest,
            '_getTextError': self._getTextError,
            '_getCardsInBatlle': self._getCardsInBatlle,
            '_getElixir': self._getElixir,
            '_get_tower_health': self._get_tower_health
        }

    def _cheakTimeInBatlle(self):
        i = self.image.crop((450, 0, 538, 53))

    def _getNumeberCrown(self):
        pixel_values = [
            (200, 111, 22),  # Crown 3
            (49, 54, 54, 255),  # Crown 3 (alternative color)
            (253, 162, 65),  # Crown 2
            (63, 66, 65, 255),  # Crown 2 (alternative color)
            (210, 116, 24),  # Crown 1
            (52, 55, 55, 255)  # Crown 1 (alternative color)
        ]

        for i, pixel in enumerate(pixel_values, start=1):
            if self.image.getpixel((401, 462))[0:3] == pixel or self.image.getpixel((270, 448))[0:3] == pixel or self.image.getpixel((150, 453))[0:3] == pixel:
                return i

        return 0

    def _getTriggerOpenChest(self):
        chest_positions = [
            (109, 833, 114, 838),
            (243, 833, 248, 838),
            (376, 833, 381, 838),
            (508, 833, 513, 838)
        ]

        sumPixelChests = []
        for pos in chest_positions:
            image = self.image.crop(pos)
            width, height = image.size
            sumPixel = [0, 0, 0]

            for x in range(0, width):
                for y in range(0, height):
                    pixel = image.getpixel((x, y))
                    sumPixel[0] += pixel[0]
                    sumPixel[1] += pixel[1]
                    sumPixel[2] += pixel[2]

            sumPixelChests.append(sumPixel)

        meanPixels = [[sumPixel[0]/25, sumPixel[1]/25, sumPixel[2]/25] for sumPixel in sumPixelChests]

        for i, meanPixel in enumerate(meanPixels, start=1):
            if meanPixel[0] == 255.0 and 216.0 <= meanPixel[1] <= 255.0 and 74.0 <= meanPixel[2] <= 150.0:
                return i

        return 0

    def _getTriggerOpenedChest(self):
        for trigger in triggers_json['triggerOpenChest']:
            image = self.image.crop(trigger['position'])
            if image.getdata() == trigger['image']:
                return True

        return False

    def _getTextError(self):
        image = self.image.crop((0, 0, 100, 100))

        for trigger in triggers_json['triggerTextError']:
            if image.getdata() == trigger['image']:
                return trigger['text']

        return ''

    def _getCardsInBatlle(self):
        cards = []

        for trigger in triggers_json['triggerCardsInBatlle']:
            image = self.image.crop(trigger['position'])
            if image.getdata() == trigger['image']:
                cards.append(trigger['card_name'])

        return cards

    def _getElixir(self):
        elixir_positions = [
            (52, 752, 56, 757),
            (75, 752, 79, 757),
            (98, 752, 102, 757),
            (121, 752, 125, 757),
            (144, 752, 148, 757),
            (167, 752, 171, 757),
            (190, 752, 194, 757),
            (213, 752, 217, 757),
            (236, 752, 240, 757),
            (259, 752, 263, 757),
            (282, 752, 286, 757),
            (305, 752, 309, 757),
            (328, 752, 332, 757),
            (351, 752, 355, 757),
            (374, 752, 378, 757),
            (397, 752, 401, 757),
            (420, 752, 424, 757),
            (443, 752, 447, 757),
            (466, 752, 470, 757),
            (489, 752, 493, 757),
            (512, 752, 516, 757),
            (535, 752, 539, 757),
            (558, 752, 562, 757),
            (581, 752, 585, 757),
            (604, 752, 608, 757),
            (627, 752, 631, 757)
        ]

        elixir_count = 0

        for pos in elixir_positions:
            image = self.image.crop(pos)
            if image.getpixel((2, 2)) == (160, 192, 255, 255):
                elixir_count += 1

        return elixir_count

    def _get_tower_health(self):
        tower_health_positions = [
            (151, 125, 152, 126),
            (176, 125, 177, 126),
            (201, 125, 202, 126),
            (223, 125, 224, 126),
            (248, 125, 249, 126),
            (273, 125, 274, 126),
            (297, 125, 298, 126),
            (322, 125, 323, 126),
            (346, 125, 347, 126),
            (371, 125, 372, 126),
            (396, 125, 397, 126),
            (420, 125, 421, 126),
            (445, 125, 446, 126),
            (470, 125, 471, 126),
            (494, 125, 495, 126),
            (519, 125, 520, 126),
            (543, 125, 544, 126),
            (568, 125, 569, 126),
            (592, 125, 593, 126),
            (617, 125, 618, 126)
        ]

        tower_health = 0

        for pos in tower_health_positions:
            image = self.image.crop(pos)
            if image.getpixel((0, 0)) == (254, 254, 254, 255):
                tower_health += 1

        return tower_health

    def process_image(self, image_data):
        image = Image.open(io.BytesIO(image_data))
        self.image = image.convert('RGB')

        for trigger_name, trigger_func in self.triggers.items():
            if self.debug:
                logger.info(f"Trigger: {trigger_name}")
                start_time = time.time()

            result = trigger_func()

            if self.debug:
                elapsed_time = time.time() - start_time
                logger.info(f"Result: {result}")
                logger.info(f"Elapsed time: {elapsed_time} seconds")

        return None


def main():
    open_chest = random.choice([True, False])
    requested_card = random.choice(['Card1', 'Card2', 'Card3'])
    open_PR = random.choice([True, False])
    debug = False  # Set to True to enable debug logs

    image_data = open("image.png", "rb").read()

    triggers = ImageTriggers(open_chest, requested_card, open_PR, debug)
    triggers.process_image(image_data)


if __name__ == '__main__':
    main()
