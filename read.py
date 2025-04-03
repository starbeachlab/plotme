import numpy as np

def read_spectra_96( args):

    is_data = False
    x = []
    y = []
    name = ''
    count = 0

    for i in range( 0 , len(args)):
        print(args[i])
        cols = args[i].split(':')
        #print( len(cols)-1, 'spectra')
        filename = cols[0]
        filters = []
        if len(cols) > 1:
            filters = cols[1:]
            #print( filters)
        with open( filename ) as r:
            for l in r:
                l = l.strip()
                if not is_data and '[SpectrumData]' == l:                    
                    if len(filters) == 0 or (len(filters) > 0 and name in filters):
                        is_data = True
                        count += 1
                elif 'Title' == l[:5]:
                    c = l.split()
                    name = c[-2] + c[-1]
                elif is_data and len(l) == 0:
                    is_data = False
                    x.append(y)
                    y = []

                elif is_data:
                    v = [ float(x) for x in l.split()]
                    if v[0] > 50:
                        y.append(v[1])
    return x

def read_96_pos( args):

    files = []
    pos = []
    
    for i in range( 0 , len(args)):
        print( args[i])
        with open( args[i]) as r:
            for l in r:
                l = l.strip()
                if 'Title' == l[:5]:
                    c = l.split()
                    pos.append( c[-2] + c[-1] )
                    files.append( args[i] )
    return pos,files



def same_sized( x):
    lengths = []
    for v in x:
        lengths.append( len( v))
    mini = min( lengths)
    #print(mini)
    new = []
    for v in x:
        new.append( v[:mini] )
    return new


### BE AWARE if used in a loop, you need to reset the block at the end of the loop body: 'block = []'
def block( r , block):
    is_data = False
    for l in r:
        block.append(l)
        if "[SpectrumData]" in l:
            is_data = True
        elif is_data and len(l.strip()) == 0:
            return True
    if len(block) == 0:
        return False
    else:
        return True

def pos( block):
    for l in block:
        if 'Title' == l[:5]:
            c = l.split()
            return c[-2] + c[-1] 
    

def spectrum( block):
    is_data = False
    s = []
    for l in block:
        if "[SpectrumData]" in l:
            is_data = True
            #print( 'found')
        elif is_data and len(l.strip()) > 0:
            #print(l.strip())
            v = [ float(x) for x in l.split() ]
            if v[0] > 50:
                s.append( v[1] )
    return s


def list_from_file( name):
    a = []
    with open( name) as r:
        for l in r:
            v = [float(x) for x in l.split()]
            a.extend(v)
    return a


def matrix( stream):
    m = []
    for l in stream:
        l = l.strip()
        if l[0] == '"':
            #print( l[:100])
            m.append( [ float(x) for x in l.split(';')[3:] ] )
        else:
            m.append( [float(x) for x in l.split()] )
    return m

def spectra_and_info( stream):
    m = []
    names = []
    first = []
    delta = []
    for l in stream:
        if l[0] == '"':          
            c = l.strip().split( ';')
            if len(c) == 0:
                continue
            m.append( [float(x) for x in c[3:] ])
            names.append( c[0] )
            first.append( float(c[1]) )
            delta.append( float(c[2]) )
        elif l[0] != '#':
            m.append( [float(x) for x in l.split()] )
    return m, names, first, delta

def matrix_from_list( args):
    m = []
    for a in args:
        print(a)
        with open( a) as r:
            m.extend( matrix(r) )
    print( len(m[0]), len(m[-1]))
    return m

def col( stream):
    v = []
    for l in stream:
        v.append( float(l) )
    return v


def contains_any(s, arr):
    s = s.lower()
    for a in arr:
        if a.lower() in s:
            return True
    return False

def contains_all(s, arr):
    s = s.lower()
    for a in arr:
        if not a.lower() in s:
            return False
    return True


def count_pair_outliers( cut, m):
    nr = 0
    for i in range( len(m[0])):
        for j in range( len(m)-1 ):
            for k in range( j+1, len(m)):
                if abs( m[j][i] - m[k][i] ) > cut:
                    nr += 1
    return nr
            

def JDX_manual( name):
    print( 'USAGE', name, 'FILE1:optFILTER11:optFILTER12:..  ... OUTFILE')

def JDX( args ):
    xmini = 50
    coo = []
    spectra = []
    filters = []
    names = []
    d=[]
    print(args)
    for i in range( len(args)):
        c = args[i].split(':')
        #if len(c) > 1:
        filters = c[1:]
        print( 'filters:', filters)
        count = 0
        with open( c[0] ) as r:
            #print( 'jdx:', c[0])
            x = []
            y = []
            #d = []
            go = False
            for l in r:
                count += 1
                if l[0] == '#':
                    if "DELTA" in l and go == True:
                        delta = float(l.split('=')[-1])
                        d.append(delta)
                    elif "TITLE" in l:
                        if len(filters) == 0 or contains_all(l, filters):
                            go = True
                            name = l.split('=')[-1].strip()
                            #name = name.split( '--')[0].lower().replace('_',' ')
                            names.append( name)
                        else:
                            go = False
                        #print( l.strip(), go, len(x))
                        if len(x) > 0:
                            coo.append( x)
                            spectra.append( y)
                            x = []
                            y = []
                    elif "XFACTOR" in l:
                        xfactor = float(l.split('=')[-1])
                    elif "YFACTOR" in l:
                        yfactor = float(l.split('=')[-1])
                    continue
                if go == False:
                    #print( 'skip')
                    continue
                v = [float(a) for a in l.split()] 
                for j in range( len(v) - 1 ):
                    xval = xfactor * v[0] + j*delta
                    #print( xval, end=' ')
                    #if yfactor * v[j+1] > 1000:
                    #    print( count, end=' ')
                    if xval >= xmini:
                        x.append( xval)
                        y.append( yfactor * v[j+1] )
                #print()
                
            if len(x) > 0:
                coo.append( x)
                spectra.append( y)
                d.append( delta)
                names.append( name)
            print( 'jdx:', c[0], 'lines:', len(coo), 'cols', len(x) )
    return d, names, coo, spectra


def is_num(x):
    try:
        float(x)
        return True
    except:
        return False


def filters_from_arguments( args):
    filters = []
    arguments = []
    for i in range( len(args)):
        c = args[i].split(':')
        if len(c) > 1:
            filters.append( c[1:] )
            arguments.append( c[0] )
        else:
            filters.append( '')
            arguments.append( c[0] )
        print( 'filters for', c[0],':', filters[-1])
    return filters, arguments


def filter_spectra( specs, filters): # NOT USED
    if len( filters ) == 0:
        print( 'nothing filtered, no filter')
        return specs
    if specs[0][0][0] != '"':
        print( 'nothing filtered, no identifier by which could be filtered:', specs[0][0])
        return specs
    cleaned  = []
    for s in specs:
        if contains_all( s[0], filters):
            cleaned.append( s )
    print( 'remaining:', len(cleaned))
    return cleaned
           
    
def spectra( arguments, filters): 
    spectra = []
    xvals = []
    info = []
    for ai in range( len(arguments)):
        with open( arguments[ai]) as r:
            specs,names,xmin,xdelta = spectra_and_info( r)
            #print( 'sizes:', [ len(specs[i]) for i in range(len(specs)) ])
            #xmin = np.array(xmin).reshape( -1, 1)
            #xdelta=np.array(xdelta).reshape(-1,1)
            # filter
            if len(filters[ai]) == 0:
                spectra.extend( specs)
                # add x
                if len(xmin) > 0:
                    for i in range( len(specs)):
                        x = xmin[i] + xdelta[i] * np.array( [j for j in range(len(specs[i]))] )
                        xvals.append(x)
                        info.append(names[i])
                else:
                    for i in range( len(specs)):
                        x = range( len(specs[i]))
                        xvals.append(x)
                        info.append(None)
            else:
                count = 0
                for s,n in zip(specs,names):
                    if contains_any( n, filters[ai] ):
                        spectra.append( s )                    
                        if len(xmin) > 0:
                            x = [ xmin[count] + i * xdelta[count]  for i in range( len(specs[count])) ]
                            xvals.append( x)
                            info.append( names[count] )
                        else:
                            xvals.append( range( len(specs[count])) )
                            info.append( None)
                    count += 1
    return xvals, spectra, info


def array_from_min_delta_nr( minim, delta, nr):
    x = []
    for i in range(nr):
        x.append( minim + i * delta)
    return x
    
