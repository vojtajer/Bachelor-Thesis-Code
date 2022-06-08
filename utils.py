import datetime as dt

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from car import *
from slot import *


# If month is True then visualize for whole 31 days gives data needed for optimization
def visualize_prep(sim, slot_id, month):
    """
    Helper function for visualize function, prepares inputs for plotting of graphs from Pandas DataFrame.
    :param sim: Object of simulation we want to visualize.
    :param slot_id: Object of slot we want to visualize.
    :param month: If month is True we want to visualize whole months, if False we want average day of month.
    :return: List with timestamp and number of vehicles during timestamp located on specified slot.
    """
    if slot_id is None:
        tmp = sim.log
        # print("All slots")
    else:
        # print("Just selected slot")
        tmp = sim.slots[slot_id].log

    if month is True:
        tmp['start'] = tmp['arrival']
        tmp['end'] = tmp['departure']
        tmp_ch = tmp.loc[tmp['satisfied'] == True]
        tmp_ch = tmp_ch.drop(columns=['arrival', 'departure', 'satisfied'])
        tmp = tmp.drop(columns=['arrival', 'departure', 'satisfied'])
    else:
        tmp['start'] = tmp['arrival'].dt.time
        tmp['end'] = tmp['departure'].dt.time
        tmp = tmp.loc[tmp['arrival'].dt.date == tmp['departure'].dt.date]
        tmp_ch = tmp.loc[tmp['satisfied'] == True]
        tmp_ch = tmp_ch.drop(columns=['arrival', 'departure', 'satisfied'])
        tmp = tmp.drop(columns=['arrival', 'departure', 'satisfied'])

    # Demand traffic

    start = pd.DataFrame({'time': tmp['start'], 'status': True})
    end = pd.DataFrame({'time': tmp['end'], 'status': False})

    frame = start.append(end)
    frame = frame.sort_values('time')
    queue = frame.values.tolist()

    ctr = 0
    nxt = None
    history = []
    times = []
    ctrs = np.array(())
    while queue:
        time, status = queue.pop(0)
        if queue:
            nxt = queue[0][0]
        if status:
            ctr += 1
        else:
            ctr -= 1

        if nxt != time:
            history.append([time, ctr])
            if month:
                times.append(time)
            else:
                times.append(dt.datetime.combine(dt.date.today(), time))
            ctrs = np.append(ctrs, ctr)

    if slot_id is not None and month is False:
        ctrs = ctrs / 20  # counted as average if we want to have 24 sum-up of whole month

    # Only charged vehicles
    start = pd.DataFrame({'time': tmp_ch['start'], 'status': True})
    end = pd.DataFrame({'time': tmp_ch['end'], 'status': False})

    frame = start.append(end)
    frame = frame.sort_values('time')
    queue = frame.values.tolist()

    ctr = 0
    nxt = None
    history_ch = []
    times_ch = []
    ctrs_ch = np.array(())
    while queue:
        time, status = queue.pop(0)
        if queue:
            nxt = queue[0][0]
        if status:
            ctr += 1
        else:
            ctr -= 1

        if nxt != time:
            history_ch.append([time, ctr])
            if month:
                times_ch.append(time)
            else:
                times_ch.append(dt.datetime.combine(dt.date.today(), time))
            ctrs_ch = np.append(ctrs_ch, ctr)

    if slot_id is not None and month is False:
        ctrs_ch = ctrs_ch / 20  # should count as average over whole month?

    return times, ctrs, times_ch, ctrs_ch


def visualize(sim, slot_id, month):
    """
    Creates Matplotlib graphs with traffic data for slot in simulation and saves them into outputs folder.
    :param sim: Object of simulation we want to visualize.
    :param slot_id: Object of slot we want to visualize.
    :param month: If month is True we want to visualize whole months, if False we want average day of month.
    """
    times, ctrs, times_ch, ctrs_ch = visualize_prep(sim, slot_id, month)
    succes_rate = round((sim.slots[slot_id].vehicle_ctr / sim.slots[slot_id].total) * 100, 2)

    fig, ax = plt.subplots()
    ax.xaxis_date()
    myFmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(myFmt)
    plt.title(
        "Visual. of traffic at slot " + str(slot_id) + ":sim-" + sim.name + " during month with succs rate: " + str(
            succes_rate) + "%")
    plt.ylabel("Number of cars")
    plt.xlabel("Time")

    plt.plot(times, ctrs, color='xkcd:blue', label='Demand')
    plt.plot(times_ch, ctrs_ch, color='xkcd:red', label='Satisfied')
    plt.axhline(sim.slots[slot_id].capacity, color='xkcd:green', linestyle='dashed', label='Capacity')
    plt.axhline(0, color='xkcd:black', linestyle='dotted')
    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.savefig('outputs/sim_' + sim.name + '_slot_' + str(slot_id) + '.png', dpi=300)
    # plt.show()


def create_slots(capacity):
    """
    From list with capacity values intiates Slot objects.
    :param capacity: Integer with specified charging capacity for each slot.
    :return: List of Slot objects.
    """
    slots = []
    for x in capacity:
        slots.append(Slot(x))
    return slots


def load_traffic(name):
    """
    Function reads input from file and transfers it into list of Car objects.
    :param name: Name of CSV file with traffic export.
    :return: List of Car objects that are used for simulating charging demand.
    """
    file = open(name, "r")
    lines = file.readlines()
    traffic = []
    for line in lines:
        tmp = line.split(",")
        tmp[3] = tmp[3].rstrip("\n")
        date1 = dt.datetime.strptime(tmp[2], '%Y-%m-%d %H:%M:%S')
        date2 = dt.datetime.strptime(tmp[3], '%Y-%m-%d %H:%M:%S')
        if date1.day == date2.day:  # check if arrival and departure are from same day
            #if date1.weekday() != 5 and date1.weekday() != 6:
                charg = Car(int(tmp[0]), int(tmp[1]), date1, date2)
                traffic.append(charg)
    return traffic


def get_unique_cars(name):
    """
    Loops through traffic data and finds all unique car_ids from file specified in parameter 'name'.
    :param name: Name of CSV file with traffic export.
    :return: List with unique car_ids in integer format.
    """
    file = open(name, "r")
    lines = file.readlines()
    unique = []
    for line in lines:
        tmp = line.split(",")
        tmp[3] = tmp[3].rstrip("\n")
        date1 = dt.datetime.strptime(tmp[2], '%Y-%m-%d %H:%M:%S')
        date2 = dt.datetime.strptime(tmp[3], '%Y-%m-%d %H:%M:%S')
        if date1.day == date2.day:  # check if arrival and departure are from same day
            if date1.weekday() != 5 and date1.weekday() != 6:
                id = int(tmp[0])
                if id not in unique:
                    unique.append(id)

    return unique


def load_selected_traffic(name, selected_cars):  # in selected cars list we specify cars we want to load into traffic
    """
    Function reads input from file and transfers it into list of Car objects. Returned are only those Cars with car_id in selected_cars list.
    :param name: Name of CSV file with traffic export.
    :param selected_cars: List of wanted Cars.
    :return: List of Car objects that are used for simulating charging demand.
    """
    file = open(name, "r")
    lines = file.readlines()
    traffic = []
    for line in lines:
        tmp = line.split(",")
        tmp[3] = tmp[3].rstrip("\n")
        date1 = dt.datetime.strptime(tmp[2], '%Y-%m-%d %H:%M:%S')
        date2 = dt.datetime.strptime(tmp[3], '%Y-%m-%d %H:%M:%S')
        if date1.day == date2.day:  # check if arrival and departure are from same day
            if date1.weekday() != 5 and date1.weekday() != 6:
                id = int(tmp[0])
                if id in selected_cars:
                    charg = Car(id, int(tmp[1]), date1, date2)
                    traffic.append(charg)
    return traffic


def highlight_max(s):
    """"
    highlight the maximum in a Series red.
    """
    is_max = s == s.max()
    return ['background-color: red' if v else '' for v in is_max]


def equally_divide(number, divider):
    """
    Equally divides number and splits the remainder.
    :param number: Number we want to divide into N parts.
    :param divider: N parts we want divide the number into.
    :return: List with divided numbers.
    """
    remainder = number % divider
    integer = int(number / divider)
    splits = []
    for i in range(divider):
        splits.append(int(integer))
    for i in range(remainder):
        splits[i] += 1

    return splits
