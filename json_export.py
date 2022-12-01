# usr/bin/python

from git import Repo
import json
import re, signal, sys, time, pwn, pdb, os    # Librerías que no te hace falta instalar


# iter commit lo metemos en una lista, le dicmos el max numero de commit (todos) 
def handler_signal(signal, frame):
    print("\n\n [!] Out ....... \n")
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, handler_signal)


def extract(path):
    repo = Repo(path)       # Crea un objeto que te permite interactuar con el repositorio que hay en el path
    return repo.iter_commits()


def transform(commits, length):
    progress = [" " for i in range(102)]
    progress[0] = "["
    progress[-1] = "]"
    all_matches = []

    print("Progress:\t", end="")
    for i in range(len(progress)):
        print(progress[i], end="")
    print("\t0 %")

    count = 0
    index = int(count * 100 / length)

    patterns = [
        re.compile(r".{6}private[-.\s]keys.{6}", re.IGNORECASE),
        re.compile(r".{6}password.{6}", re.IGNORECASE),
        re.compile(r".{6}confidential.{6}", re.IGNORECASE),
        re.compile(r".{10}secret.{10}", re.IGNORECASE),
    ]

    words = [
        "private keys",
        "password",
        "confidential",
        "secret"
    ]

    results = {}
    for word in words:
        results[word] = []

    for commit in commits:
        for i in range(len(patterns)):
            word = words[i]
            matches = patterns[i].finditer(commit.message)
            for match in matches:
                if match != None:
                    results[word].append({"author": f"{commit.author}", "message": f"{commit.summary}", "authored_datetime": f"{commit.authored_datetime}"})
                    all_matches.append(match)

        count += 1
        if index != int(count * 100 / length):
            os.system('cls||clear')
            progress[index + 1] = ">"
            print("Progress:\t", end="")
            for i in range(len(progress)):
                print(progress[i], end="")
            print(f"\t{index} %")
            index = int(count * 100 / length)

    os.system('cls||clear')
    print("Progress:\t", end="")
    for i in range(len(progress)):
        print(progress[i], end="")
    print("\t100 %")
    print("Finished!")

    return all_matches, results


def load(all_matches):
    for match in all_matches:
        print(match)


def load_json(results):
    json_string = json.dumps(results, indent=4)
    with open("results.json", "w") as json_file:
        json_file.write(json_string)


def load_txt(results):
    json_string = json.dumps(results, indent=4)
    with open("results.txt", "w") as json_file:
        json_file.write(json_string)


if __name__ == "__main__":
    REPO_DIR = "./skale/skale-manager"
    commits = extract(REPO_DIR)
    length = len(list(commits))
    all_matches, results = transform(extract(REPO_DIR), length)
    load_json(results)
    load_txt(results)
