from django.db import models


class YearInfo(models.Model):
    year = models.PositiveIntegerField(null=True)
    file_name = models.TextField(null=True)
    status = models.PositiveSmallIntegerField(default=2)  # 0= draft, 1= Active, 2= Pending


# Create your models here.
class PocketMarginData(models.Model):
    year_info = models.ForeignKey(YearInfo, on_delete=models.CASCADE)
    profit_center_code = models.PositiveIntegerField()
    profit_center_name = models.TextField()
    product_segmentation = models.TextField()
    channel_partnar_ind = models.TextField()
    business_segment_group = models.TextField()
    customer_group_code = models.PositiveIntegerField()
    customer_group_name = models.TextField()
    material_number_code = models.PositiveIntegerField()
    material_name = models.TextField()
    freight_type_code = models.TextField()
    freight_types = models.TextField()
    best_fit_acc_man = models.TextField()
    manf_plant = models.TextField()
    sold_to_region = models.TextField()
    business_segment = models.TextField()
    product_family = models.TextField()
    sales_volume_mt = models.FloatField()
    gross_sale_usd = models.FloatField()
    invoice_price = models.FloatField()
    freight_costs = models.FloatField()
    freight_revenue = models.TextField()
    other_discounts_and_rebates = models.FloatField()
    pocket_price = models.FloatField()
    cogs = models.FloatField()
    pocket_margin = models.FloatField()
    pocket_margin_percentage = models.FloatField()
    volume_bands = models.TextField()
    floor_pocket_margin_corresponding_band = models.FloatField()
    target_pocket_margin_corresponding_band = models.FloatField()
    lower_than_floor_flag = models.TextField()
    lower_than_target_flag = models.TextField()
    change_in_invoice_price_per_mt_if_using_floor = models.TextField()
    change_in_invoice_price_per_mt_if_using_target = models.TextField()
    opportunity_to_floor = models.FloatField()
    opportunity_to_target = models.FloatField()
    percentage_change_in_invoice_price_or_mt_if_using_floor_margin = models.TextField()
    percentage_change_in_invoice_price_or_mt_if_using_target_margin = models.TextField()
