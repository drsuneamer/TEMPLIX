from django import forms
from .models import Review, Movie


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ('user', 'like_users')

        def __init__(self, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)
            self.fields['movie'].queryset = Movie.objects.all()