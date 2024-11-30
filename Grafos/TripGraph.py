from datetime import date,datetime,timedelta
from enum import Enum
from itertools import permutations
import math

class Modes(Enum):
    PRICE = 1
    
class Graph:
    
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertexData = [''] * size

    def addEdge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # For undirected graph

    def addVertexData(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data):
        start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [float('inf')] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size

        for _ in range(self.size):
            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i

            if u is None:
                break

            visited[u] = True

            for v in range(self.size):
                if self.adj_matrix[u][v] != 0 and not visited[v]:
                    alt = distances[u] + self.adj_matrix[u][v]
                    if alt < distances[v]:
                        distances[v] = alt

        return distances
    

def shortestPathWithMandatoryPoints(self, graph, start, end, mandatory_points):
    points = [start] + mandatory_points + [end]
    all_distances = {}
    
    for point in points:
        all_distances[point] = graph.dijkstra(point)
    
    min_distance = float('inf')
    best_path = None
    
    for perm in permutations(mandatory_points):
        current_path = [start] + list(perm) + [end]
        current_distance = 0
        
        for i in range(len(current_path) - 1):
            current_distance += all_distances[current_path[i]][current_path[i+1]]
        
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = current_path
    
    return best_path, min_distance


w = []
origin = 'Sao Paulo'
end = 'Sao Paulo'
mandatory_points = ['Barcelona', 'Paris', 'Luxemburg']
if origin != end:
    points = mandatory_points + [origin,end]
else:
    points = mandatory_points + [origin]

startDateStr = '2025-02-01'
endDateStr = '2025-02-01'
dateFormat = '%Y-%m-%d'
startDate = datetime.strptime(startDateStr,dateFormat)
endDate = datetime.strptime(endDateStr,dateFormat)

dates = []
currDate = datetime.strptime(startDateStr,dateFormat)
while currDate <= endDate:
    dates.append(startDate)
    currDate += timedelta(days=1)

g = Graph(math.pow(len(points),dates))

counter = 0
reverseIndexMap = {}
for dateItem in dates:
    for point in points:
        g.addVertexData(counter,point+dateItem.strftime(dateFormat))
        reverseIndexMap[point+dateItem.strftime(dateFormat)] = counter
        counter = counter + 1

for index, record in enumerate(w):
    g.addEdge(
        reverseIndexMap(record['origin'].astype(str)+record['travel_date'].astype(str))
        ,reverseIndexMap(record['destiny'].astype(str)+record['travel_date'].astype(str))
        ,record['price']
    )

path, distance = shortestPathWithMandatoryPoints(g, origin, end, mandatory_points)
