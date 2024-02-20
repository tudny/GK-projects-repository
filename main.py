import click
import jinja2
from pathlib import Path
from os import walk
import yaml


class Project:
    def __init__(self, name: str, images: [str], description: str, title: str, url: str, author: str):
        self.name = name
        self.images = images
        self.description = description
        self.title = title
        self.url = url
        self.author = author

    def pack_images(self, dir_name, output_dir):
        Path(f'{output_dir}/{dir_name}').mkdir(parents=True, exist_ok=True)
        for image in self.images:
            Path(f'{output_dir}/{image}').write_bytes(Path(f'{image}').read_bytes())

    @staticmethod
    def from_yaml(yaml_file, dir_name):
        data = yaml.safe_load(yaml_file)
        return Project(
            dir_name,
            [f'{dir_name}/{x}' for x in data['images']],
            data.get('description'),
            data['title'],
            data.get('link'),
            data.get('author')
        )


def collect_yaml_config(dir_name, files):
    for file in files:
        if file.endswith('.yaml') or file.endswith('.yml'):
            return Path(f'{dir_name}/{file}').read_text(encoding="utf-8")
    return None


def collect_project(dir_info, output_dir):
    dir_name, _, files = dir_info
    yaml_config = collect_yaml_config(dir_name, files)
    if yaml_config is None:
        return None
    project = Project.from_yaml(yaml_config, dir_name)
    project.pack_images(dir_name, output_dir)
    return project


def collect_projects(input_dir, output_dir):
    return [collect_project(x, output_dir) for x in walk(input_dir) if x[0] != input_dir]


@click.command()
@click.option('--input', '-i', help='Input repository', default='repositories')
@click.option('--output', '-o', help='Output file', default='output')
@click.option('--template', '-t', help='Template file', default='template')
def main(input, output, template):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template))
    template = env.get_template('webpage.html')
    content = {
        'projects': collect_projects(input, output),
        'title': 'Projekty z Grafiki Komputerowej',
    }

    Path(output).mkdir(parents=True, exist_ok=True)
    with open(f'{output}/index.html', 'w', encoding="utf-8") as f:
        f.write(template.render(content))


if __name__ == '__main__':
    main()
