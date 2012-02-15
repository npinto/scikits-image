#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import e, sqrt, pi
from numpy.lib.index_tricks import mgrid
from numpy.lib.type_check import real
#from numpy.core.oldnumeric import shape
from numpy.core.multiarray import array
from numpy import tan

from scipy import *

def circsin2d(size, blackradius=0, phase=0):
	if size % 2 == 0:
		raise ValueError, "size must be odd"
	
	yg, xg = ogrid[0:size, 0:size]
	yc = xc = size / 2

	yg = absolute(yg - yc)
	xg = absolute(xg - xc)

	const = 20
	maxfreq = const*pi
	
	mag = (yg**2. + xg**2.) ** (1./2)
	mag = (mag-blackradius)
	putmask(mag, mag<0, maxfreq)
	#mag.putmask(maxfreq, mag>xc)

	scale = log(mag+const) / log(pi)
	putmask(scale, (scale*maxfreq)<pi/2, 0)
	ret = cos(maxfreq*scale - phase)

	#ret.putmask(0, ret==ret.max())
	
	return ret

def circsin2d2(size, blackradius=0, phase=0):
	if size % 2 == 0:
		raise ValueError, "size must be odd"
	
	yg, xg = ogrid[0:size, 0:size]
	yc = xc = size / 2

	yg = absolute(yg - yc)
	xg = absolute(xg - xc)

	#maxfreq = pi/2.

	mag = (yg**2. + xg**2.) ** (1./2)
	mag = (mag-blackradius).clip(0, mag.max())
	#mag /= xc	
	#mag *= 4

	#scale = log(mag) / log(2)
	#scale = 1. / (1+mag*4)
	#scale /= scale.max()
	#print scale
	#freq = log(mag*maxfreq)
	
	#ret = sin(mag*maxfreq - phase)

	return mag
	
#def sinus(freq,orient,phase,contrast):
	#"""
	#creates a function used in sin2d--I can't see a use for it
	#outside of sin2d

	#parameters:spatial frequency (cycles per pixel), orientation
	#(radians), phase (radians), contrast(value from 0 to 1), which
	#is set to 1 when no value is specified

	#return values:function to be applied to a two-dimensional space
	#"""
	#h = cos(orient) * freq
	#v = sin(orient) * freq	
	#def inner(x,y):
		#return map((lambda x, y: contrast*e**(1j*(2*pi*(h*x+v*y)+phase))), x, y)
	#return inner

#def sin2d(freq,orient,phase,shape,contrast=1.):
	#"""
	#creates a 2d sinusoidal filter of specified frequency,
	#orientation,phase,shape,and contrast

	#parameters:spatial frequency (cycles per pixel), orientation
	#(radians), phase (radians), tuple specifying height and width
	#of resulting filter contrast (value from 0 to 1), which
	#is set to 1 when no value is specified

	#return values:2d array of sinusoid of specified parameters
	#"""
	#k, l = shape
	#sa=sinus(freq,orient,phase,contrast)
	#t=mgrid[0:k:1,0:l:1][0]
	#u=mgrid[0:k:1,0:l:1][1]
	#return real(array(sa(t,u)))



#def discretesin2d(freq,orient,phase,k):
	#"""
	#discretesin2d creates a discrete version of sin2d in which
	#the resulting sinusoid values are either 0(black) or 1(white)

	#parameters: spatial frequency (cycles per pixel), orientation
	#(radians), phase (radians), k=tuple specifying height and
	#width of resulting filter

	#return values: 2d array of sinusoid of specified parameters;
	#all values in the array are either 0 or 1
	#"""
	#sa=sinus(freq,orient,phase)
	#t=mgrid[0:k[0]:1,0:k[1]:1][0]
	#u=mgrid[0:k[0]:1,0:k[1]:1][1]
	#n=sa(t,u)
	#h,w=shape(n)
	#new=[]
	#for a in n:
		#for b in a:
			#if b>0:
				#new.append(1.)
			#else:
				#new.append(0.)
	#new2=array(new)
	#new2.shape=h,w
	#return new2

#def contrastrev(Io, contrast, tempf, phase, spatf, orient):
	#"""
	#contrastrev creates a function used in creating contrast
	#reversal stimuli of the specified parameters.  It should
	#not need to be called outside of conrev.

	#parameters:Io=initial luminance, contrast (value from zero
	#to 1), temporal frequency (cycles per second), phase (radians),
	#spatial frequency (cycles per pixel), orientation (radians)

	#return value: function that can be applied to create contrast
	#reversal stimuli
	#"""
	#def inside(x,t):
		#h=cos(orient)*spatf*2*pi
		#v=sin(orient)*spatf*2*pi
		#spwv=array([h,v])
		#return map((lambda x,t:Io*(1+contrast*sin(2*pi*tempf*t)*cos(dot(spwv, x)-phase))), x, t)
	#return inside

#def conrev(Io,contrast,tempf,phase,spatf,orient,size,time):
	#"""
	#conrev creates contrast reversal stimuli of the specified
	#parameters
	
	#parameters:Io=initial luminance, contrast (value from zero
	#to 1), temporal frequency (cycles per second), phase (radians),
	#spatial frequency (cycles per pixel), orientation (radians), size
	#(a tuple of the height and width of the resulting filter, time
	#over which stimulus is computed (seconds)

	#return value: 2d array of contrast reversal stimuli with
	#specified parameters
	#"""
	#cl=contrastrev(Io,contrast,tempf,phase,spatf,orient)
       	#t=mgrid[0.:size[0]:1.]
       	#u=mgrid[0.:size[1]:1.]
	#r=array([array([a,b]) for a in t for b in u])
	#s=float(len(r))
	#time=mgrid[0:time+time/(s-1):time/(s-1)]
	#con=array(real(cl(r,time)))
	#con.shape=size[0],size[1]
	#return con

   
