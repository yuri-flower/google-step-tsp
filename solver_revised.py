#!/usr/bin/env python3

import sys
import math
import random
import copy

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities,current_city):
    N = len(cities) 

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    dist_min=10**9

    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

    sum_dist=0
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        # while isCross()
        sum_dist += dist[current_city][next_city]
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    if dist_min > sum_dist:
        dist_min = sum_dist
        ans = tour
    
    return ans


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
                    tour[i+1],tour[j]=tour[j],tour[i+1]
                    improved=True
                    # new_tour=copy.copy(tour)
                    # new_tour[i+1],new_tour[j]=new_tour[j],new_tour[i+1]
                    # if calcurate_total_distance(cities,new_tour)<calcurate_total_distance(cities,tour):
                    #     tour=copy.copy(new_tour)
                    #     improved=True
    return tour


#i,j,k,l,m 5連続点の距離の和
def sum_dis(cities,i,j,k,l,m):
    N=len(cities)
    return distance(cities[i%N],cities[j%N])+distance(cities[j%N],cities[k%N])+distance(cities[k%N],cities[l%N])+distance(cities[l%N],cities[m%N])

# i->i+1->i+2->i+3->i+4 より i->j->k->l->i+4の方が短かったらそっちを採用
# def improve(tour,cities,dist,i,j,k,l):
#     N=len(cities)
#     if dist>sum_dis(cities,i,j,k,l,i+4):
#         dist=sum_dis(cities,i,j,k,l,i+4)
#     return dist


# 5連続点を取り出してみてその間の3つを入れ替えてみてより短い経路が見つかったらそれを採用
def three_opt(cities,tour):
    N = len(tour)
    new_tour=copy.copy(tour)
    i=0
    while i < N:
        P1,P2,P3=i+1,i+2,i+3
        min_dist=sum_dis(cities,i,i+1,i+2,i+3,i+4) # 元々の距離
        # (i+1,i+2,i+3)を入れ替える
        if min_dist>sum_dis(cities,i,i+1,i+3,i+2,i+4):
            P1,P2,P3=i+1,i+3,i+2
            # print(i+1,i+2,i+3,' -> ',P1,P2,P3,min_dist,sum_dis(cities,i,i+1,i+3,i+2,i+4))
            min_dist=sum_dis(cities,i,i+1,i+3,i+2,i+4)

        if min_dist>sum_dis(cities,i,i+2,i+1,i+3,i+4):
            P1,P2,P3=i+2,i+1,i+3
            # print(i+1,i+2,i+3,' -> ',P1,P2,P3,min_dist,sum_dis(cities,i,i+2,i+1,i+3,i+4))
            min_dist=sum_dis(cities,i,i+2,i+1,i+3,i+4)

        if min_dist>sum_dis(cities,i,i+2,i+3,i+1,i+4):
            P1,P2,P3=i+2,i+3,i+1
            # print(i+1,i+2,i+3,' -> ',P1,P2,P3,min_dist,sum_dis(cities,i,i+2,i+3,i+1,i+4))
            min_dist=sum_dis(cities,i,i+2,i+3,i+1,i+4)
        
        if min_dist>sum_dis(cities,i,i+3,i+1,i+2,i+4):
            P1,P2,P3=i+3,i+1,i+2
            # print(i+1,i+2,i+3,' -> ',P1,P2,P3,min_dist,sum_dis(cities,i,i+3,i+1,i+2,i+4))
            min_dist=sum_dis(cities,i,i+3,i+1,i+2,i+4)
       
        if min_dist>sum_dis(cities,i,i+3,i+2,i+1,i+4):
            P1,P2,P3=i+3,i+2,i+1
            # print(i+1,i+2,i+3,' -> ',P1,P2,P3,min_dist,sum_dis(cities,i,i+3,i+2,i+1,i+4))
            min_dist=sum_dis(cities,i,i+3,i+2,i+1,i+4)

        new_tour[(i+1)%N],new_tour[(i+2)%N],new_tour[(i+3)%N]=new_tour[P1%N],new_tour[P2%N],new_tour[P3%N]
        i += 3
    # print(new_tour)
        # print()
    return new_tour


def search_best_route(cities):
    N = len(cities)
    sum_dis=10**9
    for _ in range(30):
        current_city = random.randint(0, N-1)
        tour = solve(cities,current_city) # greedy
        tour = three_opt(cities,tour)
        tour = solve_cross(cities,tour) # 交差を解除
        if sum_dis>calcurate_total_distance(cities,tour):
            ans=tour
            sum_dis=calcurate_total_distance(cities,tour)
    return ans


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities=read_input(sys.argv[1])
    print_tour(search_best_route(cities))

