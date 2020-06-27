import pygame

class Button():
    def __init__(self, color, x, y, width, height, text="", text_color=(0,0,0)):
        self.color=color
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
        self.text_color=text_color

    def draw(self, window, outline=None):
        if self.text!="":
            font = pygame.font.SysFont("comicsans",40)
            text = font.render(self.text,1,self.text_color)
            self.width=text.get_width()+20
            self.height=text.get_height()+20
            if outline:
                pygame.draw.rect(window, outline, (self.x-self.width/2-2,self.y-self.height/2-2,self.width+4,self.height+4),0)
            pygame.draw.rect(window, self.color, (self.x-self.width/2, self.y-self.height/2, self.width, self.height),0)
            window.blit(text, (self.x-text.get_width()/2,self.y-text.get_height()/2))
        else:
            if outline:
                pygame.draw.rect(window, outline, (self.x-self.width/2-2,self.y-self.height/2-2,self.width+4,self.height+4),0)
            pygame.draw.rect(window, self.color, (self.x-self.width/2, self.y-self.height/2, self.width, self.height),0)

    def isOver(self,pos):
        if pos[0] > self.x-self.width/2 and pos[0] < self.x+self.width/2:
            if pos[1] > self.y-self.height/2 and pos[1] < self.y+self.height/2:
                return True
        return False
            

