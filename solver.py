#!/usr/bin/env python3

import sys
import math
import random
import copy

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# make distance list
def dist_list(cities,dist):
    N = len(cities)
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist


# greedy
def greedy(cities,current_city,dist):
    N = len(cities)
    unvisited_cities = set(range(0, N))
    tour = [current_city]
    unvisited_cities.remove(current_city)

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour,dist


# greedy 初手を2番目に近い場所からの探索にする(N=4の場合に対応するためです...)
def greedy2(cities,current_city,dist):
    N = len(cities)
    unvisited_cities = set(range(0, N))
    tour = [current_city]
    unvisited_cities.remove(current_city)

    nearest = min(unvisited_cities,
                    key=lambda city: dist[current_city][city])
    # print(current_city,nearest)
    unvisited_cities.remove(nearest)
    next_city = min(unvisited_cities,
                    key=lambda city: dist[current_city][city])
    # print(current_city, nearest, next_city)
    unvisited_cities.remove(next_city)
    tour.append(next_city)
    current_city = next_city
    unvisited_cities.add(nearest)

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour,dist


# 総距離を計算
def total_distance(tour,dist):
    length = 0
    for i in range(len(tour)):
        length += dist[tour[i-1]][tour[i % len(tour)]]
    return length


# 全てのノードの組み合わせについて、入れ替えると短くなる場合は交換
# 改善できる限り繰り返す
def change_two(tour,dist):
    N=len(tour)
    improved = True
    while improved:
        improved=False
        for i in range(1,N):
            for j in range(i+2,N+1):
                A,B,C,D = tour[i-1],tour[i],tour[j-1],tour[j%N]
                if dist[A][B]+dist[C][D] > dist[A][C]+dist[B][D]:
                    tour[i:j] = reversed(tour[i:j])
                    # print(A,B,C,D,tour)
                    improved=True
    return tour,dist



############ ここから　交差している2点 -> swapに使いました ##########
############### このプログラムでは今回は使ってないです ##############

# 点p1,p2を通る直線の方程式にp3を代入
def f(p1,p2,p3):
    return (p2[0]-p1[0]) * (p3[1]-p1[1]) - (p2[1]-p1[1]) * (p3[0]-p1[0])


# p1-p2とp3-p4がクロスしているかの判定
def isCross(p1,p2,p3,p4):
    return f(p1,p2,p3)*f(p1,p2,p4)<0 and f(p3,p4,p1)*f(p3,p4,p2)<0

################## ここまで ###################



def search_best_route(cities):
    N = len(cities)
    sum_dis = 10**9 # とりあえず大きい値で初期化
    dist = [[0] * N for i in range(N)]
    for _ in range(N): # スタート地点を全ノードで試す
        current_city = _
        dist = dist_list(cities,dist)

        tour, dist = greedy(cities,current_city,dist) # greedy
        tour,dist = change_two(tour,dist)
        # print(_,tour)
        # 最も距離の短いものを選択
        if sum_dis>total_distance(tour,dist):
            ans=tour
            sum_dis=total_distance(tour,dist)
        
        tour, dist = greedy2(cities,current_city,dist) # greedy
        tour,dist = change_two(tour,dist)
        # print(_,tour,total_distance(tour,dist))
        # 最も距離の短いものを選択
        if sum_dis>total_distance(tour,dist):
            ans=tour
            sum_dis=total_distance(tour,dist)
    return ans


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities=read_input(sys.argv[1])
    print_tour(search_best_route(cities))