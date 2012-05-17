#NUMerical PYthon is used for the matrix analysis, and is specifically helpful with determining the median delta-preferences:
from numpy import array, random

#Generates random ballots with dimentions based on voters and candidates
def randomBallots(voters, candidates, votersEqual = True):
	return array([randomBallot(candidates, votersEqual) for voter in range(voters)])

#Generates a single voter's random ballot
def randomBallot(candidates, votersEqual = True):
	ballot = array([randomVote() for candidate in range(candidates)])
	if votersEqual and len(ballot) > 1:
		ScaleFactor = 1.0 / ballot.ptp(0)
		ballot = ballot * ScaleFactor
	ballot -= min(ballot)
	return ballot

#Returns a random vote from 0 to 1
def randomVote():
	return random.uniform(0, 1)