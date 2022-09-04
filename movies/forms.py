from django import forms
from .models import Rate

class RateForm(forms.ModelForm):

    CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★')
    ]

    star = forms.IntegerField(
        label = '별점',
        widget = forms.Select(
            choices = CHOICES,
            attrs = {
                
            }
        )
    )

    content = forms.CharField(
        label = '리뷰',
        help_text = '  영화의 한줄평을 작성해주세요!',
        widget = forms.Textarea(
            attrs = {

            }
        )
    )

    class Meta:
        model = Rate
        fields = ['content', 'star']

