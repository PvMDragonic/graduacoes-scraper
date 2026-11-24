from scraper import Scraper
from time import sleep
import sys
import os

if getattr(sys, "frozen", False): # Apenas quando rodar como executável.
    os.chdir(os.path.dirname(sys.executable))

    from seleniumbase.drivers import brave_drivers, cft_drivers
    for pkg in (brave_drivers, cft_drivers):
        os.makedirs(os.path.dirname(os.path.realpath(pkg.__file__)), exist_ok = True)

def main():
    index = 300000
    fails = 0

    while True:
        if fails >= 3:
            break
                
        scraper = Scraper(f"https://plataformacarolinabori.mec.gov.br/consulta-publica/processo/detalhar/{index}")
        
        results = scraper.scrape()

        if results == 'ERROR1':
            fails += 1 # Vai cair aqui repetidamente quando as páginas acabarem.
        else:
            fails = 0
            if results and results.startswith('https'):
                with open("resultados.txt", "a", encoding="utf-8") as file:
                    print('Resultado encontrado!')
                    file.write(results + "\n")

        print(f"Página nº {index} analisada.")
        scraper.close()
        index += 1
        sleep(0.5)
            
if __name__ == "__main__":
    main()