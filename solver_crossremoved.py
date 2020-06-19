#!/usr/bin/env python3

import sys
import math
import random
import copy

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# greedy
def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


def calcurate_total_distance(cities, tour):
    N = len(tour)
    return sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]])
                              for i in range(N))


# 点p1,p2を通る直線の方程式にp3を代入
def f(p1,p2,p3):
    return (p2[0]-p1[0]) * (p3[1]-p1[1]) - (p2[1]-p1[1]) * (p3[0]-p1[0])


# p1-p2とp3-p4がクロスしているかの判定
def isCross(p1,p2,p3,p4):
    return f(p1,p2,p3)*f(p1,p2,p4)<0 and f(p3,p4,p1)*f(p3,p4,p2)<0


def solve_cross(cities,tour):
    N=len(tour)
    improved=True
    while improved:
        improved=False
        for i in range(N):
            for j in range(i+2,N):
                if isCross(cities[tour[i]],cities[tour[i+1]],cities[tour[j]],cities[tour[(j+1)%N]]):
                    # tour[i+1],tour[j]=tour[j],tour[i+1]
                    # improved=True
                    # total distanceが短くなる時だけ変更
                    new_tour=copy.copy(tour)
                    new_tour[i+1],new_tour[j]=new_tour[j],new_tour[i+1]
                    if calcurate_total_distance(cities,new_tour)<calcurate_total_distance(cities,tour):
                        tour=copy.copy(new_tour)
                        improved=True
    return tour


def search_best_route(cities):
    N = len(cities)
    sum_dis=10**9
    # スタート地点は全てのノードで試す
    for _ in range(N):
        current_city = _
        tour = solve(cities,current_city) # greedy
        tour = solve_cross(cities,tour) # 交差を解除
        if sum_dis>calcurate_total_distance(cities,tour):
            ans=tour
            sum_dis=calcurate_total_distance(cities,tour)
    return ans


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities=read_input(sys.argv[1])
    print_tour(search_best_route(cities))

