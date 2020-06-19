N=5
print([(start, start + length)
            for length in range(N, 1, -1)
            for start in range(N - length + 1)]
)
l=[]
for i in range(N):
    for j in range(i+2,N+1):
        l.append((i,j%N))
print(l)