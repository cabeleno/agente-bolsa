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
    # 1. Entrar en la web
    dr.get("https://www.astursalud.es/demandantes-empleo?p_p_id=AstursaludPortletBepe&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_AstursaludPortletBepe_article_id=56884")
    time.sleep(10) # Espera larga para que cargue todo

    # 2. Seleccionar Area IV (usando el valor interno '4' que es más seguro)
    area = Select(dr.find_element(By.ID, "_AstursaludPortletBepe_area"))
    area.select_by_value("4") 
    print("Área IV seleccionada")
    time.sleep(3) # Pausa para que la web procese el cambio

    # 3. Seleccionar Enfermero/a (usando el valor interno '114' que es el de DUE)
    categoria = Select(dr.find_element(By.ID, "_AstursaludPortletBepe_categoria"))
    categoria.select_by_value("114")
    print("Categoría Enfermería seleccionada")
    time.sleep(3)

    # 4. Forzar el clic en el botón de Consultar
    # Usamos un truco de JavaScript porque a veces el botón está "tapado"
    boton = dr.find_element(By.ID, "_AstursaludPortletBepe_consultarBusca")
    dr.execute_script("arguments[0].scrollIntoView();", boton)
    time.sleep(1)
    dr.execute_script("arguments[0].click();", boton)
    print("Botón consultar pulsado")

    # 5. Esperar a que salgan los números
    time.sleep(15)
    
    # 6. Guardar solo la parte de los resultados para que no salga tanto texto basura
    cuerpo = dr.find_element(By.TAG_NAME, "body").text
    
    with open("resultado.txt", "w", encoding="utf-8") as f:
        f.write("--- INICIO DE DATOS ---\n")
        f.write(cuerpo)
        f.write("\n--- FIN DE DATOS ---")

finally:
    dr.quit()
