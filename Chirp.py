''' This generatates a single chirp.
@cf - center frequency of the chirp
@nocts - number of octaves swept out linearly (in octaves) by the chirp
@comps - number of harmonic components (all at zero phase) (1 means only the fundamental)
@amp - amplitude (should be < 1 if multiple comps)

If the cf=100 and nocts = 1, then the range is 100*2^(-.5) to 100*2^(.5).
The duration must be set in the call to generate. 
'''


import numpy as np
#import seaborn as sns
from scipy import signal
import math
#import sys

from genericsynth import synthInterface as SI

''' Create an array comprised of linear segments between breakpoints '''
# y - list of values
# s - list of number of samples to interpolate between sucessive values
def bkpoint(y,s) :
    assert(len(y)==(len(s)+1))
    sig=[]
    for j in range(len(y)-1) :
        sig=np.concatenate((sig, np.linspace(y[j], y[j+1], s[j], False)), 0)
    return sig


class Chirp(SI.MySoundModel) :

	def __init__(self, cf=440, nocts=1, comps=1, amp=1) :
		SI.MySoundModel.__init__(self)
		#create a dictionary of the parameters this synth will use
		self.__addParam__("cf", 100, 2000, cf)
		self.__addParam__("nocts", -3, 3, nocts)
		self.__addParam__("comps", 1, 5, comps)
		self.__addParam__("amp", 0, 1, amp)

	'''
		Override of base model method
	'''
	def generate(self, sigLenSecs, amp=None) :
		if amp==None : amp=self.getParam("amp")

		cf=self.getParam("cf")
		nocts=self.getParam("nocts")
		comps=self.getParam("comps")

		# envelope with 5ms attack, decay
		length = round(sigLenSecs*self.sr) # in samples
		ltrans = round(.005*self.sr)
		midms=length-2*ltrans-1
		ampenv=bkpoint([0,1,1,0,0],[ltrans,midms,ltrans,1])

		# The frequency sweep in units of octaves
		octs=np.linspace(-nocts/2, nocts/2, length, True)

		# Now generate each component with its different cf, and add them together
		signal = np.zeros(length)
		h = np.zeros(length)

		for harm in range(1,comps+1) :
			freqs=harm*cf*np.power(2.,octs)  #changes on every sample
			periods=freqs/self.sr  #portion of a period per (at each) sample
			cumstep=np.cumsum(periods)   #accumulated so we can pass it to sin
			h=np.array(np.sin(2*np.pi*cumstep))
			signal=signal+h  #add up the harmonics

		return amp*np.array(ampenv)*signal



