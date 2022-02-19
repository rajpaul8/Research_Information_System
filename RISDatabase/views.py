from django.shortcuts import render
from .models import *
from django_pivot.pivot import pivot
from django_pivot.histogram import histogram
from datetime import date
import pandas as pd
import numpy as np
from django.db.models import Sum, Count

def RISDB(request):
    # This RIS_Project_Objects Should Change With The Filters
    RIS_Project_Objects = RIS_Project.objects.all()

    # This RIS_Project_Object_Static View Should Not Change With The Filter
    RIS_Project_Objects_Static = RIS_Project.objects.all()
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


    # Year
    Year_Choices = RIS_Project.objects.values('Year').distinct().order_by('Year')

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
            RIS_Project_Objects = RIS_Project_Objects.filter(Partner_Country_Code__in=PartnerCountry)


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



    if 'YearFrom' in request.GET:
        YearFrom = request.GET['YearFrom']
        if YearFrom:
            RIS_Project_Objects = RIS_Project_Objects.filter(Year__gte=YearFrom).order_by('Year')


    if 'YearTo' in request.GET:
        YearTo = request.GET['YearTo']
        if YearTo > YearFrom:
            RIS_Project_Objects = RIS_Project_Objects.filter(Year__lte=YearTo).order_by('-Year')

        if YearTo < YearFrom:
            YearTo = int(YearFrom) + 1
            RIS_Project_Objects = RIS_Project_Objects.filter(Year__lte=YearTo)



    #####################################################################################
    #                                  For Left Sidebar Graphs -                        #

    #####################################################################################
    #                                  For Left Sidebar Cards -                         #
    #######################################################################################

    # 1 Total Country Benefited
    Total_Country_Benefited_Count = len(RIS_Project_Objects_Static.values('Partner_Country').distinct())-3

    # 2 Lines of Credit Total Disbursement
    Total_Disbursement_Of_SubModalities = RIS_Project_Objects_Static.values('Sub_Modalities').annotate(total=Sum('Disbursement_of_development_assistance_USD_million')).order_by('-total')

    # Total_Disbursement_Of_SubModalities.filter('')
    # 3 Total Disbursement_of_development_assistance_USD_million
    Country_Wise_Disbursement_Total = RIS_Project_Objects_Static.values('Partner_Country').order_by('Partner_Country').annotate(total=Sum('Disbursement_of_development_assistance_USD_million')).order_by('-total')
    Total_Disbursement_of_development_assistance = Country_Wise_Disbursement_Total.aggregate(Sum('total'))['total__sum']

    #4 Grant (Modality) Total Disbursement
    Total_Disbursement_Of_Modalities = RIS_Project_Objects_Static.values('Modalities').annotate(total=Sum('Disbursement_of_development_assistance_USD_million')).order_by('-total')

    # Time-Series Charts (Small left side card)
    # 5 Total Disbursement with Time (Cumulative) - Line Chart
    Total_Disbursement_with_Time_Static_Chart_DF = pd.DataFrame(RIS_Project_Objects_Static.values('Year').annotate(total=Sum('Disbursement_of_development_assistance_USD_million')).order_by('Year'))
    Total_Disbursement_with_Time_Static_Chart_DF.replace(to_replace=[None], value=0, inplace=True)
    Total_Disbursement_with_Time_Static_Chart_DF['Cumulative_Disbursement_Frequency'] = Total_Disbursement_with_Time_Static_Chart_DF['total'].cumsum()
    Total_Disbursement_with_Time_Static_Chart = Total_Disbursement_with_Time_Static_Chart_DF.to_dict('records')


    # 6 Sub Modality Wise No_of_Slots_Utilized -Donut Chart
    SubModality_Wise_Number_Of_Slots_Utilized_DF = pd.DataFrame(RIS_Project_Objects_Static.values('Sub_Modalities').annotate(Number_Of_Slots=Sum('No_of_Slots_Utilized')))
    SubModality_Wise_Number_Of_Slots_Utilized_DF.replace(to_replace=[None], value=0, inplace=True)
    SubModality_Wise_Number_Of_Slots_Utilized_Chart = SubModality_Wise_Number_Of_Slots_Utilized_DF.to_dict('records')


    ###########################################################################################
    #              Section For Dynamic Changing Charts With Filters                   #
    # Here I'm using RIS_Project_Objects That Gets Changed With The Filters
    ###########################################################################################

    # 1 Cumulative Disbursement With Time With Partner Region Wise - Bar Chart
    Total_Disbursement_with_Time_Dynamic_Chart_DF = pd.DataFrame(RIS_Project_Objects.values('Year').annotate(total=Sum('Disbursement_of_development_assistance_USD_million')).order_by('Year'))
    Total_Disbursement_with_Time_Dynamic_Chart_DF.replace(to_replace=[None], value=0, inplace=True)
    Total_Disbursement_with_Time_Dynamic_Chart_DF['Cumulative_Disbursement_Frequency'] = Total_Disbursement_with_Time_Dynamic_Chart_DF['total'].cumsum()
    Total_Disbursement_with_Time_Dynamic_Chart = Total_Disbursement_with_Time_Dynamic_Chart_DF.to_dict('records')


    # 2 Total Disbursement With Modality - Polar Chart
    Total_Disbursement_With_Modality = RIS_Project_Objects.values('Modalities').annotate(total=Sum('Disbursement_of_development_assistance_USD_million'))


    # 3 For Geography Mapping
    # Region_Wise_Total_Number_Of_Project_Total_Disbursement_And_Total_Commitment

    # Region_Wise_Number_Of_Projects_For_Mapping = RIS_Project_Objects_Static.values('Partner_Region').order_by('Partner_Region').annotate(NumberOfProjects=Count('id'))

    Region_Wise_Disbursement_of_development_assistance_USD_million_Commitment_of_development_assistance_USD_million_For_Mapping = RIS_Project_Objects.values('Partner_Country').order_by('Partner_Country').annotate(Disbursement=Sum('Disbursement_of_development_assistance_USD_million'), Commitment=Sum('Commitment_of_development_assistance_USD_million'))
    # print(Region_Wise_Disbursement_of_development_assistance_USD_million_Commitment_of_development_assistance_USD_million_For_Mapping)
    print(request.GET, 'Request')

    context = {
        'RIS_Project_Objects': RIS_Project_Objects,
        # --------------- Filtering Form ---------------------- #
        'Partner_Region_Choices': Partner_Region_Choices,
        'Sub_Region_Choices': Sub_Region_Choices,
        'Partner_Country_Choices': Partner_Country_Choices,
        'Modalities_Choices': Modalities_Choices,
        'SubModalities_Choices': SubModalities_Choices,

        'Year_Choices': Year_Choices,


        #---------------------Left Side Card Stats-----------------#
        'Total_Country_Benefited_Count': Total_Country_Benefited_Count,
        'Total_Disbursement_Of_SubModalities': Total_Disbursement_Of_SubModalities,
        'Total_Disbursement_of_development_assistance': Total_Disbursement_of_development_assistance,
        'Total_Disbursement_Of_Modalities': Total_Disbursement_Of_Modalities,
        'Total_Disbursement_with_Time_Static_Chart': Total_Disbursement_with_Time_Static_Chart,
        'SubModality_Wise_Number_Of_Slots_Utilized_Chart': SubModality_Wise_Number_Of_Slots_Utilized_Chart,

        #-----------Middle Section Dynamic Changing Charts and Graphs----------------#
        'Total_Disbursement_with_Time_Dynamic_Chart': Total_Disbursement_with_Time_Dynamic_Chart,
        'Total_Disbursement_With_Modality': Total_Disbursement_With_Modality,


        # Mapping - via Leaflet Bottom Section
        'Region_Wise_Disbursement_of_development_assistance_USD_million_Commitment_of_development_assistance_USD_million_For_Mapping': Region_Wise_Disbursement_of_development_assistance_USD_million_Commitment_of_development_assistance_USD_million_For_Mapping,

        'values': request.GET
    }
    return render(request, 'RIS_DB/RIS_DB_Home.html', context)

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