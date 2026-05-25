from django import forms
from urllib.parse import urlparse
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url", "").strip()

        if not github_url:
            return github_url

        parsed_url = urlparse(github_url)

        if parsed_url.netloc not in ("github.com", "www.github.com"):
            raise forms.ValidationError("Ссылка должна вести на GitHub.")

        return github_url