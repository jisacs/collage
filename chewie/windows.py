import pygame
import sys
import os
from .collage_maker import create_collage
from .text_input import TextInput

def pilImageToSurface(pilImage):
    mode = pilImage.mode
    size = pilImage.size
    data = pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode)

class CollageViewer:
    def __init__(self, images, output, width, height):
        """Initialize the Collage Viewer with advanced features."""
        self.images = images
        self.output = output
        self._setup_initial_collage(width, height)
        self._setup_display()
        self._setup_scaling()
        self.width = width
        self.height = height
        self._setup_inputs()
    
    def _setup_initial_collage(self, width, height):
        """Create the initial collage image."""
        try:
            self.original_image = pilImageToSurface(
                create_collage(self.images, width, height)
            )
        except Exception as e:
            print(f"Error creating collage: {e}")
            self.original_image = None
    
    def _setup_display(self):
        """Configure display settings."""
        self.screen_width, self.screen_height = 1600, 1200
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), 
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Collage Viewer")
    
    def _setup_scaling(self):
        """Initialize scaling and positioning attributes."""
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.BACKGROUND_COLOR = (240, 240, 240)
        self.GRID_COLOR = (200, 200, 200)
        self.font = pygame.font.Font(None, 24)
    
    def _setup_inputs(self):
        """Create text input boxes for width and height."""

        input_width, input_height = 120, 40
        input_y = 30
        
        self.height_input = TextInput(
            x=10, 
            y=input_y, 
            width=input_width, 
            height=input_height, 
            default_text=str(int(self.height))
        )
        
        self.width_input = TextInput(
            x=140, 
            y=input_y, 
            width=input_width, 
            height=input_height, 
            default_text=str(int(self.width))
        )
    
    def zoom(self, factor):
        """Adjust image zoom with limits."""
        self.scale *= factor
        self.scale = max(0.1, min(self.scale, 10))
    
    def render(self):
        """Render the current state of the collage viewer."""
        self._clear_screen()
        scaled_image = self._get_scaled_image()
        self._draw_image(scaled_image)
        self._render_text_and_inputs()
        pygame.display.flip()
    
    def _clear_screen(self):
        """Clear the screen with background color."""
        self.screen.fill(self.BACKGROUND_COLOR)
    
    def _get_scaled_image(self):
        """Calculate and return scaled image."""
        scaled_width = int(self.original_image.get_width() * self.scale)
        scaled_height = int(self.original_image.get_height() * self.scale)
        return pygame.transform.scale(
            self.original_image, 
            (scaled_width, scaled_height)
        )
    
    def _draw_image(self, scaled_image):
        """Position and draw the scaled image."""
        scaled_width = scaled_image.get_width()
        scaled_height = scaled_image.get_height()
        pos_x = (self.screen_width - scaled_width) // 2 + self.offset_x
        pos_y = (self.screen_height - scaled_height) // 2 + self.offset_y
        self.screen.blit(scaled_image, (pos_x, pos_y))
    
    def _render_text_and_inputs(self):
        """Render text information and input boxes."""
        texts = [
            
            (f"Height:", (10, 10)),
            (f"Width:", (140, 10)),
            (f"Scale: {self.scale:.2f}x", (10, self.screen_height - 60)),
            ("Scroll to zoom, Arrow keys to move, Esc to quit", 
             (10, self.screen_height - 30))
        ]
        
        for text, pos in texts:
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, pos)
        
        self.height_input.draw(self.screen)
        self.width_input.draw(self.screen)
    
    def run(self):
        """Main event loop for the viewer."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                running = self._handle_event(event)
            
            self.render()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def _handle_event(self, event):
        """Process a single pygame event."""
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.VIDEORESIZE:
            self._resize_window(event)
        
        height_result = self.height_input.handle_event(event)
        width_result = self.width_input.handle_event(event)
        
        self._process_input_results(height_result, width_result)
        self._handle_zoom_and_navigation(event)
        
        return True
    
    def _resize_window(self, event):
        """Resize the window and reposition inputs."""
        self.screen_width, self.screen_height = event.size
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), 
            pygame.RESIZABLE
        )

    
    def _process_input_results(self, height_result, width_result):
        """Process height and width input results."""
        if height_result is not None:
            try:
                new_height = float(height_result)
                if 0 < new_height < self.screen_height:
                    self._update_collage_height(new_height)
            except ValueError:
                print("Invalid height input")
        
        if width_result is not None:
            try:
                new_width = float(width_result)
                if 0 < new_width < self.screen_width:
                    self._update_collage_width(new_width)
            except ValueError:
                print("Invalid width input")
    
    def _update_collage_height(self, new_height):
        """Update collage height and regenerate image."""
        self.height = new_height
        self.original_image = pilImageToSurface(
            create_collage(self.images, int(self.width), int(self.height))
        )
    
    def _update_collage_width(self, new_width):
        """Update collage width and regenerate image."""
        self.width = new_width
        self.original_image = pilImageToSurface(
            create_collage(self.images, int(self.width), int(self.height))
        )
    
    def _handle_zoom_and_navigation(self, event):
        """Handle zoom and navigation events."""
        if event.type == pygame.MOUSEWHEEL:
            self.zoom(1.1 ** event.y)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            move_speed = 10
            if event.key == pygame.K_LEFT:
                self.offset_x += move_speed
            elif event.key == pygame.K_RIGHT:
                self.offset_x -= move_speed
            elif event.key == pygame.K_UP:
                self.offset_y += move_speed
            elif event.key == pygame.K_DOWN:
                self.offset_y -= move_speed
        
        return True
