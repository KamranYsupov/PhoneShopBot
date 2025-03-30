from django.contrib import admin


class ArchiveModelAdminMixin(admin.ModelAdmin):
    exclude = ('is_archived', )

    def get_queryset(self, request):
        try:
            return self.model.objects.filter(is_archived=False)
        except TypeError:
            return self.model.objects.all()