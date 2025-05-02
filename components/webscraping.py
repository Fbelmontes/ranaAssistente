import requests
from bs4 import BeautifulSoup
import pandas as pd

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

def extract_event_details(soup):
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

def extract_page_data(page_number):
    url = f"https://rio.websummit.com/schedule/page/{page_number}/" if page_number > 1 else "https://rio.websummit.com/schedule/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
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
                details = extract_event_details(soup)
                event_data.update(details)
                eventos.append(event_data)
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

def start_scraping():
    all_events = []
    page = 1
    while True:
        print(f"Processando página {page}...")
        page_events = extract_page_data(page)
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
        return df  # Retorna o DataFrame com todos os eventos
    else:
        return None
