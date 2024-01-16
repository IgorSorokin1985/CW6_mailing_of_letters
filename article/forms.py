from django import forms
from article.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ('slug', 'status', 'data_created', 'data_published', 'number_views')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields["is_published"].widget.attrs['class'] = 'form-check-input'
