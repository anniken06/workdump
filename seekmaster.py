import json
import os
import shlex
import subprocess
import time
import urllib.parse


class CommandGenerator:
    def __init__(self, command_template, replace_dict={"": [""]}, handle_responses=lambda responses: responses):
        self.command_template = command_template
        self.replace_dict = replace_dict
        self.handle_responses = handle_responses

    def generate_commands(self):
        commands = [self.command_template]
        for keyword, replacements in self.replace_dict.items():
            commands = [command.replace(keyword, replacement) for command in commands for replacement in replacements]
        return commands

    def run_subprocess_and_get_results(self, command, max_length=1024, timeout=1):
        print(">> Running: ", str(command)[ :max_length])
        args = shlex.split(command)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err, rc) = *process.communicate(), process.returncode
        time.sleep(Config.cooldown_time)
        print(">> Results: ", str((out, err, rc))[ :max_length])
        if rc != 0:
            print(">> Command failed!")
            if Config.auto_y or input("Retry command (y)?: ") == 'y':
                return self.run_subprocess_and_get_results(command)
        return {'command': command, 'stdout': out, 'stderr': err, 'returncode': rc}

    def generate_responses(self, commands):
        responses = []
        for command in commands:
            responses += [self.run_subprocess_and_get_results(command)]
        return responses

    def process_responses(self):
        commands = self.generate_commands()
        responses = self.generate_responses(commands)
        print("Printing responses:\n\n", "\n\n".join(map(lambda response: str(response), responses)))
        return self.handle_responses(responses)

class Config:
    auto_y = True
    max_query_size = float('inf')  # 100
    cooldown_time = 1

def search_jobs(keywords, page=1, data_collection=[]):
    search_template = "curl 'https://chalice-search-api.cloud.seek.com.au/search?siteKey=AU-Main&sourcesystem=houston&userqueryid=97ec6621797cfebd8a0f96a5bc59d139-1449239&userid=2734ad6f-4c64-49e0-aff0-6f615ec2cb82&usersessionid=2734ad6f-4c64-49e0-aff0-6f615ec2cb82&eventCaptureSessionId=bdbc2f3d-c84b-40c1-bf60-bad7564b3380&where=All+Australia&page=<PAGE>&seekSelectAllPages=true&keywords=<KEYWORDS>&include=seodata&isDesktop=true' -H 'Origin: https://www.seek.com.au' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://www.seek.com.au/java-java-jobs' -H 'Connection: keep-alive' -H 'X-Seek-Site: Chalice' --compressed"
    search_replace_dict = {
        "<KEYWORDS>": [urllib.parse.quote_plus(keywords)],
        "<PAGE>": [str(page)],
    }
    if Config.auto_y or input("Run search jobs (y)? ") == 'y':
        search_generator = CommandGenerator(command_template=search_template, replace_dict=search_replace_dict)
        responses = search_generator.process_responses()
        json_response = json.loads(responses[0]['stdout'].decode('utf-8'))
        data_collection += json_response['data']
        print("Current data_collection size: ", len(data_collection))
        if len(data_collection) < Config.max_query_size and len(data_collection) < json_response['totalCount']:
            return search_jobs(keywords, page + 1, data_collection)
        return data_collection
    return data_collection


if __name__ == '__main__':
    pprint = lambda o: print(json.dumps(o, indent=2))
    do_listings_query = False
    external_file_path = "listings.json"

    if do_listings_query:
        listings = search_jobs("java")
        with open(external_file_path, 'w') as outfile: json.dump(listings, outfile, indent=4)
        print(">> Listing saved to external file")
    else:
        with open(external_file_path, 'r') as infile: listings = json.load(infile)
        print(">> Listing loaded from external file")

    unique_ids = set([listing['id'] for listing in listings])


    print(">> Entering Interactive mode: Input Ctrl + Z to exit.")
    import code; code.interact(local={**locals(), **globals()})
    print(">> Done!")

#curl "https://chalice-experience.cloud.seek.com.au/job/37162625?isDesktop=true^&locale=AU" -H "Origin: https://www.seek.com.au" -H "Accept-Encoding: gzip, deflate, br" -H "Accept-Language: en-US,en;q=0.9" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36" -H "Accept: application/json, text/plain, */*" -H "Referer: https://www.seek.com.au/job/37162625?type=standout" -H "If-None-Match: W/^\^"e86-I553tIAg7654QmbWH+FrADxPO7I^\^"" -H "Connection: keep-alive" -H "X-Seek-Site: Chalice" --compressed

#curl "https://ca-jobapply-ex-api.cloud.seek.com.au/jobs/37162625/" -H "Origin: https://www.seek.com.au" -H "Accept-Encoding: gzip, deflate, br" -H "Accept-Language: en-US,en;q=0.9" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36" -H "Accept: application/json, text/plain, */*" -H "Referer: https://www.seek.com.au/job-apply/37162625" -H "Connection: keep-alive" -H "X-Seek-Site: SEEK JobApply" --compressed