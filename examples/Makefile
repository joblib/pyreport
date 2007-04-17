smalllist=latex.png simple.png pylab.png 

filelist=${smalllist} example.pdf example.html example.python example2.pdf example2.html example2.python

all: ${filelist}

small: ${smalllist} 

install: small
	cp ${filelist} /home/varoquau/www/src/computers/pyreport
	cp example_pyreport_0.png /home/varoquau/www/src/computers/pyreport
	cp example_pyreport_1.png /home/varoquau/www/src/computers/pyreport
	cp example2_pyreport_0.png /home/varoquau/www/src/computers/pyreport
	cp example2_pyreport_1.png /home/varoquau/www/src/computers/pyreport
	cp example2_pyreport_2.png /home/varoquau/www/src/computers/pyreport
	cd /home/varoquau/www && make

clean:
	rm -f ${filelist}
	rm -rf DEBUG

%.python: %.py
	cp $< $@

export:
	print pass

pylab.png: pylabex.png
	cp $< $@

%.png: %.eps
	convert -density 93 $<  $@ 
	#convert -density 650 $< -resize 650  $@ 
	rm $<

%.html: %.py ../pyreport
	../pyreport -l -s -o $@ $<

%.eps: %.py ../pyreport
	../pyreport -l -s -o $@ $<

%.pdf: %.py ../pyreport
	../pyreport -l -s $<

