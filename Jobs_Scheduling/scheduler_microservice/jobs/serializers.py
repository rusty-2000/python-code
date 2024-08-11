from rest_framework import serializers
from .models import Job
from django.utils import timezone
from croniter import croniter
import iso8601

class JobSerializer(serializers.ModelSerializer):
    next_run = serializers.CharField(required=False, allow_null=True)
    last_run = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Job
        fields = ['id', 'name', 'description', 'cron_expression', 'next_run', 'last_run', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {'cron_expression': {'required': True}}

    def validate_cron_expression(self, value):
        if not value:
            raise serializers.ValidationError("This field is required.")
        try:
            croniter(value)
        except ValueError as e:
            raise serializers.ValidationError(f"Invalid cron expression: {str(e)}")
        return value

    def validate_datetime_field(self, value, field_name):
        if value:
            try:
                dt = iso8601.parse_date(value)
                if dt.tzinfo is None:
                    dt = timezone.make_aware(dt)
                if field_name == 'next_run' and dt < timezone.now():
                    raise serializers.ValidationError(f"{field_name.capitalize()} time must be in the future.")
                return dt
            except iso8601.ParseError:
                raise serializers.ValidationError(f"Invalid datetime format for {field_name}. Use ISO 8601 format (e.g., '2023-04-15T12:00:00Z').")
        return value

    def validate_next_run(self, value):
        return self.validate_datetime_field(value, 'next_run')

    def validate_last_run(self, value):
        return self.validate_datetime_field(value, 'last_run')

    def create(self, validated_data):
        if 'next_run' not in validated_data or not validated_data['next_run']:
            cron = croniter(validated_data['cron_expression'], timezone.now())
            validated_data['next_run'] = cron.get_next(timezone.datetime)
        return super().create(validated_data)

    def validate(self, data):
        if 'cron_expression' not in data:
            raise serializers.ValidationError({'cron_expression': 'This field is required.'})
        return data