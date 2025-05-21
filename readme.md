# Výzkumná otázka:

Jaká cizí pracoviště citují výstupy ZČU?

# Cíl práce: 

Vizualizovat tzv. citační mapu znázorňující, která cizí pracoviště nejvíce citují publikační výstupy našeho výzkumníka/skupiny/pracoviště, umožňující identifikovat:
- Kde dochází k vzájemnému citování, 
- kde my citujeme je, ale oni nás zpětně nikoliv, 
- kde oni citují hojně nás, ale my je nikoliv.

---
# Vypracovali:
- Romová Jana - Bublle map
- Vladař Dominik - Square-tree map

---
# GitHub
https://github.com/romova/SCOPUS_API.git

Obsahuje adresáře:
- Data - scripty pro zisk a čištění dat a zkompletovaná data
- Citation map - vizualizace, transformovaná data a kod pro transformaci
- Square tree map - vizualizace

---
# Vypracování
Obě práce byly vytvořeny jako webové stránky pomocí knihovny D3.js

## Zdroj dat
- SCOPUS API - články, instituce, autoři
- CrossRef API - citace a reference článků
- geo-coding API - geo souřadnice institucí a měst