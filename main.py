"""
A simulation of an M/M/c queueing system.
"""

import matplotlib.pyplot as plt
import random

class Player:
    def __init__(self, arrival_time):
        """
        Stores the initial data

        Arguments: arrival_time - the time the players arrived into the queue

        TESTS::
            
            >>> a = Player(10)
            >>> a.arrival_time
            10

            >>> a = Player(20)
            >>> a.arrival_time
            20

            >>> a = Player(30)
            >>> a.arrival_time
            30
        """

        self.arrival_time = arrival_time
    
    def enter_queue(self, queue):
        """
        Places the player in the queue

        TESTS:
        
        Adding an a player to an empty queue::

            >>> random.seed(1)
            >>> q = Queue(1,2)
            >>> a = Player(0)
            >>> a.enter_queue(q)
            >>> '%.02f' %a.service_time
            '0.14'
            >>> '%.02f' %a.service_start_time
            '0.00'
            >>> '%.02f' %a.service_end_time
            '0.14'
            >>> '%.02f' %a.cost
            '0.14'
            >>> ['%.02f' %e for e in q.next_available_times]
            ['0.14', '0.00']

        Now we add a player to a queue with one busy server::

            >>> a = Player(0.1)
            >>> a.enter_queue(q)
            >>> '%.02f' %a.service_time
            '1.88'
            >>> '%.02f' %a.service_start_time
            '0.10'
            >>> '%.02f' %a.service_end_time
            '1.98'
            >>> '%.02f' %a.cost
            '1.88'
            >>> ['%.02f' %e for e in q.next_available_times]
            ['0.14', '1.98']
        
        Now both servers are blocked and the arriving Player must wait::

            >>> a = Player(0.12)
            >>> a.enter_queue(q)
            >>> '%.02f' %a.service_time
            '1.44'
            >>> '%.02f' %a.service_start_time
            '0.14'
            >>> '%.02f' %a.service_end_time
            '1.59'
            >>> '%.02f' %a.cost
            '1.47'
            >>> ['%.02f' %e for e in q.next_available_times]
            ['1.59', '1.98']

        Finally a player that arrives after the queue has emptied should move straight to service::

            >>> a = Player(2)
            >>> a.enter_queue(q)
            >>> '%.02f' %a.service_time
            '0.29'
            >>> '%.02f' %a.service_start_time
            '2.00'
            >>> '%.02f' %a.service_end_time
            '2.29'
            >>> '%.02f' %a.cost
            '0.29'
            >>> ['%.02f' %e for e in q.next_available_times]
            ['2.29', '1.98']

        """

        next_available_time = min(queue.next_available_times)
        next_available_server = queue.next_available_times.index(next_available_time)

        self.service_time = queue.service_time()
        self.service_start_time = max(self.arrival_time, next_available_time)
        self.service_end_time = self.service_start_time + self.service_time

        self.cost = self.service_end_time - self.arrival_time

        queue.next_available_times[next_available_server] = self.service_end_time
        queue.queue.append(self)

class Queue:
    def __init__(self, service_rate, no_of_servers = 1):
        """
        Stores the initial parameters of the queue

        Arguments: service_rate - the rate at which players are served at the queue
                   no_of_servers - the number of servers at the queue

        TESTS::
            >>> a = Queue(3, 4)
            >>> a.service_rate
            3
            >>> a.next_available_times
            [0, 0, 0, 0]

        """
        
        self.service_rate = service_rate
        self.next_available_times = [0 for server in range(no_of_servers)]
        self.queue = []

    def service_time(self):
        """
        Returns a service rate sampled from a negative exponential distribution

        TESTS::
            >>> random.seed(2)
            >>> a = Queue(5,6)
            >>> '%.02f' %a.service_time()
            '0.62'
            >>> a = Queue(3.5,6)
            >>> '%.02f' %a.service_time()
            '0.84'
            >>> a = Queue(1,6)
            >>> '%.02f' %a.service_time()
            '0.06'

        """

        return random.expovariate(self.service_rate)

    def clean_up_queue(self, time):
        """
        Removes players from a queue that have finished service

        Arguments: time - The current time of the simulation model
        
        TESTS::
         
            >>> q = Queue(3,7)    
            >>> a = Player(4)
            >>> a.service_end_time = 10
            >>> b = Player(8)
            >>> b.service_end_time = 12
            >>> c = Player(10)
            >>> c.service_end_time = 14
            >>> q.queue = [a, b, c]
            >>> q.clean_up_queue(8)
            >>> len(q.queue)
            3
            >>> q.clean_up_queue(11)
            >>> len(q.queue)
            2
            >>> q.clean_up_queue(13)
            >>> len(q.queue)
            1
        """

        self.queue = [Player for Player in self.queue if Player.service_end_time > time]

class SimulationModel():
    
    def __init__(self, arrival_rate, service_rate, no_of_servers):
        """
        Stores the parameters of the Model
        
        TESTS::
            >>> a = SimulationModel(5, 4, 2)
            >>> a.arrival_rate
            5
            >>> a.queue.service_rate
            4
            >>> len(a.queue.next_available_times)
            2

        """

        self.arrival_rate = arrival_rate
        self.queue = Queue(service_rate, no_of_servers)

    def main_simulation_loop(self, simulation_time):

        """
        Runs the simulation model and outputs performance measures

        Arguments: simulation_time - The length of time 

        TESTS::

            >>> random.seed(4)
            >>> a = SimulationModel(6, 7, 2)
            >>> players, snaps = a.main_simulation_loop(20)
            >>> len(players)
            129
            >>> a = SimulationModel(10, 2, 6)
            >>> players, snaps = a.main_simulation_loop(20)
            >>> len(players)
            177
            >>> for ID in players:
            ...     if players[ID].cost < 0:
            ...         print player.cost

        A negative time causes no players to move through the model::

            >>> a = SimulationModel(10, 2, 6)
            >>> players,snaps = a.main_simulation_loop(-20)
            >>> len(players)
            0

        Cant have a negative amount of servers::

            >>> a = SimulationModel(6, 7, -2)
            >>> players, snaps = a.main_simulation_loop(20)
            Traceback (most recent call last):
            ...
            ValueError: min() arg is an empty sequence
         
        """
        
        time = 0
        players = {}
        snapshots = {}
        no_of_players = 0
        
        while time < simulation_time:
            
            
            new_player = Player(time)
            no_of_players += 1
            players[no_of_players] = new_player 

            new_player.enter_queue(self.queue)
            self.queue.clean_up_queue(time)
            
            time += random.expovariate(self.arrival_rate)
            snapshots[time] = Snapshot(players, self.queue)

        
        return players, snapshots 

class Snapshot:
   
    def __init__(self, players, queue):
        """
        Stores the state of the system for analysis 
        """
        
        self.queue_length = len(queue.queue)
        self.average_cost = sum(players[ID].cost for ID in players )/len(players)


class DataAnalyser:
    
    def plot_queue_length(self, time, arrival_rate, service_rate, servers):
        """
        Function to plot the length of a queue over time
        """

        a = SimulationModel(arrival_rate, service_rate, servers)
        players, snaps = a.main_simulation_loop(time)

        times = [snap for snap in snaps]
        times.sort()

        plot_data = [[snap for snap in snaps],[snaps[snap].queue_length for snap in snaps]]

        plt.plot(plot_data[0],plot_data[1])
        plt.show()

D = DataAnalyser()
D.plot_queue_length(50,10,5,3)
