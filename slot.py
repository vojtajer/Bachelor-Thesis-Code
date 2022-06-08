from datetime import timedelta
import pandas as pd

max_char_time = timedelta(hours=5)


class Slot:
    id_counter = 0

    def __init__(self, capacity):
        """
        Initiation function at the beginning of simulation. Each slot represents one parking lot with N chargers.
        Object variables used for simulation purposes and storage of results.
        :param capacity: Integer representing N chargers available.
        """
        self.id = Slot.id_counter #Same as Car.park_id
        Slot.id_counter += 1
        self.capacity = capacity #Capacity of charging stations, size of taken array can not be bigger than capacity
        self.taken = [] #Array representing charging slots, cars are appended
        self.char_time = timedelta(0, 0) #Total charging time
        self.vehicle_ctr = 0 #Number of charged cars
        self.tmp_log = []
        self.log = pd.DataFrame() #DataFrame is created at the end of simulation
        self.total_kWh = 0 #Total electricity output in kWh.
        self.total = 0 #Total number of cars that needed charging during simulation

    def delete_departed(self, time):
        """
        When new car arrives, function checks if in taken array are not cars that should have left already.
        :param time: Every car that is in taken spot with departure timestamp before this timestamp is deleted from taken array.
        """
        for car in self.taken:
            if car.departure < time:
                self.taken.remove(car)

    def add_arrival(self, arriving_car):
        """
        Appends car to taken array if charging spot is available. Calculates duration of charging and charged electricity. Updates object variables.
        :param arriving_car: Object of class Car; if charging spot is available function updates Slot variables with values from Car.
        :return: True if charging spot is available and False if not.
        """
        if self.capacity > len(self.taken): #If
            self.tmp_log.append([arriving_car.car_id, arriving_car.park_id, arriving_car.arrival, arriving_car.departure, True])
            self.taken.append(arriving_car)
            self.vehicle_ctr += 1
            delta = arriving_car.departure - arriving_car.arrival
            if delta > max_char_time:
                delta = max_char_time
            self.char_time += delta

            return True
        else:
            self.tmp_log.append([arriving_car.car_id, arriving_car.park_id, arriving_car.arrival, arriving_car.departure, False])
            return False
