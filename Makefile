all: generate

generate:
	mkdir -p tmp/
	python update_html

open:
	(cd tmp && open index.html)

edit:
	python edit_db

create:
	python create_db

clean:
	rm -rf tmp/
	rm *.pyc
	rm lib/*.pyc
