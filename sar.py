from numpy import *
from math import *
from scipy.misc import imsave
import scipy
h=1000
lmin=1000
l=1000
x=1000
k=4e12
dx=0.5
dl=0.5
st=1e-5
c=3e8
bw=k*st
sp=1.5*bw
freq=5e8
pwr=100
tm=3e-5
slen=tm*sp
dt=1/sp
tmin=1414/c

def signalr(t,par):
	tt=pi*k*pow(t-(st/2),2)
	#print t
	return complex(cos(tt-par),sin(tt-par))*(0<=t and t<st)

print slen
snls=zeros(int(sp*st),dtype=complex)
for i in  range(len(snls)):
	snls[i]=signalr(i*dt,0)
snlr=zeros([int(x/dx),int(slen)],dtype=complex)
snl2=zeros([int(x/dx),int(slen)],dtype=complex)
#snl3=zeros([int(x/dx),int(slen)],dtype=complex)
for i in  range(len(snlr)):
	rr=sqrt(pow(h,2)+pow(1500,2)+pow(i*dx-500,2))
	tos=2*rr/c
	for j in  range(len(snlr[i])):
		snlr[i][j]=signalr(j*dt-tos,2*pi*tos*freq)/pow(rr,4)
		#print j
imsave("test.bmp",real(snlr));

for i in range(len(snlr)):
	snl2[i]=convolve(snlr[i],flipud(conjugate(snls)),'same')
imsave("test2.bmp",real(snl2));
snl3=fft.fftshift(fft.fft(snl2,axis=0),axes=0)
imsave("test3.bmp",real(snl3));
def rcmc(ll,fr):
	a=-(2*c*fr*sqrt(((2*freq+c*fr)*(2*freq-c*fr)*(pow(h,2)+pow(ll,2)))/4))/(-pow(c,2)*pow(fr,2)+4*pow(freq,2))
	rrr=sqrt(pow(ll,2)+pow(h,2)+pow(a,2))
	return rrr
def r2ti(r):
	return 2*r/(c*dt)
snl4=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(snl4)):
	for j in range(len(snl4[i])):
		if(tm*sp>int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))+st*sp/2) and int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))+st*sp/2)>=0):
			snl4[i][j]=snl3[i][int(r2ti(rcmc(j*dl+lmin,(i*dx/x-0.5)/dx))+st*sp/2)]
imsave("test4.bmp",real(snl4));
snl5=fft.ifft(fft.ifftshift(snl4,axes=0),axis=0)
imsave("test5.bmp",real(snl5));
filt=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(filt)):
	for j in range(len(filt[i])):
		rrr=sqrt(pow(j*dl+l,2)+pow(h,2)+pow((i*dx)-x/2,2))
		tos=2*rrr/c
		par=-tos*2*pi*freq
		filt[i][j]=complex(cos(par),sin(par))
imsave("filt.bmp",real(filt));
snl6=zeros([int(x/dx),int(l/dl)],dtype=complex)
for i in range(len(snl6[0])):
	snl6[:,i]=convolve(snl5[:,i],flipud(conjugate(filt[:,i])),'same')
imsave("test6.bmp",abs(snl6));
	
	