from enum import Enum
from typing import List, Union
from datetime import datetime
import uuid


class VehicleType(Enum):
    Bike = 1
    Car = 2
    Truck = 3


class Vehicle:
    def __init__(self, license_number: str, vehicle_type: VehicleType):
        self.license_number = license_number
        self.vehicle_type = vehicle_type


class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: VehicleType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_free = True
        self.vehicle = None

    def assign_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.is_free = False

    def remove_vehicle(self):
        self.vehicle = None
        self.is_free = True


class Floor:
    def __init__(self, floor_number: int):
        self.floor_number = floor_number
        self.spots: List[ParkingSpot] = []

    def add_spot(self, spot: ParkingSpot):
        self.spots.append(spot)

    def check_availability(self, vehicle_type: VehicleType) -> Union[ParkingSpot, None]:
        for spot in self.spots:
            if spot.spot_type == vehicle_type:
                return spot
        return None


class Ticket:
    def __init__(self, ticket_id: str, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = ticket_id
        self.entry_time = datetime.now()
        self.vehicle = vehicle
        self.exit_time = None
        self.spot = spot

    def set_exit_time(self):
        self.exit_time = datetime.now()


class FareCalculator:
    price_per_hour_map = {
        "Bike": 20,
        "Car": 30,
        "Truck": 50
    }
    @staticmethod
    def calculate_fare(total_duration_hours: int, vehicle_type: VehicleType):
        price_per_hour = FareCalculator.price_per_hour_map[vehicle_type.name]
        return total_duration_hours * price_per_hour


class ParkingLot:
    def __init__(self):
        self.floors = []

    def add_floor(self, floor: Floor):
        self.floors.append(floor)

    def assign_spot(self, vehicle: Vehicle) -> Union[Ticket, None]:
        for floor in self.floors:
            spot = floor.check_availability(vehicle.vehicle_type)
            if not spot:
                continue
            spot.assign_vehicle(vehicle)
            ticket = Ticket(str(uuid.uuid4()), vehicle, spot)
            return ticket

    @staticmethod
    def free_spot(ticket: Ticket):
        ticket.spot.remove_vehicle()
        ticket.set_exit_time()
        total_duration = (ticket.exit_time - ticket.entry_time).total_seconds()/3600
        total_duration_hours = max(1, total_duration)
        fare = FareCalculator.calculate_fare(total_duration_hours, ticket.vehicle.vehicle_type)
        print(f"Total amount: {fare}")


spot1 = ParkingSpot("1", VehicleType.Bike)
spot2 = ParkingSpot("2", VehicleType.Car)

floor1 = Floor(1)

floor1.add_spot(spot1)
floor1.add_spot(spot2)

parking_lot = ParkingLot()
parking_lot.add_floor(floor1)

vehicle_1 = Vehicle("KA-05-LY-2101", VehicleType.Bike)
entry_ticket = parking_lot.assign_spot(vehicle_1)
if entry_ticket:
    parking_lot.free_spot(entry_ticket)
