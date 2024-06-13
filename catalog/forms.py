from django.core.exceptions import ValidationError
from django.forms import ModelForm

from catalog.models import Category, Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, name in self.fields.items():
            name.widget.attrs['class'] = 'form-control'


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        exclude = ("owner",)


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("owner",)

    def clean(self):
        stap = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_name = self.cleaned_data
        name = cleaned_name.get('name').lower()
        for name_stap in stap:
            if name_stap in name:
                raise ValidationError('Нельзя использовать слова: {}'.format(name_stap))


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get('is_activ_version')

        if is_active:
            # Деактивируем все другие версии
            Version.objects.exclude(pk=self.instance.pk).update(is_activ_version=False)
        else:
            # Проверяем, есть ли хотя бы одна активная версия, если текущая не активна
            active_versions = Version.objects.exclude(pk=self.instance.pk).filter(is_activ_version=True)
            if not active_versions.exists():
                raise ValidationError('Должна быть хотя бы одна активная версия')

        return cleaned_data

    def save(self, commit=True):
        # Обрабатываем сохранение после очистки
        instance = super().save(commit=False)

        if instance.is_activ_version:
            # Деактивируем все версии, кроме текущей
            Version.objects.exclude(pk=instance.pk).update(is_activ_version=False)

        if commit:
            instance.save()

        return instance
