from django.test import TestCase,Client

from .models import Flight, Airport, Passenger
class FlightTestCase(TestCase):

    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(Code="AAA", City="City A")
        a2 = Airport.objects.create(Code="BBB", City="City B")

        # Create flights.
        Flight.objects.create(Origin=a1, Destination=a2, Duration=100)
        Flight.objects.create(Origin=a1, Destination=a1, Duration=200)
        Flight.objects.create(Origin=a1, Destination=a2, Duration=-100)
    def test_departures_count(self):
        a = Airport.objects.get(Code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(Code="AAA")
        self.assertEqual(a.arrivals.count(), 1)
    def test_valid_flight(self):
        a1 = Airport.objects.get(Code="AAA")
        a2 = Airport.objects.get(Code="BBB")
        f = Flight.objects.get(Origin=a1, Destination=a2, Duration=100)
        self.assertTrue(f.is_valid_flight())
    def test_invalid_flight_Destination(self):
        a1 = Airport.objects.get(Code="AAA")
        f = Flight.objects.get(Origin=a1, Destination=a1)
        self.assertFalse(f.is_valid_flight())
    def test_invalid_flight_Duration(self):
        a1 = Airport.objects.get(Code="AAA")
        a2 = Airport.objects.get(Code="BBB")
        f = Flight.objects.get(Origin=a1, Destination=a2, Duration=-100)
        self.assertFalse(f.is_valid_flight())
    def test_index(self):

    # Set up client to make requests
        c = Client()

    # Send get request to index page and store response
        response = c.get("/flights/")

    # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

    # Make sure three flights are returned in the context
        self.assertEqual(response.context["flights"].count(), 3)
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(Code="AAA")
        f = Flight.objects.get(Origin=a1, Destination=a1)

        c = Client()
        response = c.get(f"/{f.id}/book")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(max("id"))["max_id"]

        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)