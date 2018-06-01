import os
import re


def get_searchdir():
    data_path = "data"
    script_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_path, data_path)

def full_listdir(dir):
    return [os.path.join(dir, file) for file in os.listdir(dir)]

def read_dir_files(dir):
    str_lines = []
    for file in full_listdir(dir):
        with open(file, encoding="utf8") as f:
            str_lines += f.readlines()
    return str_lines

def find_user_posts(str_lines, upper_substr, lower_substr):
    should_store = False
    posts = []
    for line in str_lines:
        if upper_substr in line and not should_store:
            should_store = True
            temp_post = ""
        if should_store:
            temp_post += line
        if lower_substr in line and should_store:
            should_store = False
            posts += [temp_post]
    return posts

def filter_posts(posts, contains_conditions):
    filtered_posts = []
    for post in posts:
        if all([c in post for c in contains_conditions]):
            filtered_posts += [post]
    return filtered_posts

def display_posts(posts):
    for post in posts: 
        print(">"*20)
        print(post.replace("\n", "||"))
        print("<"*20)
        print()


if __name__ == "__main__":
    str_lines = read_dir_files(get_searchdir())
    posts = find_user_posts(str_lines, "> ‎Better Living Subdivision Carpool", "· More")
    filtered_posts = filter_posts(posts, ["6", "pm"])
    display_posts(filtered_posts)
    print("Finished printing all relevant posts.")

#import code; code.interact(local=dict(locals(), **globals()))