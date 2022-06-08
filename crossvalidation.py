import random
import datetime as dt
from optimize import *


def crossvalidate_optimal(sets, cpct):
    """
    K-fold crossvalidation on shuffled set. Function finds optimal setup for training data and then tests found setup on testing data.
    :param sets: Shuffled set from get_sets() function.
    :param cpct: Available charging stations that have to be divided between slots.
    :return: List with simulations of trained setup on testing data and list with simulations of overfitted setup.
    """
    tmp_sets = sets.copy()
    test = []

    train_sims = []
    test_sims = []

    for i in range(0, 28, 4):
        test = []
        tmp_sets = sets.copy()
        for j in range(4):
            add = tmp_sets[i]
            test.extend(add)
            tmp_sets.remove(add)
        train = [item for sublist in tmp_sets for item in sublist]
        train = order_set(train)
        train = [item for sublist in train for item in sublist]

        test = order_set(test)
        test = [item for sublist in test for item in sublist]

        # print("Length of train set: " + str(len(train)))
        # print("Length of test set: " + str(len(test)))

        train_opt = find_optimal(None, train, cpct)
        test_opt = find_optimal(None, test, cpct)

        # print("Sum of train capacity: " + str(train_opt))
        # print("Sum of test capacity: " + str(test_opt))

        train_slots = create_slots(train_opt)
        sim_train = Simulation(test, train_slots, "trained setup on test data")
        sim_train.simulate()

        test_slots = create_slots(test_opt)
        sim_test = Simulation(test, test_slots, "overfitted setup on test data")
        sim_test.simulate()

        # Append to lists of results
        train_sims.append(sim_train)
        test_sims.append(sim_test)

        print("-----------")

    return train_sims, test_sims

def crossvalidate_equal(sets, cpct):
    """

    :param sets: Shuffled set from get_sets() function.
    :param cpct: Available charging stations that is equally be divided between slots.
    :return:
    """
    tmp_sets = sets.copy()
    test = []

    equal_cpct = equally_divide(sum(cpct), len(cpct))
    equal_sims = []

    for i in range(0, 28, 4):
        test = []
        tmp_sets = sets.copy()
        for j in range(4):
            add = tmp_sets[i]
            test.extend(add)
            tmp_sets.remove(add)

        test = order_set(test)
        test = [item for sublist in test for item in sublist]

        equal_slots = create_slots(equal_cpct)
        sim_equal = Simulation(test, equal_slots, "equal setup on test data")
        sim_equal.simulate()

        # Append to lists of results
        equal_sims.append(sim_equal)

        print("-----------")

    return equal_sims



def get_sets(name):
    """
    Shuffle data into 28 groups each containing one set of weekdays.
    :param name: Name of file with input.
    :return: Shuffled set.
    """
    file = open(name, "r")
    lines = file.readlines()
    days = []
    last_date = None
    buffer = []
    week = [[], [], [], [], []]
    ctr = 0
    for line in lines:

        tmp = line.split(",")
        tmp[3] = tmp[3].rstrip("\n")
        date1 = dt.datetime.strptime(tmp[2], '%Y-%m-%d %H:%M:%S')
        date2 = dt.datetime.strptime(tmp[3], '%Y-%m-%d %H:%M:%S')
        if last_date is None:
            last_date = date1
        if last_date.day != date1.day:
            if len(buffer) > 0:
                week[last_date.weekday()].append(buffer)
                # days.append(buffer)
            buffer = []
            last_date = date1
        if date1.day == date2.day:  # check if arrival and departure are from same day
            if date1.weekday() != 5 and date1.weekday() != 6:
                charg = Car(int(tmp[0]), int(tmp[1]), date1, date2, ctr)
                buffer.append(charg)
                ctr += 1

    week[last_date.weekday()].append(buffer)
    # days.append(buffer)

    for w in week:
        random.shuffle(w)

    set = []
    for i in range(len(week[0])):
        subset = []
        for w in week:
            subset.append(w.pop())
        set.append(subset)

    return set


def take_var(object):
    """
    Helper function for function order_set(), takes object variable.
    :param object: Single object of class Car.
    :return: Returns int - order_id object variable.
    """
    return object[0].order_id


def order_set(set):
    """
    Returns ordered set based on order_id. Function needed in crossvalidate when putting shuffled sets together.
    :param set: Unordered set of Car objects.
    :return: Ordered set of Car objects.
    """
    set.sort(key=take_var)
    return set

