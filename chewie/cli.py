import click
import os
from .collage_maker import make_collage as create_collage
from .windows import display_collage

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
@click.option('--view', '-v', is_flag=True, help='Open the collage in a Pygame window')
def make_collage(input_folder, output, width, height, view):
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

    try:
        collage_image = create_collage(images, output, width, height)
        if collage_image is not False:
            click.echo(f"Collage created successfully: {output}")
            
            # View the collage if the --view flag is set
            if view:
                try:
                    display_collage(output)
                except Exception as view_error:
                    click.echo(f"Error displaying collage: {view_error}")
        else:
            click.echo("Failed to create collage.")
    except Exception as e:
        click.echo(f"Error creating collage: {e}")

if __name__ == '__main__':
    main()