import json
import argparse
from datetime import datetime, timedelta


def read_json_file(file_name):
    with open(file_name) as file:
        data = json.load(file)
        return data


def calculate_by_period(total_minutes, period, min_datetime, max_datetime):
    pre_total_minutes = total_minutes
    start = start_time = datetime.strptime(period['startTimeSchFormatted'], '%Y/%m/%d %H:%M')
    end = end_time = datetime.strptime(period['endTimeSchFormatted'], '%Y/%m/%d %H:%M')
    while start_time <= end_time:
        start_time = start_time + timedelta(minutes=1)

        if min_datetime is not None and start_time < min_datetime:
            continue

        if max_datetime is not None and start_time > max_datetime:
            continue

        # Saturday and Sunday
        if start_time.weekday() == 5 or start_time.weekday() == 6:
            total_minutes += 1
            continue

        # Work day
        if datetime(start_time.year, start_time.month, start_time.day, 9, 0, 0) < start_time < datetime(start_time.year, start_time.month, start_time.day, 18, 0, 0):
            continue

        total_minutes += 1
    hours = round((total_minutes-pre_total_minutes)/60)
    print("%s   ->   %s   %s:   %s" % (start, end, period['recipient'], hours))
    return total_minutes


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--file', '-f', help="json file name")
    arg_parser.add_argument('--start', '-s', help="start time with format %Y/%m/%d %H:%M")
    arg_parser.add_argument('--end', '-e', help="end time with format %Y/%m/%d %H:%M")
    args = arg_parser.parse_args()
    min_datetime = max_datetime = None

    if args.file is None:
        print("please enter file name!")
        exit()

    if args.start is not None:
        min_datetime = datetime.strptime(args.start, '%Y/%m/%d %H:%M')

    if args.end is not None:
        max_datetime = datetime.strptime(args.end, '%Y/%m/%d %H:%M')

    data = read_json_file(args.file)
    f_layer = data['fLayer']
    weeks = f_layer['weeks']
    result = {}
    for week in weeks:
        layers = week['layers']
        for layer in layers:
            periods = layer['periods']
            for period in periods:
                if period['recipient'] not in result:
                    result[period['recipient']] = calculate_by_period(0, period, min_datetime, max_datetime)
                else:
                    result[period['recipient']] = calculate_by_period(result[period['recipient']], period, min_datetime, max_datetime)

    for k, v in result.items():
        print("%s: %s" % (k, round(v/60)))
