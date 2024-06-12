from django.db import models

# Create your models here.
items_choices=(
    ('Veg','Veg'),
    ('Non-Veg','Non-Veg'),
    ('Egg','Egg'),
    ('Refreshment','Refreshment')
)

class Items(models.Model):
    items_id=models.IntegerField(primary_key=True)
    items_name = models.CharField(max_length=100)
    items_price = models.IntegerField()
    items_description = models.CharField(max_length=350)
    items_type=models.CharField(choices=items_choices, max_length=150)
    items_image = models.ImageField()

    def __str__(self):
        return self.items_name

    


