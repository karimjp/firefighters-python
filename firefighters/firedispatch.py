from abc import ABC, abstractmethod
from typing import List

from firefighters.city import City
from firefighters.city_node import CityNode
from firefighters.firefighter import FireFighter


class FireDispatch(ABC):

    @property
    @abstractmethod
    def firefighters(self) -> List[FireFighter]:
        """
        Get the list of firefighters

        :return: List of hired firefighters
        """
        pass

    @firefighters.setter
    @abstractmethod
    def firefighters(self, num_firefighters: int) -> None:
        """
        Hires a number of firefighters

        :param num_firefighters:
        """
        pass

    @abstractmethod
    def dispatch_firefighters(self, burning_buildings: List[CityNode]):
        """
        The FireDispatch will be notified of burning buildings via this method. It will then dispatch the
        firefighters and extinguish the fires. We want to optimize for total distance traveled by
        all firefighters.

        :param burning_buildings: list of locations with burning buildings
        """
        pass


class FireDispatchImpl(FireDispatch):

    def __init__(self, city: City):
        self._city = city
        self._firefighters = []

    @property
    def firefighters(self) -> List[FireFighter]:
        return self._firefighters

    @firefighters.setter
    def firefighters(self, num_firefighters: int) -> None:
        from firefighters.firefighter import FireFighterImpl
        for num_firefighter in range(0, num_firefighters):
            self._firefighters.append(FireFighterImpl(self._city))

    def dispatch_firefighters(self, burning_buildings: List[CityNode]):
        for burning_building in burning_buildings:
            firefighter = self._firefighters.pop(0)
            firefighter.extinguish_fire(burning_building)
            self._firefighters.append(firefighter)
