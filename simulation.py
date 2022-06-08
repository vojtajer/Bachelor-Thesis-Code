from utils import *

power = 17


class Simulation:

    def __init__(self, traffic, slots, name):
        """
        Intitates Simulation object with all neccessary object variables.
        :param traffic: Data of traffic that will be simulated later.
        :param slots: Charging slots that will try to satisfy traffic demand.
        :param name: Name of simulation.
        """
        self.total_ch_time = timedelta(0, 0)
        self.charged_cars = 0
        self.traffic = traffic
        self.slots = slots
        self.total_cars = len(traffic)
        self.total_kWh = 0
        self.name = name
        self.log = pd.DataFrame()  # log from all slots
        Slot.id_counter = 0

    def simulate(self):
        """
        From traffic data simulates charging demand on each slot and sumarizes results of simulation.
        """
        for car in self.traffic:
            park = car.park_id
            self.slots[park].delete_departed(car.arrival)
            self.slots[park].add_arrival(car)

        # Final sum up and
        for slot in self.slots:
            slot.log = pd.DataFrame(slot.tmp_log, columns=['car_id', 'park_id', 'arrival', 'departure', 'satisfied'])
            slot.total = len(slot.tmp_log)
            self.charged_cars += slot.vehicle_ctr
            self.total_ch_time += slot.char_time
            slot.total_kWh = (slot.char_time.days * 24 + slot.char_time.seconds / 3600) * power
            self.total_kWh += slot.total_kWh
            self.log = self.log.append(slot.log)

        if self.name != "tmp_opt":
            print("Total charging time: " + str(self.total_ch_time) + ", distributed electricity: " + str(
                self.total_kWh) + " kWh, charged cars: " + str(self.charged_cars) + "/" + str(
                self.total_cars) + " = " + str((self.charged_cars / self.total_cars) * 100) + "%, name: " + self.name)
        # print("End of simulation")

    def simulate_slot(self, slot_id):
        """
        Function simulates only selected spot. Saves time during optimization.
        :param slot_id: ID of slot we want to simulate.
        """
        for car in self.traffic:
            if car.park_id == slot_id:
                park = car.park_id
                # print("This is " + str(park) + " and selected is " + str(slot_id))
                self.slots[park].delete_departed(car.arrival)
                self.slots[park].add_arrival(car)

        slot = self.slots[slot_id]
        slot.log = pd.DataFrame(slot.tmp_log, columns=['car_id', 'park_id', 'arrival', 'departure', 'satisfied'])
        slot.total = len(slot.tmp_log)
        self.charged_cars += slot.vehicle_ctr
        self.total_ch_time += slot.char_time

        slot.total_kWh = (slot.char_time.days * 24 + slot.char_time.seconds / 3600) * power
