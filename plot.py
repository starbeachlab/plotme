#!/usr/bin/python3


#######################################
###  COPYRIGHT: RENE STARITZBICHLER  ##
###             02.02.2020           ##
#######################################


import matplotlib.pyplot as plt
import sys
import read


### SELECT RANGES OF PLOTTING

#xmin = 900
#xmax = 1100

#xmin = 250
#xmax = 3150

#ymin = 0
#ymax = 1200


filters, arguments = read.filters_from_arguments( sys.argv[1:] )
if len( arguments) != len( sys.argv[1:]):
    print( 'WARNING: check this')
    exit(1)
print(arguments)
print(filters)

fname = ""
for d in arguments[0].split( '\\')[:-1]:
    fname += d + '\\'
for f,a in zip( filters, arguments):
    fname += a.split('\\')[-1][:-4] + '_'  ### WINDOWS !!!!
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
if False:
    axes.set_xlim([xmin,xmax])
    print ( "x limits: " + str(xmin) + " " + str(xmax))
if False:
    axes.set_ylim([ymin,ymax])
    print ( "y limits: " + str(ymin) + " " + str(ymax))


# set to 'False' if you don't want to create .png
if True:
    print("safe as: " + fname)
    plt.savefig(fname)

# comment this out when you don't want extra window with plots to pop up (e.g. when iterating through many groups)
plt.show()
