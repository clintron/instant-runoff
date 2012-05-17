#This allows the Python 3.2 print function to work properly, rather than using print as a keyword
from __future__ import print_function

#NUMerical PYthon is used for the matrix analysis, and is specifically helpful with determining the median delta-preferences:
from numpy import *#zeros, array, ones, argmax, ndarray

#This imports the actual voting system code
from best import *#newSystemElection, eliminationElection, pluralityElection, printArray

from randomBallots import *#randomBallots, randomBallot

from functools import *

import itertools
from pprint import pprint

#import cProfile

honestUtilitiesFile = open('VotingTestingData/honestUtilities.txt', 'w')
strategicUtilitiesFile = open('VotingTestingData/strategicUtilities.txt', 'w')
strategicUtilityDifferencesFile = open('VotingTestingData/strategicUtilityDifferences.txt', 'w')
databases = (honestUtilitiesFile, strategicUtilitiesFile, strategicUtilityDifferencesFile)

def testOneStrategy(system, candidates, ballots, voterIndex):
	#Insert the random ballot:
	tacticalVote = randomBallot(len(candidates))
	temp = ballots.T
	temp[voterIndex] = tacticalVote

	#Run an election to find the winner out of the candidateSet:
	return system(candidates, temp.T)

def testNStrategies(system, candidates, ballots, voterIndex):
	return [testOneStrategy(system, candidates, ballots, voterIndex) for i in range(2)]

def testOneVoter(system, candidates, ballots, voterIndex):
	tacticalVoter = ballots.T[voterIndex].copy()

	honestWinner = system(candidates, ballots)

	honestUtility = tacticalVoter[honestWinner]
	#print("\nHonest utility: " + (str(honestUtility)))
	honestUtilitiesFile.write(str(honestUtility) + "\t")

	winners = testNStrategies(system, candidates, ballots, voterIndex)
	strategicUtilities = tacticalVoter[winners]
	#print("Strategic utilities: " + (str(strategicUtilities)))
	strategicUtilitiesFile.write("\t")
	strategicUtilitiesFile.write("\t".join(map(str, strategicUtilities)))

	differences = strategicUtilities - honestUtility
	#print("Difference: " + (str(differences)))
	strategicUtilityDifferencesFile.write("\t")
	strategicUtilityDifferencesFile.write("\t".join(map(str, differences)))

def testNVoters(system, candidates, ballots):
	return testOneVoter(system, candidates, ballots, 0)

def testOneSimulation(system, numCandidates, numVoters):
	ballots = randomBallots(numVoters, numCandidates).T
	candidates = array(range(numCandidates))
	return testNVoters(system, candidates, ballots)

def testNSimulations(system, name = ""):
	print(name)
	[database.write(name + ("\t")) for database in databases]

	[testOneSimulation(system, 3, 7) for trial in range(10000)]
	#results = array([testOneSimulation(system, 3, 7) for trial in range(NUM_TRIALS/5)])
	#arr = sum(results, axis = 0)
	#print(arr)

	print("\n")
	[database.write("\n") for database in databases]

	#return results

def testSystems(testingframework, systems):
	[testingframework(system[0], system[1]) for system in systems]

pluralitySystems = ((P, "Plurality"),
                    (AP, "Anti-Plurality"),
                    (PLoser, "Plurality Loser"),
                    (APLoser, "Anti-Plurality Loser"),
                    (Dictatorship, "Dictatorship (for Strategic test, assumes you are not the dictator)"))
                    
NonDetSystems = ((RandomBallot, "Random Ballot (This does not work well with Strategic test)"))

RangeSystems = ((RangeVoting, "Range Voting"),
                (partial(CElse, RangeVoting), "Condorcet Else Range Voting"),
                (RangeVotingLoser, "Range Voting Loser"),
                (partial(CElse, RangeVotingLoser), "Condorcet Else Range Voting Loser"))

condorcetElseSystems = ((partial(CElse, P), "Condorcet Else Plurality"),
                        (partial(CElse, AP), "Condorcet Else Anti-Plurality"),
                        (partial(CElse, PLoser), "Condorcet Else Plurality Loser"),
                        (partial(CElse, APLoser), "Condorcet Else Anti-Plurality Loser"),

                        (partial(CElse, (partial(Elim, PLoser))), "Condorcet Else (Repeatedly Eliminate Plurality Loser)"),
                        (partial(CElse, (partial(Elim, APLoser))), "Condorcet Else (Repeatedly Eliminate Anti-Plurality Loser)"))

condorcetElimSystems = ((partial(CElseElim, P), "Condorcet Else Eliminate Plurality"),
                        (partial(CElseElim, AP), "Condorcet Else Eliminate Anti-Plurality"),
                        (partial(CElseElim, PLoser), "Condorcet Else Eliminate Plurality Loser"),
                        (partial(CElseElim, APLoser), "Condorcet Else Eliminate Anti-Plurality Loser"),

                        (partial(CElse, eliminationElection), "Elimination System (Not yet properly implemented)"),

                        (partial(CElse, newSystemElection), "New Non-deterministic System"))

ElimSystems = ((partial(Elim, P), "Repeatedly Eliminate Plurality"),
               (partial(Elim, AP), "Repeatedly Eliminate Anti-Plurality"),
               (partial(Elim, PLoser), "Repeatedly Eliminate Plurality Loser (Instant Runoff / AV)"),
               (partial(Elim, APLoser), "Repeatedly Eliminate Anti-Plurality Loser"))

AllSystems = concatenate((pluralitySystems, RangeSystems, condorcetElseSystems, ElimSystems, condorcetElimSystems))

print("\nBeginning Tests:")
print("-------------------")

#cProfile.run("testSystems(testNSimulations, AllSystems)", "profile.txt")
testSystems(testNSimulations, AllSystems)
#testNSimulations(partial(CElse, eliminationElection), "Elimination System (Not yet properly implemented)")