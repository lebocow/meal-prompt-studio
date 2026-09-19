# Raport de verificare

Data: 19 septembrie 2026.

## Verificări executate

**28/28 teste unitare Node au trecut.** Testele extrag scriptul `prompt-core` direct din `index.html`. Au fost verificate: calculul țintelor de carbohidrați, separatoare zecimale, câmpuri goale versus zero, subtotaluri parțiale, prioritatea noilor ținte, cerințe fixe, validări numerice, produse/etichete, unități, escaping, import/export, formatul de ieșire, reguli de ulei și porționare, lipsa dependențelor externe și determinismul generatorului.

**23/23 teste de interfață Playwright/Chromium au trecut.** Au fost verificate: generare, blocarea ieșirii vechi după editări, persoane și etichete dinamice, carbohidrați automați/manuali, import TXT/Markdown, import/export JSON, descărcare TXT, tratarea erorilor, copy fallback, profiluri, opt-out pentru salvare, navigare cu tastatura, shortcut-ul de generare, preseturi și format personalizat.

**Layout inspectat vizual** în Chromium la desktop. Test automat pentru absența scrollului orizontal la 390 px în toate cele patru taburi și după generare.

**Nicio cerere de rețea a aplicației** observată la încărcarea documentului sau generarea promptului în aceste teste. Fișierul nu include scripturi, CSS ori fonturi externe și nu folosește `fetch`, `XMLHttpRequest` sau `sendBeacon`.

## Limitele verificării

Mediul de test a blocat navigarea către adrese `file://` și HTTP localhost printr-o politică de browser. Interfața a fost verificată prin `page.set_content()` cu întregul document HTML, fără a modifica această politică.

Căile de succes pentru persistență și Clipboard API au fost verificate cu înlocuitori de test expliciți. Căile de eroare au fost verificate separat, inclusiv lipsa reală a stocării într-un document fără origine. Aceste teste nu certifică permisiunile reale de clipboard sau persistența fișierelor locale din orice browser.

Nu a fost verificată deschiderea reală prin `file://`, persistența reală după închiderea/repor­nirea browserului, Safari, Firefox ori un deployment GitHub Pages. Aplicația este autonomă și construită pentru deschidere directă, fără dependențe de server; aceste comportamente merită un smoke test pe dispozitivul utilizatorului.

Nu a fost creat repository-ul GitHub și nu a fost publicat un site. Nu s-a trimis un prompt către un model AI și nu s-a validat nutrițional niciun meniu. Testele vizează generatorul și interfața, nu garantează răspunsurile unui asistent extern.
