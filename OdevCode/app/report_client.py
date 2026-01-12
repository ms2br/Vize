import requests

API_URL = "http://127.0.0.1:5001/report/top_recommended_movies"

def get_top_movies(limit=10):
    try:
        response = requests.get(f"{API_URL}?limit={limit}")
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            print("Hata:", data["error"])
            return

        print(f"En çok önerilen {limit} film:")
        for idx, movie in enumerate(data, start=1):
            print(f"{idx}. {movie['title']} - {movie['count']} kez önerildi")
    except requests.exceptions.RequestException as e:
        print("API çağrısında hata oluştu:", e)

if __name__ == "__main__":
    get_top_movies(limit=5)
