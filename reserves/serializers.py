from rest_framework import serializers
from .models import Reserve
from datetime import timedelta
from orders.models import OrderStatus

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', 'start_reserve', 'finish_reserve', 'assigned_order', 'assigned_chairs', 'table']

    def validate_overlapping(self, data):
        """Validar que no haya superposiciones para la misma mesa"""
        start_reserve = data.get('start_reserve')
        finish_reserve = data.get('finish_reserve')
        table = data.get('table')

        overlapping_reservations = Reserve.objects.filter(
            table=table,
            start_reserve__lt=finish_reserve - timedelta(minutes=5),
            finish_reserve__gt=start_reserve,
        ).exclude(assigned_order__status='cancelled')  # Excluir reservas canceladas

        # Si estamos actualizando, excluir la reserva actual
        if self.instance:
            overlapping_reservations = overlapping_reservations.exclude(id=self.instance.id)

        if overlapping_reservations.exists():
            raise serializers.ValidationError("Ya existe una reserva que se superpone para esta mesa y rango de tiempo.")

        return data

    def validate_assigned_chairs(self, value):
        """Validar que el número de sillas asignadas esté entre min_chairs y max_chairs de la mesa asociada"""
        table = self.initial_data.get('table')
        if not table:
            raise serializers.ValidationError("Una mesa debe estar asignada a la reserva.")

        try:
            from .models import Table
            table_instance = Table.objects.get(id=table)
        except Table.DoesNotExist:
            raise serializers.ValidationError("Mesa no encontrada.")

        if value < table_instance.min_chairs or value > table_instance.max_chairs:
            raise serializers.ValidationError(
                f"El número de sillas asignadas debe estar entre {table_instance.min_chairs} y {table_instance.max_chairs}."
            )

        return value

    def validate(self, data):
        """Validaciones adicionales para el serializer"""
        start_reserve = data.get('start_reserve')
        finish_reserve = data.get('finish_reserve')

        if start_reserve and finish_reserve and start_reserve >= finish_reserve:
            raise serializers.ValidationError("La fecha/hora de inicio debe ser anterior a la fecha/hora de finalización.")

        # Obtener el ID de la mesa a la que se asignará la reserva
        table_id = data.get('table')  # ID de la mesa

        if not table_id:
            raise serializers.ValidationError("Debe asignarse una mesa a la reserva.")

        # Verificar superposiciones excluyendo reservas canceladas
        overlapping_reservations = Reserve.objects.filter(
            table=table_id,
            start_reserve__lt=finish_reserve - timedelta(minutes=5),
            finish_reserve__gt=start_reserve,
        ).exclude(assigned_order__status=OrderStatus.CANCELLED)  # Excluir reservas canceladas

        # Si estamos actualizando, excluir la reserva actual
        instance = getattr(self, 'instance', None)
        if instance:
            overlapping_reservations = overlapping_reservations.exclude(id=instance.id)

        if overlapping_reservations.exists():
            raise serializers.ValidationError("Ya existe una reserva que ocupa este rango horario para la mesa especificada.")

        return data
