import glob
from crossvalidation import *
from optimize import *

"""
Main file is used only for debugging purposes, project is oriented on Jupyter Notebook.
"""


def debug2():
    """
    Delete in final version, only for debugging.
    """
    set = get_sets("input/complete_traffic_export.csv")
    new_set = []
    for s in set:
        new_set.extend(s)
    ordered_set = order_set(new_set)
    flat_list = [item for sublist in ordered_set for item in sublist]

    tmp_cpct = [14, 1, 2, 3, 1, 1, 6, 1, 2, 3, 3, 1, 1, 2, 2, 40, 24, 27]  # sum 98, len 18
    slots = create_slots(tmp_cpct)
    sim1 = Simulation(flat_list, slots, "sim1")
    sim1.simulate()

    traffic = load_traffic("input/complete_traffic_export.csv")
    slots = create_slots(tmp_cpct)
    sim2 = Simulation(traffic, slots, "sim2")
    sim2.simulate()

    traffic = []
    files = sorted(glob.glob("input/*_traffic_export_*.csv"))
    for file in files:
        traffic.extend(load_traffic(file))

    slots = create_slots(tmp_cpct)
    sim3 = Simulation(traffic, slots, "sim3")
    sim3.simulate()

    print("done")


def debug():
    """
    Delete in final version, only for debugging.
    """
    # arriving_car = create_setup(98, 18) #sum, len
    tmp_cpct = [14, 1, 2, 3, 1, 1, 6, 1, 2, 3, 3, 1, 1, 2, 2, 40, 24, 27]
    traffic = load_traffic("traffic_export.csv")
    slots = create_slots(tmp_cpct)
    sim1 = Simulation(traffic, slots, "Skoda")
    sim1.simulate()
    print(sim1.slots[3].total_kWh)

    slots = create_slots(tmp_cpct)
    sim2 = Simulation(traffic, slots, "slot")
    sim2.simulate_slot(3)

    print(sim2.slots[3].total_kWh)
    print("debug")

    import time

    start = time.time()
    tmp_cpct = [14, 1, 2, 3, 1, 1, 6, 1, 2, 3, 3, 1, 1, 2, 2, 40, 24, 27]
    traffic = load_traffic("input/3_traffic_export_may.csv")
    optml = find_optimal(None, traffic, tmp_cpct)
    end = time.time()
    print(end - start)
    print(optml)


def my_main():
    """
    Delete in final version, only for debugging.
    """
    tmp_cpct = [14, 1, 2, 3, 1, 1, 6, 1, 2, 3, 3, 1, 1, 2, 2, 40, 24, 27]  # sum 98, len 18
    traffic = load_traffic("traffic_export.csv")
    slots = create_slots(tmp_cpct)
    sim1 = Simulation(traffic, slots, "sim1")
    sim1.simulate()

    print("my_main")


def sim_all():
    """
    Vizualizes outputs from 3 different simulations.
    """
    sims = []

    tmp_cpct = [14, 1, 2, 3, 1, 1, 6, 1, 2, 3, 3, 1, 1, 2, 2, 40, 24, 27]
    traffic = load_traffic("traffic_export.csv")
    slots = create_slots(tmp_cpct)
    sim1 = Simulation(traffic, slots, "Skoda")
    sim1.simulate()
    sims.append(sim1)

    weighted_setup = [5, 16, 11, 4, 10, 17, 5, 4, 21, 9, 1, 5, 13, 2, 1, 3, 3, 3]
    slots2 = create_slots(weighted_setup)
    sim2 = Simulation(traffic, slots2, "weighted")
    sim2.simulate()
    sims.append(sim2)

    equal_setup = [8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
    slots3 = create_slots(equal_setup)
    sim3 = Simulation(traffic, slots3, "equal")
    sim3.simulate()
    sims.append(sim3)

    slots_id = np.arange(0, 18, 1)

    for sim in sims:
        for id in slots_id:
            visualize(sim, id)


if __name__ == "__main__":
    cpct_50 = [67, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    eq = equally_divide(sum(cpct_50), len(cpct_50))
    print(sum(eq))
    # import time
    #
    # start = time.time()
    # tmp_cpct = [14, 1, 2, 3, 1, 1, 6, 1, 2, 3, 3, 1, 1, 2, 2, 40, 24, 27]
    # traffic = load_traffic("input/3_traffic_export_may.csv")
    # optml = find_optimal(None, traffic, tmp_cpct)
    # end = time.time()
    # print(end - start)
    # print(optml)

    # tmp_cpct = [10.0, 5.0, 6.0, 8.0, 5.0, 4.0, 8.0, 11.0, 3.0, 12.0, 4.0, 13.0, 6.0, 5.0, 4.0, 12.0, 9.0, 9.0]  # sum 98, len 18
    # traffic = load_traffic("traffic_export.csv")
    # slots = create_slots(tmp_cpct)
    # sim1 = Simulation(traffic, slots, "sim1")
    # sim1.simulate()
    # start = time.time()
    # tmp_cpct = [14, 1, 2, 3, 1, 1, 6, 1, 2, 3, 3, 1, 1, 2, 2, 40, 24, 27]
    # traffic = load_traffic("input/3_traffic_export_may.csv")
    # optml = find_optimal(None, traffic, tmp_cpct)
    # end = time.time()
    # print(end - start)
    # print(optml)
    # my_main()
    # sim_all()
    # debug()
