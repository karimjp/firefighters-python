from firefighters.city import City
from firefighters.city import CityNode
from typing import List
from queue import Queue


class Navigation:
    """Calculates the shortest path from a source to a destination location"""

    def __init__(self, city: City):
        self.travel_record = TravelRecord(city)

    def __get_shortest_path(self, destination_location: CityNode) -> List[CityNode]:
        """
        Generates a shortest path representation from the travel record.

        :param destination_location

        :return: a list of CityNode objects that represents the shortest path
        """
        ordered_path = []
        current_node = self.travel_record.read_graph_node(destination_location)
        while current_node.parent and current_node.distance != 0:
            ordered_path.insert(0, current_node)
            current_node = self.travel_record.read_graph_node(current_node.parent)

        return ordered_path

    def get_route(self, city: City, source_location: CityNode, destination_location: CityNode) -> List[CityNode]:
        """
        Traverses a city from a source to a destination location using BFS in order to find the shortest path.

        :param city
        :param source_location
        :param destination_location

        :return: a list of CityNode objects that represents the shortest path
        """
        arrived = False
        q = Queue()
        q.put(source_location)
        # set source node (distance, parent) to 0,None
        self.travel_record.update_graph_node(source_location, 0, None)
        while not q.empty() and not arrived:
            parent = q.get()
            for neighbor in city.get_neighbor_locations(self.travel_record.read_graph_node(parent)):
                if self.travel_record.is_graph_node_unvisited(neighbor):
                    self.travel_record.update_graph_node(neighbor,
                                                         self.travel_record.read_graph_node(parent).distance + 1,
                                                         parent)
                    if neighbor == destination_location:
                        arrived = True
                        break
                    q.put(neighbor)
        return self.__get_shortest_path(destination_location)


class CityGraphNode(CityNode):
    """An extended representation of a CityNode to store distance and parent state required by BFS."""

    def __init__(self, x_coordinate, y_coordinate, distance=-1, parent=None):
        super().__init__(x_coordinate, y_coordinate)
        self._distance = distance
        self._parent = parent

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, distance):
        self._distance = distance

    @property
    def parent(self):
        return self._parent;

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def __str__(self) -> str:
        return f"CityNode{{x={self._x_coordinate}, y={self._y_coordinate}, d={self.distance}, p={self.parent}}}"


class TravelRecord:
    """A city like representation to log BFS traversal state in a city"""
    NOT_VISITED = -1

    def __init__(self, city: City):
        self._data = [[CityGraphNode(x, y, TravelRecord.NOT_VISITED, None) for y in range(0, city.y_dimension)] for x in
                      range(0, city.x_dimension)]

    def read_graph_node(self, location: CityNode):
        return self._data[location.x_coordinate][location.y_coordinate]

    def update_graph_node(self, location: CityNode, distance, parent):
        self._data[location.x_coordinate][location.y_coordinate].distance = distance
        self._data[location.x_coordinate][location.y_coordinate].parent = parent

    def is_graph_node_unvisited(self, location: CityNode):
        return self.read_graph_node(location).distance == TravelRecord.NOT_VISITED

    def __str__(self) -> str:
        formatted = "\n"
        for row in self._data:
            formatted += ",".join([str(item) for item in row]) + "\n"

        return f"TravelRecord[{formatted}]"
