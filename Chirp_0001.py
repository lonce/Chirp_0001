import numpy as np
import math

from genericsynth import synthInterface as SI
from Chirp import Chirp  # This is "event" synthesizer this pattern synth will use


''' Create an array comprised of linear segments between breakpoints '''
# y - list of values
# s - list of number of samples to interpolate between sucessive values
def bkpoint(y,s) :
    assert(len(y)==(len(s)+1))
    sig=[]
    for j in range(len(y)-1) :
        sig=np.concatenate((sig, np.linspace(y[j], y[j+1], s[j], False)), 0)
    return sig

def oct2freq(octs, bf=440.) :
    return bf * np.power(2,octs)

def freq2oct(freq, bf=440.) :
    return np.log2(freq/bf)

################################################################################################################
class PatternSynth(SI.MySoundModel) :

	def __init__(self, cf_exp=440, nocts=2, rate_exp=0, irreg_exp=1, evdur=.25, cfsd=0, evamp=.5) :

                SI.MySoundModel.__init__(self)


                #get the sub synth
                self.evSynth=Chirp(oct2freq(cf_exp), nocts)


		#create a dictionary of the parameters this synth will use
                #cf_exp is number of octaves relative to 440 cps
                self.__addParam__("cf_exp", 
                        freq2oct(self.evSynth.getParam('cf', "min")), 
                        freq2oct(self.evSynth.getParam('cf', "max")), 
                        freq2oct(self.evSynth.getParam('cf')),
			lambda v :
				self.evSynth.setParam('cf', oct2freq(v)))

                self.__addParam__("nocts", 
                        self.evSynth.getParam('nocts', "min"), 
                        self.evSynth.getParam('nocts', "max"), 
                        self.evSynth.getParam('nocts'),
			lambda v :
                                self.evSynth.setParam('nocts', v))

                self.__addParam__("rate_exp", -10, 10, rate_exp)
                self.__addParam__("irreg_exp", 0, 50, irreg_exp)

                self.__addParam__("evdur", .001, 10, evdur)
                self.__addParam__("cfsd", 0, 10, cfsd)

                #My "hard coded" defaults for the subsynth
                self.evSynth.setParam('comps', 2)
                self.evSynth.setParam('amp', .2) #should be smaller for overlapping events...



	'''
		Override of base model method
	'''
	def generate(self,  durationSecs) :
                elist=SI.noisySpacingTimeList(self.getParam("rate_exp"), self.getParam("irreg_exp"), durationSecs)
                return self.elist2signal(elist, durationSecs)


	''' Take a list of event times, and return our signal of filtered pops at those times'''
	def elist2signal(self, elist, sigLenSecs) :
                numSamples=self.sr*sigLenSecs
                sig=np.zeros(sigLenSecs*self.sr)
                cfsd=self.getParam("cfsd")

                for nf in elist :
                        startsamp=int(round(nf*self.sr))%numSamples

                        # create some deviation in center frequency
                        #perturbedCf = 440*np.power(2,self.getParam("cf_exp")+np.random.normal(scale=cfsd)/12)
                        perturbedCf = oct2freq(self.getParam("cf_exp")+np.random.normal(scale=cfsd)/12)

                        self.evSynth.setParam("cf", perturbedCf)
                        gensig = self.evSynth.generate(self.getParam("evdur"))
                        sig = SI.addin(gensig, sig, startsamp)


                # envelope with 10ms attack, decay at the beginning and the end of the whole signal. Avoid rude cuts
                length = int(round(sigLenSecs*self.sr)) # in samples
                ltrans = round(.01*self.sr)
                midms=length-2*ltrans-1
                ampenv=bkpoint([0,1,1,0,0],[ltrans,midms,ltrans,1])

                return np.array(ampenv)*sig
