import pandas as pd
import requests
import tabula
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

# Load CSV
df = pd.read_csv('daten.csv')
df['Datum'] = df['Datum'].apply(pd.to_datetime)

# Get new data
soup = BeautifulSoup(requests.get('https://corona.karlsruhe.de/aktuelle-fallzahlen').content, 'html.parser')
last_update = datetime.strptime(soup.select('h5 > span:nth-child(3)')[0]['datetime'], '%Y %m %d'),

if last_update[0] > df.iloc[-1]['Datum']:
    print("Need new data.")
    # Get PDF and load it
    pdfUrl = soup.find('a', href=True, text='Fallzahlen in tabellarischer Form (PDF Download)')['href']
    t = tabula.read_pdf(pdfUrl, pages=1)
    # Parse data
    df = df.append({'Datum': last_update[0],
                    'Gesamtzahl': t[0][t[0]['Gemeinde'] == "Stutensee"].iloc[0]['Gesamtzahl'],
                    'Infiziert': t[0][t[0]['Gemeinde'] == "Stutensee"].iloc[0]['Derzeit Infiziert']},
                   ignore_index=True)

    # Save CSV
    df.to_csv('daten.csv', index=False)
else:
    print("No new data needed.")

print(df)

# Calculate values
df['Neue Infektionen'] = df['Gesamtzahl'].diff()
df['7-Tage Inzidenz'] = df['Gesamtzahl'].diff(periods=7) / 25052 * 100000

# Write image
ax = df.plot.line(x='Datum', y='Infiziert')
df.plot.line(x='Datum', y='Neue Infektionen', ax=ax).get_figure().savefig('infektionen.png')
df.plot.line(x='Datum', y='7-Tage Inzidenz').get_figure().savefig('inzidenz.png')

# Write 7-day-incidence
seven_day = round(df.iloc[-1]["7-Tage Inzidenz"], 1)
Path("_includes").mkdir(parents=True, exist_ok=True)
incidenceFile = open('_includes/aktuelle_inzidenz.md', 'w')
print(str(seven_day).replace(".", ","), file=incidenceFile, end='')
incidenceFile.close()
