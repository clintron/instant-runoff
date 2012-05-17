"""
This Python code is under the Creative Commons 3.0 license
that requires proper attribution of idea origin well as code authorship.
Code and algorithm are written by Rafael Cosman
The Numpy code that computes the edge priorities was supplied by Peter Lindener as noted below

This code is written as if one is trying to select the winner of a set of candidates,
but it actually reverses itself with each recursive call.
The code was written in this manner for readability.

In this code the following convnetions are used:
Condorcet -> C
Plurality -> P

The winner of some system S is simply refered to as S, while the loser is referred to as SLoser
"""

#This allows the Python 3.2 print function to work properly, rather than using print as a keyword
from __future__ import print_function

#NUMerical PYthon is used for the matrix analysis, and is specifically helpful with determining the median delta-preferences:
from numpy import *#array, dot, newaxis, median, isnan, isinf, asarray, zeros, copy, bincount, argmax, amax

#Provides randomness used for the gaussisan convolutions:
from random import randint

import functools

class memoized(object):
	'''Decorator. Caches a function's return value each time it is called.
	If called later with the same arguments, the cached value is returned 
	(not reevaluated).
	'''
	def __init__(self, func):
		self.func = func
		self.cache = {}
	def __call__(self, *args):
		try:
			return self.cache[args]
		except KeyError:
			value = self.func(*args)
			self.cache[args] = value
			return value
		except TypeError:
			# uncachable -- for instance, passing a list as an argument.
			# Better to not cache than to blow up entirely.
			return self.func(*args)
	def __repr__(self):
		'''Return the function's docstring.'''
		return self.func.__doc__
	def __get__(self, obj, objtype):
		'''Support instance methods.'''
		return functools.partial(self.__call__, obj)

"""
Meta-Systems
"""
#Condorcet Winner if there is one, else returns the winner of system
def CElse(system, candidates, ballots):
	CWinner = C(candidates, ballots)
	if(CWinner != None):
		return CWinner

	return system(candidates, ballots)

#Check this:
def CElseElim(system, candidates, ballots):
	while True:
		CWinner = C(candidates, ballots)
		if CWinner != None:
			return CWinner
		else:
			elim = system(candidates, ballots)
			candidates = delete(candidates, elim)
			ballots = delete(ballots, ballots[where(candidates == elim)], axis = 0)

#Repeatedly eliminates the winner of System, until there is one candidate remaining
def Elim(system, candidates, ballots):
	while len(ballots) > 1:
		elim = where(candidates == system(candidates, ballots))
		candidates = delete(candidates, elim)
		ballots = delete(ballots, elim, axis = 0)
	assert(len(candidates) == 1)
	return candidates[0]

"""
Systems
"""
#General form of the Dictaroship system. Accepts an index for the voter to be the dictator.
def DictatorshipByVoter(voter, candidates, ballots):
	return P(candidates, array(ballots[:,voter:voter+1]))#Dictatorship is just plurality of the dictator :)
#Dictatorship by the voter with the highest index!
def Dictatorship(candidates, ballots):
	return DictatorshipByVoter(len(ballots)-1, candidates, ballots)#The last voter is always the dictator
#Randomly selects a ballot, and this ballot becomes the societal preference! Implemented as Dictatorship by a random voter.
def RandomBallot(candidates, ballots):
	return DictatorshipByVoter(randint(0, len(ballots)), candidates, ballots)#Random ballot is just dictatorship of a random voter

#Range Voting:
def RangeVoting(candidates, ballots):
	return candidates[sum(ballots, axis=1).argmax()]
#Range Voting Loser:
def RangeVotingLoser(candidates, ballots):
	return candidates[sum(ballots, axis=1).argmin()]

#Finds the winner or loser of the set of candidates
def newSystemElection(candidates, ballots, numTests = 20):
	simulations = map(randomElection, [copy(candidates) for i in range(numTests)], [copy(ballots) for i in range(numTests)])

	simulations = concatenate((simulations, candidates), axis=0)
	wins = bincount(simulations)
	sortedWins = sort(wins)[::-1]#reverse it

	if(twosampleproptest(sortedWins[0], numTests, sortedWins[1], numTests, 2.0) or numTests > 10000):
		return mode(simulations)
	else:
		return newSystemElection(candidates, ballots, numTests * 4)

#Plurality:
def P(candidates, ballots):
	return candidates[mode(argmax(ballots, axis = 0))]
#Plurality Loser
def PLoser(candidates, ballots):
	return candidates[antimode(argmax(ballots, axis = 0))]

#Anti-Plurality (Whoever gets the fewest last place votes wins):
def AP(candidates, ballots):
	return candidates[antimode(argmin(ballots, axis = 0))]
#Anti-Plurality Loser (Whoever gets the most last place votes):
def APLoser(candidates, ballots):
	return candidates[mode(argmin(ballots, axis = 0))]

def ShulzelikeSystem(candidates, ballots):
	priorities = calcPriorities(candidates, ballots)

#Recursively finds the winner or loser of the set of candidates, depending on the value of the boolean "winner". Not yet fully implemented.
def eliminationElection(candidates, ballots, winner = True):
	priorities = calcPriorities(candidates, ballots)
	"""
	#Base case of condorset loser: (Just for optimization, as pointed out in the Durham, Lindener paper)
	for index in range(len(priorities)):
		if ((priorities > 0) != winner)[index].all():
			return self.difference(CandidateSet(array([self.candidates[index]]))).election(ballots, winner, depth)
	"""
	#raise alpha until there is a false in the ultimate connectivity matrix:
	(UltimateConMat, alpha) = elimEdges(candidates, priorities)
	if alpha > 1:
		return candidates[0]#pick a random winner?

	#If there are no islands, search within all but the top cycle (this is the most conservative move):
	if not hasIslands(UltimateConMat):
		potentialLosers = notTopCycle(candidates, UltimateConMat)
	#detect any islands (orphaned candidates), and search within their losers:
	else:
		#print("Islands have been detected!")
		return candidates[0]
		"""
		potentialLosers = array(0)
		for island in islands(candidates, UltimateConMat):
			potentialLosers = potentialLosers, island.election(ballots, not winner, depth + 1)
		if potentialLosers.len() == self.len():
			#self.println("Islands have forced a tie: " + str(potentialLosers.candidates))
			return self
		"""
	losers = potentialLosers.election(ballots, not winner, depth + 1)
	#losers.println("[Eliminating " + losers.electionType() + "s: " + str(losers.candidates) + "]")
	potentialWinners = self.difference(losers)

	winners = potentialWinners.election(ballots, winner, depth)
	#self.println(self.electionType() + ": " + str(winners.candidates))

	return winners

"""
Helper functions
"""
#Finds the winner or loser of the set of candidates by repeatedly adding noise and dropping down to the Schwartz set.
def randomElection(candidates, ballots):
	while len(candidates) > 1:
		UltimateConMat = UltCon_BoolMat(calcPriorities(candidates, ballots) >= 0)
		if differentiated(UltimateConMat):#len(topCycle(candidates, UltimateConMat)) < len(candidates):
			candidates = topCycle(candidates, UltimateConMat)
		else:
			for i in range(20):
				ballots[randint(0, len(ballots)-1)][randint(0, len(ballots[0])-1)] += .01

	return candidates[0]

#Raises alpha until there is a false in the ultimate connectivity matrix
#Intelegently sweeps alpha down in a binary fashion until continuation would cause de-differentiation. Can select correct alpha to arbitrarially small error.
def elimEdges(candidates, Median):
	alpha = 1
	stepSize = 1
	while stepSize > 0:
		if differentiated(UltCon_BoolMat(Median >= (alpha - stepSize))[0]):
			alpha -= stepSize
		stepSize *= .5

	return (UltCon_BoolMat(Median >= alpha)[0], alpha)

#Island relationships are detected by a false in the ultimate connectivity matrix AND its transpose:
def hasIslands(UltimateConMat):
	return not((UltimateConMat | UltimateConMat.T).all())

#This method was contributed by Peter Lindener
def normalizedDeltaPrefs(candidates, ballots):
	RelevantBallots = ballots[candidates,:]
	ScaleFactor = 1.0 / RelevantBallots.ptp(0)
	ScaleFactor[isnan(ScaleFactor)] = 0.0#Nans will be generated by devide by zero from people with zero ballot spans. Their scale factor should be 0 to make all deltaprefs 0
	ScaleFactor[isinf(ScaleFactor)] = 0.0#Infs will be generated by devide by zero from people with zero ballot spans. Their scale factor should be 0 to make all deltaprefs 0
	DeltaPrefs = ( RelevantBallots[newaxis,:,:] - RelevantBallots[:,newaxis,:] ).T
	NormalizedDeltaPrefs = DeltaPrefs * ScaleFactor[:,newaxis,newaxis]
	return NormalizedDeltaPrefs
#Calculates the priorities of the edges. This implementation uses the median preference differences, because this discourages gaming.
def calcPriorities(candidates, ballots):
	Median = median( normalizedDeltaPrefs(candidates, ballots), axis=0 )
	setDiagonal(Median, 1)#The edge strength between a candidate and himself should be 1
	return Median

#Returns the top cycle based on the Ultimate Connectivity Matrix, assuming that there are absolutely no island relationships. Always returns a CandidateSet containing at least one candidate
def topCycle(candidates, UltimateConMat):
	wins = UltimateConMat.sum(True, int)
	topCandidates = candidates[(wins.max() == wins).nonzero()]
	return array(topCandidates)

#This method was contributed by Peter Lindener. It computes the Ultimate Connectivity Matrix based on a one-hop matrix.
@memoized
def UltCon_BoolMat(OneHopBoolMat):
	size = OneHopBoolMat.shape[0]
	OneToNHopMat = OneHopBoolMat.copy()              # Set up inital calculation state
	TwoToNHopMat = OneHopBoolMat.copy()
	h    = 1
	while( h < size ) :                                     # Loop untill all hops must have been propogated
		TwoToNHopMat = dot( OneToNHopMat, OneToNHopMat )    # Square matrix, each time doubling hop coverage, with boolean matrix Muliply
		OneToNHopMat = TwoToNHopMat | OneHopBoolMat         # Fold in the single hop term

		h <<= 1    # Double, keep track of hop coverage count
	return OneToNHopMat

#Sets the upper-left to bottom-right diagonal of arr to val
def setDiagonal(arr, val):
	size = arr.shape[0]
	for index in range(size):
		arr[index][index] = val

#Determines if the ultimate connectivity matrix passed has differentiated sufficiently to allow some degree of ordering between candidates
@memoized
def differentiated(UltimateConMat):
	return not UltimateConMat.all()

#Returns the mode of the set of numbers.
def mode(arr):
	return bincount(arr).argmax()
#Returns the least common of a set of numbers (NOTE: Will not return an element not present!)
def antimode(arr):
	return bincount(arr).argmin()

from math import sqrt
def twosampleproptest(x1,  n1,   x2,  n2,  zvalue):
	p1hat = float(x1)/n1
	p2hat = float(x2)/n2
	phat = float(x1 +x2)/(n1+n2)
	samplestat =  p1hat - p2hat
	se = sqrt(phat*(1.0-phat) * (1.0/n1 + 1.0/n2))
	return samplestat/se > zvalue

#Returns the Condorcet Winner if there is one:
def C(candidates, ballots):
	return CGeneral(True, candidates, ballots)
#Returns the Condorcet Loser if there is one:
def CLoser(candidates, ballots):
	return CGeneral(False, candidates, ballots)
#Returns the Condorcet Winner/Loser depending on the value of the boolean "winner". Returns None if there is no Condorcet winner/loser.
def CGeneral(winner, candidates, ballots):
	priorities = calcPriorities(candidates, ballots)
	for index in range(len(priorities)):
		if ((priorities > 0) == winner)[index].all():
			return candidates[index]
"""		
#Returns a set containing all islands, based on the Ultimate Connectivity Matrix passed. CURRENTLY DOES NOT WORK FULLY. It gives you all maximal subsets, rather than just those that form islands.
def islands(candidates, UltimateConMat):
	islandSet = set()
	if not hasIslands(UltimateConMat):
		islandSet.add(self)
		return islandSet

	for candidate in candidates:
		for island in difference(self, {candidate}).islands(UltimateConMat.compress(self.candidates != candidate, axis=0).compress(self.candidates != candidate, axis=1)):
			islandSet.add(island)
	return islandSet
	#return [CandidateSet(self.candidates[where(UltimateConMat[index])]) for index in range(len(UltimateConMat))]
"""