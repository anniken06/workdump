import multiprocessing as mp
import shlex
import subprocess as sp
import time

from Config import Config
from ProxyService import ProxyService


get_id = lambda: getattr(mp.current_process(), 'name')


class CommandExecutor:  # TODO: use generators() more
    def __init__(self):
        self.execution_context = {}

    def chunk_commands(self, commands, workers):
        k = -(-len(commands) // workers)
        return [commands[k * i:k * (i + 1)] for i in range(0, workers)]
        # for i in range(0, workers): yield commands[k * i:k * (i + 1)]

    def dechunk_results(self, results_chunks):
        return [result for results_chunk in results_chunks for result in results_chunk]

    def run_command_simple(self, command):
        print(f">> Running {get_id()}: {command}")
        process = sp.Popen(shlex.split(command), stdout=sp.PIPE, stderr=sp.PIPE)
        start_time = time.time()
        (out, err, rc, duration) = (*process.communicate(), process.returncode, time.time() - start_time)
        time.sleep(Config.timeout)
        result = {'command': command, 'stdout': out, 'stderr': err, 'returncode': rc, 'duration': duration}
        print(f"<< Results {get_id()}: {result}")
        return result

    def run_command_retry(self, md, command):
        if Config.use_proxy:
            command = command + md[get_id()].get('proxy', "")
        result = self.run_command_simple(command)
        if result['returncode'] != 0:
            print(">><< Command failed since return code is not zero! Retrying with a new context...")
            if Config.use_proxy:
                md[get_id()] = {'proxy': ProxyService.generate_proxy(renew=True)}
            return self.run_command_retry(md, command)
        return result

    def run_commands(self, md, commands):
        if Config.use_proxy:
            md[get_id()] = {'proxy': ProxyService.generate_proxy()}
        print(f">> Running process on {get_id()}.")
        calculations = [self.run_command_retry(md, command) for command in commands]
        print(f"<< Finished process on {get_id()}.")
        return calculations

    def run_commands_on_workers(self, commands, workers):
        md = mp.Manager().dict()
        with mp.Pool(processes=workers) as pool:
            print(">> Multiprocessing pool loaded.")
            commands_chunks = self.chunk_commands(commands, workers)
            workers_handles = [pool.apply_async(self.run_commands, args=[md, commands_chunk]) for commands_chunk in commands_chunks]
            results_chunk = [worker.get(Config.wait_time) for worker in workers_handles]
            results = self.dechunk_results(results_chunk)
            print("<< Multiprocessing pool unloaded.")
        self.execution_context = dict(md)
        print(">> Stored execution_context: {}".format(self.execution_context))
        return results


if __name__ == '__main__':
    pass
    # generate and test
