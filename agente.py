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
o.add_argument("--disable-dev-shm-usage")
o.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)

try:
    # Vamos directo a la página de la bolsa
    dr.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")
    time.sleep(15) # Esperamos 15 segundos a que cargue algo
    
    # HACEMOS UNA FOTO PARA VER QUÉ PASA
    dr.save_screenshot("captura.png")
    
    # Intentamos leer el texto por si acaso
    with open("resultado.txt", "w", encoding="utf-8") as f:
        f.write(dr.find_element(By.TAG_NAME, "body").text)

finally:
    dr.quit()
