from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4
from datetime import datetime

class Table(models.Model):
    x_position = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    y_position = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    min_chairs = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    max_chairs = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    assigned_chairs = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    # TODO: assignedOrder = models.UUIDField(default=uuid4)
    reserved = models.BooleanField(default=False)
    reserved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return basic info about the table"""
        return f'Table at ({self.x_position}, {self.y_position}), Min Chairs: {self.min_chairs}, Max Chairs: {self.max_chairs}, Assigned Chairs: {self.assigned_chairs} Reserved: {self.reserved}'