from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Customer, Order
from .forms import CustomerForm, OrderForm

@login_required
def customer_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-created_at')

    customers = Customer.objects.all()

    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    valid_sort_options = ['first_name', '-first_name', 'created_at', '-created_at']
    if sort_by in valid_sort_options:
        customers = customers.order_by(sort_by)

    paginator = Paginator(customers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customers/customer_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    })

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add New Customer'})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.customer = customer
            order.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        order_form = OrderForm()

    orders = customer.orders.all().order_by('-order_date')
    total_spent = sum(order.amount for order in orders if order.status == 'Completed')

    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'orders': orders,
        'total_spent': total_spent,
        'order_form': order_form,
    })

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Edit Customer'})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})