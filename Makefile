PKG_NAME = crypto-stat
BIN_PATH = /bin

default: run

run:
	./crypto-stat/main.py

uninstall:
	sudo rm -f ${BIN_PATH}/${PKG_NAME}

install: uninstall
	sudo ln -s ${shell pwd}/crypto-stat/main.py ${BIN_PATH}/${PKG_NAME}
