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
o.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)
wait = WebDriverWait(dr, 30)

try:
    dr.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")
    time.sleep(10)

    # --- PASO CLAVE: BUSCAR Y ENTRAR EN EL IFRAME ---
    # Muchas webs oficiales meten el formulario en un 'iframe'
    iframes = dr.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        dr.switch_to.frame(0) # Entramos en el primer marco si existe
        print("Entrado en el iframe")

    # Ahora buscamos el área (esperando hasta 20 segundos)
    area_el = wait.until(EC.presence_of_element_located((By.ID, "_AstursaludPortletBepe_area")))
    Select(area_el).select_by_value("4")
    print("Área IV seleccionada")
    
    time.sleep(2)
    
    cat_el = dr.find_element(By.ID, "_AstursaludPortletBepe_categoria")
    Select(cat_el).select_by_value("114")
    print("Enfermería seleccionada")
    
    time.sleep(2)
    
    btn = dr.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
    dr.execute_script("arguments[0].click();", btn)
    print("Consultar pulsado")

    time.sleep(15)
    
    # Guardamos el resultado
    with open("resultado.txt", "w", encoding="utf-8") as f:
        f.write(dr.find_element(By.TAG_NAME, "body").text)

finally:
    dr.quit()
