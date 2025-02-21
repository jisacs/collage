import click

@click.group()
@click.version_option(version="0.1.0")
def main():
    """Chewie CLI: Your versatile command-line companion."""
    pass

@main.command()
@click.argument('name', default='World')
def hello(name):
    """Say hello to someone."""
    click.echo(f"Hello, {name}!")

if __name__ == '__main__':
    main()