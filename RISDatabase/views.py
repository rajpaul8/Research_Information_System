from django.shortcuts import render
from .models import *
from django_pivot.pivot import pivot
import pandas as pd
from datetime import date

from django.db.models import Sum, Count

def RISDB(request):
    RIS_Project_Objects = RIS_Project.objects.all()
    #####################################################################################
    #                                  For Dependent Filters ---                        #
    #####################################################################################
    # Partner Country is dependant on Sub Region and sub region is dependant on Partner Region
    Partner_Region_Choices = Partner_Region.objects.all()
    Sub_Region_Choices = Sub_Region.objects.all()
    Partner_Country_Choices = Partner_Country.objects.all()

    # Modalities
    Modalities_Choices = RIS_Project.objects.values('Modalities').distinct()

    # Sub Modalities
    SubModalities_Choices = RIS_Project.objects.values('Sub_Modalities').distinct()

    # Sector
    Sector_Choices = RIS_Project.objects.values('Sector').distinct()

    # Year
    Year_Choices = RIS_Project.objects.values('Year').distinct()

    #####################################################################################
    #                                  Filters Logic---                                 #
    #####################################################################################

    if 'PartnerRegion' in request.GET:
        PartnerRegion = request.GET.getlist('PartnerRegion')
        # print(PartnerRegion)
        if PartnerRegion:
            RIS_Project_Objects = RIS_Project_Objects.filter(Partner_Region_Code__in=PartnerRegion)

    if 'SubRegion' in request.GET:
        SubRegion = request.GET.getlist('SubRegion')
        # print(SubRegion)
        if SubRegion:
            RIS_Project_Objects = RIS_Project_Objects.filter(Code_of_Sub_Region__in=SubRegion)

    if 'PartnerCountry' in request.GET:
        PartnerCountry = request.GET.getlist('PartnerCountry')
        # print(PartnerCountry)
        if PartnerCountry:
            RIS_Project_Objects = RIS_Project_Objects.filter(Code_of_Sub_Region__in=PartnerCountry)

    if 'Modalities' in request.GET:
        Modalities = request.GET.getlist('Modalities')
        # print(Modalities)
        if Modalities:
            RIS_Project_Objects = RIS_Project_Objects.filter(Modalities__in=Modalities)

    if 'SubModalities' in request.GET:
        SubModalities = request.GET.getlist('SubModalities')
        # print(SubModalities)
        if SubModalities:
            RIS_Project_Objects = RIS_Project_Objects.filter(Sub_Modalities__in=SubModalities)


    if 'Sector' in request.GET:
        Sector = request.GET.getlist('Sector')
        # print(Sector)
        if Sector:
            RIS_Project_Objects = RIS_Project_Objects.filter(Sector__in=Sector)

    if 'YearFrom' in request.GET:
        YearFrom = request.GET['YearFrom']
        if YearFrom:
            RIS_Project_Objects = RIS_Project_Objects.filter(Year__gte=YearFrom)

    if 'YearTo' in request.GET:
        YearTo = request.GET['YearTo']
        if YearTo:
            RIS_Project_Objects = RIS_Project_Objects.filter(Year__lte=YearTo)

        #####################################################################################
    #                                  For Left Sidebar Graphs -                         #
    #######################################################################################
    # 1 Display Region-Wise Number Of Projects
    Region_Wise_Number_Of_Projects = RIS_Project_Objects.values('Partner_Region').order_by('Partner_Region').annotate(total=Count('id'))

    # 2 Display Modality-Wise Number Of Projects
    Modality_Wise_Number_Of_Projects = RIS_Project_Objects.values('Modalities').order_by('Modalities').annotate(total=Count('id'))

    # 3 Display Sector-Wise Number Of Projects
    Sector_Wise_Number_Of_Projects = RIS_Project_Objects.values('Sector').order_by('Sector').annotate(total=Count('id'))


    #####################################################################################
    #                                  For Right Sidebar Cards -                         #
    #######################################################################################

    # 1 Project in Current Year
    currentYear = date.today().year
    Projects_In_Current_Year_Count = len(RIS_Project_Objects.filter(Year=currentYear))

    # 2 Total Projects Till Now
    TotalProjectsTillNow = len(RIS_Project_Objects)

    # 3 Country With Most Projects
    Country_Wise_Number_Of_Projects = RIS_Project_Objects.values('Partner_Country').order_by('Partner_Country').annotate(total=Sum('Disbursement_of_development_assistance_Rs_Crore')).order_by('-total')[0]
    Country_With_Most_Projects = Country_Wise_Number_Of_Projects['Partner_Country']

    # 4 Total Disbursement_of_development_assistance_Rs_Crore
    Total_Disbursement_of_development_assistance = Country_Wise_Number_Of_Projects['total']

    #####################################################################################
    #                                  For Middle Section Charts -                         #
    #######################################################################################

    # 1 Display Year Wise Number Of Projects
    Year_Wise_Number_Of_Projects = RIS_Project_Objects.values('Year').order_by('Year').annotate(total=Count('id'))

    # 2 Display Year Wise Disbursement_of_development_assistance_Rs_Crore
    Year_Wise_Disbursement = RIS_Project_Objects.values('Year').order_by('Year').annotate(total=Sum('Disbursement_of_development_assistance_Rs_Crore'))


    context = {
        'RIS_Project_Objects': RIS_Project_Objects,
        # --------------- Filtering Form ---------------------- #
        'Partner_Region_Choices': Partner_Region_Choices,
        'Sub_Region_Choices': Sub_Region_Choices,
        'Partner_Country_Choices': Partner_Country_Choices,
        'Modalities_Choices': Modalities_Choices,
        'SubModalities_Choices': SubModalities_Choices,
        'Sector_Choices': Sector_Choices,
        'Year_Choices': Year_Choices,
        'Year_Wise_Number_Of_Projects': Year_Wise_Number_Of_Projects
    }
    return render(request, 'RIS_DB\RIS_DB_Home.html', context)

# AJAX For Dynamically Filtering Dropdown Menu
def Load_Dependent_Sub_Region_Filters(request):
    Partner_Region_id = request.GET.getlist('PartnerRegionId[]')
    subRegion = Sub_Region.objects.filter(Partner_Region_Name_id__in=Partner_Region_id).distinct()
    partnerCountry = Partner_Country.objects.filter(Partner_Region_Name_id__in=Partner_Region_id).distinct()
    context = {'Sub_Region': subRegion,
               'partnerCountry': partnerCountry
               }
    return render(request, 'partials/drill_down_filters/DrillDown_Sub_Region_Filter.html', context)


def Load_Dependent_Partner_Country_Filters(request):
    Sub_Region_id = request.GET.getlist('SubRegionId[]')
    partnerCountry = Partner_Country.objects.filter(Sub_Region_Name_id__in=Sub_Region_id).distinct()
    return render(request, 'partials/drill_down_filters/DrilDown_Partner_Country_Filter.html', {'Partner_Country': partnerCountry})




