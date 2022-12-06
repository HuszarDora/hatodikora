# 1. feladat: 60-70%
#   Építsetek egy 5 elemű portfóliót ETF-ből. (unconstrict optimalization) (lehetőleg ne 1 közeli korelációukat)
#   választási szempontok:
#       kellő hosszúságú history renelkezésre állása (legyen benne a 2008-as, min 10 év)
#       (etfdb.com, yahoo finance)
#   multi asset class (equity, fixed income,commodity energy, commodity raw materials, commodity food)
#   Historikus napi hozamok alapján
#   Portfólió hozamának számítása:
#       Feltételezzük, hogy a portfólió napi szinten újrasúlyozódik, ami azt jelenti, hogy a portfólió súlyokat fixen tartjuk.
#       thát a portfólió effektív hozama megegyezik az alkotó effektív hozamának portfólió súlyokkal súlyozott átlagával
#   A sharp mutató szzámításához szükséges kockázatmentes hozam legyen a USD Govt yield curve 3 hónapos tenorjából
#   Találjátok ki mi az optimális portfólió súly (ex post optimization)
#       Célfüggvény 1: globális maximális sharpe portfólió, az adott összes rendelkezésre álló közös hisory-ra vonatkozóan, (pl ha 2008-tól van adat, akkor 2008 és 2022 közötti időszakban mért sharp mutató)
#       Célfüggvény 2: megelőző 5 év csúszóablakos sharpe portfólió (ennél az optimális súlyok naponta fognak változni az ablak mozdulásával)
#       Célfüggvény 3: maximális drawdown minimalizálása (https://corporatefinanceinstitute.com/resources/wealth-management/maximum-drawdown/)
#       Célfüggvény 4: maximális drawdown minimalizálása 5 éves csúszóablakoknál
#   Optimális portfóliósúlyok ábrázolása (1. és 3. esetben egy pont lesz)
#   Szöveges elemzés: hogyan változott és miért
#   Sharp mutató: exess returnből számoljuk (hozam-kockázatmentes)
#   Drawdownnál nem kell levonni a kockázatmentes hozamot
#   5 éves csúszóablakosnál: portfólió szórása
#   chartokat le lehet menteni file-ba