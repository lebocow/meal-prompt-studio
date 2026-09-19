# Raport de verificare

Data: 19 septembrie 2026.

## Verificare la publicare pe GitHub Pages

- Repository: https://github.com/lebocow/meal-prompt-studio
- Aplicație: https://lebocow.github.io/meal-prompt-studio/
- GitHub a confirmat finalizarea cu succes a primei publicări, din `main`, rădăcina proiectului, cu HTTPS activat.
- Cele 28 de teste Node au fost rulate din nou: 28/28 au trecut.
- Fișierul `index.html` publicat este identic cu cel din arhiva inițială (SHA-256: `70ab9826ccd71da911e4ba8b0ac7d2a1b8e5cac31f628199ec65bf3dc1543b0e`).
- Verificare efectuată în browser pe adresa HTTPS: pagina se deschide, un meniu de test generează promptul, butoanele de copiere și descărcare devin active, iar editarea meniului dezactivează copierea promptului vechi.
- Această verificare nu a inclus copierea efectivă în clipboard, descărcarea unui fișier sau verificarea persistenței după repornirea browserului.

Secțiunile de mai jos păstrează raportul arhivei inițiale, anterior publicării. Cele 23 de teste Playwright descrise acolo nu au fost rulate din nou la publicare.

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
