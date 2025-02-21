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


class CollageViewer:
    def __init__(self, images, output, width, height):
        """
        Initialize the Collage Viewer with advanced features.
        
        :param image_path: Path to the collage image file
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
        self.screen_width, self.screen_height = 800, 600
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
        
        # Buttons
        button_width, button_height = 50, 30
        button_y = self.screen_height - button_height - 10
        self.plus_button = Button(10, button_y, button_width, button_height, "+")
        self.minus_button = Button(70, button_y, button_width, button_height, "-")
    
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
        self.draw_grid()
        
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
        height_text = self.font.render(f"Height: {int(self.height)}", True, (0, 0, 0))
        help_text = self.font.render("Scroll to zoom, Arrow keys to move, Esc to quit", True, (0, 0, 0))
        
        self.screen.blit(scale_text, (10, 10))
        self.screen.blit(height_text, (10, 40))
        self.screen.blit(help_text, (10, self.screen_height - 60))
        
        # Draw buttons
        self.plus_button.draw(self.screen)
        self.minus_button.draw(self.screen)
        
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
                    
                    # Reposition buttons
                    button_y = self.screen_height - 40
                    self.plus_button.rect.y = button_y
                    self.minus_button.rect.y = button_y
                
                # Mouse click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if self.plus_button.is_clicked(mouse_pos):
                            try:
                                self.height=self.height+self.height/10
                                self.original_image = pilImageToSurface(create_collage(self.images, int(self.width), int(self.height)))
                            except Exception as e:
                                print(f"Error creating collage: {e}")
                                return False

                        elif self.minus_button.is_clicked(mouse_pos):
                            try:
                                self.height=self.height-self.height/10
                                self.original_image = pilImageToSurface(create_collage(self.images, int(self.width), int(self.height)))
                            except Exception as e:
                                print(f"Error creating collage: {e}")
                                return False
                        
                     
                            
                
                # Zoom with mouse wheel
                elif event.type == pygame.MOUSEWHEEL:
                    # Adjust scale with scroll
                    self.zoom(1.1 ** event.y)
                
                # Keyboard navigation
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Arrow key navigation
                    move_speed = 10
                    if event.key == pygame.K_LEFT:
                        self.offset_x += move_speed
                    elif event.key == pygame.K_RIGHT:
                        self.offset_x -= move_speed
                    elif event.key == pygame.K_UP:
                        self.offset_y += move_speed
                    elif event.key == pygame.K_DOWN:
                        self.offset_y -= move_speed
            
            # Render the scene
            self.render()
            
            # Control frame rate
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
