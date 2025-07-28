from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, UOM, Order, OrderDetail
import json
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404


def get_products(request):
    products = Product.objects.select_related('uom').all()
    data = [
        {
            "product_id": p.id,
            "name": p.name,
            "uom_id": p.uom.id,
            "price_per_unit": float(p.price_per_unit),
            "uom_name": p.uom.uom_name
        } for p in products
    ]
    return JsonResponse(data, safe=False)

def get_uom(request):
    uoms = UOM.objects.all()
    data = [{"uom_id": u.id, "uom_name": u.uom_name} for u in uoms]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def insert_product(request):
    data = json.loads(request.body)
    uom = get_object_or_404(UOM, id=data['uom_id'])
    Product.objects.create(name=data['product_name'], uom=uom, price_per_unit=data['price_per_unit'])
    return JsonResponse({"status": "success"})

@csrf_exempt
@require_http_methods(["POST"])
def delete_product(request):
    data = json.loads(request.body)
    Product.objects.filter(id=data['product_id']).delete()
    return JsonResponse({"status": "deleted"})

@csrf_exempt
@require_http_methods(["POST"])
def update_product(request):
    data = json.loads(request.body)
    product = get_object_or_404(Product, id=data['product_id'])
    product.name = data['product_name']
    product.uom = get_object_or_404(UOM, id=data['uom_id'])
    product.price_per_unit = data['price_per_unit']
    product.save()
    return JsonResponse({"status": "updated"})

@csrf_exempt
@require_http_methods(["POST"])
def insert_uom(request):
    data = json.loads(request.body)
    UOM.objects.create(uom_name=data['uom_name'])
    return JsonResponse({"status": "uom added"})

def get_all_orders(request):
    orders = Order.objects.all().order_by('-datetime')
    data = [
        {
            "order_id": o.id,
            "customer_name": o.customer_name,
            "total": float(o.total),
            "datetime": o.datetime.strftime('%Y-%m-%d %H:%M:%S')
        } for o in orders
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def insert_order(request):
    data = json.loads(request.body)

    if not data.get('customer_name'):
        return JsonResponse({"error": "Customer name is required"}, status=400)

    order = Order.objects.create(customer_name=data['customer_name'], total=data['grand_total'])
    for item in data['order_details']:
        product = get_object_or_404(Product, id=item['product_id'])
        OrderDetail.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            total_price=item['total_price']
        )
    return JsonResponse({"status": "order saved"})

def get_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    details = OrderDetail.objects.filter(order=order).select_related('product')
    items = [
        {
            "product_name": d.product.name,
            "quantity": d.quantity,
            "total_price": float(d.total_price)
        } for d in details
    ]
    return JsonResponse({
        "order_id": order.id,
        "customer_name": order.customer_name,
        "datetime": order.datetime.strftime('%Y-%m-%d %H:%M:%S'),
        "total": float(order.total),
        "items": items
    })

