import time
import requests
import argparse  # ДОБАВИТЬ!
import sys
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

def fetch_get(url, timeout):  # ДОБАВИТЬ timeout
    """Выполняет GET запрос"""
    try:
        response = requests.get(url, timeout=timeout)  # УБРАТЬ f"{url}get"
        return {
            'url': url,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.text
        }
    except Exception as e:
        raise Exception(f"Failed: {url} - {str(e)}")

def manage_hedge(urls, timeout=2):
    with ThreadPoolExecutor(max_workers=len(urls)) as executor:
        futures = {executor.submit(fetch_get, url, timeout): url for url in urls}
        
        done, pending = wait(futures, timeout=timeout, return_when=FIRST_COMPLETED)
        
        if not done:  # ДОБАВИТЬ проверку
            raise TimeoutError("All requests timed out")
        
        first_future = next(iter(done))
        try:
            result = first_future.result()
            for future in pending:
                future.cancel()
            return result  # УБРАТЬ print отсюда
        except Exception as e:
            # Проверяем остальные запросы
            for future in pending:
                try:
                    result = future.result(timeout=0)
                    return result
                except:
                    continue
            raise Exception("All requests failed")

def parse_args():
    parser = argparse.ArgumentParser(description='Hedged HTTP requests')
    parser.add_argument('-t', '--timeout', type=int, default=15, 
                       help='Timeout in seconds (default: 15)')
    parser.add_argument('urls', nargs='+', help='URLs to request')
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        result = manage_hedge(args.urls, args.timeout)
        # Выводим результат в нужном формате
        print(f"\nURL: {result['url']}")
        print(f"Status: {result['status_code']}")
        print(f"\nHeaders:\n{result['headers']}")
        print(f"\nBody:\n{result['body'][:500]}")  # Первые 500 символов
    except TimeoutError:
        sys.exit(228)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()