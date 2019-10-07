## Opsgenie Duty Parser

This tool is used to parse and calculate number of hours that a team member worked for duty in month.

### The rules are:
- On weekend (Sunday & Saturday), full of working hours are paid.
- On weekdays, only accept the hours that NOT in working time range (from 9:00 to 18:00)

### Usage:
```shell
python duty_parser.py -f duty_september.json -s "2019/09/01 00:00" -e "2019/10/01 00:00"
```
- `-f`: json file name
- `-s`: start time with format Y/m/d H:M
- `-e`: end time with format Y/m/d H:M
