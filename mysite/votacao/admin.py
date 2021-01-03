from django.contrib import admin

from .models import Municipio, MunicipioZona, TipoCandidato

admin.site.register(TipoCandidato)
# admin.site.register(Municipio)
# admin.site.register(MunicipioZona)

@admin.register(MunicipioZona)
class MunicipioZonaAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'zona', 'secao')


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero')
    search_fields = ['nome']