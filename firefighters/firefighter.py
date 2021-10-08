from abc import ABC, abstractmethod

from firefighters.city_node import CityNode
from firefighters.city import City

from typing import List

from firefighters.navigation import Navigation


class FireFighter(ABC):

    @property
    @abstractmethod
    def location(self) -> CityNode:
        """
        Get the firefighter's current location. Initially, the firefighter should be at the FireStation

        :return: CityNode representing the firefighter's current location
        """
        pass

    @property
    @abstractmethod
    def distance_traveled(self) -> int:
        """
        Get the total distance traveled by this firefighter. Distances should be represented using TaxiCab
        Geometry: https://en.wikipedia.org/wiki/Taxicab_geometry

        :return: the total distance traveled by this firefighter
        """
        pass


class FireFighterImpl(FireFighter):
    def __init__(self, city: City):
        self._city = city
        self._location = CityNode(city.fire_station.location.x_coordinate, city.fire_station.location.y_coordinate)
        self.traversed_path = []

    @property
    def location(self) -> CityNode:
        return self._location

    @location.setter
    def location(self, location: CityNode):
        self._location = location

    @property
    def distance_traveled(self) -> int:
        return sum([1] * len(self.traversed_path))

    def travel(self, path: List[CityNode]) -> None:
        """
        Move the firefighter through a path in the city to a building on fire.

        :param path: Ordered list of locations to reach a destination
        """
        for location in path:
            self.location = location
            self.traversed_path.append(location)

    def extinguish_fire(self, victim_location: CityNode) -> None:
        """
        Extinguishes a fire at the victim_location in the firefighters current city

        :param victim_location: Location to extinguish a fire
        """
        navigation = Navigation(self._city)
        route = navigation.get_route(self._city, self._location, victim_location)
        self.travel(route)
        self._city.get_building_from_node(self.location).extinguish_fire()
