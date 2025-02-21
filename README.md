# Chewie: Image Collage Maker 🖼️

## Overview

Chewie is a powerful and intuitive CLI application that transforms your image collections into stunning collages. With advanced features and an interactive viewer, creating and exploring image collages has never been easier!

## Features 🌟

### Collage Creation
- 📁 Create collages from entire image folders
- 🎨 Customizable collage width and height
- 🖼️ Supports multiple image formats (JPG, PNG, GIF, BMP, TIFF)

### Interactive Collage Viewer
- 🔍 Zoom in and out with mouse scroll
- 🧭 Navigate using arrow keys
- 📏 Real-time scale display
- 🖥️ Fully resizable window

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chewie.git

# Install dependencies
pip install .
```

## Usage

### Create a Collage

```bash
# Basic usage
chewie make-collage /path/to/image/folder

# Customize collage dimensions
chewie make-collage /path/to/image/folder -w 1000 -h 800 -o my_collage.jpg

# Create and immediately view the collage
chewie make-collage /path/to/image/folder --view
```

### Collage Viewer Controls

- 🖱️ **Scroll Wheel**: Zoom in and out
- ⬅️⬆️⬇️➡️ **Arrow Keys**: Move around the image
- **Esc**: Close the viewer

## Example

```bash
# Create a collage from vacation photos and view it
chewie make-collage ~/Pictures/Vacation2023 -o summer_memories.jpg --view
```

## Requirements

- Python 3.8+
- Click
- Pillow
- Pygame

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your License Here]

## Acknowledgments

- Inspired by the joy of preserving memories
- Built with ❤️ and Python