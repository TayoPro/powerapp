from . models import Category, ShopCart


def cat(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }

    return context



def cartread(request):
    cartread = ShopCart.objects.filter(paid_order=False, user__username=request.user.username)
    itemread = 0
    for item in cartread:
        itemread += item.quantity

    context = {
        'itemread': itemread
    }

    return context