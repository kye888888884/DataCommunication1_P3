import math

### n번 시행했을 때 p의 확률의 사건이 k번 이상 발생할 확률
def indep_events(n, p, k):
    return sum([(math.comb(n, i) * p**i * (1-p)**(n-i)) for i in range(n + 1)][k:])

print(indep_events(35, 0.1, 11)) # ~= 0.0004