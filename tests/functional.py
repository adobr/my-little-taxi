import requests

CAR_URL = "http://localhost:8090/car"
NEAREST_CAR_URL = "http://localhost:8090/nearest_cars"


class TestClass():
    """
    This tests should be run on running app already connected to the database
    TODO: start and stop throw testing
    """

    def test_data_updation(self):
        url = "{}?car_id=1&ll=0.0,0.0".format(CAR_URL, 1)
        r = requests.post(url)
        assert (r.status_code == 200)
        assert (r.text.startswith("You data was successfully added."))
        assert ("#00001" in r.text)

    def test_incorrect_data_updation(self):
        url = "{}?ll={}".format(CAR_URL, 1, "0.0,0.0")
        r = requests.post(url)
        assert (r.text == "Parameter car_id is required.")

    def has_error_message(self, text):
        return "Something went wrong" in text

    def test_non_existent_car(self):
        url = "{}?car_id={}".format(CAR_URL, -1)
        r = requests.get(url)
        assert (self.has_error_message(r.text))
        assert ("Car not found in the database." in r.text)

    def test_existing_car(self):
        requests.post("{}?ll={}".format(CAR_URL, 1, "0.0,0.0"))
        url = "{}?car_id={}".format(CAR_URL, 1)
        r = requests.get(url)
        assert ("#00001" in r.text)

    def test_nearest_cars(self):
        requests.post("{}?car_id={}&ll={}".format(CAR_URL, 1, "0.0,0.0"))
        url = "{}?ll={}&count={}".format(NEAREST_CAR_URL, "0.0,0.0", 100)
        r = requests.get(url)
        assert ("#00001" in r.text)
        assert ("0km" in r.text)
