import multiprocessing
import os


def split_params(params, workers):
    k = -(-len(params) // workers)
    for i in range(0, workers):
        yield params[k * i:k * (i + 1)]

def merge_results(results_split):
    return [result for result_split in results_split for result in result_split]

def my_processor_sum(l):
    name = f"{{worker={multiprocessing.current_process()}, OS_pid={os.getpid()}}}"
    print(f">>> Running process on {name}.")
    calculated_sum = sum(l)
    print(f"<<< Finished process on {name}.")
    return [calculated_sum]

def my_processor_minus(l):
    name = f"{{worker={multiprocessing.current_process()}, OS_pid={os.getpid()}}}"
    print(f">>> Running process on {name}.")
    calculation = list(map(lambda x: x-100, list(l)))
    print(f"<<< Finished process on {name}.")
    return calculation

if __name__ == '__main__':
    workers = 20
    timeout = None
    with multiprocessing.Pool(processes=workers) as pool:  # todo remove lists()
        print(">> Multiprocessing pool loaded.")
        params = list(range(100, 0, -1))

        params_split = list(split_params(params, workers))
        workers_split = [pool.apply_async(my_processor_sum, args=[params]) for params in params_split]
        results_split = [workers.get(timeout) for workers in workers_split]
        results = merge_results(results_split)

        print(f"Parameters: {params}")
        print(f"Parameters splits: {params_split}")
        print(f"Results splits: {results_split}")
        print(f"Results: {results}")


        params = list(range(100, 0, -1))

        params_split = list(split_params(params, workers))
        workers_split = [pool.apply_async(my_processor_minus, args=[params]) for params in params_split]
        results_split = [workers.get(timeout) for workers in workers_split]
        results = merge_results(results_split)

        print(f"Parameters: {params}")
        print(f"Parameters splits: {params_split}")
        print(f"Results splits: {results_split}")
        print(f"Results: {results}")

        import code; code.interact(local={**locals(), **globals()})
        print(">> Multiprocessing pool unloaded.")