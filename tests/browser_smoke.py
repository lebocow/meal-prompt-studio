"""Optional browser checks. Runtime app has no dependencies.

Run: python -m pip install playwright
     python -m playwright install chromium
     python tests/browser_smoke.py

Uses set_content to exercise the complete single-file document without a server.
Persistence and clipboard success paths use explicit test doubles, not browser
permission overrides. Normal unavailability paths are also checked. A real
file:// open and HTTPS clipboard permissions should additionally be checked
manually on the target browser. CHROMIUM_PATH may select an installed Chromium.
"""
from pathlib import Path
import json
import os
import unittest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
MENU = 'Plan for 3 days. Alex: 4 meals. Maria: lunch and dinner only. Raw chicken, rice, milk and oats. The exact recipe quantities must be audited.'

class BrowserSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        options = {'headless': True, 'args': ['--no-sandbox']}
        executable = os.getenv('CHROMIUM_PATH')
        if executable:
            options['executable_path'] = executable
        cls.browser = cls.playwright.chromium.launch(**options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1100})
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.errors = []
        self.requests = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.on('request', lambda request: self.requests.append(request.url))
        self.page.set_content(HTML)

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.context.close()

    def ready(self):
        self.page.locator('#menu').fill(MENU)
        self.page.locator('#generateButton').click()
        self.assertTrue(self.page.locator('#copyButton').is_enabled())
        return self.page.locator('#promptOutput').input_value()

    def tab(self, name):
        self.page.locator(f'#tab-{name}').click()

    def mock_storage(self):
        self.page.evaluate('''() => {
          const data = {};
          window.__store = data;
          Object.defineProperty(window, 'localStorage', { configurable: true, value: {
            getItem: k => Object.prototype.hasOwnProperty.call(data,k) ? data[k] : null,
            setItem: (k,v) => {data[k] = String(v)}, removeItem: k => {delete data[k]}
          }});
        }''')

    def test_01_initial_view_no_requests(self):
        self.assertIn('MealPrompt', self.page.title())
        self.assertFalse(self.page.locator('#copyButton').is_enabled())
        self.assertEqual(self.requests, [])
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'))

    def test_02_empty_menu_error_focus(self):
        self.page.locator('#generateButton').click()
        self.assertEqual(self.page.locator('#menu').get_attribute('aria-invalid'), 'true')
        self.assertEqual(self.page.evaluate('document.activeElement.id'), 'menu')
        self.assertTrue(self.page.locator('#promptOutput').is_hidden())

    def test_03_generate_full_prompt(self):
        text = self.ready()
        self.assertIn(MENU, text)
        self.assertIn('Calories: 2400 kcal per day', text)
        self.assertIn('Approximately 306 g', text)
        self.assertIn('included_meals — per-day subtotal', text)
        self.assertIn('2. **Summary of Changes:**', text)
        self.assertEqual(self.requests, [])

    def test_04_stale_copy_disabled_then_updated(self):
        self.ready()
        self.tab('people')
        self.page.locator('#person-0-calories').fill('2500')
        self.assertFalse(self.page.locator('#copyButton').is_enabled())
        self.assertEqual(self.page.locator('#person-0-carbs').input_value(), '331')
        self.page.locator('#generateButton').click()
        self.assertIn('Calories: 2500 kcal per day', self.page.locator('#promptOutput').input_value())

    def test_05_custom_carbs_and_scope_changes(self):
        self.tab('people')
        self.page.locator('#person-1-scope').select_option('full_day')
        self.assertEqual(self.page.locator('#person-1-calorieTolerance').input_value(), '50')
        self.page.locator('#person-0-carbMode').select_option('manual')
        self.page.locator('#person-0-carbs').fill('306,5')
        self.tab('menu')
        text = self.ready()
        self.assertIn('Carbohydrates: 306.5 g (explicit target)', text)

    def test_06_impossible_target_blocks_generation(self):
        self.tab('people')
        self.page.locator('#person-0-calories').fill('300')
        self.tab('menu')
        self.page.locator('#menu').fill(MENU)
        self.page.locator('#generateButton').click()
        self.assertEqual(self.page.locator('#tab-people').get_attribute('aria-selected'), 'true')
        self.assertFalse(self.page.locator('#copyButton').is_enabled())
        self.assertEqual(self.page.locator('#person-0-calories').get_attribute('aria-invalid'), 'true')

    def test_07_add_remove_people(self):
        self.tab('people')
        self.page.locator('#addPerson').click()
        self.assertEqual(self.page.locator('.person-card').count(), 3)
        self.page.once('dialog', lambda d: d.accept())
        self.page.locator('[data-action=remove-person][data-index="2"]').click()
        self.assertEqual(self.page.locator('.person-card').count(), 2)

    def test_08_gymbeam_label_and_duplicate_protection(self):
        self.tab('nutrition')
        self.page.locator('[data-action=add-peanut]').click()
        self.page.locator('[data-action=add-peanut]').click()
        self.assertEqual(self.page.locator('.product-card').count(), 1)
        self.assertEqual(self.page.locator('#product-0-kcal').input_value(), '603')
        self.tab('menu')
        text = self.ready()
        self.assertIn('Energy: 603 kcal', text)
        self.assertIn('Fibre: 7.6 g', text)

    def test_09_blank_label_cannot_generate(self):
        self.tab('nutrition')
        self.page.locator('#addProduct').click()
        self.tab('menu')
        self.page.locator('#menu').fill(MENU)
        self.page.locator('#generateButton').click()
        self.assertEqual(self.page.locator('#tab-nutrition').get_attribute('aria-selected'), 'true')
        self.assertFalse(self.page.locator('#copyButton').is_enabled())

    def test_10_quick_constraints_not_duplicated(self):
        self.tab('rules')
        for _ in range(2):
            self.page.locator('[data-action=quick-milk]').click()
        self.assertEqual(self.page.locator('#hardConstraints').input_value().count('250 ml'), 1)
        self.page.locator('[data-action=quick-dough]').click()
        self.page.locator('[data-action=quick-banana]').click()
        self.tab('menu')
        text = self.ready()
        self.assertIn('exactly 250 ml', text)
        self.assertIn('fixed 400 g', text)
        self.assertIn('Do not use banana.', text)

    def test_11_txt_download_matches_generated_output(self):
        output = self.ready()
        with self.page.expect_download() as event:
            self.page.locator('#downloadButton').click()
        self.assertTrue(event.value.suggested_filename.endswith('.txt'))
        self.assertEqual(Path(event.value.path()).read_text(), output)

    def test_12_json_export_import_roundtrip(self):
        self.ready()
        with self.page.expect_download() as event:
            self.page.locator('[data-action=export-config]').first.click()
        exported = Path(event.value.path()).read_bytes()
        parsed = json.loads(exported)
        self.assertEqual(parsed['state']['menu'], MENU)
        self.page.locator('#menu').fill('Changed')
        self.page.once('dialog', lambda d: d.accept())
        self.page.locator('#configFile').set_input_files({'name':'config.json','mimeType':'application/json','buffer':exported})
        self.assertEqual(self.page.locator('#menu').input_value(), MENU)
        self.assertFalse(self.page.locator('#copyButton').is_enabled())

    def test_13_malformed_json_import_preserves_draft(self):
        self.page.locator('#menu').fill(MENU)
        self.page.locator('#configFile').set_input_files({'name':'broken.json','mimeType':'application/json','buffer':b'{no'})
        self.assertEqual(self.page.locator('#menu').input_value(), MENU)
        self.assertIn('JSON valid', self.page.locator('#toast').inner_text())

    def test_14_text_file_import_and_menu_escaping(self):
        text = '<meal_plan>\nMeniu & un text <script>window.__bad = true</script>\n</meal_plan>'
        self.page.locator('#menuFile').set_input_files({'name':'menu.md','mimeType':'text/markdown','buffer':text.encode()})
        self.assertEqual(self.page.locator('#menu').input_value(), text)
        self.page.locator('#generateButton').click()
        self.assertIn('&lt;script&gt;', self.page.locator('#promptOutput').input_value())
        self.assertFalse(self.page.evaluate('Boolean(window.__bad)'))

    def test_15_clipboard_unavailable_falls_back_to_manual(self):
        text = self.ready()
        self.page.evaluate('''() => {Object.defineProperty(navigator,'clipboard',{configurable:true,value:undefined});document.execCommand=()=>false;}''')
        self.page.locator('#copyButton').click()
        self.assertIn('Ctrl/⌘+C', self.page.locator('#toast').inner_text())
        selection = self.page.locator('#promptOutput').evaluate('(e)=>e.selectionEnd-e.selectionStart')
        self.assertEqual(selection, len(text))

    def test_16_clipboard_success_via_explicit_test_double(self):
        text = self.ready()
        self.page.evaluate('''() => {Object.defineProperty(window,'isSecureContext',{configurable:true,value:true});Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.__copied=text;}}});}''')
        self.page.locator('#copyButton').click()
        self.assertEqual(self.page.evaluate('window.__copied'), text)
        self.assertIn('Prompt copiat', self.page.locator('#toast').inner_text())

    def test_17_storage_blocked_does_not_break_generation(self):
        self.assertIn('indisponibilă', self.page.locator('#saveStatus').inner_text())
        self.ready()
        self.assertTrue(self.page.locator('#copyButton').is_enabled())

    def test_18_autosave_and_optout_via_storage_test_double(self):
        self.mock_storage()
        self.page.locator('#menu').fill(MENU)
        self.page.wait_for_timeout(450)
        data = self.page.evaluate('window.__store')
        self.assertTrue(any(k.endswith('draft') for k in data))
        self.page.locator('#autosave').uncheck()
        data = self.page.evaluate('window.__store')
        self.assertFalse(any(k.endswith('draft') for k in data))
        self.assertTrue(any(k.endswith('autosave') and v == 'false' for k,v in data.items()))

    def test_19_profile_save_load_via_storage_test_double(self):
        self.mock_storage()
        self.page.locator('#menu').fill(MENU)
        self.page.once('dialog', lambda d: d.accept('Test profile'))
        self.page.locator('[data-action=save-profile]').first.click()
        self.page.locator('#menu').fill('Changed')
        self.page.locator('[data-action=profiles]').click()
        self.assertIn('Test profile', self.page.locator('#profileList').inner_text())
        self.page.once('dialog', lambda d: d.accept())
        self.page.locator('#profileList').get_by_role('button',name='Încarcă').click()
        self.assertEqual(self.page.locator('#menu').input_value(), MENU)

    def test_20_keyboard_tabs_and_generate_shortcut(self):
        self.page.locator('#tab-menu').focus()
        self.page.keyboard.press('ArrowRight')
        self.assertEqual(self.page.locator('#tab-people').get_attribute('aria-selected'), 'true')
        self.page.keyboard.press('End')
        self.assertEqual(self.page.locator('#tab-nutrition').get_attribute('aria-selected'), 'true')
        self.tab('menu')
        self.page.locator('#menu').fill(MENU)
        self.page.keyboard.press('Control+Enter')
        self.assertTrue(self.page.locator('#copyButton').is_enabled())

    def test_21_mobile_layout_all_tabs(self):
        self.page.set_viewport_size({'width':390,'height':844})
        for tab in ['menu','people','rules','nutrition']:
            self.tab(tab)
            self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'), tab)
        self.tab('menu')
        self.ready()
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth'))

    def test_22_preset_replacement_clears_stale_output(self):
        self.ready()
        self.page.locator('[data-action=profiles]').click()
        self.page.once('dialog', lambda d: d.accept())
        self.page.locator('[data-action=preset-original]').click()
        self.assertEqual(self.page.locator('#menu').input_value(), '')
        self.assertTrue(self.page.locator('#promptOutput').is_hidden())
        self.assertFalse(self.page.locator('#copyButton').is_enabled())
        self.tab('rules')
        self.assertIn('250 ml', self.page.locator('#hardConstraints').input_value())
        self.tab('nutrition')
        self.assertEqual(self.page.locator('#product-0-kcal').input_value(), '603')

    def test_23_custom_format_and_precision(self):
        self.tab('rules')
        self.page.get_by_text('Setări avansate pentru răspuns',exact=True).click()
        self.page.locator('#rounding').select_option('2')
        self.page.locator('#missingData').select_option('flag')
        self.page.locator('#customFormat').fill('<meal_plan>my format</meal_plan>')
        self.tab('menu')
        text = self.ready()
        self.assertIn('to 2 decimal places',text)
        self.assertIn('<desired_format>',text)
        self.assertIn('Do not invent missing nutrition values',text)

if __name__ == '__main__':
    unittest.main(verbosity=2)
