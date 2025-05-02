import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from streamlit import st

# ============ Configuração do navegador ============ 
def setup_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Para rodar em segundo plano no Streamlit
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# ============ Funções de scraping ============ 
def extract_speakers(soup):
    speakers = []
    for speaker in soup.select('[class*="ListItemStyles__StyledListItemWrapper"]'):
        try:
            name = speaker.select_one('[class*="ListItemStyles__ItemTitle"]').get_text(strip=True)
            role_raw = speaker.select_one('[class*="ListItemStyles__StyledContent"]').get_text(strip=True)
            role = re.sub(r'(?<=[a-z])(?=[A-Z])', '\n', role_raw)
            speakers.append(f"{name} ({role})")
        except:
            continue
    return "; ".join(speakers) if speakers else "N/A"

def extract_event_details(driver, event_url):
    try:
        driver.get(event_url)
        time.sleep(1.5)
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        description = "N/A"
        try:
            description = soup.select_one('[class*="GeneralSessionDetailsLayout__StyledDescription"]').get_text(strip=True)
        except:
            pass
        speakers = extract_speakers(soup)
        return {
            "Descrição": description,
            "Palestrantes": speakers
        }
    except Exception as e:
        print(f"\nErro ao acessar página do evento: {str(e)[:100]}...")
        return {
            "Descrição": "N/A",
            "Palestrantes": "N/A"
        }

def extract_page_data(driver, page_number):
    url = f"https://rio.websummit.com/schedule/page/{page_number}/" if page_number > 1 else "https://rio.websummit.com/schedule/"
    try:
        driver.get(url)
        time.sleep(2.5)
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, window.innerHeight * 0.8);")
            time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        eventos = []
        for card in soup.select('[class*="SessionCardStyled__SessionCardWrapper"]'):
            try:
                event_link = f"https://rio.websummit.com{card.find('a')['href']}" if card.find('a') else None
                if not event_link:
                    continue
                event_data = {
                    "Título": card.select_one('[class*="SessionCardStyled__SessionCardHeader"]').get_text(strip=True),
                    "Horário": card.select_one('[class*="SessionCardStyled__SessionCardDateTime"]').get_text(strip=True),
                    "Local": card.select_one('[class*="SessionCardLocation__StyledAddress"]').get_text(strip=True),
                    "Tag": card.select_one('[class*="SessionCardStyled__SessionTrackLabel"]').get_text(strip=True) if card.select_one('[class*="SessionCardStyled__SessionTrackLabel"]') else "Sem Tag",
                    "Link": event_link
                }
                details = extract_event_details(driver, event_link)
                event_data.update(details)
                eventos.append(event_data)
                driver.back()
                time.sleep(1.5)
            except Exception as e:
                print(f"\nErro em um card: {e}")
                continue
        return eventos
    except Exception as e:
        print(f"\nErro ao acessar página {page_number}: {str(e)[:100]}...")
        return []

def gerar_hiperlink(row):
    link = row["Link"]
    titulo = row["Título"].replace('"', '')
    return f'=HYPERLINK("{link}", "{titulo}")'

# ============ Função principal (sem GUI) ============ 
def start_scraping(progress_var):
    driver = setup_driver()
    all_events = []
    page = 1
    try:
        while True:
            progress_var.set(page * 5)
            print(f"Processando página {page}...")
            page_events = extract_page_data(driver, page)
            if not page_events:
                print(f"\nPágina {page} vazia. Encerrando coleta.")
                break
            all_events.extend(page_events)
            page += 1

        if all_events:
            df = pd.DataFrame(all_events).drop_duplicates(subset=['Título', 'Horário', 'Local'], keep='first')
            df['Título com Link'] = df.apply(gerar_hiperlink, axis=1)
            cols = ['Título com Link', 'Horário', 'Local', 'Tag', 'Descrição', 'Palestrantes']
            df = df[cols]
            return df
        else:
            print("Nenhum evento encontrado.")
            return None
    finally:
        driver.quit()
