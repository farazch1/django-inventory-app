from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm

@login_required
def inventory_view(request):
    items = Item.objects.all()
    form = ItemForm()

    user = request.user
    is_admin = user.groups.filter(name='Admins').exists()
    is_employee = user.groups.filter(name='Employees').exists()
    is_viewer = user.groups.filter(name='Viewers').exists()

    if request.method == 'POST':
        if 'add_item' in request.POST:
            if is_admin or is_employee:
                form = ItemForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('inventory')
        elif 'remove_item' in request.POST:
            if is_admin:
                item_id = request.POST.get('remove_item')
                Item.objects.filter(id=item_id).delete()
                return redirect('inventory')

    return render(request, 'inventory/inventory.html', {
        'items': items,
        'form': form,
        'is_admin': is_admin,
        'is_employee': is_employee,
        'is_viewer': is_viewer
    })
