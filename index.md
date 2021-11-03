---
# this is an empty front matter - necessary for Jekyll
---

## Aktuelle Daten

Die aktuelle 7-Tage-Inzidenz vom **{{ "now" | date: "%d.%m.%Y" }}** liegt bei **{% include aktuelle_inzidenz.md %}**.

## Historische Daten

### Historie der Infektionen

Das Diagram zeigt den Verlauf der Gesamtzahl der Infektionen und der Neuinfektionen in Stutensee.

![Historie der Corona-Infektionen in Stutensee](infektionen.png)

### Historie der 7-Tage-Inzidenz

Das Diagram zeigt den Verlauf der Gesamtzahl der 7-Tage-Inzidenz in Stutensee.

![Historie 7-Tage-Inzidenz in Stutensee](inzidenz.png)

## Erklärung

Die Daten stammen von der Seite [https://corona.karlsruhe.de/aktuelle-fallzahlen](https://corona.karlsruhe.de/aktuelle-fallzahlen). Sie werden jeden Vormittag aktualisiert und auf dieser Basis die aktuelle 7-Tage-Inzidenz berechnet.
