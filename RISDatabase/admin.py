from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin




class RIS_ProjectAdmin( ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Year', 'Partner_Region')
    use_bulk = True
    # list_filter = ('Category', 'Author')
    # search_fields = ('Title', 'Author', 'Submission_Date', 'Category')
    # list_per_page = 20


admin.site.register(RIS_Project, RIS_ProjectAdmin)

class Partner_RegionAdmin( ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id','Partner_Region_Name')
    use_bulk = True
admin.site.register(Partner_Region, Partner_RegionAdmin)

class Sub_RegionAdmin( ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'Partner_Region_Name', 'Sub_Region_Name')
    use_bulk = True
admin.site.register(Sub_Region, Sub_RegionAdmin)

class Partner_Country_Admin( ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'Partner_Region_Name','Sub_Region_Name','Partner_Country_Name')
    use_bulk = True
admin.site.register(Partner_Country, Partner_Country_Admin)