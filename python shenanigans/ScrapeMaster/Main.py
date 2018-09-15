import json
import urllib.parse
import os

from Config import Config
from CommandGenerator import CommandGenerator
from CommandExecutor import CommandExecutor


pprint = lambda obj: print(json.dumps(obj, indent=2))
interact = lambda: exec("print('Entering interactive mode: Press Ctrl+Z to exit.\n');import code;code.interact(local={**locals(), **globals()})")


def search_jobs(keywords, page=1, data_collection=[]):
    search_template = "curl 'https://chalice-search-api.cloud.seek.com.au/search?siteKey=AU-Main&sourcesystem=houston&userqueryid=97ec6621797cfebd8a0f96a5bc59d139-1449239&userid=2734ad6f-4c64-49e0-aff0-6f615ec2cb82&usersessionid=2734ad6f-4c64-49e0-aff0-6f615ec2cb82&eventCaptureSessionId=bdbc2f3d-c84b-40c1-bf60-bad7564b3380&where=All+Australia&page=<PAGE>&seekSelectAllPages=true&keywords=<KEYWORDS>&include=seodata&isDesktop=true' -H 'Origin: https://www.seek.com.au' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: https://www.seek.com.au/java-java-jobs' -H 'Connection: keep-alive' -H 'X-Seek-Site: Chalice' --compressed"
    search_replace_dict = {
        "<KEYWORDS>": [urllib.parse.quote_plus(keywords)],
        "<PAGE>": [str(page)], }
    if not do_query_listings:
        print(">> Loading queries from listings.json")
        with open(os.path.join(Config.data_path, "listings.json"), 'r') as infile:
            return json.load(infile)
    if Config.auto_y or input("Run search jobs (y)? ") == 'y':
        executor = CommandExecutor()
        raw_executor_results = executor.run_commands_on_workers(
            commands=CommandGenerator.generate_commands(search_template, search_replace_dict),
            workers=1)
        json_response = json.loads(raw_executor_results[0]['stdout'].decode('utf-8'))
        data_collection += json_response['data']
        print("Current data_collection size: ", len(data_collection))
        if len(data_collection) < json_response['totalCount']:
            return search_jobs(keywords, page + 1, data_collection)
        print(">> Saving to listings.json")
        with open(os.path.join(Config.data_path, "listings.json"), 'w') as outfile:
            json.dump(data_collection, outfile, indent=4)
        return data_collection


def view_applications(ids):
    view_template = 'curl "https://ca-jobapply-ex-api.cloud.seek.com.au/jobs/<ID>/" -H "Origin: https://www.seek.com.au" -H "Accept-Encoding: gzip, deflate, br" -H "Accept-Language: en-US,en;q=0.9" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36" -H "Accept: application/json, text/plain, */*" -H "Referer: https://www.seek.com.au/job-apply/<ID>" -H "Connection: keep-alive" -H "X-Seek-Site: SEEK JobApply" --compressed'
    view_replace_dict = {"<ID>": ids, }
    if not do_query_applications:
        print(">> Loading queries from applications.json")
        with open(os.path.join(Config.data_path, "applications.json"), 'r') as infile:
            return json.load(infile)
    if Config.auto_y or input("Run view applications (y)? ") == 'y':
        executor = CommandExecutor()
        raw_executor_results = executor.run_commands_on_workers(
            commands=CommandGenerator.generate_commands(view_template, view_replace_dict),
            workers=20)
        raw_results = [raw_result for raw_result in raw_executor_results]
        results = [json.loads(raw_result['stdout'].decode('utf-8')) for raw_result in raw_results]
        print(">> Saving to applications.json")
        with open(os.path.join(Config.data_path, "applications.json"), 'w') as outfile:
            json.dump(results, outfile, indent=4)
        return results


def view_post(ids):
    view_template = 'curl "https://chalice-experience.cloud.seek.com.au/job/<ID>?isDesktop=true^&locale=AU" -H "Origin: https://www.seek.com.au" -H "Accept-Encoding: gzip, deflate, br" -H "Accept-Language: en-US,en;q=0.9" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36" -H "Accept: application/json, text/plain, */*" -H "Referer: https://www.seek.com.au/job/<ID>?type=standout" -H "If-None-Match: W/^\^"e86-I553tIAg7654QmbWH+FrADxPO7I^\^"" -H "Connection: keep-alive" -H "X-Seek-Site: Chalice" --compressed'
    view_replace_dict = {"<ID>": ids, }
    if not do_query_posts:
        print(">> Loading queries from posts.json")
        with open(os.path.join(Config.data_path, "posts.json"), 'r') as infile:
            return json.load(infile)
    if Config.auto_y or input("Run view posts (y)? ") == 'y':
        executor = CommandExecutor()
        raw_executor_results = executor.run_commands_on_workers(
            commands=CommandGenerator.generate_commands(view_template, view_replace_dict),
            workers=20)
        raw_results = [raw_result for raw_result in raw_executor_results]
        results = [json.loads(raw_result['stdout'].decode('utf-8')) for raw_result in raw_results]
        print(">> Saving to posts.json")
        with open(os.path.join(Config.data_path, "posts.json"), 'w') as outfile:
            json.dump(results, outfile, indent=4)
        return results


if __name__ == '__main__':  # lint using: flake8 --max-line-length=1000
    do_query_listings = False
    do_query_applications = False
    do_query_posts = False

    # load data
    queried_jobs = search_jobs("java")
    job_ids = set([job['id'] for job in queried_jobs])
    queried_applications = view_applications(job_ids)
    queried_posts = view_post(job_ids)

    # process data
    melbid = 1002

    visa_apps = [app for app in queried_applications if "visa" in str(app)]
    melb_visa_app_ids = [app['id'] for app in visa_apps if app['location']['id'] == melbid]
    melb_visa_posts = [post for post in queried_posts if post['id'] in melb_visa_app_ids]
    with open(os.path.join(Config.data_path, "melb_posts.json"), 'w') as outfile:
        json.dump(melb_visa_posts, outfile, indent=4)
    pprint([post['title'] for post in melb_visa_posts])

    interact()
