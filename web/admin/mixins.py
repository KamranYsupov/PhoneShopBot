from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse


class ArchiveModelAdminMixin(admin.ModelAdmin):
    exclude = ('is_archived', )

    def get_queryset(self, request):
        try:
            return self.model.objects.filter(is_archived=False)
        except TypeError:
            return self.model.objects.all()


class ArchivedTabularInlineAdminMixin(admin.TabularInline):
    def get_queryset(self, request):
        try:
            return super().get_queryset(request).filter(
                is_archived=False
            )
        except TypeError as e:
            return super().get_queryset(request)


class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = self.model.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_change" % (
                    self.model._meta.app_label,
                    self.model._meta.model_name
                ),
                args=(obj.pk,)
            )
        )
