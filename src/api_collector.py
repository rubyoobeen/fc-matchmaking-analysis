import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("NEXON_API_KEY")
# print(f"API Key loaded: {API_KEY[:10] if API_KEY else 'NOT FOUND'}")

BASE_URL = "https://open.api.nexon.com"

HEADERS = {
    "x-nxopen-api-key": API_KEY
}

# get user ouid from nickname 
def get_ouid(nickname):
    url = f"{BASE_URL}/fconline/v1/id"
    params = {"nickname": nickname}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        return response.json()["ouid"]
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return None

# get list of match IDs for a user
def get_match_ids(ouid, matchtype=30, offset=0, limit=100):
    url = f"{BASE_URL}/fconline/v1/match"
    params = {
        "ouid": ouid,
        "matchtype": matchtype,
        "offset": offset,
        "limit": limit,
        "orderby": "desc"
    }
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return []

# get details of one match
def get_match_detail(matchid):
    url = f"{BASE_URL}/fconline/v1/match-detail"
    params = {"matchid": matchid}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return None

if __name__ == "__main__":
    nickname = "nickname-placeholder"

    print(f"Getting ouid for: {nickname}")
    ouid = get_ouid(nickname)
    print(f"ouid: {ouid}")
    
    if ouid:
        print(f"\nGetting match IDs...")
        match_ids = get_match_ids(ouid)
        print(f"Found {len(match_ids)} matches")
        
        all_matches = []
        for i, matchid in enumerate(match_ids):
            print(f"Fetching match {i+1}/{len(match_ids)}...")
            detail = get_match_detail(matchid)
            if detail:
                all_matches.append(detail)
        
        # Save to JSON (raw complete data)
        with open("data/matches_raw.json", "w", encoding="utf-8") as f:
            json.dump(all_matches, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(all_matches)} matches to data/matches_raw.json")