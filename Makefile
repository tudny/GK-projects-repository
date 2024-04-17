PACKNAME=projekty-z-grafiki.tar.gz
OUTPUT=output

.PHONY: all build pack clean clean-all

all: run pack

build: requirements.txt
	python -m venv venv
	pip install -r requirements.txt

run: build main.py
	python main.py --output $(OUTPUT)

pack: run
	tar -C $(OUTPUT) -czf $(PACKNAME) index.html repositories

clean:
	rm -rf $(OUTPUT)
	rm -rf *.tar.gz

clean-all: clean
	rm -rf venv

