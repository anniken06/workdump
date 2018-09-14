from multiprocessing import Pool, Manager, Lock, current_process as mpproc
from shlex import split as shsplit 
from subprocess import Popen, PIPE
from time import sleep, time as cur_time
from CommandGenerator import CommandGenerator

timeout = 10
timeout2 = None
god = {}
"""
def thanks_getproxylist():
    proxy_generator = CommandExecutor().run_command("curl https://api.getproxylist.com/proxy")
    proxy_json = json.loads(proxy_generator.process_responses()[0]['stdout'].decode('utf-8'))
    return f" -x {proxy_json['protocol']}://{proxy_json['ip']}:{proxy_json['port']} "
def thanks_ipify():
    return CommandGenerator("curl https://api.ipify.org").process_responses()[0]['stdout'].decode('utf-8')
"""

class CommandExecutor:  # TODO: use generators more
    def __init__(self):
        self.execution_context = {}

    def safe_get(self, dobj, *indexes):  #TODO!!
        pass
        """
        try:
            return dobj
        except:
            return dobj
        """


    def chunk_commands(self, commands, workers):
        k = -(-len(commands) // workers)
        return [commands[k * i:k * (i + 1)] for i in range(0, workers)]
        #for i in range(0, workers): yield commands[k * i:k * (i + 1)]

    def dechunk_results(self, results_chunks):
        return [result for results_chunk in results_chunks for result in results_chunk]

    def run_command(self, command):
        print(f">> Running: {command}")
        print(mpproc().name)
        self.execution_context[mpproc().name, "proxy"] = "ZZZZZZZZZZZZZZZZZZZZZZZZZ"
        god[mpproc().name, "proxy"] = "ZZZZZZZZZZZZZZZZZZZZZZZZZ"
        process = Popen(shsplit(command), stdout=PIPE, stderr=PIPE)
        start_time = cur_time()
        (out, err, rc, duration) = (*process.communicate(), process.returncode, cur_time() - start_time)
        sleep(timeout)
        result = {'command': command, 'stdout': out, 'stderr': err, 'returncode': rc, 'duration': duration}
        print(f"<< Results: {result}")
        if rc != 0:  # TODO
            print(">><< Command failed since return code is not zero! Retrying with a new context...")
            self.execution_context["new"] = "stuff"
            return self.run_command(command)
        return result

    def run_commands(self, commands):
        print(f">> Running process on {mpproc().name}.")
        calculations = [self.run_command(command) for command in commands]
        print(f"<< Finished process on {mpproc().name}.")
        return calculations

    def run_commands_on_workers(self, commands, workers):
        #self.m = Manager()
        #lock = self.m.Lock()
        with Pool(processes=workers) as pool:
            print(">> Multiprocessing pool loaded.")
            commands_chunks = self.chunk_commands(commands, workers)
            workers_handles = [pool.apply_async(self.run_commands, args=[commands_chunk]) for commands_chunk in commands_chunks]
            results_chunk = [worker.get(timeout2) for worker in workers_handles]
            results = self.dechunk_results(results_chunk)
            print("<< Multiprocessing pool unloaded.")
        return results


if __name__ == '__main__':
    commands = CommandGenerator.generate_commands(
        "echo <STR1> <STR2> <STR3>",
        {"<STR1>": [1,3], "<STR2>": [1,3], "<STR3>": [1,3]}
    )
    workers = 10
    executor = CommandExecutor()
    raw_executor_results = executor.run_commands_on_workers(commands, workers)
    executor_results = [result['stdout'].decode('utf-8') for result in raw_executor_results]
    import code; code.interact(local={**locals(), **globals()})
