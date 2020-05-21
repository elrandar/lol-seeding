import csv
import sys
from riotwatcher import LolWatcher, ApiError

lol_watcher = LolWatcher('') //API KEY
region = 'euw1'

elo_tier = {
    "IRON": 0,
    "BRONZE": 10,
    "SILVER": 20,
    "GOLD": 30,
    "PLATINUM": 35,
    "DIAMOND": 50,
    "MASTER": 70,
    "GRANDMASTER": 80,
    "CHALLENGER": 100
}

elo_rank = {
    "I": 5,
    "II": 4,
    "III": 3,
    "IV": 0
}


def open_file(csvFilename):

    with open(csvFilename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            compute_team(row)

def compute_team(team):
    print('Team:', team["teamname"])
    strings = ["invocateur1", "invocateur2","invocateur3","invocateur4","invocateur5"]
    flexEloSum = 0
    flexEloN = 5
    rankedEloSum = 0
    rankedEloN = 5
    for i in range(5):
        print('\t', team[strings[i]])
        elo = get_elo(team[strings[i]])
        if (elo[0] != -1):
            rankedEloSum += elo[0]
        else:
            rankedEloN -= 1
        if (elo[1] != -1):
            flexEloSum += elo[1]
        else:
            flexEloN -= 1
        print("\t\t", elo)
    print("Ranked ELO :", rankedEloSum / rankedEloN)
    print("Flex ELO :", flexEloSum / flexEloN, '\n')
        # print('\t\t', get_elo(team[strings[i]]))


def get_elo(summoner_name):
    try:
        me = lol_watcher.summoner.by_name(region, summoner_name)
    except:
        print("\t\tSummoner not found")
        return -1, -1
    else:
        ranked_stats = lol_watcher.league.by_summoner(region, me['id'])
        if (len(ranked_stats) == 0):
            print("\t\tNo data")
            return -1, -1
        else:
            ranked_elo = compute_elo(ranked_stats[0]['rank'], ranked_stats[0]['tier'])
            print("\t\tRanked :", ranked_stats[0]['tier'], ranked_stats[0]['rank'], ranked_elo)
            if (len(ranked_stats) != 1):
                flex_elo = compute_elo(ranked_stats[1]['rank'], ranked_stats[1]['tier'])
                print("\t\tFlex :", ranked_stats[1]['tier'], ranked_stats[1]['rank'], flex_elo)
            else:
                flex_elo = -1
                print("\t\tFlex : UNRANKED")
            return (ranked_elo, flex_elo)

def compute_elo(rank, tier):
    return elo_rank[rank] + elo_tier[tier]


def main(argv):
    print("opening thingie :")
    open_file(argv[1])


if __name__ == '__main__':
    main(sys.argv)