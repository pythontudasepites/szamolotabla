from math import *
from itertools import product
import tkinter as tk

root = tk.Tk()
root.title('Számolótábla')


def get_cell_indexes(entry_widget):
    gi = entry_widget.grid_info()
    return gi.get('row'), gi.get('column')


def convertible_to_int(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False


def convertible_to_float(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False


def convertible_to_complex(s: str):
    try:
        complex(s)
        return True
    except ValueError:
        return False


def get_cell_numvalue(ci, ri):
    """A megadott oszlop- és sorindexű beviteli mező tartalmának megfelelő számértékét adja vissza, ha az
    számként értelmezhető. Ha nem, akkor magát a tartalmat."""
    cell_value: str = ebx_vars[(ri, ci)][0].get()
    if convertible_to_int(cell_value):
        return int(cell_value)
    elif convertible_to_float(cell_value):
        return float(cell_value)
    elif convertible_to_complex(cell_value):
        return complex(cell_value)
    else:
        return cell_value


def converted_cellref(cell_str) -> str:
    """A 'cell(B:1)' konvertálása 'cell(2,1)' formára"""
    arg: str = cell_str.strip('cell()')
    args = arg.split(':')
    ci, ri = ord(args[0].upper()) - ord('A') + 1, int(args[1])
    return cell_str.replace(arg, f'{ci},{ri}')


def find_cellref(s: str, pattern='cell(??)'):
    eleje, vége = pattern.split('??')
    if eleje in s:
        k = s.find(eleje)
        v = s[k + len(eleje):].find(vége)
        return sub if ':' in (sub := s[k:k + len(eleje) + v + 1]) else ''
    return ''


def eval_cell_content_event_handler(e):
    ebx = e.widget  # Az eseménnyel érintett beviteli mező.
    eval_cell_content(ebx)


def eval_cell_content(entry_widget):
    # Az argumentumban kapott beviteli mező kontrollváltozójának kikérése.
    ebx_var = ebx_vars.get(get_cell_indexes(entry_widget))[0]
    # A kontrollváltozó értékének, vagyis a beviteli mező tartalmának kikérése.
    cv = ebx_var.get()
    # Ha a mező nem üres, és az első karakter egy = jel, akkor kiértékeljük a tartalmát.
    if cv != '' and cv[0] == '=':
        # A továbbiakban az = jel utáni karaktersorral dolgozunk.
        expr = cv[1:]
        # Ha van kifejezést meghatározó karaktersor az = jel után, akkor azt az egyenlőségjellel együtt
        # eltároljuk, majd megkíséreljük kiértékelni.
        if expr:
            # Eltároljuk a nem üres kifejezést az adott cellához, hogy később elő lehessen hívni
            # megtekintéshez vagy szerkesztéshez.
            ebx_vars.get(get_cell_indexes(entry_widget))[1] = cv
            # Megkeressük az összes "cell(B:3)" formájú cellahivatkozást, ha van.
            while cellref_found := find_cellref(expr):
                # A "cell(B:3)" formájú cellahivatkozást jelentő karaktersort "get_cell_numvalue(2,3)" formára cseréljük.
                cellvalue = converted_cellref(cellref_found).replace('cell', 'get_cell_numvalue')
                # A kifejezésben minden "cell(B:3)" formájú karaktersort "get_cell_numvalue(2,3)" formára cseréljük, hogy
                # A kiértékeléskor a get_cell_numvalue(2,3) függvényt lehessen meghívni.
                expr = expr.replace(cellref_found, cellvalue)

            # Megkíséreljük kiértékelni a kifejezést az eval() beépített függvény segítségével.
            try:
                # A sikeres kiértékelés eredményét beírjuk a cellába.
                ebx_var.set(eval(expr))
            except Exception as exc:
                # Ha valamiért hiba merül fel a kiértékelés során, akkor a hiba okát írjuk a cellába.
                ebx_var.set(type(exc).__name__)


def reveal_cell_expression_event_handler(e):
    """Az eseménnyel érintett beviteli mezőhöz tarozó képlet megjelenítése a mezőben"""
    ebx = e.widget  # Az eseménnyel érintett beviteli mező.
    reveal_cell_expression(ebx)


def reveal_cell_expression(entry_widget):
    # A beviteli mezőhöz rendelt kontrollváltozó és az eltárolt kifejezés kikérése az ezeket tartalmazó szótárból.
    ebx_var, expression = ebx_vars.get(get_cell_indexes(entry_widget))
    # Ha tartozik az adott cellához kifejezés (nem üres a karakterlánc), akkor azt megjelenítjük a beviteli mezőben.
    if expression:
        # Az eseményyel érintett beviteli mezőhöz tartozó kontrollváltozó értékének a kifejezést adjuk.
        ebx_var.set(expression)
        # A beviteli mezőben a kurzort a kifejezés végére állítjuk.
        entry_widget.icursor('end')


def update_expressions(e):
    """A táblázat minden cellájában aktualizálja a képlet értékét."""
    for ebx in e.widget.master.grid_slaves():
        reveal_cell_expression(ebx)
        eval_cell_content(ebx)


def move_cursor(e):
    """Az eseménnyel érintett beviteli mezőből a kurzort az alatta levő cellába viszi. Ha nincs alatta cella, akkor
    a jobbra mellette levőbe. Ha ez sincs, akkor marad a kurzor az aktuális cellában
    """
    ebx = e.widget  # Az eseménnyel érintett beviteli mező.
    ri, ci = get_cell_indexes(ebx)  # Az eseménnyel érintett beviteli mező sor- és oszlopindexének meghatározása.
    try:
        # Megkíséreljük a fókuszt az aktuális cella alatti cellára tenni.
        ebx.master.grid_slaves(ri + 1, ci)[0].focus_set()
    except IndexError:
        # Ha nincs alatta cella, akkor megkíséreljük a fókuszt az aktuális cellától jobbra levő cellára tenni.
        try:
            ebx.master.grid_slaves(ri, ci + 1)[0].focus_set()
        except IndexError:
            # Ha nincs mellette levő cella sem (jobb alsó sarokcellában vagyunk), akkor a fókusz marad az aktuális cellán.
            pass


def fit_column_width(e, default=False):
    """Az eseménnyel érintett beviteli mező oszlopa szélességének az oszlop leghosszabb cellatartalmához
    történő igazítása, vagy ha a defaukt True, akkor az alapértelmezett értékre állítása.
    """
    # Az eseménnyel érintett cella (beviteli mező) oszlopindexének meghatározása.
    _, ci = get_cell_indexes(e.widget)
    # Ha a default False, akkor az alapértelmezett érték lesz az adott oszlop szélessége.
    # Ha a default True, akkor az adott oszlopban a leghosszabb karakterlánc hossza + 1 karakter lesz a szélesség.
    column_width = 20
    if not default:
        max_text_lenght = max([len(ebx_vars.get((ri, ci))[0].get()) for ri in range(num_of_rows + 1)])
        column_width = max_text_lenght + 1
    # Végigvesszük az adott oszlop minden sorában levő cellát és beállítjuk a szélességét.
    for ri in range(num_of_rows + 1):
        ebx = e.widget.master.grid_slaves(ri, ci)[0]
        ebx.config(width=column_width)


def delete_cell_content(e):
    """Az eseménnyel érintett beviteli mező kontrollváltozójának értékét és a képletet üres karaktersorra állítja."""
    cell_data: list = ebx_vars.get(get_cell_indexes(e.widget))
    cell_data[0].set('')
    cell_data[1] = ''


# A táblázat sor- és oszlopszámának megadása.
num_of_rows, num_of_columns = 20, 6
# A táblázat egy adott pozíciójában levő beviteli mezőhöz (entry box) tartozó kontrollváltozót és
# képletet (kifejezést) egy szótárban tároljuk, ahol a kulcs egy kételemű tuple a sor- és oszlopindexekkel, a hozzá
# rendelt érték pedig egy kételemű lista, amely első eleme a kontrollváltozó, a második a képletet leíró karaktersor.
ebx_vars: dict[tuple, list[tk.StringVar, str]] = {}

# Táblázatrács kirajzolása.
for ri, ci in product(range(num_of_rows + 1), range(num_of_columns + 1)):
    # A sor- és oszlopindexeken végighaladva felöltjük a szótárt kezdeti értékekkel (üres StringVar és üres string)
    ebx_vars[(ri, ci)] = [tk.StringVar(), '']
    # Létrehozzuk az egyes cellákhoz tartozó grafikus beviteli mezőket, és kontrollváltozóként a szótárban előbb
    # létrehozott StringVar objektumot rendeljük. Beállítjuk a mezők betűtípusát és szélességét.
    ebx = tk.Entry(root, textvariable=ebx_vars.get((ri, ci))[0], font=('Noto Mono', 12), width=20)
    # A táblázat első sora és oszlopa a sor- és oszlopazonosítokat tartalmazzák, ezért e beviteli mezőket
    # letiltjuk, hogy tartalmuk ne legyen változtatható. A közös konfig paramétereiket egy szótárban határozzuk meg.
    headers_common_params = dict(state=tk.DISABLED, disabledbackground='gray95',
                                 justify=tk.CENTER, font=('Arial', 12, 'bold'))
    # Az első sor egyes beviteli mezőiben az angol abc nagybetűi lesznek mint oszlopazonosítók.
    if ri == 0 and ci > 0:
        ebx_vars[(ri, ci)][0].set(chr(ord('A') + ci - 1))
        ebx.config(**headers_common_params)
    # Az első oszlop egyes beviteli mezőiben a sorszámok jelennek meg 1-től kezdődő egészekként.
    # Az első oszlop szélességét a legnagyobb sorszám szélességét figyelembe véve állítjuk be.
    if ci == 0:
        ebx.config(width=len(str(num_of_rows)) + 2, **headers_common_params)
        if ri > 0:
            ebx_vars[(ri, ci)][0].set(ri)
    # A beviteli mezőket lehelyezzük a rács sor- és oszlopindexekkel maghatározott pozíciójába.
    ebx.grid(row=ri, column=ci, sticky='we')

# Egy cellában az Enter megnyomására kiértékeli a cell tartalmát, majd a kurzort az alatta levő
# cellába viszi. Ha nincs alatta cella, akkor a mellette levőbe. Ha az sincs, akkor a cellában hagyja.
# Végül, a táblázat összes celláját, amiben van képlet újra kiértékeli, hogy az esetleges változások érvényesüljenek.
root.bind_class('Entry', '<Key Return>', eval_cell_content_event_handler)
root.bind_class('Entry', '<Key Return>', move_cursor, add=True)
# root.bind_class('Entry', '<Key Return>', lambda e: update_expressions(e.widget.master), add=True)
root.bind_class('Entry', '<Key Return>', update_expressions, add=True)

# Események és eseménykezelők összerendelése.

# Ha a celláról elvesszük a fókuszt (Tab gomb lenyomással vagy másik cellába kattintással), akkor hasonlóan, mint az
# Enter esetén az adott cella értéke meghatározásra kerül, majd ennek ismeretében a tábla összes képlete újraszámolódik.
root.bind_class('Entry', '<FocusOut>', eval_cell_content_event_handler)
# root.bind_class('Entry', '<FocusOut>', lambda e: update_expressions(e.widget.master), add=True)
root.bind_class('Entry', '<FocusOut>', update_expressions, add=True)

# Ha a cellában kétszer kattintunk, akkor előjön a cella értékét meghatározó képlet, ha volt ilyen.
root.bind_class('Entry', '<Double ButtonPress 1>', reveal_cell_expression_event_handler)

# A jobb egérgombbal duplán kattintva egy cellán, az adott oszlop szélessége úgy változik, hogy
# az oszlop cellái közül a leghosszabb szöveg is látszódjon.
root.bind_class('Entry', '<Double Button 3>', lambda e: fit_column_width(e))

# A jobb egérgombbal duplán kattintva egy cellán, miközben a Ctrl gomb nyomva van, az alapértelmezett értékre
# állítjuk az oszlop szélességét.
root.bind_class('Entry', '<Control Double Button 3>', lambda e: fit_column_width(e, True))

# A Del gomb hatására a cella tartalma és a mögöttes képlet (ha volt) törlődik.
root.bind_class('Entry', '<Key Delete>', delete_cell_content)

root.mainloop()
