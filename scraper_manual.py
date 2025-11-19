# SCRAPER OTOMOTO - TRYB MANUAL ASSIST
# Uruchom ten skrypt w PowerShell: python scraper_manual.py [nazwa_pliku.xlsx]

import sys
import requests
import re
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd
import time
from datetime import datetime

# Konfiguracja
SEARCH_URL = "https://www.otomoto.pl/osobowe/volkswagen/passat/seg-sedan?search%5Bfilter_enum_fuel_type%5D=diesel&search%5Bfilter_enum_generation%5D=gen-b5-fl-2000-2005&search%5Badvanced_search_expanded%5D=true"
LIMIT = 13

# Nazwa pliku z argumentu lub z timestampem
if len(sys.argv) > 1:
    OUT_FILE = sys.argv[1]
else:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUT_FILE = f"listings_{timestamp}.xlsx"

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

SESSION = requests.Session()
SESSION.headers.update(UA)

# --------- Pomocnicze funkcje ekstrakcji (port z notebooka) ---------
PARAM_KEY_MAP = {
    'brand': ['marka','make','brand'],
    'model': ['model','modelname'],
    'year': ['rok','year','production'],
    'mileage': ['przebieg','mileage','odometer'],
    'fuel_type': ['paliwo','rodzaj paliwa','fuel'],
    'transmission': ['skrzynia','skrzynia biegów','transmission','gearbox'],
    'capacity': ['pojemność','pojemnosc','enginecapacity','engine_displacement','enginecapacity'],
    'power': ['moc','power','hp','kw'],
    'color': ['kolor','color'],
    'doors': ['liczba drzwi','doors'],
    'seats': ['liczba miejsc','seats'],
    'body_type': ['nadwozie','typ nadwozia','body'],
    'condition': ['stan','condition'],
    'country': ['kraj pochodzenia','kraj','origin'],
    'vin': ['vin'],
}

def _map_params(params):
    norm = {}
    for key, patterns in PARAM_KEY_MAP.items():
        for p in patterns:
            for k,v in params.items():
                if p in k.lower():
                    norm[key] = v
                    break
            if key in norm:
                break
    return norm

def _jsonld_blocks(soup):
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string) if sc.string else None
            if not data:
                continue
            if isinstance(data, list):
                for d in data:
                    yield d
            else:
                yield data
        except Exception:
            continue

def _parse_jsonld(soup):
    out = {}
    for blk in _jsonld_blocks(soup):
        t = blk.get('@type') or blk.get('@context','')
        if isinstance(t, list):
            t = " ".join(t)
        if any(k in str(t).lower() for k in ['vehicle','product','offer','car']):
            brand = blk.get('brand')
            if isinstance(brand, dict):
                out['brand'] = brand.get('name','')
            elif isinstance(brand, str):
                out['brand'] = brand
            out.setdefault('model', blk.get('model','') or blk.get('name',''))
            prod = blk.get('productionDate') or blk.get('releaseDate')
            if prod:
                out['year'] = str(prod)[:4]
            mileage = blk.get('mileageFromOdometer')
            if isinstance(mileage, dict):
                out['mileage'] = str(mileage.get('value',''))
            elif mileage:
                out['mileage'] = str(mileage)
            offers = blk.get('offers')
            if isinstance(offers, dict):
                out['price'] = str(offers.get('price',''))
                out['currency'] = str(offers.get('priceCurrency',''))
            fuel = blk.get('fuelType')
            if isinstance(fuel, dict):
                out['fuel_type'] = fuel.get('name','')
            elif fuel:
                out['fuel_type'] = fuel
            cap = blk.get('engineDisplacement') or blk.get('engineCapacity')
            if isinstance(cap, dict):
                out['capacity'] = str(cap.get('value',''))
            elif cap:
                out['capacity'] = str(cap)
            power = blk.get('enginePower')
            if isinstance(power, dict):
                out['power'] = str(power.get('value',''))
            elif power:
                out['power'] = str(power)
            color = blk.get('color')
            if color:
                out['color'] = color
            body = blk.get('bodyType')
            if body:
                out['body_type'] = body
    return out

def _balanced_json(raw: str):
    start = raw.find('{')
    if start == -1:
        return None
    buf = []
    depth = 0
    in_str = False
    esc = False
    for ch in raw[start:]:
        buf.append(ch)
        if esc:
            esc = False
            continue
        if ch == '\\':
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                break
    try:
        return json.loads(''.join(buf))
    except Exception:
        return None

def _extract_from_state(state):
    out = {}
    def walk(parent_key, obj):
        if isinstance(obj, dict):
            if 'price' in obj and isinstance(obj['price'], (int,float,str)):
                out.setdefault('price', str(obj['price']))
            if 'amount' in obj and isinstance(obj['amount'], (int,float,str)):
                out.setdefault('price', str(obj['amount']))
            if 'priceAmount' in obj:
                out.setdefault('price', str(obj.get('priceAmount')))
            if 'currency' in obj and isinstance(obj['currency'], str):
                out.setdefault('currency', obj['currency'])
            if 'priceCurrency' in obj and isinstance(obj['priceCurrency'], str):
                out.setdefault('currency', obj['priceCurrency'])
            for k in ['brand','make']:
                if k in obj and isinstance(obj[k], (str,dict)):
                    out.setdefault('brand', obj[k]['name'] if isinstance(obj[k],dict) else obj[k])
            for k in ['model','modelName']:
                if k in obj and isinstance(obj[k], str):
                    out.setdefault('model', obj[k])
            for k in ['year','productionYear','production']:
                if k in obj and obj[k]:
                    out.setdefault('year', str(obj[k])[:4])
            for k in ['mileage','odometer']:
                if k in obj and obj[k]:
                    out.setdefault('mileage', str(obj[k]))
            for k in ['fuel','fuelType']:
                if k in obj and obj[k]:
                    out.setdefault('fuel_type', obj[k] if isinstance(obj[k],str) else obj[k].get('name',''))
            for k in ['engineCapacity','engine_displacement','engineDisplacement']:
                if k in obj and obj[k]:
                    out.setdefault('capacity', str(obj[k]))
            for k in ['power','hp','kw']:
                if k in obj and obj[k]:
                    out.setdefault('power', str(obj[k]))
            if (('label' in obj or 'name' in obj or 'title' in obj) and ('value' in obj or 'val' in obj or 'text' in obj)):
                label = (obj.get('label') or obj.get('name') or obj.get('title') or '').strip()
                value = obj.get('value') or obj.get('val') or obj.get('text')
                if isinstance(value, dict):
                    value = value.get('name') or value.get('value')
                if isinstance(value, list):
                    value = ', '.join(str(x) for x in value if x)
                if label and value:
                    mapped = _map_params({label: str(value)})
                    for k,v in mapped.items():
                        out.setdefault(k, v)
            for k,v in obj.items():
                if isinstance(v, (dict,list)):
                    walk(k, v)
        elif isinstance(obj, list):
            for it in obj:
                walk(parent_key, it)
    walk('', state)
    return out

def _parse_embedded_state(soup):
    out = {}
    for sc in soup.find_all('script'):
        t = (sc.get('type') or '').lower()
        sid = (sc.get('id') or '').lower()
        txt = sc.string or sc.get_text() or ''
        state = None
        if 'application/json' in t and ('__next_data__' in sid or 'state' in sid):
            try:
                state = json.loads(txt)
            except Exception:
                state = None
        if state is None and ('__NEXT_DATA__' in txt or '__INITIAL_STATE__' in txt or 'initialState' in txt):
            m = re.search(r'(?:__NEXT_DATA__|__INITIAL_STATE__|initialState)\s*=\s*({.*?})\s*[;\n<]', txt, re.S)
            if m:
                state = _balanced_json(m.group(1))
        if state:
            extracted = _extract_from_state(state)
            for k,v in extracted.items():
                out.setdefault(k, v)
    return out

PRICE_REGEX = re.compile(r"([0-9][0-9 .\u00A0]{1,15})(PLN|EUR|USD|GBP|zl|zł)?", re.I)

def _extract_price(soup):
    price_txt = ""
    currency = ""
    selectors = [
        '[data-testid*="price" i]', '[data-qa*="price" i]', '[data-cy*="price" i]',
        '[class*="price" i]', '[id*="price" i]'
    ]
    for sel in selectors:
        try:
            for tag in soup.select(sel):
                txt = tag.get_text(" ", strip=True)
                if txt and PRICE_REGEX.search(txt.replace('\u00A0',' ')):
                    price_txt = txt
                    break
            if price_txt:
                break
        except Exception:
            continue
    if not price_txt:
        mp = soup.find("meta", attrs={'property':'product:price:amount'})
        if mp:
            price_txt = mp.get('content','')
        mc = soup.find("meta", attrs={'property':'product:price:currency'})
        if mc:
            currency = mc.get('content','')
    if not price_txt:
        price_container = soup.find(['div','h3','span'], class_=re.compile(r"offer-price|price", re.I))
        if price_container:
            price_txt = price_container.get_text(" ", strip=True)
    if price_txt:
        m = PRICE_REGEX.search(price_txt.replace('\u00A0',' '))
        if m:
            num = m.group(1)
            cur = m.group(2) or currency
            num = re.sub(r"[^0-9]", "", num)
            if cur:
                cur = 'PLN' if ('zl' in cur.lower() or 'zł' in cur.lower()) else cur.upper()
            return num, cur
    return "",""

def _extract_params_html(soup):
    params = {}
    param_items = soup.find_all(["li","div"], class_=re.compile(r"offer-params__item|parameter|param-item|detail|params|label"))
    for item in param_items:
        label_tag = item.find(["span","div","p"], class_=re.compile(r"label|key|name|title"))
        value_tag = item.find(["div","span","p","a"], class_=re.compile(r"value|val|data|number|val|content"))
        if label_tag and value_tag:
            k = label_tag.get_text(strip=True)
            v = value_tag.get_text(" ", strip=True)
            if k and v:
                params[k] = v
    if not params:
        for dt in soup.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            if dd:
                k = dt.get_text(strip=True)
                v = dd.get_text(" ", strip=True)
                if k and v:
                    params[k] = v
    if not params:
        for li in soup.find_all('li'):
            spans = li.find_all(['span','div'])
            if len(spans) >= 2:
                k = spans[0].get_text(strip=True)
                v = spans[1].get_text(" ", strip=True)
                if k and v and len(k) < 40 and len(v) < 80:
                    params[k] = v
    return params

def _extract_features(soup):
    feats = []
    try:
        containers = soup.select('[data-testid*="equipment" i], [class*="equipment" i], [class*="features" i], [data-qa*="equipment" i]')
    except Exception:
        containers = []
    for c in containers:
        for li in c.find_all('li'):
            t = li.get_text(strip=True)
            if 2 < len(t) < 80:
                feats.append(t)
    if not feats:
        for li in soup.find_all('li', class_=re.compile(r"feature|equipment", re.I)):
            t = li.get_text(strip=True)
            if 2 < len(t) < 80:
                feats.append(t)
    seen = set()
    ordered = []
    for f in feats:
        if f not in seen:
            seen.add(f)
            ordered.append(f)
    return ordered


def listing_links_from_results(html, base_url):
    """Zwraca listę absolutnych URL-i do kart ogłoszeń"""
    soup = BeautifulSoup(html, "html.parser")
    hrefs = [a.get("href") for a in soup.find_all("a", href=True)]
    abs_hrefs = [urljoin(base_url, h) for h in hrefs if h]
    patterns = [
        re.compile(r"https?://[^/]*otomoto\.pl/.+?/oferta/.+?ID[A-Za-z0-9]+\.html"),
        re.compile(r"/oferta/"),
    ]
    matches = []
    for h in abs_hrefs:
        for p in patterns:
            try:
                if p.search(h):
                    matches.append(h)
                    break
            except Exception:
                continue
    seen = set()
    result = []
    for u in matches:
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result


def extract_data_from_page(page, url):
    """Ekstrakcja z Playwright page + BeautifulSoup + osadzone stany"""
    data = {
        'url': url,'title':'','brand':'','model':'','year':'','mileage':'','price':'','currency':'','fuel_type':'','transmission':'','capacity':'','power':'','color':'','doors':'','seats':'','body_type':'','condition':'','country':'','vin':'','features':'','description':'',
    }
    # Spróbuj tytuł
    try:
        h1 = page.locator('h1').first
        if h1.count() > 0:
            data['title'] = (h1.text_content() or '').strip()
        else:
            data['title'] = page.title() or ''
    except Exception:
        pass

    # JSON-LD przez Playwright (szybciej niż Soup)
    try:
        jd_texts = page.eval_on_selector_all("script[type='application/ld+json']", "els => els.map(e=>e.textContent)")
        if jd_texts:
            for txt in jd_texts:
                try:
                    obj = json.loads(txt)
                    objs = obj if isinstance(obj, list) else [obj]
                    for o in objs:
                        t = str(o.get('@type') or '').lower()
                        if any(k in t for k in ['vehicle','product','offer','car']):
                            b = o.get('brand')
                            if isinstance(b, dict):
                                data['brand'] = data['brand'] or b.get('name','')
                            elif isinstance(b, str):
                                data['brand'] = data['brand'] or b
                            data['model'] = data['model'] or o.get('model') or o.get('name','')
                            prod = o.get('productionDate') or o.get('releaseDate')
                            if prod:
                                data['year'] = data['year'] or str(prod)[:4]
                            mil = o.get('mileageFromOdometer')
                            if isinstance(mil, dict):
                                data['mileage'] = data['mileage'] or str(mil.get('value',''))
                            elif mil:
                                data['mileage'] = data['mileage'] or str(mil)
                            offers = o.get('offers')
                            if isinstance(offers, dict):
                                data['price'] = data['price'] or re.sub(r'[^0-9]','', str(offers.get('price','')))
                                data['currency'] = data['currency'] or str(offers.get('priceCurrency',''))
                            fuel = o.get('fuelType')
                            if isinstance(fuel, dict):
                                data['fuel_type'] = data['fuel_type'] or fuel.get('name','')
                            elif fuel:
                                data['fuel_type'] = data['fuel_type'] or fuel
                            cap = o.get('engineDisplacement') or o.get('engineCapacity')
                            if isinstance(cap, dict):
                                data['capacity'] = data['capacity'] or re.sub(r'[^0-9]','', str(cap.get('value','')))
                            elif cap:
                                data['capacity'] = data['capacity'] or re.sub(r'[^0-9]','', str(cap))
                            powv = o.get('enginePower')
                            if isinstance(powv, dict):
                                data['power'] = data['power'] or re.sub(r'[^0-9]','', str(powv.get('value','')))
                            elif powv:
                                data['power'] = data['power'] or re.sub(r'[^0-9]','', str(powv))
                except Exception:
                    continue
    except Exception:
        pass

    # Osadzony stan (window.__NEXT_DATA__ / __INITIAL_STATE__)
    try:
        state = page.evaluate("() => window.__NEXT_DATA__ || window.__INITIAL_STATE__ || window.initialState || null")
        if state:
            extracted = _extract_from_state(state)
            for k,v in extracted.items():
                if k in data and not data[k] and v:
                    data[k] = str(v)
    except Exception:
        pass

    # Renderowany HTML → Soup parsowanie reszty
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    # PARAMS przez JS (dt/dd + heurystyki data-testid + direct testid)
    try:
        js_params = page.evaluate(
            r"""
            () => {
              const map = {};
              // dt/dd pairs
              document.querySelectorAll('dt').forEach(dt=>{
                const dd = dt.nextElementSibling;
                if(dd && dd.tagName && dd.tagName.toLowerCase()==='dd'){
                  const k = (dt.textContent||'').trim();
                  const v = (dd.textContent||'').replace(/\s+/g,' ').trim();
                  if(k && v){ map[k]=v; }
                }
              });
              // testid-based sections
              const testids = ['year','mileage','fuel_type','gearbox','body_type','power','capacity','color','door_count','nr_seats','country_origin','new_used','vin','transmission','version'];
              testids.forEach(tid=>{
                const el = document.querySelector(`[data-testid="${tid}"]`);
                if(el){
                  const ps = el.querySelectorAll('p');
                  if(ps.length >= 2){
                    const k = ps[0].textContent.trim();
                    const v = ps[ps.length-1].textContent.replace(/\s+/g,' ').trim();
                    if(k && v){ map[k] = v; }
                  }
                }
              });
              // parameter/param containers
              document.querySelectorAll('[data-testid*="parameter" i], [class*="parameter" i], [class*="param" i]').forEach(el=>{
                const label = el.querySelector('[class*="label" i], [data-testid*="label" i], dt');
                const value = el.querySelector('[class*="value" i], [data-testid*="value" i], dd');
                const k = label && (label.textContent||'').trim();
                const v = value && (value.textContent||'').replace(/\s+/g,' ').trim();
                if(k && v){ map[k]=v; }
              });
              return map;
            }
            """
        )
        if js_params:
            mapped_js = _map_params(js_params)
            for k,v in mapped_js.items():
                if k in data and not data[k]:
                    data[k] = v
    except Exception:
        pass

    # PARAMS
    try:
        mapped = _map_params(_extract_params_html(soup))
        for k,v in mapped.items():
            if k in data and not data[k]:
                data[k] = v
    except Exception:
        pass

    # PRICE
    try:
        price, curr = _extract_price(soup)
        if price and not data['price']:
            data['price'] = price
        if curr and not data['currency']:
            data['currency'] = curr
    except Exception:
        pass

    # FEATURES
    try:
        feats_js = page.evaluate(
            """
            () => {
              const items = [];
              const findFromHeading = (txt) => {
                const heads = Array.from(document.querySelectorAll('h2, h3, h4')).filter(h=> (h.textContent||'').toLowerCase().includes(txt));
                heads.forEach(h=>{
                  const section = h.closest('section') || h.parentElement;
                  if(!section) return;
                  section.querySelectorAll('li').forEach(li=>{
                    const t = (li.textContent||'').replace(/\\s+/g,' ').trim();
                    if(t && t.length>2 && t.length<80) items.push(t);
                  });
                });
              };
              findFromHeading('wyposa');
              if(items.length===0){
                document.querySelectorAll('[data-testid*=\"equipment\" i], [class*=\"equipment\" i], [class*=\"features\" i]').forEach(c=>{
                  c.querySelectorAll('li').forEach(li=>{
                    const t = (li.textContent||'').replace(/\s+/g,' ').trim();
                    if(t && t.length>2 && t.length<80) items.push(t);
                  });
                });
              }
              return Array.from(new Set(items));
            }
            """
        ) or []
        feats = feats_js or _extract_features(soup)
        if feats and not data['features']:
            data['features'] = '; '.join(feats)
    except Exception:
        pass

    # DESCRIPTION
    if not data['description']:
        desc = soup.find('div', class_=re.compile(r"description|offer-description", re.I))
        if desc:
            data['description'] = desc.get_text(" ", strip=True)[:800]

    # Heurystyki z tytułu
    title_lower = data['title'].lower()
    if not data['brand']:
        if title_lower.startswith('volkswagen'):
            data['brand'] = 'Volkswagen'
    if not data['model'] and 'passat' in title_lower:
        data['model'] = 'Passat'
    # Silnik w tytule np. 1.9 TDI → pojemność i paliwo
    if not data['capacity']:
        m_liters = re.search(r'(\d\.\d)\s?(tdi|fsi|mpi|cdti|hdi|gdi|ecoboost|benzyna|diesel)', title_lower)
        if m_liters:
            liters = m_liters.group(1)
            try:
                data['capacity'] = str(int(float(liters.replace(',', '.'))*1000))
            except Exception:
                pass
    if not data['fuel_type']:
        if 'tdi' in title_lower or 'diesel' in title_lower:
            data['fuel_type'] = 'Diesel'
        elif 'benz' in title_lower or 'fsi' in title_lower:
            data['fuel_type'] = 'Benzyna'
    # Moc np. 130 KM
    if not data['power']:
        m_power = re.search(r'(\d{2,3})\s?KM', html, re.I)
        if m_power:
            data['power'] = m_power.group(1)
    # Pojemność skokowa w treści np. 1 896 cm3
    if not data['capacity']:
        m_cap = re.search(r'(\d[\d\s]{2,5})\s?cm3', html)
        if m_cap:
            data['capacity'] = re.sub(r'[^0-9]','', m_cap.group(1))
    # Rok produkcji
    if not data['year']:
        m_year = re.search(r'(19|20)\d{2}', html)
        if m_year:
            year_val = m_year.group(0)
            if 1980 <= int(year_val) <= 2025:
                data['year'] = year_val
    # Przebieg
    if not data['mileage']:
        m_mil = re.search(r'(\d[\d\s]{3,9})\s?km', html, re.I)
        if m_mil:
            data['mileage'] = re.sub(r'[^0-9]','', m_mil.group(1))
    
    # Waluta (PLN domyślnie dla OTOMOTO Polska)
    if not data['currency']:
        if data['price']:
            data['currency'] = 'PLN'

    # Normalizacje
    if data['mileage']:
        data['mileage'] = re.sub(r'[^0-9]','', str(data['mileage']))
    if data['capacity'] and re.search(r"[0-9]", str(data['capacity'])):
        data['capacity'] = re.sub(r'[^0-9]','', str(data['capacity']))
    if data['power'] and re.search(r"[0-9]", str(data['power'])):
        data['power'] = re.sub(r'[^0-9]','', str(data['power']))
    return data


def scrape_with_manual_assist():
    """Główna funkcja scrapingu z interakcją użytkownika"""
    # Krok 1: Pobierz linki
    print("📥 Pobieram linki z wyników wyszukiwania...")
    print(f"   URL: {SEARCH_URL}")
    resp = SESSION.get(SEARCH_URL, timeout=30)
    resp.raise_for_status()
    links = listing_links_from_results(resp.text, SEARCH_URL)[:LIMIT]
    print(f"✓ Znaleziono {len(links)} linków\n")
    
    if not links:
        print("❌ Brak linków – sprawdź URL wyszukiwania")
        return
    
    rows = []
    
    with sync_playwright() as p:
        # Uruchom widoczną przeglądarkę
        print("🌐 Uruchamiam przeglądarkę Chromium...")
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent=UA['User-Agent'],
            locale='pl-PL',
            extra_http_headers=UA
        )
        page = context.new_page()
        
        try:
            # Pierwszy link - INTERAKTYWNIE
            first_url = links[0]
            print(f"\n{'='*70}")
            print(f"🔗 PIERWSZY LINK: {first_url}")
            print(f"{'='*70}")
            print("\n⏸️  PAUZA – TERAZ TWOJA KOLEJ:")
            print("   1. W oknie przeglądarki kliknij 'Akceptuję' na cookies")
            print("   2. Rozwiąż CAPTCHA jeśli się pojawi")
            print("   3. Sprawdź czy widzisz pełne dane ogłoszenia (cenę, parametry)")
            print("   4. ⚠️ WAŻNE: NIE ZAMYKAJ okna przeglądarki!")
            print("   5. Wróć tutaj i naciśnij ENTER ⬇️\n")
            
            try:
                page.goto(first_url, wait_until='domcontentloaded', timeout=120000)
            except Exception as nav_err:
                print(f"⚠️ Ostrzeżenie: timeout przy przejściu do pierwszego linku (próbuję dalej): {nav_err}")
            try:
                page.wait_for_selector("h1, [data-testid*='price' i], dt, script[type='application/ld+json']", timeout=90000)
            except Exception:
                pass
            
            # CZEKAJ NA ENTER
            input("👉 Naciśnij ENTER aby kontynuować... ")
            
            print("\n✅ OK! Pobieram dane z pierwszej strony i kontynuuję...\n")
            
            # Zbierz dane z pierwszej strony
            time.sleep(0.8)
            # DEBUG: save first page HTML
            try:
                html_debug = page.content()
                with open('debug_first_page.html', 'w', encoding='utf-8') as f:
                    f.write(html_debug)
                print("[DEBUG] Zapisano debug_first_page.html")
            except Exception:
                pass
            
            # Ekstrakcja danych z pierwszej strony
            try:
                data = extract_data_from_page(page, first_url)
                rows.append(data)
                print(f"[1/{len(links)}] ✓ {data.get('title', 'Brak tytułu')[:50]} → {data.get('price','?')} {data.get('currency','')}")
                print(f"[DEBUG 1] brand={data.get('brand')}, model={data.get('model')}, year={data.get('year')}, mileage={data.get('mileage')}, fuel={data.get('fuel_type')}, capacity={data.get('capacity')}, power={data.get('power')}")
            except Exception as e:
                print(f"❌ Błąd podczas ekstrakcji pierwszej strony: {e}")
                if "closed" in str(e).lower():
                    print("⚠️ UWAGA: Przeglądarka została zamknięta!")
                    print("   NIE ZAMYKAJ okna przeglądarki ręcznie - zostaw je otwarte.")
                    print("   Skrypt automatycznie zamknie przeglądarkę po zakończeniu.")
                    return
                raise
            
            # Pozostałe linki - AUTOMATYCZNIE
            for i, url in enumerate(links[1:], start=2):
                time.sleep(0.8)
                try:
                    try:
                        page.goto(url, wait_until='domcontentloaded', timeout=120000)
                    except Exception as nav_err:
                        print(f"   ⚠️ Ostrzeżenie: timeout przy przejściu → {url} (próbuję dalej)")
                    try:
                        page.wait_for_selector("h1, [data-testid*='price' i], dt, script[type='application/ld+json']", timeout=90000)
                    except Exception:
                        pass
                    time.sleep(0.8)
                    data = extract_data_from_page(page, url)
                    rows.append(data)
                    print(f"[{i}/{len(links)}] ✓ {data.get('title', 'Brak tytułu')[:50]} → {data.get('price','?')} {data.get('currency','')}")
                except Exception as e:
                    print(f"[{i}/{len(links)}] ✗ Błąd: {e}")
                    rows.append({'url': url, 'error': str(e)})
            
        finally:
            context.close()
            browser.close()
    
    # Eksport do XLSX
    print(f"\n💾 Eksportuję dane do {OUT_FILE}...")
    cols = ['url', 'title', 'brand', 'model', 'year', 'mileage', 'price', 'currency',
            'fuel_type', 'transmission', 'capacity', 'power', 'color', 'doors', 'seats',
            'body_type', 'condition', 'country', 'vin', 'features', 'description']
    
    df = pd.DataFrame(rows)
    for c in cols:
        if c not in df.columns:
            df[c] = ''
    df = df[cols]
    
    # Zapisz do nowego pliku (zawsze tworzy nowy z timestampem)
    df.to_excel(OUT_FILE, index=False, engine='openpyxl')
    print(f"✅ GOTOWE! Zapisano {len(rows)} wierszy → {OUT_FILE}")
    # Statystyka braków
    try:
        print("\nBraki wartości na kolumnę (0 = super):")
        for c in cols:
            empties = (df[c].astype(str).str.len()==0) | (df[c].isna())
            print(f" - {c:12}: {int(empties.sum())}")
    except Exception:
        pass
    print(f"📊 Lokalizacja: {sys.path[0]}\\{OUT_FILE}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  OTOMOTO SCRAPER - TRYB MANUAL ASSIST")
    print("="*70 + "\n")
    
    try:
        scrape_with_manual_assist()
    except KeyboardInterrupt:
        print("\n\n⚠️ Przerwano przez użytkownika")
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()
