import csv

def navblue_to_myflightbook(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fields = ['DateOut', 'Text4', 'From', 'To', 'PIC', 'SIC']
        writer = csv.DictWriter(outfile, fieldnames=fields)

        writer.writeheader()

        dateText = ''

        for row in reader:

            #Date doesn't appear on every row
            if row['ï»¿RaidoLab_Name'].strip():
                dateText = row['ï»¿RaidoLab_Name'].strip()

            #Flags
            flagsString = row['Text4'].split(',')

            flags = {
                'P': False, #Positioning
                'T': False, #Training
                'X': False #In Command
            }

            for flag in flagsString:
                cleaned_flag = ''.join([char for char in flag if not char.isdigit()])
                flags[cleaned_flag] = True
            
            if not flags['T']:
               continue
            
            #Calculate Times
            duration = time_difference(row['TimeText_ActualValidFrom'], row['TimeText_ActualValidToString'])

            if duration == 0:
                continue

            picTime = 0
            sicTime = duration
            
            if flags['X']:
                picTime = duration

            #Other fields
            srcAirport = row['Text11']
            dstAirport = row['Text12']

            writer.writerow({
                'DateOut': dateText,
                'From': srcAirport,
                'To': dstAirport,
                'PIC': picTime,
                'SIC': sicTime
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
