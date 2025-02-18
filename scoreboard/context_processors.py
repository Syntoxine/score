from .models import Score

def common_context(request):
    # This is the context that's always sent for the sidebar to display correctly
    return {
        "nav_scores": Score.objects.all(),
        "score": None,
    }