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
   
