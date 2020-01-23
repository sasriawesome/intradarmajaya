from django import forms


class LectureForm(forms.ModelForm):
    class Meta:
        exclude = ['reg_number', 'date_created']

    inner_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'disabled': 'disable'})
    )

