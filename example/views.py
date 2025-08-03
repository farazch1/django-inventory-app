# # example/views.py
# from datetime import datetime

# from django.http import HttpResponse

# def index(request):
#     now = datetime.now()
#     html = f'''
#     <html>
#         <body>
#             <h1>Hello from Vercel!</h1>
#             <p>The nowww is { now }.</p>
#         </body>
#     </html>
#     '''
#     return HttpResponse(html)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm

@login_required
def inventory_view(request):
    items = Item.objects.all()
    form = ItemForm()
    is_admin = request.user.groups.filter(name='Admins').exists()

    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = ItemForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('inventory')
        elif 'remove_item' in request.POST:
            if is_admin:
                item_id = request.POST.get('remove_item')
                Item.objects.filter(id=item_id).delete()
                return redirect('inventory')

    return render(request, 'inventory/inventory.html', {'items': items, 'form': form, 'is_admin': is_admin})