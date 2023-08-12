from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def ApiOverview(request):
	api_urls = {
		'all_items': '/',
		'Search by Category': '/?category=category_name',
		'Search by Subcategory': '/?subcategory=category_name',
		'Add': '/create',
		'Update': '/update/pk',
		'Delete': '/item/pk/delete'
	}

	return Response(api_urls)


@api_view(['POST'])
def add_items(request):
    item = ItemSerializer(data=request.data)
    print(item)
 
    # validating for already existing data
    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
     
    if request.query_params:
        items=Item.objects.filter(**request.query_params.dict())
    else:
        items=Item.objects.all()

    if items:
        serializer=ItemSerializer(items,many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def find_items(request,pk):
    try:
        item=Item.objects.get(pk=pk)
        #item=Item.objects.filter(category=anything)
        serializer=ItemSerializer(item)
        return Response(serializer.data)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def update_items(request,pk):
    item=Item.objects.get(pk=pk)
    serializer=ItemSerializer(instance=item, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

