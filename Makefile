filelist=help.rst download.rst index.txt release.txt help.rst latest.rst

small: ${filelist}
	cd pyreport/examples && make small

all: ${filelist}
	cd pyreport/examples && make

install: all
	cp ${filelist} /home/varoquau/www/src/computers/pyreport
	cd pyreport/examples && make install

clean:
	rm -rf pyreport/DEBUG
	cd pyreport/examples && make clean

release:
	make clean
	test "$$(./pyreport/pyreport --version)" != "$$(/home/varoquau/www/src/computers/pyreport/pyreport --version)" || print "!!!! WARNING !!!! Version number has not been changed"
	cp pyreport/pyreport /home/varoquau/www/src/computers/pyreport
	make commit
	make push
	make install
	make export
	make web

commit:
	sed 's/DEBUG = True/DEBUG = False/' -i pyreport/pyreport.py
	bzr commit
	sed 's/DEBUG = False/DEBUG = True/' -i pyreport/pyreport.py

push:
	bzr push sftp://1and1/pyreport

web:
	cp index.txt release.txt /home/varoquau/www/src/computers/pyreport
	cd /home/varoquau/www && make && make install

help.rst: pyreport
	#echo "::" > help.rst
	#echo "" >> help.rst
	rm -f help.rst
	./pyreport/pyreport -h >> help.rst
	echo "" >> help.rst
	sed 's/^/  /' -i help.rst

download.rst: pyreport
	rm -f download.rst
	echo '* `'$$(./pyreport/pyreport --version) '<./pyreport>`_'  > download.rst

latest.rst: pyreport
	rm -f latest.rst
	echo '`download '$$(./pyreport/pyreport --version) '<./release.html>`_'  > latest.rst

export: 
	scp ${filelist} 1and1:computers/pyreport
	cd pyreport/examples && make export

