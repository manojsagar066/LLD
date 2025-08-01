# parking lot:
# can have multiple floors
# each floor will have multiple slots for vehicles
# parking lot should support different vehicle types (bike, car, truck)
# generate ticket before parking will have entry time stamp
# different pricing strategy for different vehicle types
from enum import Enum
from dataclasses import dataclass
import uuid
from datetime import datetime


class VehicleType(Enum):
    Bike = 1
    Car = 2
    Truck = 3


class Vehicle:
    def __init__(self, license_number, vehicle_type: VehicleType):
        self.license_number = license_number
        self.vehicle_type = vehicle_type


class Ticket:
    def __init__(self, id, vehicle: Vehicle, spot):
        self.ticket_id = id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time = None

    def set_exit_time(self):
        self.exit_time = datetime.now()


class ParkingSpot:
    def __init__(self, spot_id, spot_type: VehicleType):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_free = True
        self.vehicle = None

    def assign_vehicle(self, vehicle):
        self.vehicle = vehicle
        self.is_free = False

    def remove_vehicle(self):
        self.is_free = True
        self.vehicle = None


class ParkingFloor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.spots = []

    def add_spot(self, spot):
        self.spots.append(spot)

    def get_available_spot(self, vehicle: Vehicle):
        for spot in self.spots:
            if spot.is_free and spot.spot_type == vehicle.vehicle_type:
                return spot
        return None


class ParkingLot:
    def __init__(self):
        self.floors = []

    def add_floor(self, parking_floor):
        self.floors.append(parking_floor)

    def assign_spot(self, vehicle: Vehicle):
        for floor in self.floors:
            spot = floor.get_available_spot(vehicle)
            if spot:
                spot.assign_vehicle(vehicle)
                ticket_id = str(uuid.uuid4())
                ticket = Ticket(ticket_id, vehicle, spot)
                return ticket
        raise Exception("Spots not available")

    @staticmethod
    def release_spot(ticket):
        ticket.set_exit_time()
        fee = FareCalculator.calculate_fare(ticket)
        ticket.spot.remove_vehicle()
        return fee


class FareCalculator:
    rate_per_hour = {
        VehicleType.Bike: 20,
        VehicleType.Car: 50,
        VehicleType.Truck: 70
    }
    @staticmethod
    def calculate_fare(ticket: Ticket):
        entry_time = ticket.entry_time
        exit_time = ticket.exit_time
        total_duration = (exit_time - entry_time).total_seconds()/3600
        hourly_rate = FareCalculator.rate_per_hour[ticket.vehicle.vehicle_type]
        return max(1, int(total_duration))*hourly_rate


lot = ParkingLot()
floor1 = ParkingFloor(1)
spot1 = ParkingSpot(1, VehicleType.Bike)
spot2 = ParkingSpot(2, VehicleType.Car)
floor1.add_spot(spot1)
floor1.add_spot(spot2)
lot.add_floor(floor1)

vehicle = Vehicle("KA-05-LY-2101", VehicleType.Bike)
try:
    ticket = lot.assign_spot(vehicle)
    lot.release_spot(ticket)
except Exception as e:
    print(repr(e))
