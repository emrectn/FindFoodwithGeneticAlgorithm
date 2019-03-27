import numpy as np
import random as rdm
from enum import Enum
import copy

N = 10
GENE_SIZE = N*N*2
FOOD_COUNT = 30
MUTATION_RATE = 0.1
CHROMOSOME_COUNT = 10
GENERATION_SIZE = 20


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


def create_chromosome(n=N, count=None):
    num = n*n*2 if not count else count
    chromosome = np.random.randint(low=1, high=5, size=num, dtype="int")

    return chromosome


def create_chromosome_details(chromosome_list):
    chromosome_details = list()

    for i in chromosome_list:
        details = dict()
        details['chromosome'] = i
        chromosome_details.append(details)
    return chromosome_details


def create_table_and_direction(n=N, food_count=FOOD_COUNT):
    cnt = 0
    array = np.zeros((n+2, n+2), dtype="int")
    array[0, :] = list(map(lambda x: -1, array[0, :]))
    array[:, -1] = array[:, 0] = array[-1, :] = array[0, :]
    array[(n+1)//2, (n+1)//2] = 5

    if food_count < (n*n/2):
        while cnt != food_count:
            x = rdm.randint(1, n)
            y = rdm.randint(1, n)

            if array[x, y] == 0:
                array[x, y] = 3
                cnt += 1
    else:
        print("Food overflow. Please reduce 'food_count'")

    return array


def eat_food(table, chromosome, n=N, food_count=FOOD_COUNT):
    eaten_food_count = 0
    x = y = (n+1) // 2
    cnt = 0

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
            table[x, y] = 9
            eaten_food_count += 1

        else:
            table[x, y] = 9
            pass

        if eaten_food_count == food_count:
            status = "Done"
            return status, eaten_food_count, cnt

        # print("i: {} x : {}, y:{}".format(i,x,y))
        cnt += 1
    status = "NotFound"
    return status, eaten_food_count, cnt


def selection_chromosome(chromosome_list):
    rates = [i['rate'] for i in chromosome_list]
    sum_of_rates = sum(rates)
    rates = list(map(lambda x: x/sum_of_rates, rates))
    chosen_index_list = np.random.choice(len(chromosome_list), 10, p=rates)
    return chosen_index_list


def create_selection_chromosome_list(chromosome_list, selections):
    new_chromosomes = copy.deepcopy(chromosome_list)

    for i, value in enumerate(selections):
        new_chromosomes[i] = chromosome_list[value]
        new_chromosomes[i]['status'] = 'Select'
        new_chromosomes[i].update(dict.fromkeys(['eaten', 'rate'], 0))
        # new_chromosomes[i].update(dict.fromkeys(['cnt', 'eaten', 'rate'], 0))
    return new_chromosomes


def crossover(chromosomes):

    crossover_ch = list()
    length = len(chromosomes[0]['chromosome'])

    for i in range(len(chromosomes) // 2):
        gene_change_list = np.random.choice([0, 1], length).tolist()

        ch1 = list()
        ch1 = list()
        ch1 = chromosomes[(2*i)]['chromosome'].tolist()
        ch2 = chromosomes[(2*i+1)]['chromosome'].tolist()

        for index, change in enumerate(gene_change_list):
            if change:
                ch1[index], ch2[index] = ch2[index], ch1[index]

        crossover_ch.append(dict())
        crossover_ch.append(dict())
        crossover_ch[(2*i)]['chromosome'] = ch1
        crossover_ch[(2*i+1)]['chromosome'] = ch2

    return crossover_ch


def mutation(chromosomes, mutation=MUTATION_RATE):

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


if '__main__' == __name__:
    table = create_table_and_direction()
    # print(table)
    chromosomes = [create_chromosome(0, GENE_SIZE) for x in range(CHROMOSOME_COUNT)]
    chromosome_list = create_chromosome_details(chromosomes)
    # print(chromosome_list)

    # Her bir kromozomun yediği yemeklerin başarı oranları.
    for i in range(len(chromosome_list)):
        chromosome = chromosome_list[i]['chromosome']
        status, eaten_food_count, cnt = eat_food(table, chromosome)
        chromosome_list[i]['cnt'] = cnt
        chromosome_list[i]['status'] = status
        chromosome_list[i]['eaten'] = eaten_food_count
        chromosome_list[i]['rate'] = eaten_food_count / FOOD_COUNT

    # for i in chromosome_list:
    #     print(i['status'], " ", i['eaten'], " ", i['rate'])

    # Find most successful chromosome
    most_success_ch = max(chromosome_list, key=lambda d: d['eaten'])
    print("max : ", most_success_ch)

    if most_success_ch == FOOD_COUNT:
        print("All the food are over.")

    selections = selection_chromosome(chromosome_list)

    # print(selections)

    chromosome_list = create_selection_chromosome_list(chromosome_list, selections)

    # crosover
    chromosome_list = crossover(chromosome_list)

    # mutation
    chromosome_list = mutation(chromosome_list)

