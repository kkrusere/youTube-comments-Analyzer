from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .youtube_scraper import get_youtube_video_id, get_video_data
import json

@csrf_exempt
def get_comments(request):
    """
    API view to retrieve YouTube video comments by video URL.
    Expects a POST request with 'youtube_url' in JSON payload.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            youtube_url = data.get('youtube_url', None)

            if not youtube_url:
                return JsonResponse({'error': 'YouTube URL not provided'}, status=400)

            video_id = get_youtube_video_id(youtube_url)

            if not video_id:
                return JsonResponse({'error': 'Invalid YouTube URL'}, status=400)

            video_data = get_video_data(video_id)
            return JsonResponse(video_data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)
