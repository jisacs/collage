import pygame
import sys
import os
from .collage_maker import create_collage

def pilImageToSurface(pilImage):
    mode = pilImage.mode
    size = pilImage.size
    data = pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode)

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

class CollageViewer:
    def __init__(self, collage_image):
        """
        Initialize the Collage Viewer with advanced features.
        
        :param image_path: Path to the collage image file
        """
        # Initialize Pygame
        pygame.init()
        
        # Load the image
        self.original_image = pilImageToSurface(collage_image)
        print("Pil3")
        self.image = self.original_image.copy()

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
        help_text = self.font.render("Scroll to zoom, Arrow keys to move, Esc to quit", True, (0, 0, 0))
        self.screen.blit(scale_text, (10, 10))
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
                            self.zoom(1.2)  # Zoom in
                        elif self.minus_button.is_clicked(mouse_pos):
                            self.zoom(0.8)  # Zoom out
                
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

def display_collage(images, output, width, height):
    """
    Display the collage image using an advanced Pygame viewer.
    
    :param image_path: Path to the collage image file
    """
    try:
        collage_image = create_collage(images, width, height)

    except Exception as e:
        print(f"Error creating collage: {e}")
        return False

    try:
        viewer = CollageViewer(collage_image)
        viewer.run()
        return True
    except FileNotFoundError:
        print(f"Error: Image file not found at {output}")
        return False
    except pygame.error as e:
        print(f"Pygame error: {e}")
        return False

def main(image_path=None):
    """
    Main function to display a collage image.
    If no image path is provided, it tries to find the most recent collage.
    
    :param image_path: Optional path to the collage image
    """
    if not image_path:
        # Try to find the most recent collage in the current directory
        current_dir = os.getcwd()
        collage_files = [f for f in os.listdir(current_dir) if f.startswith('collage') and f.endswith(('.jpg', '.png', '.jpeg'))]
        
        if not collage_files:
            print("No collage image found.")
            return False
        
        # Sort by modification time and get the most recent
        collage_files.sort(key=lambda x: os.path.getmtime(os.path.join(current_dir, x)), reverse=True)
        image_path = os.path.join(current_dir, collage_files[0])
    
    return display_collage(image_path)

if __name__ == '__main__':
    main()