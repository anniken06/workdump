class ProxyService:
    @staticmethod
    def generate_proxy():
        print("Using hard-coded proxy")
        return " -x socks4://24.196.116.14:64312 "
        #proxy_results = CommandExecutor().run_command_simple("curl https://api.getproxylist.com/proxy")
        #proxy_json = json.loads(proxy_results['stdout'].decode('utf-8'))
        #print(proxy_json)
        #return f" -x {proxy_json['protocol']}://{proxy_json['ip']}:{proxy_json['port']} "

    @staticmethod
    def test_proxy():
        pass
        #return CommandGenerator("curl https://api.ipify.org").process_responses()[0]['stdout'].decode('utf-8')


if __name__ == '__main__':
    pass
    # generate and test
