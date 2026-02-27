import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")
    time.sleep(5)
    
    # Rellenar Area IV
    select_area = Select(driver.find_element(By.ID, "_AstursaludPortletBepe_area"))
    select_area.select_by_visible_text("Area IV")
    
    # Rellenar Enfermero
    select_cat = Select(driver.find_element(By.ID, "_AstursaludPortletBepe_categoria"))
    select_cat.select_by_visible_text("ENFERMERO/A-ATS/DUE")
    
    # Clic en Consultar
    boton = driver.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
    driver.execute_script("arguments[0].click();", boton)
    time.sleep(10)
    
    # Guardar lo que se ve en pantalla
    texto = driver.find_element(By.TAG_NAME, "body").text
    with open("resultado.txt", "w", encoding="utf-8") as f:
        f.write(texto)
finally:
    driver.quit()
