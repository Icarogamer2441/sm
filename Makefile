./dist/smrun ./dist/ioasm: smrun.py ioasm.py
	pyinstaller --onefile smrun.py
	pyinstaller --onefile ioasm.py

install:
	mv ./dist/* /usr/local/bin/
	rm -r ./build ./dist *.spec

clear:
	rm -r ./dist ./build *.spec

.PHONY: install clear