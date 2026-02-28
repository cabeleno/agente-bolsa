import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)

driver.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")

area = wait.until(EC.presence_of_element_located((By.ID, "_AstursaludPortletBepe_area")))
Select(area).select_by_visible_text("Area IV")

cat = driver.find_element(By.ID, "_AstursaludPortletBepe_categoria")
Select(cat).select_by_visible_text("ENFERMERO/A-ATS/DUE")

boton = driver.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
driver.execute_script("arguments[0].click();", boton)

time.sleep(15)

texto = driver.find_element(By.TAG_NAME, "body").text

with open("resultado.txt", "w", encoding="utf-8") as f:
    f.write(texto)

driver.quit()
