import pygame


class TextInput:
    def __init__(self, x, y, width, height, default_text='', font_size=24):
        """
        Create a text input box
        
        :param x: X coordinate of input box top-left corner
        :param y: Y coordinate of input box top-left corner
        :param width: Input box width
        :param height: Input box height
        :param default_text: Initial text in the input box
        :param font_size: Size of the font
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.default_text = default_text
        self.text = default_text
        self.font = pygame.font.Font(None, font_size)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.first_click = True
    
    def handle_event(self, event):
        """Handle pygame events for the input box"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
                
                # Clear text on first click
                if self.first_click:
                    self.text = ''
                    self.first_click = False
            else:
                self.active = False
                
                # Reset to default if no text entered
                if not self.text:
                    self.text = self.default_text
                    self.first_click = True
            
            # Change the input box color
            self.color = self.color_active if self.active else self.color_inactive
            
            # Re-render the text
            self.txt_surface = self.font.render(self.text, True, self.color)
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Return the current text when Enter is pressed
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character
                    self.text = self.text[:-1]
                else:
                    # Add typed character
                    self.text += event.unicode
                
                # Re-render the text
                self.txt_surface = self.font.render(self.text, True, self.color)
        
        return None
    
    def draw(self, screen):
        """Draw the input box and text"""
        # Blit the text
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.w = width
        
        # Draw the rect
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
