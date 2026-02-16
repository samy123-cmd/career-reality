def seo_defaults(request):
    # Build canonical URL without query parameters to prevent duplicate indexing.
    canonical_url = f"{request.scheme}://{request.get_host()}{request.path}"

    # Keep header category navigation populated across all templates.
    categories = []
    try:
        from content.models import Category
        categories = Category.objects.all()
    except Exception:
        categories = []

    return {
        "article_meta_title": "",
        "article_meta_description": "",
        "og_type": "",
        "og_title": "",
        "og_description": "",
        "og_image": "",
        "twitter_title": "",
        "twitter_description": "",
        "twitter_image": "",
        "meta_robots": "index, follow",
        "canonical_url": canonical_url,
        "categories": categories,
    }
