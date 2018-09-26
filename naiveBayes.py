# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter
    that gives the best accuracy on the held-out validationData.
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"
    Prob = util.Counter()
    for label in trainingLabels:
      Prob[label] += 1.0
    Prob.normalize()
    self.Prob = Prob

    counts = {}
    total = {}
    for features in self.features:
      counts[features] = {0: util.Counter(), 1: util.Counter()}
      total[features] = util.Counter()

    for i in range(len(trainingData)):
      datum = trainingData[i]
      label = trainingLabels[i]

      for(features,val) in datum.items():
        counts[features][val][label] += 1.0
        total[features][label] += 1.0

    bestCond = {}
    bestAcc = None
    
    for k in kgrid:
      valid = 0
      condProb = {}
      self.condProb = condProb
      for features in self.features:
          condProb[features] = {0: util.Counter(), 1: util.Counter()}
                
            
      for features in self.features:
          for value in [0, 1]:
              for y in self.legalLabels:
                  condProb[features][value][y] = (counts[features][value][y] + k) / (total[features][y] + k * 2)

      predictions = self.classify(validationData)

      for i, prediction in enumerate(predictions):
         valid += validationLabels[i] == prediction 
      acc = valid / len(predictions)

      if acc > bestAcc or bestAcc is None:
         bestAcc = acc
         self.k = k
         bestCond = condProb
      
      self.condProb = bestCond
    
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    To get the list of all possible features or labels, use self.features and
    self.legalLabels.
    """
   
    logJoint = util.Counter()
    evidence = datum.items()
    "*** YOUR CODE HERE ***"
    for y in self.legalLabels:
        logJoint[y] = math.log(self.Prob[y])
        for features in self.condProb:
            prob = self.condProb[features][datum[features]][y]
            logJoint[y] += (prob and math.log(prob) or 0.0)

    return logJoint

   

  

def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds

    
      
