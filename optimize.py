import numpy as np

from simulation import *


def find_max(sim):
    """
    Helper function for find_optimal() function. Finds number of chargers that would each charging spot need to achieve
    100% satisfied vehicles.
    :param sim: Simulation for which we want to find maximum values.
    :return: List with values of maximum capacity of each slot.
    """
    max_values = []
    for i in range(len(sim.slots)):
        times, ctrs, times_ch, ctrs_ch = visualize_prep(sim, i, True)
        max_values.append(max(ctrs))

    return max_values


def find_optimal(sim, traffic, cpct):
    """
    Function finds optimal capacity value for each spot with given budget.
    :param sim: Simulation for which we want to find optimal capacity values.
    :param traffic: Traffic for which we want to optimise charing setup.
    :param cpct: Setup of charging slot with available capacity.
    :return:
    """
    slots = create_slots(cpct)
    sim = Simulation(traffic, slots, "tmp_opt")
    sim.simulate()

    opt_cpct = find_max(sim)
    tmp_slots = create_slots(opt_cpct)
    tmp_sim = Simulation(traffic, tmp_slots, "tmp_opt")
    tmp_sim.simulate()

    limit = sum(cpct)
    diff = 0
    max_cpct = []
    while sum(opt_cpct) != limit:
        # print(sum(opt_cpct))
        max = np.NINF

        # print(tmp_sim.total_kWh)

        for i in range(len(sim.slots)):
            if opt_cpct[i] > 0:
                tmp_cpct = opt_cpct.copy()
                tmp_cpct[i] = tmp_cpct[i] - 1
                tmp_slots = create_slots(tmp_cpct)
                slot_sim = Simulation(traffic, tmp_slots, "slot")
                slot_sim.simulate_slot(i)
                tmp_diff = slot_sim.slots[i].total_kWh - tmp_sim.slots[i].total_kWh
                # print(tmp_diff)
                tmp_kWh = tmp_sim.total_kWh + tmp_diff

                # print(str(tmp_sim.slots[i].total_kWh) + " --- " + str(tmp_sim.total_kWh))

                if max < tmp_kWh:
                    max = tmp_kWh
                    old_kWh = tmp_sim.slots[i].total_kWh
                    new_kWh = slot_sim.slots[i].total_kWh
                    slt_id = i
                    # print("Found new max at: " + str(i))
                    max_cpct = tmp_cpct.copy()

        opt_cpct = max_cpct.copy()
        tmp_sim.total_kWh += diff
        tmp_sim.slots[slt_id].total_kWh = new_kWh

    return opt_cpct
