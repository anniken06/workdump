import json
import os
import shlex
import subprocess as sp

from Config import Config


def get_simple_results(command):
    return sp.Popen(shlex.split(command), stdout=sp.PIPE).communicate()[0].decode('utf-8')


class ProxyService:
    def generate_proxy(renew=False):
        proxy_command = "curl https://api.getproxylist.com/proxy"
        if renew:
            print("Renewing proxy.txt")
            proxy_result = get_simple_results(proxy_command)
            proxy_json = json.loads(proxy_result)
            with open(os.path.join(Config.src_path, "proxy.txt"), 'w') as wpf:
                wpf.write(f"{proxy_json['protocol']}://{proxy_json['ip']}:{proxy_json['port']}")
        print("Loading proxy.txt")
        with open(os.path.join(Config.src_path, "proxy.txt"), 'r') as rpf:
            proxy = f" -x {rpf.read()} "
        return proxy

    def test_proxy():
        ip_command = "curl https://api.ipify.org"
        with open(os.path.join(Config.src_path, "proxy.txt"), 'r') as rpf:
            proxy = f" -x {rpf.read()} "
        original_ip = get_simple_results(ip_command)
        proxy_ip = get_simple_results(f"{ip_command}{proxy}")
        print(f"Original ip: {original_ip}\nProxy ip: {proxy_ip}")
        return original_ip != proxy_ip


if __name__ == '__main__':
    print(f"Proxy: {ProxyService.generate_proxy()}")
    print(f"Proxy test: {ProxyService.test_proxy()}")
    # print(ProxyService.generate_proxy(True))
    pass  # generate and test
