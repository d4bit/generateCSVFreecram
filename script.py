import requests
import links
from bs4 import BeautifulSoup
import csv

def scrape_urls(urls, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Question and Options', 'Answer Explanation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            questions = soup.find_all('div', class_='qa-question')
            options = soup.find_all('div', class_='qa-options')
            answers = soup.find_all('div', class_='qa-answerexp')

            for i in range(len(questions)):
                question = questions[i].text.strip()
                options_text = options[i].text.strip()
                answer_span = answers[i].find('span')
                if answer_span:
                    answer_text = answer_span.text.strip()
                    colon_index = answer_text.find(":")
                    answer = answer_text[colon_index+1:].strip() if colon_index != -1 else answer_text
                else:
                    answer = "No answer found"

                writer.writerow({'Question and Options': question + "\n" + options_text, 'Answer Explanation': answer})

def main():
    output_file = 'output.csv'
    scrape_urls(links.enlaces, output_file)
    print("Datos exportados exitosamente a", output_file)

if __name__ == "__main__":
    main()
