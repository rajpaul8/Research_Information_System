from django.db import models
from datetime import datetime


class Partner_Region(models.Model):
    Partner_Region_Name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.Partner_Region_Name


# Linked with Partner Region
class Sub_Region(models.Model):
    Partner_Region_Name = models.ForeignKey(Partner_Region, on_delete=models.CASCADE, blank=True, null=True)
    Sub_Region_Name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Sub_Region_Name


# Linked to Sub_Region which is linked with Partner Region
class Partner_Country(models.Model):
    Partner_Region_Name = models.ForeignKey(Partner_Region, on_delete=models.CASCADE, blank=True, null=True)
    Sub_Region_Name = models.ForeignKey(Sub_Region, on_delete=models.CASCADE, blank=True, null=True)
    Partner_Country_Name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Partner_Country_Name


class RIS_Project(models.Model):
    YEAR_CHOICES = []
    for r in range(1947, (datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    Year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
    Partner_Country_Code = models.ForeignKey(Partner_Country, on_delete=models.SET_NULL, blank=True, null=True)
    # Linked to Partner Country
    Partner_Country = models.CharField(max_length=100, default="", blank=True, null=True)
    # ISO_Alpha_3_Code = models.CharField(max_length=10, default="", blank=True, null=True)
    Partner_Region_Code = models.ForeignKey(Partner_Region, on_delete=models.SET_NULL, blank=True, null=True)
    # Linked with Partner Region
    Partner_Region = models.CharField(max_length=100, default="", blank=True, null=True)
    Code_of_Sub_Region = models.ForeignKey(Sub_Region, on_delete=models.SET_NULL, blank=True, null=True)
    # Linked with Sub Region
    Sub_Region = models.CharField(max_length=100, default="", blank=True, null=True)
    # Code_of_Ministries = models.IntegerField(default=0, blank=True)
    # Ministries = models.CharField(max_length=10, default="", blank=True, null=True)
    # Modalities_Code = models.IntegerField(default=0, blank=True)
    Modalities = models.CharField(max_length=100, default="", blank=True, null=True)
    # Sub_Modalities_Code = models.IntegerField(default=0, blank=True)
    Sub_Modalities = models.CharField(max_length=100, default="")
    # Entry_Description_Projects_Programmes_etc = models.TextField(default="", blank=True, null=True)
    # Sector_Code = models.IntegerField(default=0, blank=True)
    # Sector = models.CharField(max_length=100, default="", blank=True, null=True)
    # Activity_Sub_Sector = models.CharField(max_length=100, default="", blank=True, null=True)
    # Name_of_Programme = models.CharField(max_length=100, default="", blank=True, null=True)
    # Brief_Description_of_project_Vocational_training_institution_IT_centre_etc = models.CharField(max_length=100, default="",blank=True, null=True)
    No_of_Slots_Utilized = models.IntegerField(default=0, blank=True)
    # No_of_slots_Announced = models.IntegerField(default=0, blank=True)
    # Kind_Assistance = models.CharField(max_length=100, default="", blank=True, null=True)
    # Disbursement_of_development_assistance_Rs = models.DecimalField(max_digits=200, decimal_places=100, blank=True,null=True)
    # Disbursement_of_development_assistance_Rs_Crore = models.DecimalField(max_digits=200, decimal_places=100, blank=True,null=True)
    # Exchange_rate = models.DecimalField(max_digits=200, decimal_places=100, blank=True, null=True)
    # Disbursement_of_development_assistance_USD = models.DecimalField(max_digits=200, decimal_places=100, blank=True,null=True)
    Disbursement_of_development_assistance_USD_million = models.DecimalField(max_digits=200, decimal_places=100,blank=True, null=True)
    # Commitment_of_development_assistance_Rs = models.DecimalField(max_digits=200, decimal_places=100, blank=True,null=True)
    # Commitment_of_development_assistance_Rs_Crore = models.DecimalField(max_digits=200, decimal_places=100, blank=True,null=True)
    # Commitment_of_development_assistance_USD = models.DecimalField(max_digits=200, decimal_places=100, blank=True,null=True)
    Commitment_of_development_assistance_USD_million = models.DecimalField(max_digits=200, decimal_places=100,blank=True, null=True)
    # Sources = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return str(self.Modalities)

    class Meta:
        verbose_name = 'RIS Database'