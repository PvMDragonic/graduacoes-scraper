from scraper import Scraper
from time import sleep

def main():
    index = 300000

    while True:                
        scraper = Scraper(f"https://plataformacarolinabori.mec.gov.br/consulta-publica/processo/detalhar/{index}")
        
        results = scraper.scrape()

        if results and results.startswith('https'):
            with open("resultados.txt", "a", encoding="utf-8") as file:
                print('Resultado encontrado!')
                file.write(results + "\n")

        print(f"Página nº {index} analisada.")
        index += 1
        sleep(0.5)
            
if __name__ == "__main__":
    main()