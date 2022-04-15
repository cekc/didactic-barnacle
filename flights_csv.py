from models import Flight

def read_csv(filename: str) -> dict[str, Flight]:
	flights: dict[str, Flight] = {}
	with open(filename) as f:
		for l in f:
			try:
				vals = [v.strip() for v in l.split(',', maxsplit=4)]
				flights[vals[0]] = Flight(
					id=vals[0],
					departure=vals[1],
					arrival=vals[2],
					success=(vals[3] == 'success'))
			except:
				pass
	return flights

def dump_csv(filename: str, flights: dict[str, Flight]):
	with open(filename, 'w') as f: 
		for flight in flights.values():
			s = 'success' if flight.success else 'fail'
			print(f'{flight.id}, {flight.departure}, {flight.arrival}, {s}', file=f)
		









