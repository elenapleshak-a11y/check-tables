import urllib.parse
from typing import Dict, List, Tuple

def extract_path(url: str) -> str:
    """
    Извлекает путь из URL (без протокола и домена)
    """
    try:
        parsed = urllib.parse.urlparse(url)
        path = parsed.path
        
        # Если путь пустой, возвращаем "/"
        if not path:
            return "/"
        
        # Добавляем "/" в начало если его нет
        if not path.startswith('/'):
            path = '/' + path
            
        return path
    except Exception as e:
        raise ValueError(f"Некорректный URL: {url} - {e}")

def process_urls(urls: List[str]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Обрабатывает список URL и возвращает два словаря:
    - url_to_supplement: связка оригинальный URL -> дополнение
    - supplement_to_url: связка дополнение -> оригинальный URL
    """
    url_to_supplement = {}
    supplement_to_url = {}
    
    for url in urls:
        try:
            supplement = extract_path(url)
            url_to_supplement[url] = supplement
            supplement_to_url[supplement] = url
        except ValueError as e:
            print(f"Ошибка обработки URL: {e}")
            continue
            
    return url_to_supplement, supplement_to_url

def compare_sites(old_site_urls: List[str], new_site_urls: List[str]) -> Dict[str, List[Tuple[str, str]]]:
    """
    Сравнивает два сайта и возвращает результаты сравнения
    """
    # Обрабатываем старый сайт
    old_url_to_supplement, old_supplement_to_url = process_urls(old_site_urls)
    old_supplements = set(old_supplement_to_url.keys())
    
    # Обрабатываем новый сайт
    new_url_to_supplement, new_supplement_to_url = process_urls(new_site_urls)
    new_supplements = set(new_supplement_to_url.keys())
    
    # Находим совпадения
    common_supplements = old_supplements.intersection(new_supplements)
    
    # Находим различия
    only_in_old = old_supplements - new_supplements
    only_in_new = new_supplements - old_supplements
    
    # Формируем результаты
    results = {
        "одинаковые URL": [],
        "разные URL (только в старом)": [],
        "разные URL (только в новом)": [],
        "битые URL": []
    }
    
    # Одинаковые URL
    for supplement in common_supplements:
        old_url = old_supplement_to_url[supplement]
        new_url = new_supplement_to_url[supplement]
        results["одинаковые URL"].append((old_url, new_url))
    
    # URL только в старом сайте
    for supplement in only_in_old:
        old_url = old_supplement_to_url[supplement]
        results["разные URL (только в старом)"].append((old_url, supplement))
    
    # URL только в новом сайте
    for supplement in only_in_new:
        new_url = new_supplement_to_url[supplement]
        results["разные URL (только в новом)"].append((new_url, supplement))
    
    return results

def save_results_to_file(results: Dict[str, List[Tuple[str, str]]], filename: str = "comparison_results.txt"):
    """
    Сохраняет результаты в файл
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for category, urls in results.items():
            f.write(f"\n{'='*50}\n")
            f.write(f"{category}: {len(urls)}\n")
            f.write(f"{'='*50}\n")
            
            for url_pair in urls:
                if category == "одинаковые URL":
                    old_url, new_url = url_pair
                    f.write(f"Старый: {old_url}\n")
                    f.write(f"Новый:  {new_url}\n")
                else:
                    url, supplement = url_pair
                    f.write(f"URL: {url}\n")
                    f.write(f"Путь: {supplement}\n")
                f.write("-" * 30 + "\n")

def main():
    """
    Основная функция скрипта
    """
    # Пример данных - замените на ваши списки URL
    old_site_urls = [
        "https://old-site.ru/",
        "https://old-site.ru/catalog",
        "https://old-site.ru/about",
        "https://old-site.ru/contact",
        "https://old-site.ru/blog/article-1",
        "https://old-site.ru/invalid-url",  # Пример некорректного URL
    ]
    
    new_site_urls = [
        "https://new-site.com/",
        "https://new-site.com/catalog",
        "https://new-site.com/about-us",  # Измененный путь
        "https://new-site.com/contact",
        "https://new-site.com/blog/new-article",  # Новый путь
        "https://new-site.com/services",  # Новый раздел
    ]
    
    print("Начинаем сравнение сайтов...")
    
    # Сравниваем сайты
    results = compare_sites(old_site_urls, new_site_urls)
    
    # Выводим результаты
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ СРАВНЕНИЯ:")
    print("="*60)
    
    for category, urls in results.items():
        print(f"\n{category}: {len(urls)}")
        if urls:
            for url_pair in urls[:5]:  # Показываем первые 5 для примера
                if category == "одинаковые URL":
                    old_url, new_url = url_pair
                    print(f"  Старый: {old_url}")
                    print(f"  Новый:  {new_url}")
                else:
                    url, supplement = url_pair
                    print(f"  URL: {url}")
                    print(f"  Путь: {supplement}")
                print("  " + "-" * 40)
            if len(urls) > 5:
                print(f"  ... и еще {len(urls) - 5} URL")
    
    # Сохраняем полные результаты в файл
    save_results_to_file(results)
    print(f"\nПолные результаты сохранены в файл: comparison_results.txt")
    
    # Сводная статистика
    print("\n" + "="*60)
    print("СВОДНАЯ СТАТИСТИКА:")
    print("="*60)
    total_old = len(old_site_urls)
    total_new = len(new_site_urls)
    same = len(results["одинаковые URL"])
    diff_old = len(results["разные URL (только в старом)"])
    diff_new = len(results["разные URL (только в новом)"])
    
    print(f"Всего URL в старом сайте: {total_old}")
    print(f"Всего URL в новом сайте: {total_new}")
    print(f"Одинаковые URL: {same}")
    print(f"Уникальные для старого сайта: {diff_old}")
    print(f"Уникальные для нового сайта: {diff_new}")
    print(f"Совпадение: {(same/total_old)*100:.1f}% (от старого сайта)")

if __name__ == "__main__":
    main()
