from scraper import Scraper
from random import uniform
from time import sleep
import sys
import os

if getattr(sys, "frozen", False): # Apenas quando rodar como executável.
    os.chdir(os.path.dirname(sys.executable))

    from seleniumbase.drivers import brave_drivers, cft_drivers
    for pkg in (brave_drivers, cft_drivers):
        os.makedirs(os.path.dirname(os.path.realpath(pkg.__file__)), exist_ok = True)

def ask_start_index(default: int = 300000) -> int:
    while True:
        value = input(f"Insira o íncide inicial, ou pressione Enter para usar o padrão (300,000): ").strip()
        if not value:
            return default
        if value.isdigit():
            return int(value)

def ask_major(default: str = 'PSICOLOGIA') -> str:
    while True:
        value = input(f"Insira o curso, ou pressione Enter para usar o padrão (PSICOLOGIA): ").strip()
        if not value:
            return default
        else:
            return value.upper().strip()

def main():
    BASE_URL = "https://plataformacarolinabori.mec.gov.br/consulta-publica/processo/detalhar/{}"
    index = ask_start_index()
    fails = 0

    scraper = Scraper(ask_major())

    try:
        while fails < 3:
            results = scraper.scrape(BASE_URL.format(index))

            if results is None:
                fails += 1 # Vai cair aqui repetidamente quando as páginas acabarem.
            else:
                fails = 0
                if results and results.startswith('https'):
                    with open("resultados.txt", "a", encoding="utf-8") as file:
                        print('Resultado encontrado!')
                        file.write(results + "\n")

            print(f"Página nº {index} analisada.")
            sleep(uniform(1.0, 1.5))
            index += 1
    finally:
        scraper.close()   
            
if __name__ == "__main__":
    main()