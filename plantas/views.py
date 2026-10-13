from django.shortcuts import render,redirect
from .models import Planta
from .forms import PlantaForm
from django.db.models import Sum
# Create your views here.

def inicio(request):
    plantas = Planta.objects.all()
    cantidad_plantas = plantas.count()
    planta_mas_cara = Planta.objects.order_by('-precio').first()
    

    resultado_stock = Planta.objects.aggregate(Sum('stock'))
    stock_total = resultado_stock['stock__sum'] or 0

    contexto = {
        'cantidad_plantas': cantidad_plantas,
        'planta_mas_cara': planta_mas_cara,
        'stock_total': stock_total,
    }
    return render(request, 'paginas/inicio.html', contexto)

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def plantas(request):
    buscar = request.GET.get('buscar')
    if buscar:
        lista_plantas = Planta.objects.filter(nombre__icontains=buscar)
    else:
        lista_plantas = Planta.objects.all()
        
    contexto = {
        'plantas': lista_plantas,
        'buscar': buscar,
    }
    return render(request, 'plantas/index.html', contexto)
        
    contexto = {
        'plantas': lista_plantas,
        'buscar': buscar,
    }
    return render(request, 'plantas/index.html', contexto)

def crear(request):
    formulario = PlantaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('plantas')
    return render(request, 'plantas/crear.html', {'formulario': formulario})

def editar(request, id):
    planta = Planta.objects.get(id=id)
    formulario = PlantaForm(request.POST or None, request.FILES or None, instance=planta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('plantas')
    return render(request, 'plantas/editar.html', {'formulario': formulario})

def eliminar(request, id):
    planta = Planta.objects.get(id=id)
    planta.delete()
    return redirect('plantas')

# ==========================================
# ENDPOINTS API REST (EVALUACIÓN 3)
# ==========================================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import Http404
from .serializers import PlantaSerializer

class PlantaList(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        buscar = request.GET.get('buscar')
        if buscar:
            plantas = Planta.objects.filter(nombre__icontains=buscar)
        else:
            plantas = Planta.objects.all()
        serializer = PlantaSerializer(plantas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PlantaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantaDetail(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Planta.objects.get(pk=pk)
        except Planta.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        planta = self.get_object(pk)
        serializer = PlantaSerializer(planta)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        planta = self.get_object(pk)
        serializer = PlantaSerializer(planta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        planta = self.get_object(pk)
        planta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)