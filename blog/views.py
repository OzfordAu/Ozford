# from django.shortcuts import render
# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from .models import BlogIndex

# def blog_index(request, page_id):
#     blog_index_page = BlogIndex.objects.get(id=page_id)
#     context = blog_index_page.get_context(request)

#     # Check if the request is an HTMX request
#     if request.headers.get('HX-Request') == 'true':
#         # Render only the partial template for HTMX requests
#         return HttpResponse(render_to_string('blog/partials/_blog_list.html', context))

#     # Render the full page for normal requests
#     return render(request, 'blog/blog_index.html', context)