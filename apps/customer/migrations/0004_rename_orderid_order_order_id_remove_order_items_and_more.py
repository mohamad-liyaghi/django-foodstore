# Generated by Django 4.0.4 on 2022-12-12 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_alter_food_description_alter_food_name'),
        ('customer', '0003_rename_created_order_date_created_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orderid',
            new_name='order_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.RemoveField(
            model_name='order',
            name='prepared_items',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('prepared', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='customer.order')),
            ],
        ),
    ]
