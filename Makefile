filelist=help.rst download.rst index.txt release.txt help.rst latest.rst

small: ${filelist}
	cd examples && make small

all: ${filelist}
	cd examples && make

install: all
	cp ${filelist} /home/varoquau/www/src/computers/pyreport
	cd examples && make install

release:
	cp pyreport /home/varoquau/www/src/computers/pyreport
	make install

push:
	bzr push sftp://1and1/pyreport

web:
	cp index.txt /home/varoquau/www/src/computers/pyreport
	cd /home/varoquau/www && make && make install

help.rst: pyreport
	#echo "::" > help.rst
	#echo "" >> help.rst
	rm -f help.rst
	./pyreport -h >> help.rst
	echo "" >> help.rst
	sed 's/^/  /' -i help.rst

download.rst: pyreport
	rm -f download.rst
	echo '* `'$$(./pyreport --version) '<./pyreport>`_'  > download.rst

latest.rst: pyreport
	rm -f latest.rst
	echo '`download '$$(./pyreport --version) '<./release.html>`_'  > latest.rst

export: 
	scp ${filelist} 1and1:computers/pyreport
	cd examples && make export

