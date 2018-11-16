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

def test_add_dataset():
    curl = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/dataset' -H 'Origin: https://manila1.cpaas.awsiondev.infor.com:18010' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=678348ba-6632-453b-8834-ebf85a38b33d; JSESSIONID=04672184E1323D87FAB0FDE7E7EFE47A' -H 'Connection: keep-alive' --data-binary '{\"id\":null,\"name\":\"small-utf-test\",\"description\":\"small-utf-test\",\"datasourceType\":\"MANUAL\",\"lastUpdatedBy\":null,\"lastUpdatedOn\":null,\"size\":0,\"status\":\"DRAFT\",\"sqlQuery\":\"\",\"documentNames\":[],\"documentType\":\"\",\"sampleChunk\":\"Employee ID;Employee Name;Role;Birthday;Hire Date;Rating;Manager,\\r\\nsalientes;Joana Salientes;Management;1982-02-15;2017-10-26;85;Cez Lumaad\\r\\nggenove;Gena Genove;Java Programming;1980-11-15;2017-01-29;79;Rommel Dollison,\\r\\njramos;Jay Ryan Ramos;Quality Assurance;1985-04-18;2017-09-02;93;Cez Lumaad,\\r\\ndespejo;David Espejo;Quality Assurance;1989-11-11;2017-09-02;73;Jay Ryan Ramos,\\r\\nmacson;Maria Theresa Acson;Test Automation;1988-01-22;2017-10-26;86;Jay Ryan Ramos,\\r\\nesereno;Emil Sereno;.Net Framework;1995-01-27;2017-08-26;91;Cez Lumaad,\\r\\nmlumaad;Cez Lumaad;Management;1979-01-29;2017-10-26;80;Rommel Dollison,\\r\\nlcaviles;Lassiter Caviles;Java Programming;1992-04-03;2017-09-02;60;Cez Lumaad,\\r\\ncnario;Charlotte Camille Nario;Test Automation;1988-03-17;2017-10-26;80;Jay Ryan Ramos,\\r\\njfrancisco;Jose Leandro Francisco;Java Programming;1983-06-02;2017-09-02;99;Cez Lumaad,\\r\\nacolar;Annika Pearl Colar;Java Programming;1988-06-06;2017-06-19;83;Cez Lumaad,\\r\\nepaduano;Enrico Paduano;Test Automation;1984-08-26;2017-09-02;99;Rommel Dollison,\\r\\nfnarzoles;Ferdinand Narzoles;Test Automation;1983-09-11;2017-08-23;97;Cez Lumaad,\\r\\nmamanaguit;Mary Ann Managuit;Test Automation;1990-10-20;2017-09-02;86;Jay Ryan Ramos,\\r\\njatienza;Judy Atienza;Quality Assurance;1980-11-13;2017-08-23;80;Jay Ryan Ramos,\\r\\nkiledan;Kristine Iledan;Management;1981-09-09;2017-10-26;72;Cez Lumaad\",\"header\":true,\"delimiter\":\";\",\"encoding\":\"UTF-8\",\"externalJsonSchema\":{\"type\":\"object\",\"properties\":[{\"name\":\"employeeID\",\"schema\":{\"type\":\"string\",\"nullable\":true}},{\"name\":\"employeeName\",\"schema\":{\"type\":\"string\",\"nullable\":true}},{\"name\":\"role\",\"schema\":{\"type\":\"string\",\"nullable\":true}},{\"name\":\"birthday\",\"schema\":{\"type\":\"string\",\"nullable\":true}},{\"name\":\"hireDate\",\"schema\":{\"type\":\"string\",\"nullable\":true}},{\"name\":\"rating\",\"schema\":{\"type\":\"string\",\"nullable\":true}},{\"name\":\"manager,\",\"schema\":{\"type\":\"string\",\"nullable\":true}}]}}' --compressed --insecure"
    return CurlGenerator(curl).process_responses()

def test_upload_dataset(DS_ID):
    #ORIGINAL = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/dataset/<DS_ID>/upload' -H 'Origin: https://manila1.cpaas.awsiondev.infor.com:18010' -H 'X-Infor-TenantId: INTEGRATION_AX1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryBp8AftHHrUT3k62U' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=678348ba-6632-453b-8834-ebf85a38b33d; JSESSIONID=04672184E1323D87FAB0FDE7E7EFE47A' -H 'Connection: keep-alive' --data-binary $'------WebKitFormBoundaryBp8AftHHrUT3k62U\\r\\nContent-Disposition: form-data; name=\"file\"; filename=\"small_utf.csv_1535426690208_1_1\"\\r\\nContent-Type: text/dsv\\r\\n\\r\\nEmployee ID;Employee Name;Role;Birthday;Hire Date;Rating;Manager,\\r\\nsalientes;Joana Salientes;Management;1982-02-15;2017-10-26;85;Cez Lumaad\\r\\nggenove;Gena Genove;Java Programming;1980-11-15;2017-01-29;79;Rommel Dollison,\\r\\njramos;Jay Ryan Ramos;Quality Assurance;1985-04-18;2017-09-02;93;Cez Lumaad,\\r\\ndespejo;David Espejo;Quality Assurance;1989-11-11;2017-09-02;73;Jay Ryan Ramos,\\r\\nmacson;Maria Theresa Acson;Test Automation;1988-01-22;2017-10-26;86;Jay Ryan Ramos,\\r\\nesereno;Emil Sereno;.Net Framework;1995-01-27;2017-08-26;91;Cez Lumaad,\\r\\nmlumaad;Cez Lumaad;Management;1979-01-29;2017-10-26;80;Rommel Dollison,\\r\\nlcaviles;Lassiter Caviles;Java Programming;1992-04-03;2017-09-02;60;Cez Lumaad,\\r\\ncnario;Charlotte Camille Nario;Test Automation;1988-03-17;2017-10-26;80;Jay Ryan Ramos,\\r\\njfrancisco;Jose Leandro Francisco;Java Programming;1983-06-02;2017-09-02;99;Cez Lumaad,\\r\\nacolar;Annika Pearl Colar;Java Programming;1988-06-06;2017-06-19;83;Cez Lumaad,\\r\\nepaduano;Enrico Paduano;Test Automation;1984-08-26;2017-09-02;99;Rommel Dollison,\\r\\nfnarzoles;Ferdinand Narzoles;Test Automation;1983-09-11;2017-08-23;97;Cez Lumaad,\\r\\nmamanaguit;Mary Ann Managuit;Test Automation;1990-10-20;2017-09-02;86;Jay Ryan Ramos,\\r\\njatienza;Judy Atienza;Quality Assurance;1980-11-13;2017-08-23;80;Jay Ryan Ramos,\\r\\nkiledan;Kristine Iledan;Management;1981-09-09;2017-10-26;72;Cez Lumaad\\r\\n------WebKitFormBoundaryBp8AftHHrUT3k62U--\\r\\n' --compressed --insecure"
    curl = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/dataset/<DS_ID>/upload' -H 'Origin: https://manila1.cpaas.awsiondev.infor.com:18010' -H 'X-Infor-TenantId: INTEGRATION_AX1' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryBp8AftHHrUT3k62U' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=678348ba-6632-453b-8834-ebf85a38b33d; JSESSIONID=04672184E1323D87FAB0FDE7E7EFE47A' -H 'Connection: keep-alive' --data-binary $'------WebKitFormBoundaryBp8AftHHrUT3k62U\nContent-Disposition: form-data; name=\"file\"; filename=\"small_utf.csv_1535426690208_1_1\"\nContent-Type: text/dsv\n\nEmployee ID;Employee Name;Role;Birthday;Hire Date;Rating;Manager,\\r\\nsalientes;Joana Salientes;Management;1982-02-15;2017-10-26;85;Cez Lumaad\\r\\nggenove;Gena Genove;Java Programming;1980-11-15;2017-01-29;79;Rommel Dollison,\\r\\njramos;Jay Ryan Ramos;Quality Assurance;1985-04-18;2017-09-02;93;Cez Lumaad,\\r\\ndespejo;David Espejo;Quality Assurance;1989-11-11;2017-09-02;73;Jay Ryan Ramos,\\r\\nmacson;Maria Theresa Acson;Test Automation;1988-01-22;2017-10-26;86;Jay Ryan Ramos,\\r\\nesereno;Emil Sereno;.Net Framework;1995-01-27;2017-08-26;91;Cez Lumaad,\\r\\nmlumaad;Cez Lumaad;Management;1979-01-29;2017-10-26;80;Rommel Dollison,\\r\\nlcaviles;Lassiter Caviles;Java Programming;1992-04-03;2017-09-02;60;Cez Lumaad,\\r\\ncnario;Charlotte Camille Nario;Test Automation;1988-03-17;2017-10-26;80;Jay Ryan Ramos,\\r\\njfrancisco;Jose Leandro Francisco;Java Programming;1983-06-02;2017-09-02;99;Cez Lumaad,\\r\\nacolar;Annika Pearl Colar;Java Programming;1988-06-06;2017-06-19;83;Cez Lumaad,\\r\\nepaduano;Enrico Paduano;Test Automation;1984-08-26;2017-09-02;99;Rommel Dollison,\\r\\nfnarzoles;Ferdinand Narzoles;Test Automation;1983-09-11;2017-08-23;97;Cez Lumaad,\\r\\nmamanaguit;Mary Ann Managuit;Test Automation;1990-10-20;2017-09-02;86;Jay Ryan Ramos,\\r\\njatienza;Judy Atienza;Quality Assurance;1980-11-13;2017-08-23;80;Jay Ryan Ramos,\\r\\nkiledan;Kristine Iledan;Management;1981-09-09;2017-10-26;72;Cez Lumaad\n------WebKitFormBoundaryBp8AftHHrUT3k62U--' --compressed --insecure"
    replace_dict = {"<DS_ID>": [DS_ID]}
    return CurlGenerator(curl, replace_dict).process_responses()

def test_get_dataset(DS_ID):
    curl = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/dataset/<DS_ID>' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=678348ba-6632-453b-8834-ebf85a38b33d; JSESSIONID=04672184E1323D87FAB0FDE7E7EFE47A' -H 'Connection: keep-alive' --compressed --insecure"
    replace_dict = {"<DS_ID>": [DS_ID]}
    return CurlGenerator(curl, replace_dict).process_responses()


if __name__ == '__main__':
    add_dataset_requests = test_add_dataset()
    add_dataset_response = add_dataset_requests[0]['stdout'].decode('utf-8')
    add_dataset_id = json.loads(add_dataset_response)['id']

    upload_dataset_requests = test_upload_dataset(add_dataset_id)
    upload_dataset_response = upload_dataset_requests[0]['stdout'].decode('utf-8')

    get_dataset_requests = test_get_dataset(add_dataset_id)
    get_dataset_response = get_dataset_requests[0]['stdout'].decode('utf-8')

    print("Add dataset responded: ", add_dataset_response)
    print("Upload dataset responded: ", upload_dataset_response)
    print("Get dataset responded: ", json.loads(get_dataset_response)['status'])

    for i in range(20):
        try:
            get_dataset_requests = test_get_dataset(add_dataset_id)
            get_dataset_response = get_dataset_requests[0]['stdout'].decode('utf-8')
            print("Get dataset responded: ", json.loads(get_dataset_response)['status'])
            if json.loads(get_dataset_response)['status'] == "SAVED": break
            time.sleep(20)
        except: pass

    print("Entering Interactive mode: Input Ctrl + Z to exit.")
    import code; code.interact(local={**locals(), **globals()})
    print("Done!")
