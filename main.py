import click
import jinja2
from pathlib import Path
from os import walk


class Project:
    def __init__(self, name: str, image: str, description: str, title: str, url: str, author: str):
        self.name = name
        self.image = image
        self.description = description
        self.title = title
        self.url = url
        self.author = author


def resolve_image(dir_name, files, output_dir):
    if 'window.png' not in files:
        return None
    Path(f'{output_dir}/{dir_name}').mkdir(parents=True, exist_ok=True)
    Path(f'{output_dir}/{dir_name}/window.png').write_bytes(Path(f'{dir_name}/window.png').read_bytes())
    return f'{dir_name}/window.png'


def resolve_description(dir_name, files):
    if 'description.html' not in files:
        return ''
    return Path(f'{dir_name}/description.html').read_text()


def resolve_title(dir_name, files):
    if 'title.txt' not in files:
        return ''
    return Path(f'{dir_name}/title.txt').read_text()


def resolve_url(dir_name, files):
    if 'link.txt' not in files:
        return ''
    return Path(f'{dir_name}/link.txt').read_text()


def resolve_author(dir_name, files):
    if 'author.txt' not in files:
        return ''
    return Path(f'{dir_name}/author.txt').read_text()


def collect_project(dir_info):
    dir_name, _, files = dir_info
    return Project(
        resolve_title(dir_name, files),
        resolve_image(dir_name, files, 'output'),
        resolve_description(dir_name, files),
        dir_name,
        resolve_url(dir_name, files),
        resolve_author(dir_name, files)
    )


def collect_projects(input_dir):
    return [collect_project(x) for x in walk(input_dir) if x[0] != input_dir]


@click.command()
@click.option('--input', '-i', help='Input repository', default='repositories')
@click.option('--output', '-o', help='Output file', default='output')
@click.option('--template', '-t', help='Template file', default='template')
def main(input, output, template):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template))
    template = env.get_template('webpage.html')
    content = {
        'projects': collect_projects(input),
        'title': 'Projekty z Grafiki Komputerowej',
    }

    Path(output).mkdir(parents=True, exist_ok=True)
    with open(f'{output}/index.html', 'w') as f:
        f.write(template.render(content))


if __name__ == '__main__':
    main()
