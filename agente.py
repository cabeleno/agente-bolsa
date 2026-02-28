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
# Disfraz mucho más fuerte
o.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Ocultar que es un robot
o.add_argument("--disable-blink-features=AutomationControlled")

dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)
dr.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

try:
    print("Entrando en Astursalud...")
    dr.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")
    
    # Espera extra para que cargue la seguridad de la web
    time.sleep(25)
    dr.save_screenshot("intento1.png")
    
    # Intentar buscar el formulario
    found = False
    iframes = dr.find_elements(By.TAG_NAME, "iframe")
    print(f"Iframe encontrados: {len(iframes)}")
    
    for i, frame in enumerate(iframes):
        dr.switch_to.default_content()
        dr.switch_to.frame(i)
        try:
            area_el = dr.find_element(By.ID, "_AstursaludPortletBepe_area")
            found = True
            print(f"Formulario encontrado en iframe {i}")
            break
        except:
            continue
            
    if found:
        Select(area_el).select_by_value("4")
        time.sleep(5)
        Select(dr.find_element(By.ID, "_AstursaludPortletBepe_categoria")).select_by_value("114")
        time.sleep(5)
        dr.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca").click()
        time.sleep(20)
        with open("resultado.txt", "w", encoding="utf-8") as f:
            f.write(dr.find_element(By.TAG_NAME, "body").text)
    else:
        dr.save_screenshot("error_final.png")
        with open("resultado.txt", "w") as f:
            f.write("ERROR: Formulario no localizado tras reintentos.")

finally:
    dr.quit()
