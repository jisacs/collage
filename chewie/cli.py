import click
import os
from .windows import CollageViewer
import pygame

@click.group()
@click.version_option(version="0.1.0")
def main():
    """Chewie CLI: Your versatile command-line companion."""
    pass

@main.command()
@click.argument('input_folder', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output', '-o', default='collage.jpg', help='Output filename for the collage')
@click.option('--width', '-w', default=800, help='Width of the collage')
@click.option('--height', '-h', default=600, help='Initial height of each image row')
def make_collage(input_folder, output, width, height):
    """Create a collage from images in the input folder."""
    # Get all image files from the input folder
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    images = [
        os.path.join(input_folder, f) 
        for f in os.listdir(input_folder) 
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
 
    if not images:
        click.echo(f"Error: No images found in {input_folder}")
        return
    # Initialize Pygame
    pygame.init()
    viewer=CollageViewer(images, output, width, height)
    viewer.run()


if __name__ == '__main__':
    main()