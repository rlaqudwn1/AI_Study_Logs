import os
import sys
import argparse
import pandas as pd
import math
import time
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Constants
STEAM_ID64_OFFSET = 76561197960265728
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "steam_data" / "new_steam"
CHUNK_DIR = DATA_DIR / "user_chunks"
OUTPUT_DIR = DATA_DIR / "crawled_data"

# Validation
if not STEAM_API_KEY:
    print("Warning: STEAM_API_KEY not found in environment variables.")

def validate_and_convert_id(steam_id):
    """
    Validates and converts SteamID to SteamID64 format.
    """
    try:
        steam_id_int = int(steam_id)
        if steam_id_int < STEAM_ID64_OFFSET:
            return str(steam_id_int + STEAM_ID64_OFFSET)
        return str(steam_id_int)
    except ValueError:
        return None

def prepare_chunks(num_chunks=10):
    """
    Reads players.csv and private_steamids.csv, filters users,
    converts IDs, and splits them into chunks.
    """
    print(f"Base Directory: {BASE_DIR}")
    print("Loading data...")
    players_path = DATA_DIR / "players.csv"
    private_path = DATA_DIR / "private_steamids.csv"
    
    if not players_path.exists():
        print(f"Error: {players_path} does not exist.")
        return

    # Read players (has header)
    df_players = pd.read_csv(players_path)
    all_player_ids = set(df_players['playerid'].astype(str))
    print(f"Total players in players.csv: {len(all_player_ids)}")
    
    # Read private IDs
    try:
        # Check header by reading first line or using pandas sniffing
        # Assuming no header based on previous context, but being robust
        df_private = pd.read_csv(private_path, header=None)
        # Verify first element is digit
        if not str(df_private.iloc[0, 0]).isdigit():
             df_private = pd.read_csv(private_path)
        
        private_ids = set(df_private.iloc[:, 0].astype(str))
    except Exception as e:
        print(f"Error reading private_steamids.csv: {e}")
        private_ids = set()
        
    print(f"Total private IDs: {len(private_ids)}")
    
    print("Filtering and converting IDs...")
    valid_ids = []
    
    converted_private_ids = set()
    for pid in private_ids:
        c_pid = validate_and_convert_id(pid)
        if c_pid:
            converted_private_ids.add(c_pid)

    for pid in all_player_ids:
        converted_id = validate_and_convert_id(pid)
        if converted_id and converted_id not in converted_private_ids:
            valid_ids.append(converted_id)
            
    print(f"Total users to crawl after filtering: {len(valid_ids)}")
    
    # Split into chunks
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    chunk_size = math.ceil(len(valid_ids) / num_chunks)
    
    for i in range(num_chunks):
        chunk = valid_ids[i * chunk_size : (i + 1) * chunk_size]
        chunk_file = CHUNK_DIR / f"user_ids_{i}.txt"
        with open(chunk_file, 'w') as f:
            for uid in chunk:
                f.write(f"{uid}\n")
        print(f"Saved chunk {i} with {len(chunk)} IDs to {chunk_file}")


# Sync Crawling Logic

def fetch(url, params, retries=3):
    """
    Sync fetch with retry logic and rate limit handling.
    """
    backoff = 1
    for i in range(retries):
        try:
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    print(f"Warning: Non-JSON response from {url}")
                    return None
            elif response.status_code in (429, 420):
                # Rate limit hit
                wait_time = backoff * 4  # Longer wait for sync
                print(f"Rate limited ({response.status_code}). Waiting {wait_time}s...")
                time.sleep(wait_time)
                backoff *= 2
            elif response.status_code >= 500:
                # Server error, retry
                print(f"Server error {response.status_code}. Retrying in {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                # Client error (400, 401, 403, 404), do not retry
                print(f"Client error {response.status_code} for URL {url}. Skipping.")
                return None
        except requests.exceptions.RequestException as e:
            # Network error, retry
            print(f"Network error: {e}. Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff *= 2
            
    print(f"Max retries exceeded for request")
    return None

def get_player_summary(user_id):
    """
    GetPlayerSummaries for a single user.
    """
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        'key': STEAM_API_KEY,
        'steamids': user_id
    }
    return fetch(url, params)

def get_owned_games(user_id):
    """
    GetOwnedGames for a single user.
    """
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': STEAM_API_KEY,
        'steamid': user_id,
        'format': 'json',
        'include_appinfo': 1,
        'include_played_free_games': 1
    }
    return fetch(url, params)

def prune_steam_payload(payload: dict, keep_name: bool = True) -> dict:
    """
    Refines the Steam data payload to a minimum schema.
    """
    summary = payload.get("summary", {})
    
    out = {
        "steamid": payload.get("steamid"),
        "timecreated": summary.get("timecreated"),  # optional
        "loccountrycode": summary.get("loccountrycode"),  # optional
        "game_count": payload.get("game_count", 0),
        "games": []
    }

    raw_games = payload.get("games", [])
    
    for g in raw_games:
        gg = {
            "appid": g.get("appid"),
            "playtime_forever": g.get("playtime_forever", 0),
        }
        if keep_name:
            gg["name"] = g.get("name")
        out["games"].append(gg)

    return out

def process_user(steamid, output_file):
    """
    Process a single user:
    1. Get Summary
    2. Get Owned Games
    3. Prune and Save
    """
    # 1. Get Summary
    summary_data = get_player_summary(steamid)
    
    # 2. Get Owned Games
    time.sleep(0.2) # Small delay between calls for same user
    games_data = get_owned_games(steamid)
        
    # Validation
    if games_data is None: 
        return False

    # Extract Summary Info
    player_info = {}
    if summary_data and 'response' in summary_data and 'players' in summary_data['response']:
        players = summary_data['response']['players']
        if players:
            player_info = players[0]

    # Extract Games Info
    games_list = []
    game_count = 0
    if games_data and 'response' in games_data:
        games_resp = games_data['response']
        games_list = games_resp.get('games', [])
        game_count = games_resp.get('game_count', 0)

    # Prepare Payload for Pruning
    full_payload = {
        "steamid": steamid,
        "summary": player_info,
        "game_count": game_count,
        "games": games_list
    }
    
    # Prune
    final_record = prune_steam_payload(full_payload, keep_name=True)
    final_record['crawled_at'] = time.time()
    
    # Save
    try:
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(final_record, ensure_ascii=False) + "\n")
        return True
    except Exception as e:
        print(f"File write error for {steamid}: {e}")
        return False

def crawl_chunk(chunk_id, retry_zeros=False):
    chunk_file = CHUNK_DIR / f"user_ids_{chunk_id}.txt"
    if not chunk_file.exists():
        print(f"Chunk file {chunk_file} not found. Please run with --prepare first.")
        return

    print(f"Processing chunk {chunk_id} (Synchronous Mode)...")
    if retry_zeros:
        print("Option --retry_zeros matched: Re-crawling users with game_count=0.")

    with open(chunk_file, 'r') as f:
        target_ids = [line.strip() for line in f if line.strip()]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"crawled_users_{chunk_id}.jsonl"

    # Resume logic
    crawled_ids = set()
    if output_file.exists():
        print(f"Found existing output file {output_file}. Resuming...")
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if 'steamid' in data:
                        # If retry_zeros is True, we treat game_count=0 as valid ONLY if it's > 0
                        # effectively 'ignoring' the 0s so they get picked up again.
                        if retry_zeros:
                            if data.get('game_count', 0) > 0:
                                crawled_ids.add(data['steamid'])
                        else:
                            crawled_ids.add(data['steamid'])
                except json.JSONDecodeError:
                    continue
        count_ignored = 0
        if retry_zeros:
             # Just for reporting purpose, calculate how many we are ignoring
             # (This is approximate as we didn't store all lines in memory, but good enough logic above)
             pass

        print(f"Already crawled {len(crawled_ids)} users (Ready to skip).")

    ids_to_crawl = [uid for uid in target_ids if uid not in crawled_ids]
    total_to_crawl = len(ids_to_crawl)
    print(f"Remaining users to crawl: {total_to_crawl}")

    completed_count = 0
    for i, steamid in enumerate(ids_to_crawl):
        loop_start = time.time()
        success = process_user(steamid, output_file)
        
        # Progress every 10 users
        completed_count += 1
        if completed_count % 10 == 0:
             print(f"Progress: {completed_count}/{total_to_crawl} ({(completed_count/total_to_crawl)*100:.1f}%)")
        
        # Smart Sleep: Target 1.2s per user
        elapsed = time.time() - loop_start
        wait_time = max(0, 1.2 - elapsed)
        if wait_time > 0:
            time.sleep(wait_time)

    print(f"Chunk {chunk_id} completed.")

def main():
    parser = argparse.ArgumentParser(description="Steam User Crawler (Sync)")
    parser.add_argument("--prepare", action="store_true", help="Prepare chunks from source CSVs")
    parser.add_argument("--chunk", type=int, help="Single chunk ID to crawl (0-9)")
    parser.add_argument("--from_chunk", type=int, help="Start crawling from this chunk ID to the end")
    parser.add_argument("--chunks_count", type=int, default=10, help="Number of chunks to split into")
    parser.add_argument("--retry_zeros", action="store_true", help="Re-crawl users who have game_count: 0 in existing data")
    
    args = parser.parse_args()
    
    if args.prepare:
        prepare_chunks(args.chunks_count)
    elif args.chunk is not None:
        crawl_chunk(args.chunk, retry_zeros=args.retry_zeros)
    elif args.from_chunk is not None:
        for i in range(args.from_chunk, args.chunks_count):
            print(f"\n=== Starting Chunk {i} ===\n")
            crawl_chunk(i, retry_zeros=args.retry_zeros)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
