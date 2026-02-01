# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

URL = "https://englishjobs.es/in/comunidad-de-madrid"
HEADERS = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = "EnglishJobs – Empleos en Comunidad de Madrid"
ET.SubElement(channel, "link").text = URL
ET.SubElement(channel, "description").text = "Feed RSS generado de EnglishJobs: empleos que requieren inglés en Comunidad de Madrid"
ET.SubElement(channel, "language").text = "es"
ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

offers = soup.select("div.job")

for offer in offers:
    title_tag = offer.find("a")
    if not title_tag:
        continue

    title = title_tag.get_text(strip=True)
    link = title_tag.get("href")
    if link and not link.startswith("http"):
        link = "https://englishjobs.es" + link

    pubDate = offer.select_one("span.date")
    pubDate_text = pubDate.get_text(strip=True) if pubDate else datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    ET.SubElement(item, "guid").text = link
    ET.SubElement(item, "description").text = f"Oferta de empleo: {title}"
    ET.SubElement(item, "pubDate").text = pubDate_text

tree = ET.ElementTree(rss)
tree.write("rss/englishjobs_madrid.xml", encoding="utf-8", xml_declaration=True)
print("Feed generado: rss/englishjobs_madrid.xml")
