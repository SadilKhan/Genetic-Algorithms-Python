class EightQueens():

    """ Solving Eights Queen problem using Genetic Algorithm"""

    def __init__(self,numPoplulation=100,recombProb=1,mutationProb=0.8):
        self.numPopulation=100
        self.recombProb=recombProb
        self.mutationProb=mutationProb
        

        self.optimize()

    
    def optimize(self):
        self.initialize_population()
        self.fitness_used=0
        self.foundSol=False
        self.generation=0
        self.meanSolutions=[] # mean of the fitness score per generations
        self.bestSolutions=[] # Value of the best solutions per generations
        self.solutions=[]
        
        while (not self.foundSol) and (self.fitness_used<=10000):
            self.generation+=1
            selected=self.selection()
            offspring=self.crossover(selected)
            if len(offspring)>0:
     
                mutatedOffspring=self.mutation(offspring)

                newPopulation=np.concatenate((self.population,mutatedOffspring))

                self.elimination(newPopulation)


    def fitness(self,population):
        """Calculate the number of times queens are being attacked. Optimal is 0"""
        nPop=len(population)
        attacksList=[]

        for k in range(nPop):
            gene=population[k]
            attacks=0
            for i in range(len(gene)):
                valPos=gene[i]
                for j in range(i+1,len(gene)):
                    valPos-=1
                    if gene[j]==valPos:
                        attacks+=1
                valPos=gene[i]
                for j in range(i+1,len(gene)):
                    for j in range(i+1,len(gene)):
                        valPos+=1
                        if gene[j]==valPos:
                            attacks+=1
            if attacks==0:
                self.foundSol=True
                if gene not in self.solutions:
                    self.solutions.append(gene)
            attacksList.append(-attacks)
        self.fitness_used+=1
        
        return attacksList
    def mutation(self,offspring):

        """ Swap Mutation"""

        for i in range(len(offspring)):
            if np.random.rand()<=self.mutationProb:
                swapPos=np.random.randint(0,7,2)
                val1,val2=offspring[i][swapPos]
                offspring[i][swapPos[0]]=val2
                offspring[i][swapPos[1]]=val1   
        
        mutatedOffspring=offspring
        
        return mutatedOffspring

        
    def crossover(self,selected):
        """ Cut-and-Crossfill crossover"""
        
        random_cut=np.random.choice(range(1,7),1)[0]
        child0=selected[1][:random_cut]
        child1=selected[0][:random_cut]

        if np.random.rand()<=self.recombProb:
            for i in range(8):
                if selected[1][i] not in child0:
                    child0=np.append(child0,selected[1][i])

                if selected[0][i] not in child1:
                    child1=np.append(child1,selected[0][i])

            offspring=np.array([child0,child1])
            return offspring
        else:
            return []
    def selection(self):
        """Selection of Parents"""
        selected=[]
        # Choose 2 best out of 5 random
        choices=self.population[np.random.choice(range(self.numPopulation),5)]

        # Evalute fitness for all candidates
        scores=self.fitness(choices)

        # Choose the best 2 of them
        bestCandidate=choices[np.argsort(scores)[-2:]]
        selected.append(bestCandidate)
        return np.array(selected)[0]
        
    def elimination(self,newPopulation):
        """ Eliminate 2 least scoring candidates"""
        fitnessScorePop=self.fitness(newPopulation)
        sortScorePop=np.argsort(fitnessScorePop)
        self.bestSolutions.append(np.max(fitnessScorePop))
        self.meanSolutions.append(np.mean(fitnessScorePop))
        self.population=newPopulation[sortScorePop[-100:]]

        
    def initialize_population(self):
        self.population=[]

        for i in range(self.numPopulation):
            self.population.append(self.permutation())
        
        self.population=np.array(self.population)

    def permutation(self):
        return np.random.permutation(list(range(0,8)))
        
        
        
        
        
if __name__ == '__main__':
  eq=EightQueens()
  print("Best Solution is ",eq.bestSolutions)
        
