from django.conf import settings
from rest_framework import serializers
from rest_framework import status
import json
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
import uuid
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.db.models import Avg, Count, Min, Sum, Max
from django.db import transaction
from const import *
from .models import PocketMarginData, YearInfo
import numpy as np


class PocketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PocketMarginData
        fields = '__all__'

        extra_kwargs = {'year_info': {'write_only': True}}


class ScatterplotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PocketMarginData
        fields = (
            'id', 'product_family', 'customer_group_name', 'sales_volume_mt', 'sold_to_region',
            'pocket_margin_percentage')


class WaterfallSerializer(serializers.ModelSerializer):
    single = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = PocketMarginData
        fields = ('single', 'total', 'customer_group_name', 'product_family', 'sales_volume_mt')

    def get_total(self, obj):
        temp = {}
        try:
            invoice_price = float(obj.invoice_price)
        except:
            invoice_price = float(0)

        try:
            freight_costs = float(obj.freight_costs)
        except:
            freight_costs = float(0)

        try:
            freight_revenue = float(obj.freight_revenue)
        except:
            freight_revenue = float(0)

        try:
            other_discounts_and_rebates = float(obj.other_discounts_and_rebates)
        except:
            other_discounts_and_rebates = float(0)
        try:
            pocket_price = float(obj.pocket_price)
        except:
            pocket_price = float(0)
        try:
            cogs = float(obj.cogs)
        except:
            cogs = float(0)

        try:
            pocket_margin = float(obj.pocket_margin)
        except:
            pocket_margin = float(0)

        temp['invoice_price'] = invoice_price
        temp['freight_costs'] = freight_costs
        temp['freight_revenue'] = freight_revenue
        temp['other_discounts_and_rebates'] = other_discounts_and_rebates
        temp['pocket_price'] = pocket_price
        temp['cogs'] = cogs
        temp['pocket_margin'] = pocket_margin
        temp['pocket_margin_percentage'] = obj.pocket_margin_percentage

        return temp

    def get_single(self, obj):

        temp = {}

        single_data = self.get_total(obj)

        temp['invoice_price'] = single_data['invoice_price'] * float(obj.sales_volume_mt)  # 0.1 = 1/10
        temp['freight_costs'] = single_data['freight_costs'] * float(obj.sales_volume_mt)
        temp['freight_revenue'] = single_data['freight_revenue'] * float(obj.sales_volume_mt)
        temp['other_discounts_and_rebates'] = single_data['other_discounts_and_rebates'] * float(obj.sales_volume_mt)
        temp['pocket_price'] = single_data['pocket_price'] * float(obj.sales_volume_mt)
        temp['cogs'] = single_data['cogs'] * float(obj.sales_volume_mt)
        temp['pocket_margin'] = single_data['pocket_margin'] * float(obj.sales_volume_mt)
        temp['pocket_margin_percentage'] = single_data['pocket_margin_percentage']

        return temp


class WaterfallSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PocketMarginData
        fields = ('id', 'invoice_price', 'freight_costs', 'freight_revenue', 'other_discounts_and_rebates',
                  'pocket_price', 'cogs', 'pocket_margin', 'pocket_margin_percentage')


class CustomerScatterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PocketMarginData
        fields = ('id', 'product_family', 'sales_volume_mt', 'pocket_margin_percentage')


class PriceBandHistogramViewSerializer(serializers.ModelSerializer):
    calculated_total_sale = serializers.SerializerMethodField()

    class Meta:
        model = PocketMarginData
        fields = (
            'id', 'customer_group_name', 'gross_sale_usd', 'pocket_margin_percentage', 'calculated_total_sale')

    def get_calculated_total_sale(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')
        sum = self.context.get('sum')

        result = pocket_margin_data_set.filter(id=obj.id).values('customer_group_name').annotate(
            total_sales=Sum('gross_sale_usd'))

        calculated_result = (result[0]['total_sales'] / sum) * 100
        return calculated_result


class HistogramDiagramViewSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = PocketMarginData
        fields = ('data',)

    def get_data(self, obj):
        sum = self.context.get('sum')
        threshold = self.context.get('threshold')
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        min_value = pocket_margin_data_set.aggregate(Min('pocket_margin_percentage'))
        max_value = pocket_margin_data_set.aggregate(Max('pocket_margin_percentage'))

        start = min_value['pocket_margin_percentage__min']
        end = max_value['pocket_margin_percentage__max']

        data = []
        for i in range(round(start), round(end) + 1, threshold):
            temp = {}
            data_set = pocket_margin_data_set.filter(pocket_margin_percentage__range=(i, i + threshold))

            temp['last_range'] = i + threshold

            if data_set.count() != 0:
                result = data_set.aggregate(total_sales=Sum('gross_sale_usd'))
                temp['calculated_total_percentage'] = (result['total_sales'] / sum) * 100
            else:
                temp['calculated_total_percentage'] = 0
            data.append(temp)

        return data


class DashboardSerializer(serializers.ModelSerializer):
    unique_metarial = serializers.SerializerMethodField()
    unique_product_families = serializers.SerializerMethodField()
    unique_customer = serializers.SerializerMethodField()
    total_freight_costs = serializers.SerializerMethodField()
    total_freight_revenue = serializers.SerializerMethodField()
    other_discounts_and_rebates = serializers.SerializerMethodField()
    product_families_less_than_25_customer = serializers.SerializerMethodField()
    number_of_recordes = serializers.SerializerMethodField()
    top_product_families_by_annual_volume = serializers.SerializerMethodField()
    top_product_families_by_annual_sales = serializers.SerializerMethodField()
    top_customer_by_annual_volume = serializers.SerializerMethodField()
    top_customer_by_annual_sales = serializers.SerializerMethodField()
    total_customer_product = serializers.SerializerMethodField()

    class Meta:
        model = PocketMarginData
        fields = ('id', 'unique_metarial', 'unique_product_families', 'unique_customer',
                  'total_freight_costs', 'total_freight_revenue', 'other_discounts_and_rebates',
                  'product_families_less_than_25_customer', 'number_of_recordes',
                  'top_product_families_by_annual_volume', 'top_product_families_by_annual_sales',
                  'top_customer_by_annual_volume', 'top_customer_by_annual_sales',
                  'total_customer_product')

    def get_unique_metarial(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        all_unique_metarial = pocket_margin_data_set.values_list('material_number_code', flat=True)
        unique_data = set(all_unique_metarial)
        lenth_of_data = len(unique_data)
        return lenth_of_data

    def get_unique_product_families(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        all_unique_product_families = pocket_margin_data_set.values_list('product_family', flat=True)
        unique_data = set(all_unique_product_families)
        lenth_of_data = len(unique_data)

        return lenth_of_data

    def get_unique_customer(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        all_unique_customer = pocket_margin_data_set.values_list('customer_group_name', flat=True)
        unique_data = set(all_unique_customer)
        lenth_of_data = len(unique_data)
        return lenth_of_data

    def get_total_freight_costs(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        all_total_freight_costs = pocket_margin_data_set.values_list('freight_costs', flat=True)
        sum = get_sum(all_total_freight_costs)
        return sum

    def get_total_freight_revenue(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        all_total_freight_revenue = pocket_margin_data_set.values_list('freight_revenue', flat=True)
        sum = get_sum(all_total_freight_revenue)
        return sum

    def get_other_discounts_and_rebates(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        all_other_discounts_and_rebates = pocket_margin_data_set.values_list('other_discounts_and_rebates',
                                                                             flat=True)
        sum = get_sum(all_other_discounts_and_rebates)
        return sum

    def get_product_families_less_than_25_customer(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        # SELECT product_family, COUNT(customer_name_sold_to) FROM data_pocketmargindata GROUP BY product_family

        data_set = pocket_margin_data_set.values('product_family').annotate(
            total_customer=Count('customer_group_name'))
        product_families_data = []
        for single_data in data_set:
            if single_data['total_customer'] < 25:
                product_families_data.append(single_data)
        return product_families_data

    def get_top_product_families_by_annual_volume(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')
        number_of_top_data = self.context.get('number_of_top_data')

        # SELECT product_family, SUM(sales_volume_mt) as total_sales FROM data_pocketmargindata GROUP BY product_family ORDER BY total_sales DESC

        data_set = pocket_margin_data_set.values('product_family').annotate(
            total_sales_volume=Sum('sales_volume_mt')).order_by('-total_sales_volume')
        try:
            number_of_top_data = int(number_of_top_data)
        except:
            number_of_top_data = 10
        return data_set[0:number_of_top_data]

    def get_top_product_families_by_annual_sales(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')
        number_of_top_data = self.context.get('number_of_top_data')

        data_set = pocket_margin_data_set.values('product_family').annotate(
            total_gross_sale_usd=Sum('gross_sale_usd')).order_by('-total_gross_sale_usd')
        try:
            number_of_top_data = int(number_of_top_data)
        except:
            number_of_top_data = 10
        return data_set[0:number_of_top_data]

    def get_top_customer_by_annual_volume(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')
        number_of_top_data = self.context.get('number_of_top_data')

        customer = pocket_margin_data_set.values('customer_group_name').annotate(
            total_sales_volume=Sum('sales_volume_mt')).order_by('-total_sales_volume')

        try:
            number_of_top_data = int(number_of_top_data)
        except:
            number_of_top_data = 10
        return customer[0:number_of_top_data]

    def get_top_customer_by_annual_sales(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')
        number_of_top_data = self.context.get('number_of_top_data')

        customer = pocket_margin_data_set.values('customer_group_name').annotate(
            total_gross_sale_usd=Sum('gross_sale_usd')).order_by('-total_gross_sale_usd')

        try:
            number_of_top_data = int(number_of_top_data)
        except:
            number_of_top_data = 10
        return customer[0:number_of_top_data]

    def get_number_of_recordes(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')

        sales_volume_set = pocket_margin_data_set.values_list('sales_volume_mt', flat=True)
        number_of_missing_sales = 0
        number_of_sales = 0
        for sales_volume in sales_volume_set:
            if sales_volume == "" or sales_volume == '0' or sales_volume == None or sales_volume == 0:
                number_of_missing_sales += 1
            elif float(sales_volume) > 0:
                number_of_sales += 1

        sum_of_all_sales_volume = pocket_margin_data_set.aggregate(Sum('sales_volume_mt'))
        sum_of_sales_volume_mt= sum_of_all_sales_volume['sales_volume_mt__sum']

        sum_of_gross_sale_usd_data = pocket_margin_data_set.aggregate(Sum('gross_sale_usd'))
        sum_of_gross_sale_usd= sum_of_gross_sale_usd_data['gross_sale_usd__sum']

        temp = {}
        temp['number_of_missing_sales'] = number_of_missing_sales
        temp['number_of_sales'] = number_of_sales
        temp['sum_of_sales_volume_mt'] = sum_of_sales_volume_mt
        temp['sum_of_gross_sale_usd'] = sum_of_gross_sale_usd

        return temp

    def get_total_customer_product(self, obj):
        pocket_margin_data_set = self.context.get('pocket_margin_data_set')
        total_unique_row = pocket_margin_data_set.values('product_family', 'customer_group_name').distinct()
        return total_unique_row.count()


class ScatterplotCalculatedSerializer(serializers.ModelSerializer):
    volume_pareto_percentage = serializers.SerializerMethodField()
    ceiling_pocket_margin_corresponding_band = serializers.SerializerMethodField()

    class Meta:
        model = PocketMarginData
        fields = ('id', 'volume_pareto_percentage', 'volume_bands', 'floor_pocket_margin_corresponding_band',
                  'target_pocket_margin_corresponding_band', 'ceiling_pocket_margin_corresponding_band')

    def get_volume_pareto_percentage(self, obj):
        sum = self.context.get('sum')
        sorted_pocket_margin_data_set = self.context.get('sorted_pocket_margin_data_set')

        sum_for_current_range = 0
        for pocket_margin_data in sorted_pocket_margin_data_set:
            sum_for_current_range += float(pocket_margin_data.sales_volume_mt)

            if pocket_margin_data.id == obj.id:
                break

        calculated_result = (sum_for_current_range / (float(sum))) * 100
        return float(calculated_result)

    def get_ceiling_pocket_margin_corresponding_band(self, obj):

        if obj.volume_bands == '1. Low':
            band_pocket_margin_data_set = PocketMarginData.objects.filter(volume_bands='1. Low').order_by(
                'sales_volume_mt')

        elif obj.volume_bands == '2. Mid':
            band_pocket_margin_data_set = PocketMarginData.objects.filter(volume_bands='2. Mid').order_by(
                'sales_volume_mt')

        else:
            band_pocket_margin_data_set = PocketMarginData.objects.filter(volume_bands='3. High').order_by(
                'sales_volume_mt')
        temp_band_pocket_margin_data_set = band_pocket_margin_data_set

        for a_low_band_pocket_data in band_pocket_margin_data_set:
            if a_low_band_pocket_data.id != obj.id:
                temp_band_pocket_margin_data_set.exclude(id=a_low_band_pocket_data.id)

            if a_low_band_pocket_data.id == obj.id:
                break

        pocket_margin_percentage_list = []
        for low_band_data in temp_band_pocket_margin_data_set:
            pocket_margin_percentage_list.append(low_band_data.pocket_margin_percentage)
        percentile_data = np.percentile(pocket_margin_percentage_list, 90)
        return percentile_data


class PieChartSerializer(serializers.ModelSerializer):
    sales_by_profit_center = serializers.SerializerMethodField()
    freight_costs_by_freight_types = serializers.SerializerMethodField()
    sum_of_all_sales_volume= serializers.SerializerMethodField()
    sum_of_all_freight_costs= serializers.SerializerMethodField()

    class Meta:
        model = PocketMarginData
        fields = ('sales_by_profit_center', 'freight_costs_by_freight_types','sum_of_all_sales_volume','sum_of_all_freight_costs')

    # SELECT profile_center, SUM(sales_volume_mt) FROM data_pocketmargindata GROUP BY profile_center

    def get_sales_by_profit_center(self, obj):
        pocket_margin_data_set = self.context.get("pocket_margin_data_set")

        sum_of_all_sales_volume = pocket_margin_data_set.aggregate(Sum('sales_volume_mt'))
        sum_sell =sum_of_all_sales_volume['sales_volume_mt__sum']

        data = pocket_margin_data_set.values('profit_center_name').annotate(total_sales_volume=Sum('sales_volume_mt'))

        for single_data in data:
            single_data['ratio']= (single_data['total_sales_volume']/sum_sell)*100
        return data

    # SELECT freight_types, SUM(freight_costs) FROM data_pocketmargindata GROUP BY freight_types

    def get_freight_costs_by_freight_types(self, obj):
        pocket_margin_data_set = self.context.get("pocket_margin_data_set")

        sum_of_all_freight_costs = pocket_margin_data_set.aggregate(Sum('freight_costs'))
        sum_freight_costs = sum_of_all_freight_costs['freight_costs__sum']

        data = pocket_margin_data_set.values('freight_types').annotate(total_freight_costs=Sum('freight_costs'))

        for single_data in data:
            single_data['ratio']= (single_data['total_freight_costs']/sum_freight_costs)*100

        return data

    def get_sum_of_all_sales_volume(self, obj):
        pocket_margin_data_set = self.context.get("pocket_margin_data_set")
        sum_of_all_sales_volume = pocket_margin_data_set.aggregate(Sum('sales_volume_mt'))
        return sum_of_all_sales_volume['sales_volume_mt__sum']

    def get_sum_of_all_freight_costs(self, obj):
        pocket_margin_data_set = self.context.get("pocket_margin_data_set")
        sum_of_all_freight_costs = pocket_margin_data_set.aggregate(Sum('freight_costs'))
        return sum_of_all_freight_costs['freight_costs__sum']





class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearInfo
        fields = '__all__'


