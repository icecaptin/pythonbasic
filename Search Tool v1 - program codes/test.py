import sys

input = sys.stdin.readline
n = int(input())
cities = [list(map(int, input().split())) for _ in range(n)]
# (1 << N) - 1 ==> 'N개의 비트를 모두 켠다'와 같음
VISITED_ALL = (1 << n) - 1

# DP를 위한 캐시 초기화
# 도시의 개수(N)에 대응하고 (1 << N)을 통해 방문한 도시 집합(visited)에 대응
# cache[N][visited] : N번 -> visited에서 방문 X한 도시 -> 0번 도시(시작 도시) 경로 저장한다고 생각하면 쉬움
cache = [[None] * (1 << n) for _ in range(n)]
INF = float('inf')
idx = 1


def find_path(last, visited):
    if visited == VISITED_ALL:
        # 마지막 방문 도시 출발 - 0번째 (출발 도시) 사이에 경로가 존재하면
        # 경로 값을 반환.
        # 경로가 존재하지 않는다면 무한값을 반환해서 답이 안되게 한다.

        return cities[last][0] or INF  # 마지막 도착 도시에서 출발 도시인 0으로 가야됨.(문제 조건)

    # cache 값이 None이 아니라는 것은 last와 visited의 계산이 이미 수행됬고,
    # 지금은 중복호출 되었다는 뜻임 -> 다시 계산하지 않고 값만 바로 반환하도록
    # 중복계산을 없애 효율성 높임 --> DP 사용하는 이유
    if cache[last][visited] is not None:
        return cache[last][visited]

    tmp = INF
    for city in range(n):
        if visited & (1 << city) == 0 and cities[last][city] != 0:
            tmp = min(tmp, find_path(city, visited | (1 << city)) + cities[last][city])
    cache[last][visited] = tmp
    return tmp


print(find_path(0, 1 << 0))