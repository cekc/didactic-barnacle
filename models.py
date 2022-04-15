import re
from pydantic import BaseModel

time_of_day_regex = r'(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])'
time_of_day_regex_compiled = re.compile(time_of_day_regex)


class TimeOfDay(int):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            pattern=f'^{time_of_day_regex}$',
            # some example postcodes
            examples=['09:00', '16:23'],
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            m = time_of_day_regex_compiled.fullmatch(v)
            if m:
                return cls(int(m.group(1))*60 + int(m.group(2)))
            else:
                raise ValueError('invalid time format')

        elif isinstance(v, int):
            if 0 <= v and v < 1440:
                return cls(v)
            else:
                raise ValueError('invalid time value')

        else:
            raise TypeError('string or int is required')

    def __str__(self):
        return f'{self//60:02d}:{self%60:02d}'

    def __repr__(self):
        return f'TimeOfDay({self.__str__})'


class Flight(BaseModel):
    id: str
    departure: TimeOfDay
    arrival: TimeOfDay
    success: bool = False

    def duration_minutes(self) -> int:
        d = self.arrival - self.departure
        if d < 0:
            d += 1440
        return d

    class Config:
        json_encoders = {
            TimeOfDay: TimeOfDay.__str__
        }

class UpdateFlightQuery(BaseModel):
    id: str
    departure: TimeOfDay
    arrival: TimeOfDay

    class Config:
        json_encoders = {
            TimeOfDay: TimeOfDay.__str__
        }