from django.shortcuts import render,redirect, get_object_or_404
from .forms import ClienteForm, RegistroForm
from .models import Cliente
import os
from django.http import FileResponse
from django.conf import settings
#Para los reportes
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Q

# Create your views here.
@login_required
def create_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(cliente_list)
    else:
        form = ClienteForm()
    return render(request, 'clientesjahr/cliente_form.html', {'form': form})
        
def cliente_list(request):
    query = request.GET.get("q")
    if query:
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(apellidos__icontains=query) | Q(telefono__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()
    return render(request, 'clientesjahr/cliente_list.html', {'clientesjahr': clientes})

@login_required
def update_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect(cliente_list)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientesjahr/cliente_form.html', {'form': form, 'cliente': cliente})

@login_required
def delete_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect(cliente_list)
    return render(request, 'clientesjahr/cliente_confirm_delete.html', {'cliente': cliente})

# reportes
def generar_pdf_cliente(request):
    response = HttpResponse(content_type='application/pdf')
    #abrir = inline, descargar = attachment

    response['Content-Disposition'] = 'inline; filename="clientes.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    pdf.setTitle("Reporte de clientes")
    fecha_generación_jahr = datetime.date.today().strftime("%d-%m-%Y")
    pagina_num_jahr = 1


    ruta_imagen = os.path.join(settings.BASE_DIR, "clientesjahr/static/img/icono_isc.jpg")
    ximg = 539  
    yimg = 720  
    ancho = 65  
    alto = 65  
    pdf.drawImage(ruta_imagen, ximg, yimg, width=ancho, height=alto)

    def pie_pagina(pdf, pag_num_jahr):
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 20, f"Fecha de generación: {fecha_generación_jahr}")
        pdf.drawString(width -110, 20, f"Página núm: {pagina_num_jahr}")

    # Titulo del reporte
    pdf.setFont("Helvetica-Bold", 16)
    texto = "Lista de Clientes"
    ancho_texto = pdf.stringWidth(texto)
    x = (width - ancho_texto) / 2
    pdf.drawString(x, height - 40, texto)

    # Ecabezados de la tabla
    pdf.setFont("Helvetica-Bold", 12)
    encabezados = ["Nombre", "Apellidos", "Telefono", "Fecha de nac."]
    x_inicial = 120
    y = height - 80
    for i, encabezado in enumerate(encabezados):
        pdf.drawString(x_inicial + i * 100, y, encabezado)

    y -= 10
    pdf.line(100, y, width-100, y)

    #Contenido de la tabla
    y -= 20
    pdf.setFont("Helvetica", 12)
    
    query = request.GET.get("q")
    if query:
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(apellidos__icontains=query) | Q(telefono__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()
    for cliente in clientes:
        pdf.drawString(120, y, cliente.nombre)
        pdf.drawString(220, y, cliente.apellidos)
        pdf.drawString(320, y, cliente.telefono)
        pdf.drawString(420, y, cliente.fecha_nac.strftime("%d-%m-%Y"))
        y -=20

        if y <= 50:
            pie_pagina(pdf, pagina_num_jahr)
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = height - 80
            for i, encabezado in enumerate(encabezados):
                pdf.drawString(x_inicial + i * 100, y, encabezado)
            y -= 10
            pdf.line(100, y, width-100, y)
            y -= 20

            pagina_num_jahr += 1


    pie_pagina(pdf, pagina_num_jahr)

    pdf.showPage()
    pdf.save()

    return response



def logout_view(request):
    logout(request)
    return redirect('login')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registration/register.html', {'form': form})