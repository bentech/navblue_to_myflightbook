import csv
from datetime import datetime

def navblue_to_myflightbook(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fields = ['Date', 'Tail Number', 'Route', 'PICUS', 'SIC', 'Flight Start', 'Flight End', 'Total Flight Time', 'Landings', 'Comments']
        writer = csv.DictWriter(outfile, fieldnames=fields)

        writer.writeheader()

        for row in reader:
            # Date doesn't appear on every row
            if row['ï»¿RaidoLab_Name'].strip():
                dateText = row['ï»¿RaidoLab_Name'].strip()

            # Flags
            flagsString = row['Text4'].split(',')

            if any('P' in flag for flag in flagsString):
                continue
            
            if any('BK' in flag for flag in flagsString):
                continue

            flags = {
                'P': False,  # Positioning
                'T': False,  # Training
                'X': False,  # In Command
            }

            for flag in flagsString:
                cleaned_flag = ''.join([char for char in flag if not char.isdigit()])
                flags[cleaned_flag] = True
            
            duration = time_difference(row['TimeText_ActualValidFrom'], row['TimeText_ActualValidToString'])
            
            if duration == 0:
                continue
            
            picusTime = 0
            sicTime =duration

            if flags['X']:
                picusTime = sicTime

            # Combine From and To into Routes
            srcAirport = row['Text11']
            dstAirport = row['Text12']
            routes = f"{srcAirport} {dstAirport}"

            # Clean and parse Times
            flight_start_str = row['TimeText_ActualValidFrom'].strip()
            flight_end_str = row['TimeText_ActualValidToString'].strip()

            flight_start = datetime.strptime(f"{dateText}{flight_start_str}", "%d%b%y%H%M")
            flight_end = datetime.strptime(f"{dateText}{flight_end_str}", "%d%b%y%H%M")

            reg = row['Text10']

            writer.writerow({
                'Date': dateText,
                'Tail Number': reg,
                'Route': routes,
                'PICUS': picusTime/60,
                'SIC': sicTime/60,
                'Flight Start': flight_start.strftime("%d%b%y %H:%M"),
                'Flight End': flight_end.strftime("%d%b%y %H:%M"),
                'Total Flight Time' : duration/ 60,
                'Landings' : 1,
            })
            
def time_difference(time1, time2):
    # Remove non-digit characters
    clean_time1 = ''.join(filter(str.isdigit, time1)).rjust(4, '0')
    clean_time2 = ''.join(filter(str.isdigit, time2)).rjust(4, '0')

    minutes1 = int(clean_time1[:2]) * 60 + int(clean_time1[2:])
    minutes2 = int(clean_time2[:2]) * 60 + int(clean_time2[2:])

    # difference in minutes
    return minutes2 - minutes1

if __name__ == '__main__':
    navblue_to_myflightbook('Report.csv', 'myflightbook.csv')
