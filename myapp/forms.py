from django import forms
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']


class ImageProcessingForm(forms.Form):
    kernel_size = forms.IntegerField(label="Kernel Size", initial=5, min_value=1, max_value=99, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    wavelet_thresh = forms.FloatField(label="Wavelet Threshold", initial=0.07, min_value=0.0, max_value=1.0, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    gaussian_coefficient = forms.IntegerField(label="Gaussian Coefficient", initial=1, min_value=0, max_value=16, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    canny_lower_bound = forms.IntegerField(label="Canny Lower Threshold", initial=100, min_value=0, max_value=300, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    canny_upper_bound = forms.IntegerField(label="Canny Upper Threshold", initial=200, min_value=0, max_value=300, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    line_boldness_strength = forms.IntegerField(label="Line Boldness", initial=0, min_value=0, max_value=5, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

