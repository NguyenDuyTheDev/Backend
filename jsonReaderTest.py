import json
from collections import Counter
from pprint import pprint
from datetime import datetime

current = datetime.now()
print(current.year)

data = json.load(open('watch-history.json', encoding="utf8"))
remove_advertise_data = [x for x in data if "details" not in x]
this_year_data = [x for x in remove_advertise_data if int(x["time"].split('-')[0]) == 2024]
only_youtube_data = [x for x in this_year_data if x["header"] == "YouTube"]
cleaned_data = only_youtube_data

#pprint("First Video of the year: " + cleaned_data[-1]["title"] + " - " + cleaned_data[-1]["subtitles"][0]["name"])

total_video = 0
watched = Counter()
watched_artist = Counter()
watched_per_month = Counter()
watched_per_day = Counter()
watched_per_hour = Counter()
month_extracted_data = []

for item in cleaned_data:
    if "titleUrl" not in item:
        # Watched a video that has been removed
        continue
    title = item["title"][7:]
    url = item["titleUrl"]
    key = f"{title} @> {url}"
    watched[key] += 1

    if "subtitles" in item:
        artist = item["subtitles"][0]["name"]
        url = item["subtitles"][0]["url"]
        key = f"{artist} @> {url}"
        watched_artist[key] += 1

    time = item["time"].split('-')[1]
    key = time
    watched_per_month[key] += 1

    time = item["time"].split('T')[0]
    key = time
    watched_per_day[key] += 1

    time = item["time"].split('T')[1][0:2]
    key = time
    watched_per_hour[key] += 1

    total_video += 1

for month in range(1, 13):
    month_cleaned_data = [x for x in cleaned_data if int(x["time"].split('-')[1]) == month]

    month_total_video = 0
    month_watched = Counter()
    month_watched_artist = Counter()
    month_watched_per_hour = Counter()

    for item in month_cleaned_data:
        if "titleUrl" not in item:
            # Watched a video that has been removed
            continue
        title = item["title"][7:]
        url = item["titleUrl"]
        key = f"{title} @> {url}"
        month_watched[key] += 1

        if "subtitles" in item:
            artist = item["subtitles"][0]["name"]
            url = item["subtitles"][0]["url"]
            key = f"{artist} @> {url}"
            month_watched_artist[key] += 1

        time = item["time"].split('T')[1][0:2]
        key = time
        month_watched_per_hour[key] += 1

        month_total_video += 1

    month_extracted_data.append({
        "month": month,
        "month_total_video": month_total_video,
        "month_watched": month_watched.most_common(10),
        "month_watched_artist": month_watched_artist.most_common(10),
        "month_watched_per_hour": month_watched_per_hour.most_common(10),
    })

extracted_data = {
    "first_video": cleaned_data[-1]["title"] + " - " + cleaned_data[-1]["subtitles"][0]["name"],
    "total_video": total_video,
    "watched": watched.most_common(10),
    "artist": watched_artist.most_common(10),
    "watcher_per_month": watched_per_month.most_common(10),
    "watched_per_day": watched_per_day.most_common(10),
    "watched_per_hour": watched_per_hour.most_common(10),
    #"monthly_data": month_extracted_data
}
pprint(extracted_data)

'''
watched = Counter()
for item in json.load(open('watch-history.json', encoding="utf8")):
    if "titleUrl" not in item:
        # Watched a video that has been removed
        continue
    title = item["title"]
    url = item["titleUrl"]
    key = f"{title} @> {url}"
    watched[key] += 1

pprint(watched.most_common(20))
'''