.PHONY: install test compile doctor serve docker build-web

install:
	pip install -e .
	pip install -r requirements.txt

test:
	python -m pytest tests/ -q

compile:
	python -m compileall docintel

doctor:
	python -m docintel.cli doctor

serve:
	python -m docintel.cli serve

docker:
	docker build -t docintel .
	docker run -p 8000:8000 docintel

build-web:
	cd web && npm install && npm run build
