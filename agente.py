import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

o = Options()
o.add_argument("--headless")
o.add_argument("--no-sandbox")
dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)

url = "https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884"
dr.get(url)
time.sleep(10)

sel_a = Select(dr.find_element(By.ID, "_AstursaludPortletBepe_area"))
sel_a.select_by_visible_text("Area IV")

sel_c = Select(dr.find_element(By.ID, "_AstursaludPortletBepe_categoria"))
sel_c.select_by_visible_text("ENFERMERO/A-ATS/DUE")

btn = dr.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
dr.execute_script("arguments[0].click();", btn)

time.sleep(15)
txt = dr.find_element(By.TAG_NAME, "body").text
with open("resultado.txt", "w", encoding="utf-8") as f:
    f.write(txt)

dr.quit()
