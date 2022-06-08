class Car:  # rename this!!!
    def __init__(self, car_id, park_id, arrival, departure, order_id=None):
        """
        Initiation method of class Car, objects of class represent charging demand.
        :param car_id: Each car has unique ID.
        :param park_id: Each charging slot has unique ID.
        :param arrival: Datetime object represents time of arriving at charging slot.
        :param departure: Datetime object represents time of departing from charging slot. Both of these timestamp together represent time window for charging the vehicle.
        :param order_id: Used only if dataset is divided into sets for crossvalidate, otherwise is None.
        """
        self.car_id = car_id
        self.park_id = park_id
        self.arrival = arrival
        self.departure = departure
        self.order_id = order_id
