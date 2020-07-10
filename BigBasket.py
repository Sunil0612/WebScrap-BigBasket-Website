import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

filename = "BigBasket.csv"
f = open(filename, "w")
headers = "Brand, Name, MRP, Price, Discount, About, Storage and Uses, Nutritional Facts, Benefits, Other Product Info, Variable weight policy, How to Use, Ingredients/Composition\n"
f.write(headers)

chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
browser = webdriver.Chrome(options=chrome_options)
url="https://www.bigbasket.com/product/all-categories/"
agent={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
page=requests.get(url, headers=agent)
soup=BeautifulSoup(page.content,'html.parser')
containers=soup.findAll("div",{"class":"uiv2-search-cover"})

for container in containers:
    minicontainers = container.find("ul")
    tempmini = minicontainers.find_all("a")
    for minicontainer in tempmini:

        links = minicontainer.get('href')
        url = "https://www.bigbasket.com" + links
        browser.get(url)
        time.sleep(5)

        page_source = browser.page_source
        nextsoup = BeautifulSoup(page_source, 'html.parser')
        nextcontainers = nextsoup.findAll("div", {"qa": "product"})
        for nextcontainer in nextcontainers:
            a_tag = nextcontainer.find("a")
            link = a_tag.get("href")
            nexturl = "https://www.bigbasket.com" + link
            try:
                browser.get(nexturl)
            except:
                continue
            temp_page_source = browser.page_source
            soup = BeautifulSoup(temp_page_source, 'html.parser')

            try:
                brand = soup.find("a", {"context": "brandlabel"}).text
            except:
                continue
            try:
                name = soup.find("h1", {"class": "GrE04"}).text.replace("\n", "").strip()
            except:
                continue
            try:
                mrp = soup.find("td", {"class": "_2ifWF"}).text.replace("\n", "").strip()
            except:
                mrp = ""
            try:
                price = soup.find("td", {"data-qa": "productPrice"}).text.replace("\n", "").strip()
            except:
                continue
            try:
                dis = soup.find_all("td", {"class": "IyLvo"})
                discount = dis[1].text.replace("\n", "").strip()
            except:
                discount = ""
            try:
                desc = soup.find("section", {"class": "_3JQUe"})
            except:
                continue
            try:
                descriptions = desc.find_all("div", {"class": "_3ezVU"})
            except:
                continue
            about = ""
            storage = ""
            benefits = ""
            other = ""
            variable = ""
            nutrition = ""
            ingred_comp = ""
            specs = ""
            how_to = ""
            for description in descriptions:
                try:
                    descp = description.find("div", {"class": "_3LyVz"}).text.split(" ")[0]
                except:
                    continue
                if descp.lower() == "about":
                    try:
                        about = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "nutritional" or descp.lower() == "nutrition":
                    try:
                        nutrition = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "benefits" or descp.lower() == "benefit":
                    try:
                        benefits = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "other":
                    try:
                        other = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "variable":
                    try:
                        variable = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "storage":
                    try:
                        storage = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "how":
                    try:
                        how_to = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "ingredient" or descp.lower() == "ingredients" or descp.lower() == "composition":
                    try:
                        ingred_comp = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                elif descp.lower() == "specification" or descp.lower() == "specifications":
                    try:
                        specs = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                    except:
                        continue
                else:
                    continue

            pack_sizes = browser.find_elements_by_class_name("_2Z6Vt")

            if (len(pack_sizes) == 0):
                f.write(str(brand.replace(",","")) + "," + str(name.replace(",", "")) + "," + str(mrp.replace(",", "")) + "," + str(
                    price.replace(",", "")) + "," + str(discount.replace(",", "")) + "," + str(about.replace(",", "")) + "," + str(
                    storage.replace(",", "")) + "," + str(nutrition.replace(",", "")) + "," + str(benefits.replace(",", "")) + "," + str(
                    other.replace(",", "")) + "," + str(variable.replace(",", "")) + "," + str(how_to.replace(",", "")) + "," + str(
                    ingred_comp.replace(",", "")) + "," + str(specs.replace(",", "")) + "\n")

            pack_sizes = browser.find_elements_by_class_name("_2Z6Vt")

            for p in pack_sizes:
                p.click()
                temp_page_source = browser.page_source
                soup = BeautifulSoup(temp_page_source, 'html.parser')

                try:
                    brand = soup.find("a", {"context": "brandlabel"}).text
                except:
                    continue
                try:
                    name = soup.find("h1", {"class": "GrE04"}).text.replace("\n", "").strip()
                    # print("name=" + name)
                except:
                    continue
                try:
                    mrp = soup.find("td", {"class": "_2ifWF"}).text.replace("\n", "").strip()
                except:
                    mrp = ""
                try:
                    price = soup.find("td", {"data-qa": "productPrice"}).text.replace("\n", "").strip()
                except:
                    continue
                try:
                    dis = soup.find_all("td", {"class": "IyLvo"})
                    discount = dis[1].text.replace("\n", "").strip()
                except:
                    discount = ""
                try:
                    desc = soup.find("section", {"class": "_3JQUe"})
                except:
                    continue
                try:
                    descriptions = desc.find_all("div", {"class": "_3ezVU"})
                except:
                    continue
                about = ""
                storage = ""
                benefits = ""
                other = ""
                variable = ""
                nutrition = ""
                ingred_comp = ""
                specs = ""
                how_to = ""
                for description in descriptions:
                    try:
                        descp = description.find("div", {"class": "_3LyVz"}).text.split(" ")[0]
                    except:
                        continue
                    if descp.lower() == "about":
                        try:
                            about = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "nutritional" or descp.lower() == "nutrition":
                        try:
                            nutrition = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "benefits" or descp.lower() == "benefit":
                        try:
                            benefits = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "other":
                        try:
                            other = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "variable":
                        try:
                            variable = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "storage":
                        try:
                            storage = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "how":
                        try:
                            how_to = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "ingredient" or descp.lower() == "ingredients" or descp.lower() == "composition":
                        try:
                            ingred_comp = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    elif descp.lower() == "specification" or descp.lower() == "specifications":
                        try:
                            specs = description.find("div", {"class": "_26MFu"}).text.replace("\n", "").strip()
                        except:
                            continue
                    else:
                        continue

                f.write(str(brand.replace(",", "")) + "," + str(name.replace(",", "")) + "," + str(
                    mrp.replace(",", "")) + "," + str(
                    price.replace(",", "")) + "," + str(discount.replace(",", "")) + "," + str(
                    about.replace(",", "")) + "," + str(
                    storage.replace(",", "")) + "," + str(nutrition.replace(",", "")) + "," + str(
                    benefits.replace(",", "")) + "," + str(
                    other.replace(",", "")) + "," + str(variable.replace(",", "")) + "," + str(
                    how_to.replace(",", "")) + "," + str(
                    ingred_comp.replace(",", "")) + "," + str(specs.replace(",", "")) + "\n")

f.close()
