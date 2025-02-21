import pygame


class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200), text_color=(0, 0, 0)):
        """
        Create a clickable button
        
        :param x: X coordinate of button top-left corner
        :param y: Y coordinate of button top-left corner
        :param width: Button width
        :param height: Button height
        :param text: Button text
        :param color: Button background color
        :param text_color: Button text color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, surface):
        """Draw the button on the given surface"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)  # Border
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        """Check if the button is clicked"""
        return self.rect.collidepoint(pos)
