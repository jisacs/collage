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

LIST_WIDTH = 250

class ThumbnailDragger:
    def __init__(self, thumbnails, list_x):
        """
        Manage dragging and dropping of thumbnails
        
        :param thumbnails: List of thumbnail dictionaries
        :param list_x: X coordinate of the thumbnail list
        """
        self.thumbnails = thumbnails
        self.list_x = list_x
        self.dragging = None
        self.drag_offset_y = 0
        self.original_y = None
    
    def handle_event(self, event, start_y):
        """
        Handle mouse events for dragging thumbnails
        
        :param event: Pygame event
        :param start_y: Starting Y coordinate of thumbnails
        :return: Boolean indicating if list was reordered
        """
       
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # Check if click is in thumbnail list area
             if event.pos[0] > self.list_x and event.pos[0] < self.list_x + LIST_WIDTH:
                # Find which thumbnail was clicked
                for i, img_data in enumerate(self.thumbnails):
                    thumb_y = start_y + i * (img_data['surface'].get_height() + 30)
                    thumb_rect = pygame.Rect(
                        self.list_x + 25, 
                        thumb_y, 
                        img_data['surface'].get_width(), 
                        img_data['surface'].get_height()
                    )
                    
                    if thumb_rect.collidepoint(event.pos):
                        self.dragging = i
                        self.drag_offset_y = event.pos[1] - thumb_y
                        self.original_y = thumb_y
                        break
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging is not None:
                # Calculate new position
                mouse_y = event.pos[1]
                new_index = max(0, min(len(self.thumbnails) - 1, 
                    (mouse_y - start_y + self.drag_offset_y) // 
                    (self.thumbnails[0]['surface'].get_height() + 30)
                ))
                
                # Reorder thumbnails
                if new_index != self.dragging:
                    moved_item = self.thumbnails.pop(self.dragging)
                    self.thumbnails.insert(new_index, moved_item)
                    return True
                
                self.dragging = None
        
        return False
    
    def get_dragged_thumbnails(self):
        """
        Get thumbnails with the dragged item highlighted
        
        :return: List of thumbnail dictionaries
        """
        return self.thumbnails

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
        self._load_image_thumbnails()
        self._setup_thumbnail_dragger()
    
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
        self.screen_width, self.screen_height = 1480, 1200
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
        self.BACKGROUND_COLOR = (0, 0, 0)  # Black background
        self.GRID_COLOR = (50, 50, 50)  # Dark gray grid to complement black background
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
    
    def _setup_thumbnail_dragger(self):
        """Initialize thumbnail drag and drop functionality."""
        list_x = self.screen_width - LIST_WIDTH
        self.thumbnail_dragger = ThumbnailDragger(self.image_thumbnails, list_x)
    
    def _load_image_thumbnails(self):
        """Load and scale thumbnails for the image list."""
        from PIL import Image
        
        self.image_thumbnails = []
        
        # Calculate maximum thumbnail dimensions
        available_height = self.screen_height - 100  # Reserve space for title and margins
        num_images = len(self.images)

        max_thumbnail_height = max(1, available_height // (num_images*6))
        max_thumbnail_width = LIST_WIDTH - 50  # Leave some margin
        
        for img_path in self.images:
            try:
                # Open image with Pillow
                pil_img = Image.open(img_path)
                
                # Resize to fit within max dimensions while maintaining aspect ratio
                pil_img.thumbnail((max_thumbnail_width, max_thumbnail_height), Image.LANCZOS)
                
                # Convert to Pygame surface
                pygame_surface = pilImageToSurface(pil_img)
                
                self.image_thumbnails.append({
                    'surface': pygame_surface,
                    'path': os.path.basename(img_path),
                    'original_size': pil_img.size,
                    'original_path': img_path
                })
            except Exception as e:
                print(f"Error loading thumbnail for {img_path}: {e}")
    
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
        self._render_image_list()
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
            (f"Nb images: {len(self.images)}", (10, self.screen_height - 60)),
            ("Scroll to zoom, Arrow keys to move, Esc to quit", 
             (10, self.screen_height - 30))
        ]
        
        for text, pos in texts:
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, pos)
        
        self.height_input.draw(self.screen)
        self.width_input.draw(self.screen)
    
    def _render_image_list(self):
        """Render the list of images on the right side of the window."""
        # Define list area
        list_x = self.screen_width - LIST_WIDTH
        
        # Draw background for image list
        list_rect = pygame.Rect(list_x, 0, LIST_WIDTH, self.screen_height)
        pygame.draw.rect(self.screen, (230, 230, 230), list_rect)
        pygame.draw.line(self.screen, (150, 150, 150), 
                         (list_x, 0), (list_x, self.screen_height), 2)
        
        # Render title
        title_font = pygame.font.Font(None, 24)
        title_text = title_font.render("Images", True, (0, 0, 0))
        self.screen.blit(title_text, (list_x + 10, 10))
        
        # Render thumbnails and filenames
        start_y = 50
        thumbnails = self.thumbnail_dragger.get_dragged_thumbnails()
        
        for i, img_data in enumerate(thumbnails):
            # Position for this thumbnail
            thumb_y = start_y + i * (img_data['surface'].get_height() + 30)
            
            if thumb_y + img_data['surface'].get_height() > self.screen_height:
                break
            
            # Draw thumbnail
            self.screen.blit(img_data['surface'], (list_x + 25, thumb_y))
            
            # Draw filename and original size
            nb_images = len(self.images)
            filename_font = pygame.font.Font(None, max(8, 16 - nb_images))
            filename_text = filename_font.render(
                f"{img_data['path']} ({img_data['original_size'][0]}x{img_data['original_size'][1]})", 
                True, (0, 0, 0)
            )
            self.screen.blit(filename_text, (list_x + 25, thumb_y + img_data['surface'].get_height() + 5))
    
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
        
        # Handle key press events
        if event.type == pygame.KEYDOWN:
            # Save collage when 'S' key is pressed
            if event.key == pygame.K_s:
                self._save_collage()
        
        # Handle thumbnail drag and drop
        start_y = 50
        
        if self.thumbnail_dragger.handle_event(event, start_y):
            # If thumbnails were reordered, update images list and regenerate collage
            self.images = [
                img_data['original_path'] for img_data in self.image_thumbnails
            ]
            
            # Regenerate collage with new image order
            try:
                self.original_image = pilImageToSurface(
                    create_collage(self.images, int(self.width), int(self.height))
                )
            except Exception as e:
                print(f"Error recreating collage: {e}")
        
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
        self._setup_thumbnail_dragger()

    def _save_collage(self):
        """
        Save the current collage to the output path.
        Provides user feedback about the save operation.
        """
        try:
            # Convert Pygame surface back to PIL Image
            from PIL import Image
            import pygame.image
            
            # Ensure output directory exists
            import os
            #os.makedirs(os.path.dirname(self.output), exist_ok=True)
            
            # Save the original image
            pygame.image.save(self.original_image, self.output)
            
            # Optional: Display save confirmation
            print(f"Collage saved successfully to {self.output}")
            
            # Optional: Create a temporary surface for save confirmation
            font = pygame.font.Font(None, 36)
            save_text = font.render("Collage Saved!", True, (0, 255, 0))
            text_rect = save_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            
            # Briefly show save confirmation
            self.screen.blit(save_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(1000)  # Show message for 1 second
        
        except Exception as e:
            print(f"Error saving collage: {e}")
            
            # Optional: Display error message
            font = pygame.font.Font(None, 36)
            error_text = font.render(f"Save Failed: {str(e)}", True, (255, 0, 0))
            text_rect = error_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            
            self.screen.blit(error_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)  # Show error for 2 seconds
    
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
