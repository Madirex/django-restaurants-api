from rest_framework import serializers
from .models import Reserve

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', 'start_reserve', 'finish_reserve', 'assigned_order', 'assigned_chairs', 'table']

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

        return data
