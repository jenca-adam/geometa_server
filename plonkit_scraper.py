from bs4 import BeautifulSoup as bs
import requests
import json
import server.database as db
import time
UAGENT = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0"}
def process_guide(guide):
    country = db.session.query(db.Country).filter(db.Country.iso2==guide.get('code','').lower()).first()
    if not country:
        return
    url = f"https://www.plonkit.net/{guide['slug']}"
    html = requests.get(url, headers=UAGENT).content
    soup  = bs(html, 'html.parser')
    script = soup.find(id="__PRELOADED_DATA__")
    if not script:
        print(html)
        return
    data = json.loads(script.text)["data"]["public"]
    step_index = 1
    for step in data["steps"]:
        meta_index=1
        if step["kind"] == "tip":
            for item in step["items"]:
                if item["kind"] == "tip":
                    image_root = item["data"].get("image", {}).get("imageUrl")
                    if image_root:
                        image = f"https://www.plonkit.net/{image_root}"
                    else:
                        image = "https://http.cat/404"
                    title = f"!PLNK-{guide['title']}-{step_index}-{meta_index}!"
                    description = "\n".join(text for text in item["data"]["text"])
                    link=f"{url}#{step_index}-{meta_index}"
                    meta_data = {"title":title, "description":description, "link":link, "image": image,}
                    db.create_meta(meta_data, "0"*10, [], country)
                meta_index+=1
            step_index+=1
GUIDES = requests.get("https://www.plonkit.net/api/guides", headers=UAGENT).json().get("data",[])
for guide in GUIDES:
    print(guide)
    process_guide(guide)
