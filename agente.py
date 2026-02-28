import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

o = Options()
o.add_argument("--headless")
o.add_argument("--no-sandbox")
o.add_argument("--disable-dev-shm-usage")
# Este es el "disfraz" para que no te bloqueen
o.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)
w = WebDriverWait(dr, 40)

try:
    # Usamos la URL base, que es más estable
    dr.get("https://www.astursalud.es/demandantes-empleo")
    time.sleep(10)
    
    # Buscamos el enlace de la bolsa y hacemos clic
    enlace = w.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Situación de las bolsas")))
    dr.execute_script("arguments[0].click();", enlace)
    
    # Ahora esperamos al formulario
    el_area = w.until(EC.presence_of_element_located((By.ID, "_AstursaludPortletBepe_area")))
    Select(el_area).select_by_visible_text("Area IV")
    
    el_cat = w.until(EC.presence_of_element_located((By.ID, "_AstursaludPortletBepe_categoria")))
    Select(el_cat).select_by_visible_text("ENFERMERO/A-ATS/DUE")
    
    btn = dr.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
    dr.execute_script("arguments[0].click();", btn)
    
    time.sleep(20)
    with open("resultado.txt", "w", encoding="utf-8") as f:
        f.write(dr.find_element(By.TAG_NAME, "body").text)

finally:
    dr.quit()
