import pygame
import sys
import os

def display_collage(image_path):
    """
    Display the collage image using Pygame.
    
    :param image_path: Path to the collage image file
    """
    # Initialize Pygame
    pygame.init()
    
    try:
        # Load the image
        image = pygame.image.load(image_path)
        
        # Get the image dimensions
        image_width, image_height = image.get_size()
        
        # Set up the display
        screen = pygame.display.set_mode((image_width, image_height))
        pygame.display.set_caption("Collage Viewer")
        
        # Fill the screen with white
        screen.fill((255, 255, 255))
        
        # Blit the image to the screen
        screen.blit(image, (0, 0))
        
        # Update the display
        pygame.display.flip()
        
        # Event loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
    
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return False
    except pygame.error as e:
        print(f"Pygame error: {e}")
        return False
    finally:
        # Quit Pygame
        pygame.quit()
        sys.exit()
    
    return True

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