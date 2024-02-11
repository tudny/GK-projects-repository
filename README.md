# Generator strony projektów z Grafiki Komputerowej

## Użycie

Szczegóły projektów znajdują się w katalogach
`<nazwa_projektu>` w katalogu `repositories`.

Każdy projekt powinien składać się z pliku `config.yaml` oraz zdjęć.

```yaml
title: "Mega super projekt"
author: "Janek Kowalski"
link: "https://github.com/XYZ/ABC"
description: |
  Projekt prezentuje proste bryły w OpenGL.
images:
  - "window1.png"
  - "window2.png"
  - "window3.png"
```

## Uruchomienie

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

Strona zostanie wygenerowana w katalogu `output`.
