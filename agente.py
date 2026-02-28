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
o.add_argument("--window-size=1920,1080")
o.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

dr = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)

try:
    print("Accediendo a la web...")
    dr.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")
    time.sleep(15)

    # Intentamos encontrar el selector de área de varias formas
    found = False
    
    # 1. Probar en la página principal
    try:
        area_el = dr.find_element(By.ID, "_AstursaludPortletBepe_area")
        found = True
        print("Encontrado en página principal")
    except:
        # 2. Si no, buscar en todos los iframes uno por uno
        iframes = dr.find_elements(By.TAG_NAME, "iframe")
        print(f"Buscando en {len(iframes)} iframes...")
        for i, frame in enumerate(iframes):
            dr.switch_to.default_content()
            dr.switch_to.frame(i)
            try:
                area_el = dr.find_element(By.ID, "_AstursaludPortletBepe_area")
                found = True
                print(f"Encontrado en iframe {i}")
                break
            except:
                continue

    if found:
        # Seleccionar Area IV
        Select(area_el).select_by_value("4")
        time.sleep(3)
        
        # Seleccionar Enfermero/a
        cat_el = dr.find_element(By.ID, "_AstursaludPortletBepe_categoria")
        Select(cat_el).select_by_value("114")
        time.sleep(3)
        
        # Click Consultar
        btn = dr.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
        dr.execute_script("arguments[0].click();", btn)
        print("Consulta enviada...")
        time.sleep(15)
        
        # Guardar resultado
        with open("resultado.txt", "w", encoding="utf-8") as f:
            f.write(dr.find_element(By.TAG_NAME, "body").text)
    else:
        print("No se encontró el formulario en ningún sitio.")
        dr.save_screenshot("error.png")
        with open("resultado.txt", "w") as f:
            f.write("ERROR: Formulario no localizado. Revisa la captura de pantalla.")

finally:
    dr.quit()
