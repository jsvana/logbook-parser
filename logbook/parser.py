import datetime
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Type,
)


from dateutil.relativedelta import relativedelta


def optional(val: Any, type: Type, default: Any):
    return type(val) if val else default


def bool_str(val: str) -> bool:
    return val == 'true'


class InvalidLogbookFileError(Exception):

    """Raised when we're passed an invalid logbook file"""


class GearType(Enum):

    FIXED_TAILWHEEL = 'fixed_tailwheel'
    FIXED_TRICYCLE = 'fixed_tricycle'
    RETRACTABLE_TAILWHEEL = 'retractable_tailwheel'
    RETRACTABLE_TRICYCLE = 'retractable_tricycle'


class EngineType(Enum):

    PISTON = 'Piston'
    RADIAL = 'Radial'


class Aircraft:

    def __init__(
        self,
        id: str,
        type_code: str,
        year: int,
        make: str,
        model: str,
        category: str,
        aircraft_class: str,
        gear_type: GearType,
        engine_type: EngineType,
        is_complex: bool,
        is_high_performance: bool,
        is_pressurized: bool,
    ) -> None:
        self.id = id
        self.type_code = type_code
        self.year = year
        self.make = make
        self.model = model
        self.category = category
        self.aircraft_class = aircraft_class
        self.gear_type = gear_type
        self.engine_type = engine_type
        self.is_complex = is_complex
        self.is_high_performance = is_high_performance
        self.is_pressurized = is_pressurized

    @classmethod
    def from_row(cls, row: List[str]) -> 'Aircraft':
        if len(row) != 50:
            raise InvalidLogbookFileError(
                '{} is not a valid aircraft row'.format(','.join(row))
            )

        return Aircraft(
            row[0],
            row[1],
            optional(row[2], int, 0),
            row[3],
            row[4],
            row[5],
            row[6],
            optional(row[7], GearType, None),
            optional(row[8], EngineType, None),
            bool_str(row[9]),
            bool_str(row[10]),
            bool_str(row[11]),
        )


class Approach:

    pass


class PersonType(Enum):

    PASSENGER = 'Passenger'


class Person:

    def __init__(self, name: str, type: PersonType) -> None:
        self.name = name
        self.type = type

    @classmethod
    def from_str(cls, person_str: str) -> List['Person']:
        if ';' not in person_str:
            raise InvalidLogbookFileError(
                '{} is not a valid person entry'.format(person_str)
            )

        parts = person_str.split(';')
        if len(parts) != 3:
            raise InvalidLogbookFileError(
                '{} is not a valid person entry'.format(person_str)
            )

        return Person(parts[0], PersonType(parts[1]))


class Flight:

    def __init__(
        self,
        date: datetime.date,
        aircraft_id: str,
        from_airport: str,
        to_airport: str,
        route: Optional[str],
        time_out: Optional[datetime.time],
        time_in: Optional[datetime.time],
        on_duty: Optional[datetime.time],
        off_duty: Optional[datetime.time],
        total_time: float,
        pic: float,
        sic: float,
        night: float,
        solo: float,
        cross_country: float,
        distance: float,
        day_takeoffs: int,
        day_landings_full_stop: int,
        night_takeoffs: int,
        night_landings_full_stop: int,
        all_landings: int,
        actual_instrument: float,
        simulated_instrument: float,
        hobbs_start: Optional[float],
        hobbs_end: Optional[float],
        tach_start: Optional[float],
        tach_end: Optional[float],
        holds: int,
        approaches: List[Approach],
        dual_given: float,
        dual_received: float,
        simulated_flight: float,
        ground_training: float,
        instructor_name: Optional[str],
        instructor_comments: Optional[str],
        people: List[Person],
        flight_review: bool,
        checkride: bool,
        ipc: bool,
        comments: str,
    ) -> None:
        self.date = date
        self.aircraft_id = aircraft_id
        self.from_airport = from_airport
        self.to_airport = to_airport
        self.route = route
        self.time_out = time_out
        self.time_in = time_in
        self.on_duty = on_duty
        self.off_duty = off_duty
        self.total_time = total_time
        self.pic = pic
        self.sic = sic
        self.night = night
        self.solo = solo
        self.cross_country = cross_country
        self.distance = distance
        self.day_takeoffs = day_takeoffs
        self.day_landings_full_stop = day_landings_full_stop
        self.night_takeoffs = night_takeoffs
        self.night_landings_full_stop = night_landings_full_stop
        self.all_landings = all_landings
        self.actual_instrument = actual_instrument
        self.simulated_instrument = simulated_instrument
        self.hobbs_start = hobbs_start
        self.hobbs_end = hobbs_end
        self.tach_start = tach_start
        self.tach_end = tach_end
        self.holds = holds
        self.approaches = approaches
        self.dual_given = dual_given
        self.dual_received = dual_received
        self.simulated_flight = simulated_flight
        self.ground_training = ground_training
        self.instructor_name = instructor_name
        self.instructor_comments = instructor_comments
        self.people = people
        self.flight_review = flight_review
        self.checkride = checkride
        self.ipc = ipc
        self.comments = comments

    @classmethod
    def from_row(cls, row: List[str]) -> 'Flight':
        if len(row) != 50:
            raise InvalidLogbookFileError(
                '{} is not a valid flight row'.format(','.join(row))
            )

        return Flight(
            datetime.datetime.strptime(row[0], '%Y-%m-%d').date(),
            row[1],
            row[2],
            row[3],
            row[4],

            # TODO(jsvana): parse these properly
            row[5],
            row[6],
            row[7],
            row[8],

            optional(row[9], float, 0.0),
            optional(row[10], float, 0.0),
            optional(row[11], float, 0.0),
            optional(row[12], float, 0.0),
            optional(row[13], float, 0.0),
            optional(row[14], float, 0.0),
            optional(row[15], float, 0.0),
            optional(row[16], int, 0),
            optional(row[17], int, 0),
            optional(row[18], int, 0),
            optional(row[19], int, 0),
            optional(row[20], int, 0),
            optional(row[21], float, 0.0),
            optional(row[22], float, 0.0),
            optional(row[23], float, 0.0),
            optional(row[24], float, 0.0),
            optional(row[25], float, 0.0),
            optional(row[26], float, 0.0),
            optional(row[27], int, 0),

            # TODO(jsvana): parse approaches
            [],

            optional(row[34], float, 0.0),
            optional(row[35], float, 0.0),
            optional(row[36], float, 0.0),
            optional(row[37], float, 0.0),
            row[38],
            row[39],

            # TODO(jsvana): parse people
            [Person.from_str(row[40 + i]) for i in range(6) if row[40 + i]],

            bool_str(row[46]),
            bool_str(row[47]),
            bool_str(row[48]),
            bool_str(row[49]),
        )


class Logbook:

    MAGIC_STR = 'ForeFlight Logbook Import'

    def __init__(self, path: Path) -> None:
        if not path.is_file():
            raise InvalidLogbookFileError(
                '{} is not a valid file'.format(path)
            )

        self.path = path
        self.aircraft: Dict[str, Aircraft] = {}
        self.flights: List[Flight] = []
        self.load()

    def load(self):
        with self.path.open() as f:
            lines = [l.strip() for l in f]

        if not lines or ',' not in lines[0] or lines[0].split(',')[0] != self.MAGIC_STR:
            raise InvalidLogbookFileError(
                '{} is not a valid logbook file'.format(self.path)
            )

        if ',' not in lines[2] or lines[2].split(',')[0] != 'Aircraft Table':
            raise InvalidLogbookFileError(
                '{} is not a valid logbook file'.format(self.path)
            )

        idx = 4
        while True:
            parts = lines[idx].split(',')
            if not parts[0]:
                break

            plane = Aircraft.from_row(parts)
            self.aircraft[plane.id] = plane
            idx += 1

        idx += 1

        if ',' not in lines[idx] or lines[idx].split(',')[0] != 'Flights Table':
            raise InvalidLogbookFileError(
                '{} is not a valid logbook file'.format(self.path)
            )

        idx += 2
        while True:
            if idx >= len(lines):
                break

            parts = lines[idx].split(',')
            if not parts[0]:
                break

            self.flights.append(Flight.from_row(parts))
            idx += 1

        self.flights.sort(key=lambda f: f.date, reverse=True)

    def flights_in_last(self, duration: datetime.timedelta) -> Iterator[Flight]:
        today = datetime.date.today()
        for flight in self.flights:
            if today - flight.date <= duration:
                yield flight

    def hours_in_last(self, duration: datetime.timedelta) -> float:
        return sum(f.total_time for f in self.flights_in_last(duration))

    @property
    def total_time(self):
        return sum(f.total_time for f in self.flights)

    def filter_category_class(self, flights, category_class):
        for flight in flights:
            if self.aircraft[flight.aircraft_id].aircraft_class == category_class:
                yield flight

    def filter_gear_types(self, flights, gear_types):
        for flight in flights:
            if self.aircraft[flight.aircraft_id].gear_type in gear_types:
                yield flight

    def general_currency_expiration(self, category_class):
        takeoffs = 0
        landings = 0
        flights = self.flights_in_last(datetime.timedelta(days=90))
        flights = self.filter_category_class(flights, category_class)
        for flight in flights:
            takeoffs += flight.day_takeoffs
            takeoffs += flight.night_takeoffs
            landings += flight.all_landings

            if takeoffs >= 3 and landings >= 3:
                expiration = flight.date + datetime.timedelta(days=90)
                return (expiration, (expiration - datetime.date.today()).days + 1)

        return (None, 0)

    def night_currency_expiration(self, category_class):
        takeoffs = 0
        landings = 0
        flights = self.flights_in_last(datetime.timedelta(days=90))
        flights = self.filter_category_class(flights, category_class)
        for flight in flights:
            takeoffs += flight.night_takeoffs
            landings += flight.night_landings_full_stop

            if takeoffs >= 3 and landings >= 3:
                expiration = flight.date + datetime.timedelta(days=90)
                return (expiration, (expiration - datetime.date.today()).days + 1)

        return ('not current', 0)

    def tailwheel_currency_expiration(self, category_class):
        takeoffs = 0
        landings = 0
        flights = self.flights_in_last(datetime.timedelta(days=90))
        flights = self.filter_category_class(flights, category_class)
        flights = self.filter_gear_types(
            flights,
            [GearType.FIXED_TAILWHEEL, GearType.RETRACTABLE_TAILWHEEL],
        )
        for flight in flights:
            takeoffs += flight.day_takeoffs
            takeoffs += flight.night_takeoffs
            landings += flight.day_landings_full_stop
            landings += flight.night_landings_full_stop

            if takeoffs >= 3 and landings >= 3:
                expiration = flight.date + datetime.timedelta(days=90)
                return (expiration, (expiration - datetime.date.today()).days + 1)

        return ('not current', 0)

    def bfr_currency_expiration(self):
        for flight in self.flights_in_last(datetime.timedelta(days=730)):
            if flight.flight_review or flight.checkride:
                expiration = flight.date + datetime.timedelta(days=730)
                expiration -= datetime.timedelta(days=expiration.day-1)
                expiration += relativedelta(months=1)
                expiration -= relativedelta(days=1)
                return (expiration, (expiration - datetime.date.today()).days + 1)

        return ('not current', 0)
