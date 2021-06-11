import pandas as pd
import requests
import matplotlib.pyplot as plt
import tabula
from bs4 import BeautifulSoup
from datetime import datetime

# Run this script once a day

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

# plt.show()
