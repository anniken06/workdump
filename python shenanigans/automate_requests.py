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


DS_IDs = [
    "c9a59c1c-a0c3-4574-9ac7-8da786c3e1d1",
    "33d5a219-9b73-40bb-86ae-0bfe59ec4966",
    "d7ceab73-f72f-41fa-9bf7-a67e5938ac51",
    "b111056b-eb06-4ede-9118-fac9a9bc9443",
    "f67b1eec-235d-42b3-9a0f-86b34efdb8b7",
    "23d84b6d-65b3-4434-b2ff-bc5916eb1f56",
    "eb313efa-32f4-4a3e-af8c-5379a1205db5",
    "0e508943-d5df-4503-9eb2-bd7d6fd390aa",
    "8ae3973d-88fe-42d5-a68d-553fe67c344c",
    "8884df38-2587-4813-bca4-6abecf596097",
    "946f8f43-064c-42e5-8e01-d83d0ef49b04",
    "59a0f7ff-dd2c-47b9-9112-18d5d606d4a9",
    "bfa6e62d-1491-4bff-ab97-8c9e4eab6724",
    "4fb2ebf8-70ad-40f3-adff-2013c497ed3e",
    "1689153c-d15a-4b8a-9c9c-3f5cb98cc364",
    "8378efe2-b185-43b1-a52f-050eedf7e4ff",
    "9261908b-04b2-42ca-baae-9620a0f7dd43",
    "d75af1fc-6e48-421f-b17c-e2a555d9aa1d",
    "e295de2f-17c0-4c4c-b2e5-4ac8a139eef5",
    "491031f7-bc1b-4243-8425-13b0917205be",
    "376a91f2-a717-4705-bb9f-da396df4bb4d",
    "1c9b57ff-fa95-456d-88bc-259a4fc49bb6",
    "b712eaf4-6b67-45a8-a5bd-e0f3fa7cae18",
    "abe2aaad-8e37-403c-ae19-ebfd1c97224e",
    "b2c67456-173c-4180-bb3c-570abe5e85b4",
    "d2782ce9-5405-4a22-bd79-ebd7c4df6ce1",
    "8bc1dd68-ce1c-4937-a26c-153e49a43084",
    "4fccf591-4111-4b2c-9ba7-a18e0f37b699",
    "e7b9760f-813d-4aca-91d1-7977f9f857e1",
    "0437cd75-dc63-4632-8507-57c4da8fbc49",
    "df7a81a2-316d-440d-b17b-d51bf275562a",
    "e36c582c-16aa-4afb-8e70-e6e5056ab2d7",
    "25c33efd-775b-4782-9bf6-de54deaeb6b7",
    "8f3bda2b-9995-4039-8846-82e88e974909",
    "9b6bfb2a-34cd-4460-92bf-7b54e54ee0db",
    "7924224e-e6dd-4c28-b13f-d94b83330fa7",
    "4ec574d7-0ba6-488d-b326-e82dde348ade",
    "71c06be9-d694-487c-9f83-f7a077eb8bc0",
    "b43137bf-61e8-40e6-858e-056043167f03",
    "d68f1f4a-015f-4fb2-84d6-05121e204cf3",
]

## Copy from Chrome > F12 > Network > particular request > Right-click > Copy > Copy as cURL (bash)
for DS_ID in DS_IDs:
    curl_save = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest/eedc621d-4102-40ee-8429-2372165b43f3?render=true' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=70d04811-95ac-4d7c-bd01-94ed7d2b642d; JSESSIONID=CFD726F8A8E60B15E038F493990EB8F5' -H 'Connection: keep-alive' --compressed --insecure"
    curl_delete = "curl 'https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest/<DS_ID>' -X DELETE -H 'Origin: https://manila1.cpaas.awsiondev.infor.com:18010' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://manila1.cpaas.awsiondev.infor.com:18010/coleman/' -H 'Cookie: XSRF-TOKEN=70d04811-95ac-4d7c-bd01-94ed7d2b642d; JSESSIONID=CFD726F8A8E60B15E038F493990EB8F5' -H 'Connection: keep-alive' --compressed --insecure"
    
    results_save = run_subprocess_and_get_results(curl_save.replace("<DS_ID>", DS_ID))
    write_to_file("backup_{}.json".format(DS_ID), results_save["stdout"])
    results_delete = run_subprocess_and_get_results(curl_delete.replace("<DS_ID>", DS_ID))
