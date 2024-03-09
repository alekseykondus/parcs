from Pyro4 import expose
import random
import time

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        start_time = time.time()
        
        print("Job Started")
        print("Workers %d" % len(self.workers))
        amount_of_points = self.read_input()
        step = amount_of_points / len(self.workers)

        mapped = []
        lastWorker = len(self.workers) - 1

        for i in range(0, lastWorker):
            mapped.append(self.workers[i].mymap(i * step, i * step + step))
        mapped.append(self.workers[lastWorker].mymap(lastWorker * step, amount_of_points))
        print('Map finished: ', mapped)

        reduced = self.myreduce(mapped, amount_of_points)
        print("Reduce finished: " + str(reduced))

        total_time = time.time() - start_time
        print("Job Finished in {:.3f} seconds".format(total_time))

        self.write_output(reduced, total_time)

    @staticmethod
    @expose
    def mymap(a, b):
        points_in_circle = 0
        for i in range(a, b):
            points_in_circle += Solver.hits_count()
        return points_in_circle

    @staticmethod
    @expose
    def myreduce(mapped, total_points):
        points_in_circle = 0
        for x in mapped:
            points_in_circle += x.value
        return 4.0 * float(points_in_circle) / float(total_points)

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            line = f.readline()
        return int(line)

    def write_output(self, output, time_elapsed):
        with open(self.output_file_name, 'w') as f:
            f.write("Result: {}\n".format(output))
            f.write("Execution Time: {:.3f} seconds\n".format(time_elapsed))

    @staticmethod
    def hits_count():
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        if (pow(x, 2) + pow(y, 2)) <= 1.0:
            return 1
        return 0