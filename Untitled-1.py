from PyQt5.QtCore import QDate

highlighted_dates = [QDate(2023, 11, 10), QDate(2023, 11, 15)]

# Append more QDate objects to the list
highlighted_dates.append(QDate(2023, 11, 20))
highlighted_dates.append(QDate(2023, 11, 25))

# Now, the list `highlighted_dates` contains the additional dates
print(highlighted_dates)

'''
file_dict = {
    '2023-11-07-tjytjyd.enc.GitDiarySync': './.enc.GitDiarySync/Nov-2023/07/2023-11-07-tjytjyd.enc.GitDiarySync',
    '2023-11-07-xsf.enc.GitDiarySync': './.enc.GitDiarySync/Nov-2023/07/2023-11-07-xsf.enc.GitDiarySync',
    '2023-11-09-aaa.enc.GitDiarySync': './.enc.GitDiarySync/Nov-2023/07/2023-11-09-aaa.enc.GitDiarySync'
}
dates = []
for file_path in file_dict.values():
    date = file_path.split('/')[-1][:10]
    dates.append(date)

print(dates)

years, months, days = zip(*(date.split('-') for date in dates))

i = 1
print(years[i], months[i], days[i])

date_dict = {} 
for file_path, year, month, day in zip(file_dict.values(), years, months, days):
    date = (year, month, day)
    date_dict[file_path] = date

print(date_dict)

opposet_dict = {} # set inside the dict

for k, v in date_dict.items():
    if v in opposet_dict:
        opposet_dict[v].add(k)
    else:
        opposet_dict[v] = {k}

print("\n")
print(opposet_dict)
print("====")
for date, filenames in opposet_dict.items():
    print(f"Date: {date}")
    for filename in filenames:
        print(f"   Filename: {filename}")

'''

