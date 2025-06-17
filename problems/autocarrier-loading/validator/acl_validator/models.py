from pydantic import BaseModel, model_validator
from typing import Dict, List, Optional, Self


class Operation(BaseModel):
    load: Optional[List[str]] = []
    unload : Optional[List[str]] = []

    @model_validator(mode='before')
    def validate_operation(cls, values: Dict) -> Dict:
        if not (values.get('load') or values.get('unload')):
            raise ValueError("An operation must have either 'load' or 'unload' or both defined.")
        return values

class Vehicle(BaseModel):
    id: str
    dimension: int

class Deck(BaseModel):
    id: str
    capacity: int
    access_via: Optional[List[List[str]]] = None


class Transporter(BaseModel):
    total_capacity: int
    decks: Dict[str, Deck]


class AutocarrierLoadingProblem(BaseModel):
    route: List[Operation]
    vehicles: Dict[str, Vehicle]
    transporter: Transporter

    @model_validator(mode='before')
    def populate_ids(cls, values: Dict) -> Dict:
        if 'vehicles' in values:
            # Transform vehicles dict to include IDs
            vehicles_with_ids = {}
            for vehicle_id, vehicle_data in values['vehicles'].items():
                # Add the vehicle ID to the vehicle data
                vehicle_data_with_id = {**vehicle_data, 'id': vehicle_id}
                vehicles_with_ids[vehicle_id] = vehicle_data_with_id
            values['vehicles'] = vehicles_with_ids
        if 'decks' in values.get('transporter', {}):
            # Transform decks dict to include IDs
            decks_with_ids = {}
            for deck_id, deck_data in values['transporter']['decks'].items():
                # Add the deck ID to the deck data
                deck_data_with_id = {**deck_data, 'id': deck_id}
                decks_with_ids[deck_id] = deck_data_with_id
            values['transporter']['decks'] = decks_with_ids
        return values

class CurrentLoad(BaseModel):    
    decks: Dict[str, List[Vehicle]]
    vehicles: Dict[str, Deck]

class DeckLoad(BaseModel):
    vehicle: str
    deck: str

def suitable_unload_path(current_load: CurrentLoad, unloading : List[str], path : List[str]) -> bool:
    """
    Check if the vehicle can be unloaded from the specified deck.
    This function checks if the vehicle is currently loaded and if the deck has a suitable unloading path.
    :param current_load: The current load of vehicles and decks.
    :param unloading: The list of vehicles to be unloaded.
    :param vehicle: The vehicle to be unloaded.
    :param deck: The deck where the vehicle is to be unloaded.
    :return: True if the vehicle can be unloaded from the deck without moving any other vehicle, False otherwise.
    """
    for step in path:
        if current_load.decks.get(step):
            # Check that all vehicles in the deck are in the unloading list
            if any(vehicle.id not in unloading for vehicle in current_load.decks[step]):
                # If any vehicle in the deck is not being unloaded, we cannot unload the vehicle
                return False
    # If all steps in the path are clear, we can unload the vehicle
    return True

def suitable_load_path(current_load: CurrentLoad, loading : List[str], path : List[str]) -> bool:
    """
    Check if the vehicle can be loaded onto the specified deck.
    This function checks if the deck is not already occupied by another vehicle and if the loading path is clear.
    :param current_load: The current load of vehicles and decks.
    :param loading: The list of vehicles to be loaded.
    :param path: The path to the deck where the vehicle is to be loaded.
    :return: True if the vehicle can be loaded onto the deck, False otherwise.
    """
    for step in path:
        if current_load.decks.get(step):
            # Check that all vehicles in the deck are in the loading list
            if any(vehicle.id not in loading for vehicle in current_load.decks[step]):
                # If any vehicle in the deck is not being loaded, we cannot load the vehicle
                return False
    # If all steps in the path are clear, we can load the vehicle
    return True

class AutocarrierLoadingSolution(BaseModel):
    instance : AutocarrierLoadingProblem
    assigned_decks: List[DeckLoad]
    deck_start_index : int = 0

    def deck_of_vehicle(self, vehicle_id : str) -> Deck:
        """
        Get the deck of each vehicle in the assigned decks.
        """
        for deck_load in self.assigned_decks:
            if deck_load.vehicle == vehicle_id:
                deck = self.instance.transporter.decks.get(deck_load.deck)
                if not deck:
                    raise ValueError(f"Deck {deck_load.deck} not found in the instance transporter decks.")
                return deck
        raise ValueError(f"Vehicle {vehicle_id} not found in the assigned decks.")

    @property
    def route_leg_loads(self) -> List[CurrentLoad]:
        """
        Calculate the current load at each stop in the route.
        This method processes the route operations to determine the load on each deck at each stop.
        :return: A list of CurrentLoad objects representing the load at each stop."""
        # if hasattr(self, '_route_leg_loads'):
        #     return self._route_leg_loads or []
        self._route_leg_loads = []      
        current_load = CurrentLoad(decks={}, vehicles={})
        for stop, operation in enumerate(self.instance.route):
            # first unload 
            for unload in operation.unload or []:
                # find the deck for this unload
                # if the deck is not found, raise an error or handle it
                if unload not in current_load.vehicles:
                    raise ValueError(f"Unload operation for vehicle {unload}, which has not been found in current load at stop {stop} in the route.")
                deck = current_load.vehicles[unload]
                vehicle = current_load.decks.get(deck.id)
                print(f"Unloading vehicle {unload} from deck {deck.id} {vehicle.id}, {current_load.decks}.")
                # check unloading path
                if not all(suitable_unload_path(current_load, operation.unload, path) for path in deck.access_via or []):
                    raise ValueError(f"Vehicle {unload} cannot be unloaded from deck {deck.id} at stop {stop} due to all occupied paths.")
                # remove the vehicle from the current load                    
                del current_load.vehicles[unload]
                del current_load.decks[deck.id]
            
            for load in operation.load or []:
                vehicle = self.instance.vehicles.get(load)                
                if not vehicle:
                    raise ValueError(f"Load operation for vehicle {load} not found in the instance vehicles.")                
                deck = self.deck_of_vehicle(vehicle.id)
                if current_load.decks.get(deck.id):
                    raise ValueError(f"Vehicle {current_load.decks.get(deck.id)} is already loaded on deck {deck.id} at stop {stop}, while trying to load vehicle {vehicle.id}.")
                # check loading path
                if not all(suitable_load_path(current_load, operation.load, path) for path in deck.access_via or []):
                    raise ValueError(f"Vehicle {vehicle.id} cannot be loaded onto deck {deck.id} at stop {stop} due to all occupied paths.")
                # add the vehicle to the current load
                current_load.decks[deck.id] = vehicle
                current_load.vehicles[vehicle.id] = deck
            # After processing the operations, append the current load to the route leg loads
            self._route_leg_loads.append(current_load)
        return self._route_leg_loads

    @model_validator(mode='after')
    def check_capacities(self) -> Self:
        assert self.route_leg_loads is not None, "Route leg loads must be calculated before checking capacities."
        total_capacity = self.instance.transporter.total_capacity
        for stop, current_load in enumerate(self.route_leg_loads):
            for deck_id, vehicle in current_load.decks.items():
                deck = self.instance.transporter.decks.get(deck_id)
                if not deck:
                    raise ValueError(f"Deck {deck_id} not found in the instance transporter decks at stop {stop}.")
                if vehicle.dimension > deck.capacity:
                    raise ValueError(f"Vehicle {vehicle.id} with dimension {vehicle.dimension} exceeds capacity of deck {deck_id} with capacity {deck.capacity} at stop {stop}.")
                total_capacity -= vehicle.dimension
            if total_capacity < 0:
                raise ValueError(f"Total capacity exceeded at stop {stop}.")
        # If all checks pass, return the instance itself
        return self
