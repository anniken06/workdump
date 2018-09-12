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
        args = shlex.split(command) ## while err??
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err, rc) = *process.communicate(), process.returncode
        time.sleep(timeout)
        print(">> Results: ", str((out, err, rc))[ :max_length])
        if rc != 0:
            print(">> Command failed!")
            if auto_y or input("Retry command (y)?: ") == 'y':
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


def get_quests():
    get_template = "curl -v '<API_URL>' -H 'Accept: application/json, text/plain, */*' --insecure"
    get_replace_dict = {
        "<API_URL>": ["https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest"],
    }
    def get_handler(responses):
        print("Processing responses from: get commands.")
        try:
            quests = json.loads(responses[0]['stdout'].decode('utf-8'))
            print("Finished looking for {} quests: {}.".format(len(quests), [quest['name'] for quest in quests]))
        except Exception as e:
            print(e)
            print(responses[0]['stderr'].decode('utf-8'))
        return quests
    if input("Run get tasks (y)? ") == 'y':
        get_generator = CommandGenerator(command_template=get_template, replace_dict=get_replace_dict, handle_responses=get_handler)
        quests = get_generator.process_responses()
        return quests

def save_quests(quests):
    save_template = "curl -v '<API_URL>/<DS_ID>?render=true' -H 'Accept: application/json, text/plain, */*' --insecure"
    save_replace_dict = {
        "<API_URL>": ["https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest"],
        "<DS_ID>": [quest['id'] for quest in quests],
    }
    def save_handler(responses):
        print("Processing responses from: save commands.")
        if not os.path.exists(backup_directory): os.makedirs(backup_directory)
        for result in responses:
            try:
                saved_quest =  json.loads(result['stdout'].decode('utf-8'))['quest']
                backup_file = os.path.join(backup_directory, "backup_{}_{}.json".format(saved_quest["name"], saved_quest["id"]))
                with open(backup_file, 'wb') as out_file:
                    out_file.write(result['stdout'])
                print("Successfully saved: {}".format(backup_file))
            except Exception as e:
                print(e)
                print(result['stderr'].decode('utf-8'))
        return "Finished saving backups to: /{}/.".format(backup_directory)
    if input("Run save tasks (y)? ") == 'y':
        save_generator = CommandGenerator(command_template=save_template, replace_dict=save_replace_dict, handle_responses=save_handler)
        print("Backup status: {}".format(save_generator.process_responses()))


def search_jobs(keywords):
    search_template = "curl 'https://chalice-search-api.cloud.seek.com.au/search?siteKey=AU-Main&sourcesystem=houston&userqueryid=97ec6621797cfebd8a0f96a5bc59d139-1449239&userid=2734ad6f-4c64-49e0-aff0-6f615ec2cb82&usersessionid=2734ad6f-4c64-49e0-aff0-6f615ec2cb82&eventCaptureSessionId=bdbc2f3d-c84b-40c1-bf60-bad7564b3380&where=All+Australia&page=1&seekSelectAllPages=true&keywords=<KEYWORDS>&include=seodata&isDesktop=true' -H 'Origin: https://www.seek.com.au' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://www.seek.com.au/java-java-jobs' -H 'Connection: keep-alive' -H 'X-Seek-Site: Chalice' --compressed"
    search_replace_dict = {
        "<KEYWORDS>": [urllib.parse.quote_plus(keywords)]
    }
    def search_handler(responses):
        json_response = json.loads(responses[0]['stdout'].decode('utf-8'))
        return json_response['data']
    if auto_y or input("Run search jobs (y)? ") == 'y':
        search_generator = CommandGenerator(command_template=search_template, replace_dict=search_replace_dict, handle_responses=search_handler)
        query = search_generator.process_responses()


if __name__ == '__main__':
    auto_y = True
    pprint = lambda o: print(json.dumps(o, indent=2))

    listings = search_jobs("java")
    # TODO hack pagination

    print("Entering Interactive mode: Input Ctrl + Z to exit.")
    import code; code.interact(local={**locals(), **globals()})
    print("Done!")

#curl "https://chalice-experience.cloud.seek.com.au/job/37162625?isDesktop=true^&locale=AU" -H "Origin: https://www.seek.com.au" -H "Accept-Encoding: gzip, deflate, br" -H "Accept-Language: en-US,en;q=0.9" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36" -H "Accept: application/json, text/plain, */*" -H "Referer: https://www.seek.com.au/job/37162625?type=standout" -H "If-None-Match: W/^\^"e86-I553tIAg7654QmbWH+FrADxPO7I^\^"" -H "Connection: keep-alive" -H "X-Seek-Site: Chalice" --compressed

#curl "https://ca-jobapply-ex-api.cloud.seek.com.au/jobs/37162625/" -H "Origin: https://www.seek.com.au" -H "Accept-Encoding: gzip, deflate, br" -H "Accept-Language: en-US,en;q=0.9" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36" -H "Accept: application/json, text/plain, */*" -H "Referer: https://www.seek.com.au/job-apply/37162625" -H "Connection: keep-alive" -H "X-Seek-Site: SEEK JobApply" --compressed