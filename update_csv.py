import re
import csv
import os.path

from bs4 import BeautifulSoup


with open('alt-images.csv', newline='', encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)

pages = []
for row in data[1:]:
    if row[0] not in pages:
        pages.append(row[0])

for page in pages:
    print(f"processing page {page}", end=", ")

    file_path = f'/../BookingNinjasPBO/bnpbo/main/default/pages/{page}'
    doc_page = open(os.path.dirname(__file__) + file_path, "r", encoding="utf-8").read()

    data_to_update = [x[:-2] for x in data if x[0] == page]
    print(f"total alt image to be update {len(data_to_update)}")

    for _data in data_to_update:
        page_soup = BeautifulSoup(doc_page, "html.parser")  # vf page parser
        img_soup = BeautifulSoup(_data[1], "html.parser")  # target img tag
        # get target img tag on the vf page
        image_url = img_soup.select_one('img').get("src")

        new_tag = page_soup.find("img", attrs={"src" : image_url})

        if _data[2] == '-' or _data[2] == '':
            print("=====skipped=====")
            continue
        new_tag["alt"] = _data[2]  # replace alt with new value

        old_tag = re.findall(r'<img[^>]+>', doc_page)
        old_tag = [x for x in old_tag if f'{image_url}' in x][0]

        # replace doc page img tag with new tag
        doc_page = doc_page.replace(old_tag, str(new_tag))

    with open(page, "w", encoding="utf-8") as f:
        f.write(doc_page)
