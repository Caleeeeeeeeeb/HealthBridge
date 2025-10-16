# Generated manually to sync with existing Supabase database schema

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthbridge_app', '0004_medicinerequest'),
    ]

    operations = [
        # Add address and phone_number to CustomUser
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        
        # Rename requester to recipient
        migrations.RenameField(
            model_name='medicinerequest',
            old_name='requester',
            new_name='recipient',
        ),
        
        # Rename quantity_needed to quantity and change type
        migrations.RemoveField(
            model_name='medicinerequest',
            name='quantity_needed',
        ),
        migrations.AddField(
            model_name='medicinerequest',
            name='quantity',
            field=models.CharField(default='1', max_length=200),
            preserve_default=False,
        ),
        
        # Rename requested_at to created_at
        migrations.RenameField(
            model_name='medicinerequest',
            old_name='requested_at',
            new_name='created_at',
        ),
        
        # Add notes field
        migrations.AddField(
            model_name='medicinerequest',
            name='notes',
            field=models.TextField(blank=True, default=''),
        ),
        
        # Remove fulfilled_at field
        migrations.RemoveField(
            model_name='medicinerequest',
            name='fulfilled_at',
        ),
        
        # Update Meta
        migrations.AlterModelOptions(
            name='medicinerequest',
            options={'ordering': ['-created_at']},
        ),
        
        # Set db_table
        migrations.AlterModelTable(
            name='medicinerequest',
            table='healthbridge_app_medicinerequest',
        ),
        
        # Update foreign key db_column
        migrations.AlterField(
            model_name='medicinerequest',
            name='recipient',
            field=models.ForeignKey(db_column='recipient_id', on_delete=django.db.models.deletion.CASCADE, related_name='medicine_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicinerequest',
            name='matched_donation',
            field=models.ForeignKey(blank=True, db_column='matched_donation_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matched_requests', to='healthbridge_app.donation'),
        ),
    ]
