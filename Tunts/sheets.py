import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# authorize edit from google API
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(creds)
wks = gc.open_by_key("1Q7QDFjX5dbVvTmsxXvM3sQWS58Dqh-hM9wwjp3JI274").sheet1

# get all values from table
data = wks.get_all_values()
# store all values of the table on a dataframe
df = pd.DataFrame(data)
# delimit table
student = df[3:30]

for i in range(0, 24):
    studentAbsences = int(student.iloc[i, 2])
    absenceCollum = i + 4
    if studentAbsences > 15:
        wks.update_cell(absenceCollum, 7, "Reprovado por falta")
    else:
        p1 = int(student.iloc[i, 3])
        p2 = int(student.iloc[i, 4])
        p3 = int(student.iloc[i, 5])
        avgScore = round((p1 + p2 + p3) / 30)
        if avgScore >= 7:
            wks.update_cell(absenceCollum, 7, "Aprovado")
            wks.update_cell(absenceCollum, 8, "0")
        elif avgScore >= 5 or avgScore < 7:
            gradeFin = 10 - avgScore
            wks.update_cell(absenceCollum, 7, "Exame Final")
            wks.update_cell(absenceCollum, 8, gradeFin)
        else:
            wks.update_cell(absenceCollum, 7, "Reprovado por nota")
