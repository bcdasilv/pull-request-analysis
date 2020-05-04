import sys
import requests
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 4:
        print("Invalid arguments. Usage: python3 scrapeGithubPR.py <repoOwner> <repoName> <numPages>")
        exit(1)

    repoOwner = sys.argv[1]
    repoName = sys.argv[2]
    numPages = int(sys.argv[3])
    get_closed_unmerged_prs(repoOwner, repoName, numPages)
    

def get_closed_unmerged_prs(repoOwner, repoName, numPages):
    f = open(repoOwner + "_" + repoName + ".csv", "w")
    f.write("project, pr_id, user, pr_title, URL\n")
    for i in range(numPages + 1):
        page = requests.get("https://github.com/" + repoOwner + "/" + repoName + "/pulls?page=" + str(i+1) + "&q=is%3Apr+is%3Aclosed+is%3Aunmerged")
        soup = BeautifulSoup(page.content, 'html.parser')
        spanElements = soup.findAll("span", {"class": "opened-by"})
        for spanEl in spanElements:
            project = repoOwner + "/" + repoName
            pr_id = spanEl.text.strip()[0:7].strip()[1:]
            user = spanEl.parent.find('a').text
            pr_title = spanEl.parent.parent.find('a').text
            url = "https://github.com/" + project + "/pull/" + pr_id
            f.write(project + "," + pr_id + "," + user + "," + pr_title + "," + url + "\n")
    f.close()



if __name__ == "__main__":
    main()