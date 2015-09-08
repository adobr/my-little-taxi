class Report():
    def __init__(self, request):
        self.request = request

    def report_error(self, error):
        self.request.write("Something went wrong.")
        self.request.write(str(error))
        self.request.finish()

    def report_result(self, result):
        for line in result:
            self.request.write(line)
        self.request.finish()

    def report_nearest_cars(self, nearest_cars):
        if not nearest_cars:
            self.report_error('We have no cars at all!')
            return
        result = []
        for (car, distance) in nearest_cars:
            result.append("{0}\t-\t{1:.2f}km\n".format(str(car), distance))
        self.report_result(result)

    def report_added_car(self, car):
        self.report_result("You data was successfully added. {}".format(str(car)))

    def report_found_cars(self, cars):
        if not cars:
            self.report_error('Car not found in the database.')
        else:
            self.report_result(str(cars[0]))