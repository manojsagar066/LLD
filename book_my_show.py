# design book-my-show style movie ticket system
# user can search for movies, select theatres, book tickets
# Entities - User, Movie, Theatre, Ticket, Payment

from datetime import datetime
from enum import Enum
import uuid
from typing import List, Dict, Union


class SeatType(Enum):
    LOWER = 1
    MIDDLE = 2
    HIGH = 3


class User:
    def __init__(self, user_id: str, name: str, email: str, phone: str):
        self._user_id = user_id
        self.name = name
        self._email = email
        self._phone = phone
        self._tickets = []

    def add_ticket(self, ticket):
        self._tickets.append(ticket)

    @property
    def tickets(self):
        return self._tickets


class Ticket:
    def __init__(self, ticket_id: str, total_seats: int, total_price: int, show_time: datetime):
        self.__ticket_id = ticket_id
        self._total_seats = total_seats
        self.total_price = total_price
        self._show_time = show_time
        self._date_of_booking = datetime.now()


class Theatre:
    def __init__(self, theatre_id: str, name: str, address: str, low: int, middle: int, high: int):
        self._theatre_id = theatre_id
        self.name = name
        self.address = address
        self.seats = {
            "low": low,
            "middle": middle,
            "high": high
        }


class SeatInfo:
    def __init__(self, theatre):
        self.lower_seats = theatre.seats.get("low")
        self.middle_seats = theatre.seats.get("middle")
        self.higher_seats = theatre.seats.get("high")


class SeatBookingEngine:
    @staticmethod
    def get_available_seats(seat_type: SeatType, seat_info: SeatInfo):
        if seat_type == SeatType.LOWER:
            return seat_info.lower_seats
        elif seat_type == SeatType.MIDDLE:
            return seat_info.middle_seats
        else:
            return seat_info.higher_seats

    @staticmethod
    def book_seats(seat_type: SeatType, seat_info: SeatInfo, seats_required: int):
        if seat_type == SeatType.LOWER:
            seat_info.lower_seats -= seats_required
        elif seat_type == SeatType.MIDDLE:
            seat_info.middle_seats -= seats_required
        else:
            seat_info.higher_seats -= seats_required


class ShowPrice:
    def __init__(self, lower_seat_price, middle_seat_price, higher_seat_price):
        self.lower_seat_price = lower_seat_price
        self.middle_seat_price = middle_seat_price
        self.higher_seat_price = higher_seat_price

    def get_per_seat_price(self, seat_type: SeatType):
        if seat_type == SeatType.LOWER:
            return self.lower_seat_price
        elif seat_type == SeatType.MIDDLE:
            return self.middle_seat_price
        else:
            return self.higher_seat_price


class Show:
    def __init__(self, show_id, movie_name: str, show_time: datetime, show_price: ShowPrice, theatre: Theatre):
        self.show_id = show_id
        self.movie_name = movie_name
        self.theatre_name = theatre.name
        self.show_time = show_time
        self.show_price = show_price
        self.seat_info = SeatInfo(theatre)
        self.seat_booking_engine = SeatBookingEngine()

    def book_show(self, seat_type: SeatType, seats_required: int) -> Union[Ticket, None]:
        available_seats = self.seat_booking_engine.get_available_seats(seat_type, self.seat_info)
        if available_seats >= seats_required:
            per_seat_price = self.show_price.get_per_seat_price(seat_type)
            total_price = per_seat_price * seats_required
            ticket = Ticket(str(uuid.uuid4()), seats_required, total_price, self.show_time)
            self.seat_booking_engine.book_seats(seat_type, self.seat_info, seats_required)
            return ticket
        return None


class Movie:
    def __init__(self, movie_id: str, name: str, genre: str):
        self.movie_id = movie_id
        self.name = name
        self.genre = genre


class Catalog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.movies = {}  # movie_name, info
            cls.shows = {}  # show_id, show
        return cls._instance

    def add_movies(self, movie: Movie):
        self.movies[movie.name] = movie

    def add_shows(self, show: Show):
        self.shows[show.show_id] = show

    def get_movies(self) -> Dict[str, Movie]:
        return self.movies

    def search_shows(self, movie_name: str) -> List[Show]:
        shows = []
        for show_id, show in self.shows.items():
            if show.movie_name == movie_name:
                shows.append(show)
        return shows


class BookingEngine:
    def __init__(self):
        self.theatres = []
        self.catalog = Catalog()

    def add_theatre(self, theatre: Theatre):
        self.theatres.append(theatre)

    def add_movie(self, movie: Movie):
        self.catalog.add_movies(movie)

    def add_shows(self, show: Show):
        self.catalog.add_shows(show)

    def get_shows(self, movie_name: str) -> List[Show]:
        return self.catalog.search_shows(movie_name)

    def get_movies(self):
        return self.catalog.get_movies()

    @staticmethod
    def book_seats(user: User, seat_type: SeatType, show: Show, seats_required: int) -> Union[Ticket, None]:
        ticket = show.book_show(seat_type, seats_required)
        if ticket:
            user.add_ticket(ticket)
            return ticket
        else:
            return None


if __name__ == "__main__":
    user = User(user_id="1", name="Manoj", email="b.b.manoj28@gmail.com", phone="12345678")
    theatre1 = Theatre(theatre_id="1", name="PVR BR", address="Bannerghatta road", low=30, middle=20, high=10)
    theatre2 = Theatre(theatre_id="2", name="PVR JP", address="JP Nagar", low=30, middle=20, high=10)

    avengers_movie = Movie(movie_id="1", name="Avengers", genre="Comic")
    kgf_movie = Movie(movie_id="2", name="KGF", genre="Thriller")

    show_price1 = ShowPrice(200, 300, 500)
    show_price2 = ShowPrice(250, 350, 550)

    show1 = Show(show_id="1", movie_name=avengers_movie.name, show_time=datetime.now(), show_price=show_price1,
                 theatre=theatre1)
    show2 = Show(show_id="2", movie_name=kgf_movie.name, show_time=datetime.now(), show_price=show_price2,
                 theatre=theatre2)

    booking_engine = BookingEngine()
    booking_engine.add_theatre(theatre1)
    booking_engine.add_theatre(theatre2)

    booking_engine.add_movie(avengers_movie)
    booking_engine.add_movie(kgf_movie)

    booking_engine.add_shows(show1)
    booking_engine.add_shows(show2)

    movies = booking_engine.get_movies()
    shows = booking_engine.get_shows(kgf_movie.name)

    ticket = booking_engine.book_seats(user=user, seat_type=SeatType.HIGH, show=shows[0], seats_required=3)
    print(ticket.total_price)


