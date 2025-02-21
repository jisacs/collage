import pygame
import sys
import os

class CollageViewer:
    def __init__(self, image_path):
        """
        Initialize the Collage Viewer with advanced features.
        
        :param image_path: Path to the collage image file
        """
        # Initialize Pygame
        pygame.init()
        
        # Load the image
        self.original_image = pygame.image.load(image_path)
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
        self.screen.blit(help_text, (10, self.screen_height - 30))
        
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
                
                # Zoom with mouse wheel
                elif event.type == pygame.MOUSEWHEEL:
                    # Adjust scale with scroll
                    old_scale = self.scale
                    self.scale *= 1.1 ** event.y
                    
                    # Limit scale between 0.1 and 10
                    self.scale = max(0.1, min(self.scale, 10))
                
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

def display_collage(image_path):
    """
    Display the collage image using an advanced Pygame viewer.
    
    :param image_path: Path to the collage image file
    """
    try:
        viewer = CollageViewer(image_path)
        viewer.run()
        return True
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
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