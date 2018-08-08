import json
import shlex
import subprocess


def run_subprocess_and_get_results(command):
    args = shlex.split(command)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err, rc) = *process.communicate(), process.returncode
    print("Running: ", command)
    print("Results: ", (out, err, rc))
    return {"command": command, "stdout": out, "stderr": err, "returncode": rc}


def write_to_file(filename, bytestring):
    with open(filename, 'wb') as out_file:
        out_file.write(bytestring)


## Copy from Chrome > F12 > Network > particular request > Right-click > Copy > Copy as cURL (bash)
curl_get = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36' --compressed --insecure"
curl_save = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest/eedc621d-4102-40ee-8429-2372165b43f3?render=true' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=70d04811-95ac-4d7c-bd01-94ed7d2b642d; JSESSIONID=CFD726F8A8E60B15E038F493990EB8F5' -H 'Connection: keep-alive' --compressed --insecure"
curl_delete = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest/<DS_ID>' -X DELETE -H 'Origin: https://manila1.cpaas.awsiondev.infor.com:18010' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=70d04811-95ac-4d7c-bd01-94ed7d2b642d; JSESSIONID=CFD726F8A8E60B15E038F493990EB8F5' -H 'Connection: keep-alive' --compressed --insecure"

results_get = run_subprocess_and_get_results(curl_get)
quests = json.loads(results_get["stdout"].decode('utf-8'))
for quest in quests:
    results_save = run_subprocess_and_get_results(curl_save.replace("<DS_ID>", quest["id"]))
    write_to_file("backup_{}_{}.json".format(quest["name"], quest["id"]), results_save["stdout"])
    results_delete = run_subprocess_and_get_results(curl_delete.replace("<DS_ID>", quest["id"]))
