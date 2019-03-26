import numpy as np
import random as rdm
from enum import Enum

N = 10
FOOD_COUNT = 30
CHROMOSOME_COUNT = 10


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
            return status, eaten_food_count

        elif table[x, y] == 3:
            table[x, y] = 9
            eaten_food_count += 1

        else:
            table[x, y] = 9
            pass

        if eaten_food_count == food_count:
            status = "Done"
            return status, eaten_food_count

        # print("i: {} x : {}, y:{}".format(i,x,y))
        cnt += 1
    status = "NotFound"
    return status, eaten_food_count


if '__main__' == __name__:
    table = create_table_and_direction()
    print(table)
    chromosomes = [create_chromosome() for x in range(CHROMOSOME_COUNT)]
    chromosome_list = create_chromosome_details(chromosomes)
    # print(chromosome_list)

    for i in range(len(chromosome_list)):
        chromosome = chromosome_list[i]['chromosome']
        status, eaten_food_count = eat_food(table, chromosome)
        chromosome_list[i]['status'] = status
        chromosome_list[i]['eaten'] = eaten_food_count
        chromosome_list[i]['rate'] = eaten_food_count / FOOD_COUNT

    for i in chromosome_list:
        print(i['status'], " ", i['eaten'], " ", i['rate'])