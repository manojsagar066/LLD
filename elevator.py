# Design elevator system
# Entities - Elevator, Scheduler, Elevator system (manages elevators)

from enum import Enum
import heapq


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class State(Enum):
    MOVING = 1
    IDLE = 2
    MAINTENANCE = 3


class RequestType(Enum):
    INTERNAL = 1
    EXTERNAL = 2


class Request:
    def __init__(self, floor: int, direction: Direction, request_type: RequestType):
        self.floor = floor
        self.direction = direction
        self.request_type = request_type


class Elevator:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.current_state = State.IDLE
        self.direction = Direction.IDLE
        self.requests = []

    def add_request(self, request: Request):
        heapq.heappush(self.requests, request.floor)

    def move(self):
        if not self.requests:
            self.current_state = State.IDLE
            self.direction = Direction.IDLE
            return

        next_floor = heapq.heappop(self.requests)
        # set direction
        if next_floor > self.current_floor:
            self.direction = Direction.UP
        elif next_floor < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

        # set current floor
        self.current_floor = next_floor
        print(f"Elevator {self.id} moved to floor {next_floor}")


class Scheduler:
    @staticmethod
    def assign(elevators, request: Request):
        best_elevator = None
        min_distance = float("inf")
        for elevator in elevators:
            if elevator.current_state == State.IDLE:
                distance = abs(request.floor - elevator.current_floor)
                if distance < min_distance:
                    min_distance = distance
                    best_elevator = elevator
        if best_elevator:
            best_elevator.add_request(request)
            best_elevator.current_state = State.MOVING


class ElevatorSystem:
    def __init__(self, num_elevators: int):
        self.elevators = [Elevator(i) for i in range(num_elevators)]
        self.scheduler = Scheduler()

    def handle_request(self, floor: int, direction: Direction):
        request = Request(floor, direction, RequestType.EXTERNAL)
        self.scheduler.assign(self.elevators, request)

    def step(self):
        for elevator in self.elevators:
            elevator.move()


system = ElevatorSystem(3)
system.handle_request(5, Direction.UP)
system.handle_request(2, Direction.DOWN)

system.step()
system.step()
