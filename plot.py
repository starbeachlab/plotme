#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import matplotlib.pyplot as plt
import read
import os

filters, arguments = read.filters_from_arguments( [ '00000216_raw.txt:A1|'] )
print(arguments)
print(filters)

xmin=790
xmax=1000
ymin=200
ymax=4000


fname = ""
for d in arguments[0].split( '\\')[:-1]:
    fname = os.path.join(fname , d)
for f,a in zip( filters, arguments):
    fname += os.path.split(a)[1][:-4] + '_'  ### WINDOWS !!!!
    if len(f) > 0:
        for c in f:
            fname += c + '_'
fname = fname[:-1] + '.png'

xdata, spectra, info = read.spectra( arguments, filters )
    
show_labels = True

def Short( descr):
    # modify to individual uses !
    if show_labels == False:
        return ""
    else:
        return descr.split('|')[1]


print( 'sizes:', len(xdata), len(spectra), len(info))



for x,y,n in zip( xdata, spectra, info):
    if n != None:
        plt.plot( x, y, label = Short( n[1:-1]), linewidth=0.5)
    else:
        plt.plot( x, y, linewidth=0.5)
    
axes = plt.gca()

# comment this out when you don't want legend (e.g. when plotting a larger group of spectra)
#plt.legend()

# set to 'False' if you don't want to use this!
if True:
    axes.set_xlim([xmin,xmax])
    print ( "x limits: " + str(xmin) + " " + str(xmax))
if True:
    axes.set_ylim([ymin,ymax])
    print ( "y limits: " + str(ymin) + " " + str(ymax))


# set to 'False' if you don't want to create .png
if True:
    print("safe as: " + fname)
    plt.savefig(fname)

# comment this out when you don't want extra window with plots to pop up (e.g. when iterating through many groups)
plt.show()
