import json
import os
import shlex
import subprocess
import time


def run_subprocess_and_get_results(command, max_length=256, timeout=1):
    args = shlex.split(command)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err, rc) = *process.communicate(), process.returncode
    #time.sleep(timeout)
    print(">> Running: ", str(command)[ :max_length])
    print(">> Results: ", str((out, err, rc))[ :max_length])
    return {'command': command, 'stdout': out, 'stderr': err, 'returncode': rc}


class CurlGenerator:
    def __init__(self, curl_template, replace_dict={"": [""]}, handle_responses=lambda responses: None):
        ## Copy from Chrome > F12 > Network > particular request > Right-click > Copy > Copy as cURL (bash)
        self.curl_template = curl_template
        self.replace_dict = replace_dict
        self.handle_responses = handle_responses

    def generate_curls(self):
        curls = [self.curl_template]
        for keyword, replacements in self.replace_dict.items():
            curls = [curl.replace(keyword, replacement) for curl in curls for replacement in replacements]
        return curls

    def generate_responses(self, curls):
        responses = []
        for curl in curls:
            responses += [run_subprocess_and_get_results(curl)]
        return responses

    def process_responses(self):
        curls = self.generate_curls()
        responses = self.generate_responses(curls)
        return self.handle_responses(responses)


if __name__ == '__main__':
    backup_directory = "backups"

    # # #  Query quests  # # # 
    get_template = "curl -v '<API_URL>' -H 'Accept: application/json, text/plain, */*' --insecure"
    get_replace_dict = {
        "<API_URL>": ["https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest"],
    }
    def get_handler(responses):
        print("Processing responses from: get curls.")
        try:
            quests = json.loads(responses[0]['stdout'].decode('utf-8'))
            print("Finished looking for {} quests: {}.".format(len(quests), [quest['name'] for quest in quests]))
        except Exception as e:
            print(e)
            print(responses[0]['stderr'].decode('utf-8'))
        return quests
    get_generator = CurlGenerator(curl_template=get_template, replace_dict=get_replace_dict, handle_responses=get_handler)
    quests = get_generator.process_responses()


    # # #  Save queried quests  # # # 
    save_template = "curl -v '<API_URL>/<DS_ID>?render=true' -H 'Accept: application/json, text/plain, */*' --insecure"
    save_replace_dict = {
        "<API_URL>": ["https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest"],
        "<DS_ID>": [quest['id'] for quest in quests],
    }
    def save_handler(responses):
        print("Processing responses from: save curls.")
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
    save_generator = CurlGenerator(curl_template=save_template, replace_dict=save_replace_dict, handle_responses=save_handler)
    print("Backup status: {}".format(save_generator.process_responses()))


    # # #  Delete queried quests  # # # 
    delete_template = "curl -v '<API_URL>/<DS_ID>' -X DELETE -H 'Accept: application/json, text/plain, */*' --insecure"
    delete_replace_dict = {
        "<API_URL>": ["https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest"],
        "<DS_ID>": [quest['id'] for quest in quests],
    }
    def delete_handler(responses):
        print("Processing responses from: delete curls.")
        return "Finished deleting {} quests.".format(len(responses))
    delete_generator = CurlGenerator(curl_template=delete_template, replace_dict=delete_replace_dict, handle_responses=delete_handler)
    print("Delete status: {}".format(delete_generator.process_responses()))


    print("Done!")


""" SAMPLE
updated_quest = quest
updated_quest . add/remove col

update quest template = "... <API>/<ID> ... <NEW_CONTENTS>"
{"<NEW CONENTS>": updated_quest}

process_responses()
"""