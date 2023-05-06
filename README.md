# Táblázatkezelők munkalapjához hasonlító egyszerű számolótábla
### E miniprojekt célja a megoldási lehetőségek átgondolásának, és a megvalósítás során a Python használatának gyakorlása.

# Az alkalmazás jellemzőinek összefoglalása: 
-	Az egyes cellákba értékeket vagy képleteket (kifejezéseket) lehet írni, aminek az eredménye megjelenik a cellában.
-	A képletek mindig az egyenlőségjellel (=) kezdődnek, és cellahivatkozásokat is tartalmazhatnak.
-	A táblázat sorait 1-tól kezdődő sorszámok azonosítják, az oszlopokat pedig az angol abc nagybetűi A-Z-ig.
-	A képletekben a táblázat egyes celláira sor- és oszlopazonosítókkal lehet hivatkozni „cell(A:1)” karaktersor formában, ahol
  A:1 az első oszlopot és első sor azonosítja.
-	A cellába írt értékek megváltozása esetén az arra a cellára hivatkozó képletek értéke is megfelelően módosul.
-	A képleteket a cellában történő dupla bal egérgomb kattintással meg lehet jeleníteni, hogy szerkeszthetőek legyenek a cellában.
- A képlet megjelenésekor a kurzor a karaktersor végére kerül.
-	A képletek akkor értékelődnek ki, ha Entert nyomunk, vagy a celláról a fókusz elkerül. Ez utóbbi akkor történik, ha 
  vagy a Tab billentyűt nyomjuk meg, vagy az egérrel egy másik cellába kattintunk. 
-	Ha Entert nyomunk, akkor a kurzor az alatta levő cellába kell, hogy menjen. Ha nincs ilyen cella, akkor a jobbra mellette levőbe. 
  Ha ilyen sincs – ami azt jelenti, hogy a jobb alsó sarokcellában vagyunk –, akkor a kurzor marad a cellában.
-	A cella tartalmát törölni a Del (delete) gomb használatával lehet. A cellába új értéket beírni csak az előző törlése után lehet.
-	A jobb egérgombbal duplán kattintva egy cellán, az adott oszlop szélessége úgy változik, hogy az oszlop cellái közül a leghosszabb 
  szöveg is látszódjon.
- A jobb egérgombbal duplán kattintva egy cellán miközben a Ctrl billentyű le van nyomva, az adott oszlop szélessége 
  az alapértelmezett értékre áll.

A fejlesztési fázisokat a https://www.facebook.com/pythontudasepites oldalon a "Hogyan készítsünk Excel táblához hasonló számolótáblát?" 
című bejegyzéssorozat ismerteti.
