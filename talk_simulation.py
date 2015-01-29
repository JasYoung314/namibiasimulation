"""A simple simulation model from the talk

Usage: talk_simulation.py [options] <demand> <service_rate> <simulation_time>

Arguments:
    demand  the demand per time unit at each station
    service_rate  the number of individuals the are served per time unit at the queue
    simulation_time  the number of time units to run the model for

"""
from __future__ import division

import random

from docopt import docopt

class Individual:
    """A class for individuals moving through the queue"""

    def __init__(self, arrival_time):
        """Storing the initial parameters of the individual
        
        Arguments: arrival_time  the time at which the individual arrives into the queue

        TESTS::
            
            >>> a = Individual(4)
            >>> a.arrival_time
            4
            >>> a = Individual(5)
            >>> a.arrival_time
            5
            >>> a = Individual(2)
            >>> a.arrival_time
            2
            >>> a = Individual(8)
            >>> a.arrival_time
            8

        """

        self.arrival_time = arrival_time

    def enter_queue(self, previous_exit_time, service_rate):
        """A method to allow an individual to enter a queue

        Arguments: previous_individual the previous individual to enter the queue
                   sevice_rate the rate at which customers are served at the queue

        TESTS:

        A individual enters an empty queue::

            >>> random.seed(2)
            >>> exit_time = 0.5
            >>> b = Individual(1)
            >>> b.enter_queue(exit_time, 1)
            >>> '%.02f' %b.service_time
            '3.12'
            >>> b.service_start
            1
            >>> '%.02f' %b.exit_time
            '4.12'

        A individual attempts to enter a queue when the server is busy::

            >>> random.seed(2)
            >>> exit_time = 2
            >>> b = Individual(1)
            >>> b.enter_queue(exit_time, 1)
            >>> '%.02f' %b.service_time
            '3.12'
            >>> b.service_start
            2
            >>> '%.02f' %b.exit_time
            '5.12'
        """

        self.service_time = random.expovariate(service_rate) 
        self.service_start = max(self.arrival_time, previous_exit_time) 
        self.exit_time = self.service_start + self.service_time
        self.wait = self.exit_time - self.arrival_time

class SimulationModel:
    """A class for the simulation model"""

    def __init__(self, demand, service_rate):
        """Stores the parameters of the queue

        Arguments: demand  the rate at which individuals arrive at the queue
                   service_rate  the rate at which individuals are served by the server

        TESTS::

            >>> s = SimulationModel(4, 5)
            >>> s.demand
            4
            >>> s.service_rate
            5
            >>> s.queue
            []

            >>> s = SimulationModel(1, 3)
            >>> s.demand
            1
            >>> s.service_rate
            3
            >>> s.queue
            []

            >>> s = SimulationModel(7, 4.2)
            >>> s.demand
            7
            >>> s.service_rate
            4.2
            >>> s.queue
            []

        """

        self.demand = demand
        self.service_rate = service_rate
        self.queue = []

    def clean_up_queue(self, time):
        """
        Removes individuals from the queue that have completed service

        Arguments: time the current time of the simulation model
        
        TESTS::
            
            >>> a = Individual(2) 
            >>> a.exit_time = 4
            >>> b = Individual(4) 
            >>> b.exit_time = 6
            >>> c = Individual(6) 
            >>> c.exit_time = 8
            >>> s = SimulationModel(4,5)
            >>> s.queue = [a,b,c]

       Wont remove any individuals if enough time has not elapsed::
       
            >>> s.clean_up_queue(1)
            >>> len(s.queue)
            3

       Only removes the correct individual::
       
            >>> s.clean_up_queue(5)
            >>> len(s.queue)
            2

       Removes the other individual now enough time has elapsed::
       
            >>> s.clean_up_queue(7)
            >>> len(s.queue)
            1

       Removes the final individual::

            >>> s.clean_up_queue(9)
            >>> len(s.queue)
            0

        """
        
        self.queue = [individual for individual in self.queue if individual.exit_time > time ]

    def main_simulation_loop(self, max_simulation_time):
        """
        Simulates the queue for the specified number of time units
        """

        t = 0
        previous_exit_time = 0
        
        individuals = {}
        no_of_individuals = 0

        while t < max_simulation_time:
            t += random.expovariate(self.demand) 
            new_individual = Individual(t) 
            individuals[no_of_individuals] = new_individual
            no_of_individuals += 1
            self.queue.append(new_individual) 
            new_individual.enter_queue(previous_exit_time, self.service_rate)
            self.clean_up_queue(t)
            previous_exit_time = new_individual.exit_time
        
        return individuals



if __name__ == '__main__':
    
    arguments = docopt(__doc__)

    demand = eval(arguments['<demand>'])
    service_rate = eval(arguments['<service_rate>'])
    simulation_time = eval(arguments['<simulation_time>'])

    Simulation_model = SimulationModel(demand, service_rate)
    individuals = Simulation_model.main_simulation_loop(simulation_time)

    average_cost = 0
    total_individuals = 0
    for ID in individuals:
        if individuals[ID].arrival_time > 200:
            average_cost += individuals[ID].wait
            total_individuals += 1

    print "----------"
    print "The Theoretical Value is: %s" %(1/(service_rate - demand))
    print "The Simulated Value is %s" %(average_cost/total_individuals)
    print "----------"

