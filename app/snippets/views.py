from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .serializers import SnippetSerializer
from .models import Snippet


class JsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super().__init__(content, **kwargs)
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        # Snippet 의 모든 objects를 가져옴
        snippets = Snippet.objects.all()

        # SnippetsSerializer 로 snippets 의 객체들을 json 렌더링 가능한 형태로 변형??
        # 딕셔너리로 변형?? 해당하는 모델의 필드에 맞는 형식을 때 검사를 통과하면??
        serializer = SnippetSerializer(snippets, many=True)
        # json 데이터 형식으로 랜더링
        # json_data = JSONRenderer().render(serializer.data)
        # 이 데이터 타입은 json 이라는것을 선언
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JSONRenderer(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

