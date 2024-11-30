import heapq
from itertools import permutations
import src.objects.DatabaseHandler 
import json

def dijkstra(graph, start, end=None):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:
            break
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def readFile(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def readFromFile(filename,startDate, endDate):
    with open(filename, "r", encoding="utf-8") as file:
        query = file.read()
    
    return query.format(
        START_DATE=startDate
        ,END_DATE=endDate
    )

def shortest_path_with_mandatory_points(graph, start, end, mandatory_points):
    points = [start] + mandatory_points + [end]
    all_distances = {}
    
    for point in points:
        all_distances[point] = dijkstra(graph, point)
    
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


if __name__ == '__main__':

    config = json.loads(readFile('src/config.json'))
    db = src.objects.DatabaseHandler.init_db(config)
    query = readFromFile('BestPath.sql','2023-02-01','2030-02-28')
    weights = src.objects.DatabaseHandler.execute_qry_and_fetch_all_records(db, 'Run Points', query)
    graph = {}

    for dict in weights:
        if dict['origin_city'] not in graph:
            graph[dict['origin_city']] = {}
        
        graph[dict['origin_city']][dict['destiny_city']] = dict['price']

    print(json.dumps(graph,indent=4))

    origin = 'Sao Paulo'
    end = 'Sao Paulo'
    mandatory_points = ['Los Angeles', 'Mexico City', 'Miami', 'Vancouver']

    path, distance = shortest_path_with_mandatory_points(graph, origin, end, mandatory_points)

    print(f"Caminho mais curto que passa por {mandatory_points} e termina em {end}: {path}")
    print(f"Preço total: {distance}")
