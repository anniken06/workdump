import json
import os
import shlex
import subprocess
import time


backup_directory = "backups"

def run_subprocess_and_get_results(command, max_length=1024, timeout=1):
    print(">> Running: ", str(command)[ :max_length])
    args = shlex.split(command) ## while err??
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err, rc) = *process.communicate(), process.returncode
    time.sleep(timeout)
    print(">> Results: ", str((out, err, rc))[ :max_length])
    return {'command': command, 'stdout': out, 'stderr': err, 'returncode': rc}


class CurlGenerator:
    def default_response_handler(responses):
        print("Handler not implemented. Simply printing responses:\n\n", "\n\n".join(map(lambda response: str(response), responses)))
        return responses

    def __init__(self, curl_template, replace_dict={"": [""]}, handle_responses=default_response_handler):
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


def get_quests():
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
    if input("Run get tasks (y/n)? ") == "y":
        get_generator = CurlGenerator(curl_template=get_template, replace_dict=get_replace_dict, handle_responses=get_handler)
        quests = get_generator.process_responses()
        return quests

def save_quests(quests):
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
    if input("Run save tasks (y/n)? ") == "y":
        save_generator = CurlGenerator(curl_template=save_template, replace_dict=save_replace_dict, handle_responses=save_handler)
        print("Backup status: {}".format(save_generator.process_responses()))

def delete_quests(quests):
    delete_template = "curl -v '<API_URL>/<DS_ID>' -X DELETE -H 'Accept: application/json, text/plain, */*' --insecure"
    delete_replace_dict = {
        "<API_URL>": ["https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest"],
        #"<DS_ID>": [quest['id'] for quest in quests],
        #"<DS_ID>": [quest['id'] for quest in quests if len(quest['activities']) < 2],
    }
    if input("Run delete tasks (y/n)? ") == "y":
        delete_generator = CurlGenerator(curl_template=delete_template, replace_dict=delete_replace_dict)
        print("Delete status: {}".format(delete_generator.process_responses()))

def update_quests(quests):
    update_template = "curl -v '<API_URL>' -X POST -H 'Content-Type: application/json' -H 'Accept: application/json, text/plain, */*' --data-binary '<QUEST_JSON>' --insecure"
    update_replace_dict = {
        "<API_URL>": ["https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest"],
        "<QUEST_JSON>": [json.dumps({"quest": quest}) for quest in quests],
    }
    if input("Run update tasks (y/n)? ") == "y":
        update_generator = CurlGenerator(curl_template=update_template, replace_dict=update_replace_dict)
        responses = update_generator.process_responses()
        print("Update status: {}".format(responses))

def scan_dynamo():
    scan_template = """aws dynamodb scan \
--region '<REGION_NAME>' \
--table-name '<TABLE_NAME>' \
--attributes-to-get 'id'
    """
    scan_replace_dict = {
        "<REGION_NAME>": ["eu-west-1"],
        "<TABLE_NAME>": ["coleman_dataset_manila1"],
    }
    def scan_handler(responses):
        load_scan_result = json.loads(responses[0]['stdout'].decode('utf-8'))
        return load_scan_result['Items']
    if input("Run scan tasks (y/n)? ") == "y":
        scan_generator = CurlGenerator(curl_template=scan_template, replace_dict=scan_replace_dict, handle_responses=scan_handler)
        keys = scan_generator.process_responses()
        return keys

def add_string_field(keys, field_name, dummy_string):
    add_template = """
aws dynamodb update-item \
--region '<REGION_NAME>' \
--table-name '<TABLE_NAME>' \
--key '<KEY>' \
--update-expression 'SET <FIELD_NAME> = :nf' \
--expression-attribute-values '{ ":nf": { "S": "<DUMMY_STRING>" }}'
    """
    add_replace_dict = {
        "<REGION_NAME>": ["eu-west-1"],
        "<TABLE_NAME>": ["coleman_dataset_manila1"],
        "<KEY>": [json.dumps(key) for key in keys],
        "<FIELD_NAME>": [field_name],
        "<DUMMY_STRING>": [dummy_string],
    }
    if input("Run add tasks (y/n)? ") == "y":
        add_generator = CurlGenerator(curl_template=add_template, replace_dict=add_replace_dict)
        responses = add_generator.process_responses()
        print("Add status: {}".format(responses))

def delete_string_field(keys, field_name):
    delete_template = """
aws dynamodb update-item \
--region '<REGION_NAME>' \
--table-name '<TABLE_NAME>' \
--key '<KEY>' \
--update-expression 'REMOVE <FIELD_NAME>'
    """
    delete_replace_dict = {
        "<REGION_NAME>": ["eu-west-1"],
        "<TABLE_NAME>": ["coleman_dataset_manila1"],
        "<KEY>": [json.dumps(key) for key in keys],
        "<FIELD_NAME>": [field_name],
    }
    if input("Run delete tasks (y/n)? ") == "y":
        delete_generator = CurlGenerator(curl_template=delete_template, replace_dict=delete_replace_dict)
        responses = delete_generator.process_responses()
        print("Delete status: {}".format(responses))


if __name__ == '__main__':
    keys = scan_dynamo()
    result1 = add_string_field(keys[:1], "NEWFIELD", "DUMMYSTRING")
    input("stop")
    result2 = delete_string_field(keys[:1], "NEWFIELD")

    print("Entering Interactive mode: Input Ctrl + Z to exit.")
    import code; code.interact(local={**locals(), **globals()})
    print("Done!")
