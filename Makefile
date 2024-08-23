./dist/smrun ./dist/ioasm ./dist/iolang: smrun.py ioasm.py iolang.py
	pyinstaller --onefile smrun.py
	pyinstaller --onefile ioasm.py
	pyinstaller --onefile iolang.py

install:
	mv ./dist/* /usr/local/bin/
	rm -r ./build ./dist *.spec

clear:
	rm -r ./dist ./build *.spec

.PHONY: install clear
