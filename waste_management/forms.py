"""
Django Forms for the Waste Collection Scheduling Management System.
Forms handle data validation for Vehicle, Route, and Schedule models.
"""

from django import forms
from .models import Vehicle, Route, Schedule
import json


# -------------------------------------------------------
# Vehicle Form
# -------------------------------------------------------
class VehicleForm(forms.ModelForm):
    """Form for creating and editing waste collection vehicles."""
    
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'driver_name', 'capacity', 'status']
        widgets = {
            'vehicle_id':  forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. V101'
            }),
            'driver_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Arun Kumar'
            }),
            'capacity':    forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 2 Tons'
            }),
            'status':      forms.Select(attrs={'class': 'form-input'}),
        }


# -------------------------------------------------------
# Route Form
# Pickup points are entered as a JSON textarea
# -------------------------------------------------------
class RouteForm(forms.ModelForm):
    """
    Form for creating and editing waste collection routes.
    Pickup points are entered as JSON array: [{"lat": 13.00, "lng": 80.25}, ...]
    """
    
    # Custom field for pickup points (human-editable JSON)
    pickup_points_json = forms.CharField(
        widget=forms.Textarea(attrs={
            'class':       'form-input',
            'rows':        6,
            'placeholder': '[{"lat": 13.0067, "lng": 80.2572}, {"lat": 13.0080, "lng": 80.2590}]'
        }),
        help_text='Enter as JSON array: [{"lat": 13.00, "lng": 80.25}]',
        required=False,
        label='Pickup Points (JSON)'
    )
    
    class Meta:
        model = Route
        fields = ['route_id', 'area', 'description']
        widgets = {
            'route_id':    forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. R201'
            }),
            'area':        forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Adyar'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows':  3,
                'placeholder': 'Optional route description...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the JSON field when editing an existing route
        if self.instance and self.instance.pk:
            self.fields['pickup_points_json'].initial = self.instance.pickup_points
    
    def clean_pickup_points_json(self):
        """Validate that pickup_points_json is valid JSON and contains lat/lng keys."""
        data = self.cleaned_data.get('pickup_points_json', '[]')
        if not data.strip():
            return '[]'
        try:
            points = json.loads(data)
            if not isinstance(points, list):
                raise forms.ValidationError("Pickup points must be a JSON array.")
            # Validate each point has lat and lng
            for i, point in enumerate(points):
                if 'lat' not in point or 'lng' not in point:
                    raise forms.ValidationError(
                        f"Point {i+1} is missing 'lat' or 'lng' key."
                    )
            return json.dumps(points)  # Return clean JSON string
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format. Please check your input.")
    
    def save(self, commit=True):
        """Override save to store the validated JSON into pickup_points field."""
        route = super().save(commit=False)
        route.pickup_points = self.cleaned_data.get('pickup_points_json', '[]')
        if commit:
            route.save()
        return route


# -------------------------------------------------------
# Schedule Form
# -------------------------------------------------------
class ScheduleForm(forms.ModelForm):
    """Form for creating and editing collection schedules."""
    
    class Meta:
        model = Schedule
        fields = ['schedule_id', 'vehicle', 'route', 'collection_date', 'status', 'notes']
        widgets = {
            'schedule_id':     forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. S501'
            }),
            'vehicle':         forms.Select(attrs={'class': 'form-input'}),
            'route':           forms.Select(attrs={'class': 'form-input'}),
            'collection_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type':  'date'
            }),
            'status':          forms.Select(attrs={'class': 'form-input'}),
            'notes':           forms.Textarea(attrs={
                'class': 'form-input',
                'rows':  3,
                'placeholder': 'Optional notes...'
            }),
        }
