'''
randvar.py

A module containing a class for building and training random variables


By Andy Exley
'''
import itertools


class RVNode:
    '''
    Represents a single random variable node in a Bayes Network
   
    '''
   
    def __init__(self, name, vrange, dependencies = None):
        '''
        Constructor for an RVNode

        vrange is a list containing the range of this RV (its possible values)
          i.e. [0, 1] for a boolean RV

        dependencies is a list of other RVNodes that this RVNode is conditionally dependent on
        '''
        self.name = name
        self.vrange = vrange
        self.deps = dependencies
        self.CPT = {}
        if self.deps == None:
            # okay, this RV does not depend on anything, we want a prior distr.
            for var in self.vrange:
                self.CPT[var] = 0
        else:
            deprangelist = []
            for dep in self.deps:
                deprangelist.append(dep.vrange)
            # okay now deprangelist is a list of lists of ranges. each possible
            # combination is a possible row in our CPT
            # it is added as a tuple key
            for row in itertools.product(*deprangelist):
                self.CPT[row] = {}
                for var in self.vrange:
                    self.CPT[row][var] = 0
                    
    def train(self, examples):
        '''trains this RV from the given examples. 
        
        If this RV is not dependent on another, we expect examples to be a list of 
        values in vrange. We just count and set probabilities in our CPT.
        e.g. if examples is [0,1,1,1,0,1,0,1,1,1] 
        then self.CPT[0] = 3 and self.CPT[1] = 7
        Note: In my example here, I stored counts. You could also store probabilities
        .3 and .7. The only thing that really matters is that when you sample the RV,
        it returns values based on the probability we trained on.
        
        If this RV is dependent on another, we expect examples to be a list of lists, 
        where each list is a single example containing values for the dependent variables and 
        this variable.
        e.g. if examples is [[0,1], [1,1], [0,1], [1,0], [0,0]]
        then self.CPT[(0,)][0] = 1
             self.CPT[(0,)][1] = 2
             self.CPT[(1,)][0] = 1
             self.CPT[(1,)][1] = 1
        '''
        if self.deps == None:
            for var in examples:
                self.CPT[var] += 1/len(examples)
        else:
            for var in examples:
                self.CPT[var[:len(var)-1][var[len(var)-1] += 1/len(examples)

    def sample(self, depvals = None):
        '''Generates a random sample from this RV.
        If this RV doesn't have dependencies, just use the CPT to generate a random value.

        If this RV has dependencies, use the given values to look up the CPT to generate a random value
        '''

        if depvals == None:
            

        

def test_simple():
    '''tests a simple RV with no dependencies
    '''
    r1 = RVNode('Rain', [0,1])
    r1.train([0,0,0,1,0,0,0,0,0,1,1,1,1,0,1]) # 9 0's, 6 1's.
    zcount = 0
    for i in range(1000):
        result = r1.sample()
        if result == 0:
            zcount += 1
    print('After 1000 samples, got %d 0s.' % zcount)

def test_1dep():
    '''tests an RV with a single dependency
    '''
    r1 = RVNode('Rain', [0,1])
    r1.train([0,0,0,1,0,0,0,0,0,1,1,1,1,0,1]) # 9 0's, 6 1's.

    r2 = RVNode('Wet', [0,1], dependencies = [r1])
       # train: it rains 6 times, 4 of those times the ground is wet.
       #        it doesn't rain 3 times, each of those times the ground is not wet.
    r2.train([[1,1], [1,1], [1,0], [1,1], [1,1], [1,0], [0,0], [0,0], [0,0]])
    zcount = 0
    for i in range(1000):
        result = r2.sample([1])
        if result == 0:
            zcount += 1
    print('After 1000 samples with rain, got %d 0s.' % zcount)
    zcount = 0
    for i in range(1000):
        result = r2.sample([0])
        if result == 0:
            zcount += 1
    print('After 1000 samples without rain, got %d 0s.' % zcount)

def test2_1dep():
    '''tests an RV with one dependency but not a bool var
    '''
    r1 = RVNode('Season', ['spring', 'summer', 'fall', 'winter'])
    r1.train(['spring', 'summer', 'fall', 'winter']) # equal prob for each
    
    r2 = RVNode('Rain', [0,1], dependencies = [r1])
    r2.train([
        ['winter', 0],
        ['winter', 1],
        ['winter', 1],
        ['spring', 0],
        ['spring', 1],
        ['summer', 0],
        ['summer', 0],
        ['summer', 0],
        ['summer', 0],
        ['summer', 0],
        ['summer', 1],
        ['fall', 0],
        ['fall', 1]
    ])
    
    zcount = 0
    for i in range(1000):
        result = r2.sample(['summer'])
        if result == 0:
            zcount += 1
    print('Out of 1000 simulated summer days, it did not rain %d of them.' % zcount)

def main():
    test_simple()
    test_1dep()

if __name__ == '__main__':
    main()
