import pygame
import time

class DeathController:
    MSG_1_X = 375
    MSG_1_Y = 300

    def __init__(self, final_score, window):
        self.font = pygame.font.SysFont("Arial", 40)
        self.final_score = str(int(final_score))
        for char in self.final_score:
            self.MSG_1_X -= 10
        self.window = window

    def run(self):
        msg = self.font.render("You died! You scored " + self.final_score + " points.", False, (255, 255, 255))
        self.window.blit(msg, (self.MSG_1_X, self.MSG_1_Y))
        pygame.display.flip()
        time.sleep(1)

        pygame.event.clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

#
# if __name__ == '__main__':
#     pygame.init()
#     pygame.font.init()
#     dc1 = DeathController(203, pygame.display.set_mode((1280, 720), 0, 32))
#     dc1.run()