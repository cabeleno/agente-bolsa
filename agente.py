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
dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)
# Espera de hasta 60 segundos
w = WebDriverWait(dr, 60)

try:
    dr.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")
    
    # Esperar a que el selector de AREA exista de verdad
    el_area = w.until(EC.presence_of_element_located((By.ID, "_AstursaludPortletBepe_area")))
    Select(el_area).select_by_visible_text("Area IV")
    
    # Esperar y seleccionar CATEGORIA
    el_cat = w.until(EC.presence_of_element_located((By.ID, "_AstursaludPortletBepe_categoria")))
    Select(el_cat).select_by_visible_text("ENFERMERO/A-ATS/DUE")
    
    # Click en Consultar
    btn = dr.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
    dr.execute_script("arguments[0].click();", btn)
    
    # Esperar 20 segundos a que salgan los resultados
    time.sleep(20)
    
    txt = dr.find_element(By.TAG_NAME, "body").text
    with open("resultado.txt", "w", encoding="utf-8") as f:
        f.write(txt)

finally:
    dr.quit()
