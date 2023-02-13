from django.shortcuts import render,HttpResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,DestroyAPIView
from .models import MenuItem,Cart,Order
from rest_framework.views import APIView
from .serializers import MenuItemserializer,Userserializer,Cartserializer,Orderserializer
from django.contrib.auth.models import User,Group
from rest_framework.permissions import DjangoModelPermissions,AllowAny
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class MenuItemDisplay(ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemserializer

class MenuItemurd(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemserializer

class Manageusers(ListCreateAPIView):
    permission_classes=[DjangoModelPermissions]
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = Userserializer
    def get_permissions(self):
        if self.request.user.groups.filter(name='manager').exists():
            return []
        else:
            raise PermissionError("403 forbidden")
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username = request.data["username"])
        user.groups.add(1)
        user.save()
        return Response('201 - Created', status= status.HTTP_201_CREATED)
    
class Manageusersrud(DestroyAPIView):
    permission_classes=[DjangoModelPermissions]
    queryset = User.objects.filter(groups__name='manager')
    serializer_class = Userserializer
    def get_permissions(self):
        if self.request.user.groups.filter(name='manager').exists():
            return []
        else:
            raise PermissionError("403 forbidden")
    def destroy(self, request,pk=None, *args, **kwargs):
        user = User.objects.get(pk=pk,groups__name='manager')
        user.groups.remove(1)
        user.save()
        return Response('200 - Success', status= status.HTTP_200_OK)


class ManageDelivery(ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = User.objects.filter(groups__name='deliverycrew')
    serializer_class = Userserializer
    def get_permissions(self):
        if self.request.user.groups.filter(name='manager').exists():
            return []
        else:
             return Response('403 - Forbidden', status= status.HTTP_403_FORBIDDEN) 
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username = request.data["username"])
        user.groups.add(2)
        user.save()
        return Response('201 - Created', status= status.HTTP_201_CREATED)

class Managedeliveryrud(DestroyAPIView):
    permission_classes=[DjangoModelPermissions]
    queryset = User.objects.filter(groups__name='deliverycrew')
    def destroy(self, request,pk=None, *args, **kwargs):
        user = User.objects.get(pk=pk)
        user.groups.remove(2)
        user.save()
        return Response('201 - Created', status= status.HTTP_201_CREATED)

class managecart(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = Cartserializer
    def get_queryset(self):
        return Cart.objects.filter(user__id=self.request.user.id)
        
    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            menu_item = MenuItem.objects.get(pk=request.data['menuitem'])
            print(menu_item)
        except:
            return Response('404 - Not found', status=status.HTTP_404_NOT_FOUND)
        try:
            cart = Cart(user=self.request.user, menuitem=menu_item, 
            quantity=request.data['quantity'], unit_price=menu_item.price, 
            price=menu_item.price * request.data['quantity'])
            
            cart.save()
            print(cart)
            return Response('201 - created', status=status.HTTP_201_CREATED)
        except:
              return Response('400 - Invalid data', status=status.HTTP_400_BAD_REQUEST)

class managerdcartrud(RetrieveUpdateDestroyAPIView):
    serializer_class = Cartserializer
    def get_queryset(self):
        return Cart.objects.filter(user__id = self.request.user.id)
    def destroy(self, request,pk=None ,*args, **kwargs):
        cart = Cart.objects.get(pk=pk)
        cart.delete()
        return  Response('200 - OK', status=status.HTTP_200_OK)


class orderView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = Orderserializer
    def get_queryset(self):
        if not(self.request.user.groups.filter(name='manager').exists()) and not(self.request.user.groups.filter(name='deliverycrew').exists()):
          return Order.objects.filter(user__id=self.request.user.id)
        elif self.request.user.groups.filter(name='manager').exists():
          return Order.objects.all()
        elif self.request.user.groups.filter(name='deliverycrew').exists():
          return Order.objects.filter(delivery_crew=self.request.user.id)        


    def post(self, request, *args, **kwargs):
            cart_data = Cart.objects.get(user__id=self.request.user.id)
            if cart_data is None:
                return  Response('404 - Not found', status=status.HTTP_404_NOT_FOUND)
            user_name = User.objects.get(pk=self.request.user.id)
            delivery_crew = User.objects.get(pk= request.data["delivery_crew"])
            if delivery_crew.groups.filter(name="deliverycrew").exists():
                order = Order(
                user = user_name,
                delivery_crew = delivery_crew,
                status = request.data["status"],
                total = cart_data.price,
                date=request.data["date"]
                )
                order.save()
                cart_data.delete()
                return  Response('200 - OK', status=status.HTTP_200_OK)
            else:
                return  Response('404 - DELIVERY GUY NOT FOUND', status=status.HTTP_404_NOT_FOUND)

class orderviewrud(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = Orderserializer
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            order = Order.objects.get(user__id = request.user.id)
            order.delete()
            return  Response('200 - OK', status=status.HTTP_200_OK)
        else:
            return  Response('404 -  NO ORDER FOUND', status=status.HTTP_404_NOT_FOUND)

    def patch(self, request,pk=None, *args, **kwargs):
        order_item = Order.objects.get(pk=pk)
        if request.user.groups.filter(name='deliverycrew').exists():
            order_item.status = request.data["status"]
            order_item.save()
            return  Response('200 - OK', status=status.HTTP_200_OK)

        


    
        

                

                


            




    


