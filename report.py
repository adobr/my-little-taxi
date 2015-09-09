class Report():
    def __init__(self, request, close_connection=True):
        self.request = request
        self.close_connection = close_connection

    def report_error(self, error):
        self.report_result(["Something went wrong.", error])

    def report_result(self, result):
        self.request.setHeader("content-type", "text/plain")
        if isinstance(result, list):
            for line in result:
                self.request.write(str(line))
                self.request.write("\n")
        else:
            self.request.write(str(result))
            self.request.write("\n")
        if self.close_connection:
            self.request.finish()

    def report_nearest_cars(self, nearest_cars):
        if not nearest_cars:
            self.report_error('We have no cars at all!')
            return
        result = []
        for (car, distance) in nearest_cars:
            result.append("{0}\t-\t{1:.2f}km".format(str(car), distance))
        self.report_result(result)

    def report_added_car(self, car):
        self.report_result("You data was successfully added. {}".format(str(car)))

    def report_found_cars(self, cars):
        if not cars:
            self.report_error('Car not found in the database.')
        else:
            self.report_result(cars[0])

    def report_to_subscriber(self, car):
        self.report_result(car)
