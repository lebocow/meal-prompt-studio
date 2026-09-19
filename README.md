# MealPrompt Studio

**[Deschide aplicația online](https://lebocow.github.io/meal-prompt-studio/)** · [Repository GitHub](https://github.com/lebocow/meal-prompt-studio)

Un formular web pentru construirea unui prompt complet de audit și ajustare a meniurilor. Lipești meniul actual, introduci țintele și regulile, apeși **Generează promptul**, apoi copiezi rezultatul într-un chat nou.

**Aplicație statică, într-un singur `index.html`.** HTML, CSS, JavaScript și promptul master sunt incluse în fișier. Nu are backend, dependențe de runtime, fonturi externe, analytics, chei API sau cereri către un model AI. Nu calculează nutriția meniului: construiește instrucțiunile pentru asistent. Singurul calcul nutrițional din interfață este ținta teoretică de carbohidrați din kcal, proteine și grăsimi.

## Deschidere locală

Descarcă `index.html` și deschide-l în browser, prin dublu-click sau **Open File / Deschide fișier**. Nu trebuie să rulezi `npm install`, un build sau un server. Celelalte fișiere sunt documentație și teste; nu sunt necesare pentru utilizare.

Un browser sau un dispozitiv administrat poate bloca deschiderea fișierelor locale. În acest caz, folosește o găzduire statică precum GitHub Pages. Dacă pagina este deschisă într-un preview care dezactivează JavaScript, descarcă fișierul și deschide-l în browserul obișnuit.

## Fluxul de utilizare

1. **Meniu:** lipește planul complet sau importă `.txt`, `.md` ori `.markdown`. Setează numărul de zile, limba meniului final și dacă mesele se repetă. Contextul și restricțiile au câmpuri separate.
2. **Ținte:** introdu persoanele și țintele per zi. Alege între **Toată ziua** și **Doar mesele incluse**. Un câmp macro gol înseamnă nespecificat, nu zero. Carbohidrații pot fi calculați automat, introduși manual sau lăsați nespecificați.
3. **Reguli:** cerințe obligatorii, preferințe flexibile, păstrarea preparatelor și ingredientelor. Setările avansate includ tolerarea datelor lipsă și un format de ieșire personalizat.
4. **Etichete:** lipește un tabel sau definește produse cu valori actualizate, numele vechi de înlocuit și baza corectă — 100 g sau 100 ml.
5. **Generează → Copiază:** lipește promptul într-un chat nou. După schimbarea datelor, generarea anterioară este marcată ca neactualizată și copierea ei este dezactivată până la regenerare.

`Ctrl/⌘ + Enter` generează promptul. Tastele săgeți, Home și End navighează între taburi atunci când focusul este pe bara de taburi.

## Ce este inclus

- Maximum 8 persoane, cu ținte și toleranțe independente.
- Carbohidrați teoretici: `(kcal − 4 × proteine − 9 × grăsimi) / 4`. La 2400 kcal, 132 g P și 72 g F rezultă 306 g C.
- Separare explicită între dieta de o zi și subtotalul zilnic al meselor incluse.
- Validare pentru meniu lipsă, numere invalide, nume duplicate, etichete incomplete și ținte care depășesc deja energia disponibilă.
- Acceptarea separatorului zecimal `,` sau `.` în câmpurile macro.
- Prioritate pentru setările actuale față de țintele și calculele vechi din meniul lipit.
- Audit numeric înainte de modificări; reguli pentru ulei, valori crude/gătite/scurse, batch-uri omogene și distribuirea corectă a porțiilor.
- Format standard cu `meal_plan`, `menu`, `person_plan`, `ingredients_nutrition`, `shopping_list`, `cooking_instructions` și rezumatul modificărilor.
- Ieșire în English, Română, Deutsch, Français, Español sau Italiano. Instrucțiunile master rămân în engleză; limba selectată este limba rezultatului cerut.
- Copiere în clipboard, selectare manuală și descărcare TXT.
- Export/import JSON, draft local și până la 20 de profiluri salvate explicit.
- Layout pentru desktop și mobil, etichete accesibile, navigare cu tastatura și respectarea preferinței reduced motion.

## Preseturi

La prima deschidere sunt afișate exemplele **Alex: 2400 kcal / 132 g P / 72 g F** și **Maria: 600 kcal pentru mesele incluse**. Sunt câmpuri editabile, nu recomandări clinice și nu ținte deduse din date medicale.

În **Profiluri**:

- **Alex 2400 + Maria 600:** reîncarcă doar configurația de bază.
- **Exemplul cu lapte & GymBeam:** adaugă regula pentru 250 ml lapte/shake Alex, excluderea bananei, ambalajul fix de 400 g aluat, preferința pentru shake-uri identice și eticheta de unt de arahide din exemplul utilizatorului.
- **Configurație goală:** începe cu o singură persoană, fără ținte precompletate.

Preseturile nu conțin un meniu personal ascuns. Datele etichetei GymBeam sunt cele furnizate de utilizator, nu valori verificate automat la producător. Nu folosi presetul cu aluat pentru un meniu fără pizza fără să elimini acea regulă.

## Salvare și confidențialitate

Datele introduse nu sunt trimise de aplicație pe internet. Dacă pagina este găzduită online, browserul descarcă pagina de la gazdă, dar aplicația nu trimite conținutul formularului către aceasta. Nu există sincronizare, autentificare sau integrare automată cu ChatGPT.

Draftul și profilurile sunt salvate necriptat în `localStorage`, separat pentru calea acestei pagini. Sunt accesibile utilizatorului browserului și scripturilor de aceeași origine. Nu folosi salvarea pe un calculator partajat pentru date sensibile. Exportul JSON conține toate câmpurile introduse, inclusiv restricții și context.

La `file://`, disponibilitatea și persistența `localStorage` depind de browser și de adresa fișierului. Mutarea sau redenumirea lui poate face draftul să pară dispărut. Modul privat, blocarea stocării, curățarea datelor și limita de spațiu pot afecta salvarea. Exportă JSON pentru o copie portabilă. Lipsa stocării nu blochează generarea.

Dezactivarea salvării automate șterge draftul aplicației, dar păstrează profilurile salvate explicit. Din Ajutor poți șterge draftul și toate profilurile acestei pagini; formularul deja deschis rămâne în memorie. Exporturile descărcate trebuie șterse separat, dacă este necesar.

Copierea automată folosește Clipboard API când este permis, apoi o alternativă compatibilă și, în ultimă instanță, selectarea textului pentru `Ctrl/⌘+C`. Nu afișează succes dacă ambele încercări automate au eșuat.

## Publicare pe GitHub Pages

Acest proiect folosește GitHub Pages, cu publicare din branch-ul `main`, directorul rădăcină (`/`). Modificările trimise în `main` sunt publicate automat. Pentru o copie în alt cont, urmează pașii de mai jos.

1. Creează un repository, de exemplu `meal-prompt-studio`.
2. Încarcă cel puțin `index.html` în rădăcină. Recomandat: adaugă și `.nojekyll`. Poți încărca întregul proiect pentru documentație și teste, dar **nu exporturi JSON personale**.
3. În repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch → main → /(root) → Save**. Folosește numele real al branch-ului dacă este diferit.
4. Deschide adresa de site afișată de GitHub Pages după deployment.

Un click pe `index.html` în lista de fișiere a repository-ului afișează codul, nu aplicația. Pentru utilizare în browser, deschide adresa GitHub Pages sau fișierul descărcat local.

Disponibilitatea Pages pentru repository-uri private depinde de plan. În mod obișnuit, site-ul Pages este public chiar dacă sursa este privată; nu publica meniuri personale în fișierele repository-ului. Formularul nu are date personale incluse, iar ceea ce tastezi nu este comis automat în GitHub.

Ghid oficial: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Structura proiectului

```text
meal-prompt-studio/
├── index.html                 # Întreaga aplicație, singura sursă de runtime
├── .nojekyll                  # Pentru publicare statică
├── .gitignore
├── package.json               # Numai scriptul opțional de teste
├── README.md
├── TEST_REPORT.md
├── LICENSE
└── tests/
    ├── core.test.cjs          # Teste Node, fără pachete externe
    └── browser_smoke.py       # Teste opționale Python + Playwright
```

CSS-ul este în `<style>`, funcțiile pure sunt în `<script id="prompt-core">`, iar logica interfeței este în `<script id="studio-ui">`. Editează această sursă unică; testele extrag și verifică scriptul din fișierul distribuit, nu o copie divergentă.

## Testare

Testele unitare nu au nevoie de instalarea unor pachete:

```sh
node --test tests/core.test.cjs
# sau
npm test
```

Testele de browser sunt opționale pentru dezvoltare, nu pentru folosirea aplicației:

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/browser_smoke.py
```

Pentru un Chromium deja instalat:

```sh
CHROMIUM_PATH=/usr/bin/chromium python tests/browser_smoke.py
```

Vezi `TEST_REPORT.md` pentru ce a fost executat și limitele verificării. Un prompt bine structurat nu garantează corectitudinea răspunsului unui model; verifică etichetele, porțiile și recomandările importante din meniul generat.

## Referințe tehnice

- localStorage și particularități `file://`: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
- Clipboard API și contextul securizat: https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText
- GitHub Pages: ghidul oficial de mai sus.

## Licență

MIT. Niciun serviciu extern și nicio bibliotecă de runtime nu sunt incluse.
