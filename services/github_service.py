import aiohttp
from dotenv import load_dotenv

import os
from datetime import datetime, timedelta

load_dotenv()

headers = {
    "Authorization": f"token {os.getenv("GITHUB_TOKEN")}",
    "Accept": "application/vnd.github.v3+json"
}


async def get_commits_for_last_hour(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    since = (datetime.now() - timedelta(days=1000)).isoformat() + "Z"
    params = {
        "since": since,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                return await response.json()
            print(f"Ошибка {response.status} для {owner}/{repo} :(")
            return


async def get_team_commits(repos: list) -> dict:
    result = dict()

    for repo in repos:
        owner, name = repo["owner"], repo["name"]
        commits = await get_commits_for_last_hour(owner, name)
        if commits:
            result[name] = dict()
            result[name]["count"] = len(commits)
            result[name]["commits"] = list((commit["commit"]["author"]["name"], commit["commit"]["message"]) for commit in commits)

    return result
