from time import sleep
import subprocess
import random
from ADB_server import ADB_server
from loguru import logger

class Bot_main:
    def __init__(self, port, android):
        logger.debug(f'Bot().__init__({port})')
        self.ADB = ADB_server(port=port)
        self.android = android
        self.port = port

    def run_command(self, command, sleep_time=1):
        getattr(self.ADB, command)()
        sleep(sleep_time)

    def runBattleMode(self, mode):
        logger.debug(f'Bot.runBattleMode {mode}')
        self.run_command('click', 650, 1200)
        self.run_command('click', 50, 50)
        if mode == 'mode_1':
            self.run_command('click', 355, 760)
        elif mode == 'mode_2':
            self.run_command('click', 125, 1000)
            self.run_command('click', 350, 880)
        elif mode == '2X2':
            self.run_command('click', 125, 1000)
            self.run_command('click', 350, 880)
            self.run_command('click', 493, 712)
        sleep(1)

    def runBattleGlobal(self):
        logger.debug('Bot.runBattleGlobal')
        self.run_command('click', 320, 832)

    def runBattleEvent(self):
        logger.debug('Bot.runBattleEvent')
        self.run_command('click', 280, 720)

    def rewardLimit(self):
        logger.debug('Bot.rewardLimit')
        self.run_command('click', 276, 600)

    def skipLimit(self):
        logger.debug('Bot.skipLimit')
        self.run_command('click', 482, 316)
        self.run_command('click', 280, 900)

    def getRewardChest(self, number):
        logger.debug(f'Bot.getRewardChest {number}')
        self.run_command('click', -25 + number * 120, 780)

    def openChest(self, number):
        logger.debug(f'Bot.openChest {number}')
        self.run_command('click', -25 + number * 120, 780)

    def openChest_2(self, flag):
        logger.debug(f'Bot.openChest {flag}')
        if flag:
            self.run_command('click', 470, 240)
            self.run_command('click', 460, 157)
            self.run_command('click', 270, 670)
        else:
            self.run_command('click', 276, 625)

    def returnHome(self):
        logger.debug('Bot.returnHome')
        self.run_command('click', 650, 1215)
        self.run_command('click', 350, 1215)

    def goToClanChat(self):
        logger.debug('Bot.goToClanChat')
        self.run_command('click', 371, 911)

    def openCloseClanChat(self):
        logger.debug('Bot.openCloseClanChat')
        self.run_command('click', 490, 61)

    def requestCard(self, id_card):
        sleep(3)
        self.run_command('click', 70, 805)
        sleep(3)
        number = int(id_card)
        line = number // 4
        slide = line // 3
        line = (number // 3) % 4
        _number = number % 4
        logger.debug(f'Bot.requestCard {id_card}, {line}, {
