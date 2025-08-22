# forms.py
from django import forms
from .models import Showtime
import datetime

class ShowtimeAdminForm(forms.ModelForm):
    time = forms.CharField(
        help_text="Enter time like '6 a.m.', '7:30 PM', etc."
    )

    class Meta:
        model = Showtime
        fields = '__all__'

    def clean_time(self):
        raw_time = self.cleaned_data['time'].strip().lower()

        # Replace “a.m.” or “p.m.” with standard format
        raw_time = raw_time.replace("a.m.", "am").replace("p.m.", "pm")

        try:
            # First try: "7 pm"
            parsed_time = datetime.datetime.strptime(raw_time, "%I %p").time()
        except ValueError:
            try:
                # Second try: "7:30 pm"
                parsed_time = datetime.datetime.strptime(raw_time, "%I:%M %p").time()
            except ValueError:
                raise forms.ValidationError("Time must be like '6 a.m.', '7:30 PM', etc.")
        return parsed_time
