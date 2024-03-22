from django.db import models

class Customer(models.Model):
    name 			= models.CharField(max_length=100)
    contact_number 	= models.CharField(max_length=20)
    email 			= models.EmailField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name 	= models.CharField(max_length=100)
    weight 	= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer 		= models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date 		= models.DateField()
    address 		= models.CharField(max_length=255)
    order_number 	= models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.all().order_by('-id').first()
            if last_order:
                last_order_number 	= int(last_order.order_number.split('ORD')[1])
                new_order_number 	= 'ORD{:05d}'.format(last_order_number + 1)
            else:
                new_order_number = 'ORD00000'
            self.order_number = new_order_number
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order 		= models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product 	= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity 	= models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} - {self.quantity}"
