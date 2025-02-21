import pygame
import sys
import os
from .collage_maker import create_collage
from .button import Button

def pilImageToSurface(pilImage):
    mode = pilImage.mode
    size = pilImage.size
    data = pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode)

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

class CollageViewer:
    def __init__(self, images, output, width, height):
        """
        Initialize the Collage Viewer with advanced features.
        
        :param images: List of image paths
        :param output: Output filename
        :param width: Collage width
        :param height: Initial row height
        """
        try:
            self.original_image = pilImageToSurface(create_collage(images, width, height))
        except Exception as e:
            print(f"Error creating collage: {e}")
            return False
        # Load the image
        self.images = images
        self.width = width
        self.height = height

        # Screen and display setup
        self.screen_width, self.screen_height = 1600, 1200
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                              pygame.RESIZABLE)
        pygame.display.set_caption("Collage Viewer")
        
        # Scaling and positioning
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        # Colors
        self.BACKGROUND_COLOR = (240, 240, 240)
        self.GRID_COLOR = (200, 200, 200)
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        
        # Text inputs
        input_width, input_height = 100, 30
        input_y = self.screen_height - input_height - 10
        
        # Height input
        self.height_input = TextInput(
            x=10, 
            y=input_y, 
            width=input_width, 
            height=input_height, 
            default_text=str(int(height))
        )
        
        # Width input
        self.width_input = TextInput(
            x=130, 
            y=input_y, 
            width=input_width, 
            height=input_height, 
            default_text=str(int(width))
        )
    
    def zoom(self, factor):
        """
        Zoom in or out by a given factor
        
        :param factor: Zoom factor (> 1 for zoom in, < 1 for zoom out)
        """
        old_scale = self.scale
        self.scale *= factor
        
        # Limit scale between 0.1 and 10
        self.scale = max(0.1, min(self.scale, 10))
    
    def draw_grid(self):
        """Draw a light grid in the background"""
        grid_size = 50
        for x in range(0, self.screen_width, grid_size):
            pygame.draw.line(self.screen, self.GRID_COLOR, (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, grid_size):
            pygame.draw.line(self.screen, self.GRID_COLOR, (0, y), (self.screen_width, y))
    
    def render(self):
        """Render the image with current scale and offset"""
        # Clear the screen
        self.screen.fill(self.BACKGROUND_COLOR)
        
        # Draw grid
        #self.draw_grid()
        
        # Scale the image
        scaled_width = int(self.original_image.get_width() * self.scale)
        scaled_height = int(self.original_image.get_height() * self.scale)
        scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        
        # Calculate position to center the image
        pos_x = (self.screen_width - scaled_width) // 2 + self.offset_x
        pos_y = (self.screen_height - scaled_height) // 2 + self.offset_y
        
        # Draw the scaled image
        self.screen.blit(scaled_image, (pos_x, pos_y))
        
        # Display scale and help text
        scale_text = self.font.render(f"Scale: {self.scale:.2f}x", True, (0, 0, 0))
        height_text = self.font.render(f"Height:", True, (0, 0, 0))
        width_text = self.font.render(f"Width:", True, (0, 0, 0))
        help_text = self.font.render("Scroll to zoom, Arrow keys to move, Esc to quit", True, (0, 0, 0))
        
        self.screen.blit(scale_text, (10, 10))
        self.screen.blit(height_text, (10, self.screen_height - 60))
        self.screen.blit(width_text, (130, self.screen_height - 60))
        #self.screen.blit(help_text, (10, self.screen_height - 30))
        
        # Draw text inputs
        self.height_input.draw(self.screen)
        self.width_input.draw(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main event loop for the viewer"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Resize event
                elif event.type == pygame.VIDEORESIZE:
                    self.screen_width, self.screen_height = event.size
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 
                                                          pygame.RESIZABLE)
                    
                    # Reposition inputs
                    input_y = self.screen_height - 40
                    self.height_input.rect.y = input_y
                    self.width_input.rect.y = input_y
                
                # Handle text input events
                height_input_result = self.height_input.handle_event(event)
                width_input_result = self.width_input.handle_event(event)
                
                # Process input results
                if height_input_result is not None:
                    try:
                        new_height = float(height_input_result)
                        if new_height > 0 and new_height < self.screen_height:
                            self.height = new_height
                            self.original_image = pilImageToSurface(
                                create_collage(self.images, int(self.width), int(self.height))
                            )
                    except ValueError:
                        print("Invalid height input")
                
                if width_input_result is not None:
                    try:
                        new_width = float(width_input_result)
                        if new_width > 0 and new_width < self.screen_width:
                            self.width = new_width
                            self.original_image = pilImageToSurface(
                                create_collage(self.images, int(self.width), int(self.height))
                            )
                    except ValueError:
                        print("Invalid width input")
                
                # Zoom with mouse wheel
                elif event.type == pygame.MOUSEWHEEL:
                    # Adjust scale with scroll
                    self.zoom(1.1 ** event.y)
                
                # Keyboard navigation
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
        
            
            # Render the scene
            self.render()
            
            # Control frame rate
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
