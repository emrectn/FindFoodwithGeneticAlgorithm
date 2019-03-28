# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:10:36 2019
@author: Emre Çetin
"""

import numpy as np
import random as rdm
from enum import Enum
import copy
import matplotlib.pyplot as plt
from numpy.random import choice
import matplotlib as mpl

"""
    @N : Table size NxN
    @GENE_SIZE : Number of genes in chromosome ex: [...]
    @FOOD_COUNT : Defines how many foods in table you have
    @MUTATION_RATE : If you have 10 genes, 1(10 * 0.1) of them will mutate.
    @CHROMOSOME_COUNT : Number of chromosomes
    @CURSOR : The place in the table. W
    @GENERATION_SIZE : Generation size
"""

N = 7
GENE_SIZE = N*N*3
FOOD_COUNT = 3
MUTATION_RATE = 0.1
CHROMOSOME_COUNT = 50
POINTER = [int((N+1)/2), int((N+1)/2)]
GENERATION_SIZE = 1000


# To recall directions
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


def create_chromosome(count=None):
    """
    Create the genes of the chromosome. Creates an array of N*N*2 by default.
    You can change the GENE_SIZE value as a parameter.
    """
    num = N*N*2 if not count else count
    chromosome = np.random.randint(low=1, high=5, size=num, dtype="int").tolist()

    # A array consisting of [1,2,3,4]
    return chromosome


def create_chromosome_details(chromosome_list):
    """
    To review the details create a dict()
    details = {'chromose': [1,4,3 ...], 'status': 'Done' or 'NotFound', 'eaten': 2}
    """
    chromosome_details = list()

    for i in chromosome_list:
        details = dict()
        details['chromosome'] = i
        chromosome_details.append(details)
    return chromosome_details


def create_table_and_direction(n=N, food_count=FOOD_COUNT):
    """
    @food_count: Defines how many foods in table you have.
    @n: table size ex: n x n

    A table was created. Empty spaces 0, edges -1, dishes 3, starting point 3
    was expressed.
    """
    cnt = 0
    array = np.zeros((n+2, n+2), dtype="int")
    array[0, :] = list(map(lambda x: -1, array[0, :]))
    array[:, -1] = array[:, 0] = array[-1, :] = array[0, :]
    array[(n+1)//2, (n+1)//2] = 5

    if food_count < (n*n/2):
        while cnt != food_count:
            # random x and y coordinates to create the food in table
            x = rdm.randint(1, n)
            y = rdm.randint(1, n)

            if array[x, y] == 0:
                array[x, y] = 3
                cnt += 1
    else:
        print("Food overflow. Please reduce 'food_count'")

    return array


def eat_food(main_table, chromosome, n=N, food_count=FOOD_COUNT):
    """
    @x,y : row-index, column-index
    Cursor moves according to the elements in the chromosome.
    If the value is -1, it goes out of the table and the state is specified as 'overflow'.
    If the value is 3, this is a food and the food_count increases. The value is changed to 0.
    """
    eaten_food_count = 0
    x = y = (n+1) // 2
    cnt = 0

    table = copy.deepcopy(main_table)
    for i in chromosome:
        if i == 1:
            x -= 1
        elif i == 2:
            y += 1
        elif i == 3:
            x += 1
        elif i == 4:
            y -= 1
        else:
            print("Error in eat_food() function")

        if table[x, y] == -1:
            status = "Overflow"
            return status, eaten_food_count, cnt

        elif table[x, y] == 3:
            table[x, y] = 0
            eaten_food_count += 1

        if eaten_food_count == food_count:
            status = "Done"
            return status, eaten_food_count, cnt

        # print("i: {} x : {}, y:{}".format(i,x,y))
        cnt += 1
    status = "NotFound"
    return status, eaten_food_count, cnt


# Weighted random selection according to the success rate of chromosomes.
def selection_chromosome(chromosome_list):
    rates = [i['rate'] for i in chromosome_list]
    sum_of_rates = sum(rates)
    if sum_of_rates == 0:
        rates = list(map(lambda x: x+(1/len(rates)), rates))
    else:
        rates = list(map(lambda x: x/sum_of_rates, rates))
    chosen_index_list = np.random.choice(len(chromosome_list), 10, p=rates).tolist()

    # Returns a list of randomly selected chromosomes.
    return chosen_index_list


# Creates a new list of selected chromosomes and resets the parameters.
def create_selection_chromosome_list(chromosome_list, selections):
    new_chromosomes = copy.deepcopy(chromosome_list)

    for i, value in enumerate(selections):
        new_chromosomes[i] = chromosome_list[value]
        new_chromosomes[i]['status'] = 'Select'
        new_chromosomes[i].update(dict.fromkeys(['eaten', 'rate'], 0))
        # new_chromosomes[i].update(dict.fromkeys(['cnt', 'eaten', 'rate'], 0))
    return new_chromosomes


def crossover(chromosomes):
    """
    @ gene_change_list: This list consists of 0-1. The list size is GENE_SIZE
    Crossover between two successive chromosomes. A new 'gene_change_list' is
    created for each pair. Look at the elements of the list with the loop.
    If the element is 1, the elements of the pairs of chromosomes change.
    If the element is 0, there is no change.
    """

    crossover_ch = list()
    length = len(chromosomes[0]['chromosome'])

    for i in range(len(chromosomes) // 2):
        gene_change_list = np.random.choice([0, 1], length).tolist()

        ch1 = list()
        ch1 = list()
        ch1 = chromosomes[(2*i)]['chromosome']
        ch2 = chromosomes[(2*i+1)]['chromosome']

        for index, change in enumerate(gene_change_list):
            if change:
                ch1[index], ch2[index] = ch2[index], ch1[index]

        crossover_ch.append(dict())
        crossover_ch.append(dict())
        crossover_ch[(2*i)]['chromosome'] = ch1
        crossover_ch[(2*i+1)]['chromosome'] = ch2

    return crossover_ch


def mutation(chromosomes, mutation=MUTATION_RATE):
    """
    @mutation_indexs: List of randomly selected indices according to mutation rate.
    A separate 'mutation_indexs' is created for each chromosome.
    The value of the elements in the indices in this list increases by 1.
    """

    length = len(chromosomes[0]['chromosome'])
    cnt = 0
    for i in chromosomes:
        mutation_indexs = np.random.choice(length, int(length*MUTATION_RATE), replace=False)
        for index in mutation_indexs:
            if i['chromosome'][index] != 4:
                i['chromosome'][index] += 1 % 5
            else:
                i['chromosome'][index] = 1
        cnt += 1
    return chromosomes


# visualize table with element(food, cursor, space)
def matris_visualize(param, size=N):
    mpl.style.use('default')
    plt.matshow(param)
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, size+1, 1))
    ax.set_yticks(np.arange(-.5, size+1, 1))
    ax.set_facecolor("black")
    ax.grid(which='both', color="black")
    plt.show(block=False)
    plt.pause(0.25)
    plt.close()


# change cursor coardinate in table
def follow_cursor(matrix, move):
    matrix[POINTER[0]][POINTER[1]] = 0
    # up
    if move == 1:
        POINTER[0] -= 1
        matrix[POINTER[0]][POINTER[1]] = 5
    # right
    elif move == 2:
        POINTER[1] += 1
        matrix[POINTER[0]][POINTER[1]] = 5
    # down
    elif move == 3:
        POINTER[0] += 1
        matrix[POINTER[0]][POINTER[1]] = 5
    # left
    else:
        POINTER[1] -= 1
        matrix[POINTER[0]][POINTER[1]] = 5


if '__main__' == __name__:
    table = create_table_and_direction()
    # print(table)
    matris_visualize(table, N)
    chromosomes = [create_chromosome(GENE_SIZE) for x in range(CHROMOSOME_COUNT)]
    chromosome_list = create_chromosome_details(chromosomes)
    # print(chromosome_list)

    for g in range(GENERATION_SIZE):
        for i in range(len(chromosome_list)):
            chromosome = chromosome_list[i]['chromosome']
            status, eaten_food_count, cnt = eat_food(table, chromosome)
            chromosome_list[i]['cnt'] = cnt
            chromosome_list[i]['status'] = status
            chromosome_list[i]['eaten'] = eaten_food_count
            chromosome_list[i]['rate'] = eaten_food_count / FOOD_COUNT

        # Find most successful chromosome
        most_success_ch = max(chromosome_list, key=lambda d: d['eaten'])

        # If completed
        if most_success_ch['status'] == "Done":
            print("All the food are over.")
            print("Generation : ", g)
            print("max : [status : {}, eaten : {}, cnt : {}".format(most_success_ch['status'], most_success_ch['eaten'], most_success_ch['cnt']))
            for i in most_success_ch['chromosome'][:most_success_ch['cnt']+1]:
                follow_cursor(table, i)
                matris_visualize(table)

            break

        selections = selection_chromosome(chromosome_list)

        # selection
        chromosome_list = create_selection_chromosome_list(chromosome_list, selections)

        # crosover
        chromosome_list = crossover(chromosome_list)

        # mutation
        chromosome_list = mutation(chromosome_list)

