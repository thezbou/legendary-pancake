# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os
os.makedirs("rss", exist_ok=True)
BASE_URL = "https://englishjobs.es"
TARGET_URL = "https://englishjobs.es/in/comunidad-de-madrid"
HEADERS = {"User-Agent": "Mozilla/5.0"}
fecha_limite = datetime.utcnow() - timedelta(days=30)
def parse_fecha(texto):
    try:
        fecha_dt = datetime.strptime(texto.strip(), "%%B %%d")
        fecha_dt = fecha_dt.replace(year=datetime.utcnow().year)
        return fecha_dt
    except:
        return datetime.utcnow()
response = requests.get(TARGET_URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "EnglishJobs - Empleos con ingl‚s en Comunidad de Madrid"
ET.SubElement(channel, "link").text = TARGET_URL
ET.SubElement(channel, "description").text = "Ofertas con ingl‚s publicadas en los £ltimos 30 d¡as"
ET.SubElement(channel, "language").text = "es"
ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%%a, %%d %%b %%Y %%H:%%M:%%S GMT")
offers = soup.select("div.job")
for offer in offers:
    title_tag = offer.find("a")
    if not title_tag:
        continue
    title = title_tag.get_text(strip=True)
    link = title_tag.get("href")
    if link and not link.startswith("http"):
        link = BASE_URL + link
    span_date = offer.select_one("span.date")
    fecha_dt = parse_fecha(span_date.get_text(strip=True)) if span_date else datetime.utcnow()
        continue
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    ET.SubElement(item, "guid").text = link
    ET.SubElement(item, "description").text = f"Oferta: {title}"
    ET.SubElement(item, "pubDate").text = fecha_dt.strftime("%%a, %%d %%b %%Y %%H:%%M:%%S GMT")
tree = ET.ElementTree(rss)
tree.write("rss/englishjobs_madrid.xml", encoding="utf-8", xml_declaration=True)
print("RSS generado en rss/englishjobs_madrid.xml")

