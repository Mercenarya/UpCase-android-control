import flet as ft
import requests

TMDB_API_KEY = 'adf41b2c25bec2d2e9c72fca0294d880'

def get_movie_videos(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos'
    params = {
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(url, params=params)
    return response.json()

def main(page: ft.Page):
    page.title = "Movie Video Example"
    
    # Fetch videos for a specific movie
    movie_id = 550  # Replace with your movie ID
    videos = get_movie_videos(movie_id)
    
    # Check if there are any videos and get the first one
    if videos and 'results' in videos and len(videos['results']) > 0:
        video_key = videos['results'][0]['key']
        video_url = f'https://www.youtube.com/watch?v={video_key}'
        
        # Create VideoMedia control
        video = ft.VideoMedia(
            video_url,
            
        )
        
        # Add the video to the page
        page.add(video)
    else:
        page.add(ft.Text("No videos found for this movie."))

    # Start the app
    

if __name__ == "__main__":
    ft.app(target=main)
