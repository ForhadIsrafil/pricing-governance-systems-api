from rest_framework.views import APIView
from .serializers import PocketDataSerializer, ScatterplotSerializer, WaterfallSerializer, WaterfallSingleSerializer, \
    CustomerScatterSerializer, PriceBandHistogramViewSerializer, DashboardSerializer, ScatterplotCalculatedSerializer, \
    PieChartSerializer, YearSerializer, HistogramDiagramViewSerializer
from const import slicer
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework import renderers, status
import json
import hashlib
import tempfile
import shutil
from django.conf import settings
import pandas as pd
from openpyxl import load_workbook
from .models import PocketMarginData, YearInfo
import permissions
from django.db.models import Avg, Count, Min, Sum
from const import get_year, get_year_for_dashboard
from django.db.models import Q
import numpy as np

# !/usr/bin/python
import MySQLdb
from decouple import config


class GetFileDataView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get uploaded default all data
    def get(self, request, format=None):
        year = request.GET.get('year')
        page_i = request.GET.get('page', 1)
        limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)
        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id)

        total_count = pocket_margin_data_set.count()
        pocket_margin_data_set = slicer(pocket_margin_data_set, int(page_i), limit)

        serializers = PocketDataSerializer(pocket_margin_data_set, many=True)

        response = {
            "data": serializers.data,
            "total_count": total_count,
            "page": page_i
        }
        return Response(response, status=status.HTTP_200_OK)


class ScatterplotView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get all Scatterplot data
    def get(self, request, format=None):
        customer_group_name = request.GET.get('customer')
        product_family = request.GET.get('product_family')

        year = request.GET.get('year')
        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if customer_group_name is not None:
            pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id,
                                                                     customer_group_name=customer_group_name).only('id',
                                                                                                                   'product_family',
                                                                                                                   'customer_group_name',
                                                                                                                   'sales_volume_mt',
                                                                                                                   'sold_to_region',
                                                                                                                   'pocket_margin_percentage')
        elif product_family is not None:
            pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id,
                                                                     product_family=product_family).only('id',
                                                                                                         'product_family',
                                                                                                         'customer_group_name',
                                                                                                         'sales_volume_mt',
                                                                                                         'sold_to_region',
                                                                                                         'pocket_margin_percentage')
        else:
            pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).only('id',
                                                                                                    'product_family',
                                                                                                    'customer_group_name',
                                                                                                    'sales_volume_mt',
                                                                                                    'sold_to_region',
                                                                                                    'pocket_margin_percentage')
        
        serializers = ScatterplotSerializer(pocket_margin_data_set, many=True)
        additional_data =self.additional_data(year, product_family)
        
        response = {
            "data": serializers.data,
            "additional_data": additional_data.data,
        }

        # print(response)

        return Response(response, status=status.HTTP_200_OK)

    def additional_data(self, year, product):

        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sorted_pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id, product_family=product).order_by(
            'sales_volume_mt')
        total_sum = PocketMarginData.objects.filter(year_info_id=year_obj.id, product_family=product).aggregate(Sum('sales_volume_mt'))
        low_indecator = total_sum['sales_volume_mt__sum'] * 0.2  # 20 %
        mid_indecator = total_sum['sales_volume_mt__sum'] * 0.8  # 80 %

        # volumn break
        low_vol_break = 0
        mid_vol_break = 0
        high_vol_break = 0

        sum = 0
        low_band_sales_volume_mt_list = []
        mid_band_sales_volume_mt_list = []
        high_band_sales_volume_mt_list = []
        arr = []
        for obj in sorted_pocket_margin_data_set:
            temp = {}
            sum += obj.sales_volume_mt
            if sum < low_indecator:
                low = 'Low'
                temp['id'] = obj.id
                temp['sum_sales_volume_mt'] = sum
                temp['Band'] = low
                arr.append(temp)

                low_vol_break = obj.sales_volume_mt
                mid_vol_break = obj.sales_volume_mt
                high_vol_break = obj.sales_volume_mt

                low_band_sales_volume_mt_list.append(obj.pocket_margin_percentage)

            elif sum >= low_indecator and sum <= mid_indecator:
                medium = 'Mid'
                temp['id'] = obj.id
                temp['sum_sales_volume_mt'] = sum
                temp['Band'] = medium
                arr.append(temp)

                mid_vol_break = obj.sales_volume_mt
                high_vol_break = obj.sales_volume_mt

                mid_band_sales_volume_mt_list.append(obj.pocket_margin_percentage)

            elif sum > mid_indecator:
                high = 'High'
                temp['id'] = obj.id
                temp['sum_sales_volume_mt'] = sum
                temp['Band'] = high
                arr.append(temp)

                high_vol_break = obj.sales_volume_mt

                high_band_sales_volume_mt_list.append(obj.pocket_margin_percentage)

        # print(low_vol_break, mid_vol_break, high_vol_break)
        # print(low_band_sales_volume_mt_list)
        # print(mid_band_sales_volume_mt_list)
        # print(high_band_sales_volume_mt_list)

        temp_low_band_data = {}
        temp_mid_band_data = {}
        temp_high_band_data = {}

        # LOW BAND DATA
        if low_band_sales_volume_mt_list != []:
            a = np.array(low_band_sales_volume_mt_list)
            temp_low_band_data['target'] = np.percentile(a, 75)
            temp_low_band_data['floor'] = np.percentile(a, 50)
            temp_low_band_data['ceiling'] = np.percentile(a, 90)
            temp_low_band_data['volumn_break'] = low_vol_break
            temp_low_band_data['line'] = "true"
        else:
            temp_low_band_data['target'] = 0
            temp_low_band_data['floor'] = 0
            temp_low_band_data['ceiling'] = 0
            temp_low_band_data['volumn_break'] = low_vol_break
            temp_low_band_data['line'] = "false"



        # MID BAND DATA
        if mid_band_sales_volume_mt_list != []:
            a = np.array(mid_band_sales_volume_mt_list)
            temp_mid_band_data['target'] = np.percentile(a, 75)
            temp_mid_band_data['floor'] = np.percentile(a, 50)
            temp_mid_band_data['ceiling'] = np.percentile(a, 90)
            temp_mid_band_data['volumn_break'] = mid_vol_break
            temp_mid_band_data['line'] = "true"
        else:
            temp_mid_band_data['target'] = 0
            temp_mid_band_data['floor'] = 0
            temp_mid_band_data['ceiling'] = 0
            temp_mid_band_data['volumn_break'] = mid_vol_break
            temp_mid_band_data['line'] = "false"


        # HIGH BAND DATA
        if high_band_sales_volume_mt_list != []:
            a = np.array(high_band_sales_volume_mt_list)
            temp_high_band_data['target'] = np.percentile(a, 75)
            temp_high_band_data['floor'] = np.percentile(a, 50)
            temp_high_band_data['ceiling'] = np.percentile(a, 90)
            temp_high_band_data['volumn_break'] = high_vol_break
            temp_high_band_data['line'] = "true"
        else:
            temp_high_band_data['target'] = 0
            temp_high_band_data['floor'] = 0
            temp_high_band_data['ceiling'] = 0
            temp_high_band_data['volumn_break'] = high_vol_break
            temp_high_band_data['line'] = "false"


        data = []
        data_temp = {}
        data_temp['low'] = temp_low_band_data
        data_temp['mid'] = temp_mid_band_data
        data_temp['high'] = temp_high_band_data
        data.append(data_temp)

        return Response(data_temp, status=status.HTTP_200_OK)




class PaginatedScatterplotView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # get paginated Scatterplot data
    def get(self, request, format=None):
        year = request.GET.get('year')
        customer_group_name = request.GET.get('customer')
        product_family = request.GET.get('product_family')
        page_i = request.GET.get('page', 1)
        limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)
        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if customer_group_name is not None:
            pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id,
                                                                     customer_group_name=customer_group_name).only('id',
                                                                                                                   'product_family',
                                                                                                                   'customer_group_name',
                                                                                                                   'sales_volume_mt',
                                                                                                                   'sold_to_region',
                                                                                                                   'pocket_margin_percentage')
        elif product_family is not None:
            pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id,
                                                                     product_family=product_family).only('id',
                                                                                                         'product_family',
                                                                                                         'customer_group_name',
                                                                                                         'sales_volume_mt',
                                                                                                         'sold_to_region',
                                                                                                         'pocket_margin_percentage')
        else:
            pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).only('id',
                                                                                                    'product_family',
                                                                                                    'customer_group_name',
                                                                                                    'sales_volume_mt',
                                                                                                    'sold_to_region',
                                                                                                    'pocket_margin_percentage')
        total_count = pocket_margin_data_set.count()
        if limit == "-1":
            limit = total_count
        pocket_margin_data_set = slicer(pocket_margin_data_set, int(page_i), limit)

        serializers = ScatterplotSerializer(pocket_margin_data_set, many=True)

        response = {
            "data": serializers.data,
            "total_count": total_count,
            "page": page_i
        }
        return Response(response, status=status.HTTP_200_OK)


class WaterFallView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get processed Waterfall data
    def get(self, request):
        year = request.GET.get('year')
        customer = request.GET.get('customer')
        product_family = request.GET.get('product_family')
        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        pocket_margin_data = None

        if customer is not None and product_family is not None:
            pocket_margin_data = PocketMarginData.objects.filter(year_info_id=year_obj.id,
                                                                 customer_group_name=customer,
                                                                 product_family=product_family).only('id',
                                                                                                     'customer_group_name',
                                                                                                     'product_family',
                                                                                                     'sales_volume_mt',
                                                                                                     'invoice_price',
                                                                                                     'freight_revenue',
                                                                                                     'other_discounts_and_rebates',
                                                                                                     'pocket_price',
                                                                                                     'cogs',
                                                                                                     'pocket_margin',
                                                                                                     'pocket_margin_percentage',
                                                                                                     'freight_costs').first()

        if pocket_margin_data is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializers = WaterfallSerializer(pocket_margin_data)
        return Response(serializers.data, status=status.HTTP_200_OK)


class WaterFallSingleView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # check valided year object
    def get_pocket_object(self, id):
        try:
            return PocketMarginData.objects.get(id=id)
        except PocketMarginData.DoesNotExist:
            raise Http404

    # get single Waterfall data-details by id
    def get(self, request, id):
        pocket_id = self.get_pocket_object(id)
        serializer = WaterfallSingleSerializer(pocket_id, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerScatterView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get CustomerScatter processed/filtered data
    def get(self, request, format=None):
        customer_group_name = request.GET.get('customer')
        sold_to_region = request.GET.get('sold_to_region')
        year = request.GET.get('year')

        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if customer_group_name is None and sold_to_region is None:
            customer_scatter_data = PocketMarginData.objects.all().only('id', 'product_family', 'sales_volume_mt',
                                                                        'pocket_margin_percentage')
        elif customer_group_name is None:
            customer_scatter_data = PocketMarginData.objects.filter(sold_to_region=sold_to_region,
                                                                    year_info_id=year_obj.id).only('id',
                                                                                                   'product_family',
                                                                                                   'sales_volume_mt',
                                                                                                   'pocket_margin_percentage')
        elif sold_to_region is None:
            customer_scatter_data = PocketMarginData.objects.filter(customer_group_name=customer_group_name,
                                                                    year_info_id=year_obj.id).only('id',
                                                                                                   'product_family',
                                                                                                   'sales_volume_mt',
                                                                                                   'pocket_margin_percentage')
        else:
            customer_scatter_data = PocketMarginData.objects.filter(customer_group_name=customer_group_name,
                                                                    sold_to_region=sold_to_region,
                                                                    year_info_id=year_obj.id).only('id',
                                                                                                   'product_family',
                                                                                                   'sales_volume_mt',
                                                                                                   'pocket_margin_percentage')

        serializers = CustomerScatterSerializer(customer_scatter_data, many=True)
        return Response(serializers.data, status.HTTP_200_OK)


class PaginatedPriceBandHistogramView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get complete paginated processed-operation of PriceBandHistogram data
    def get(self, request, format=None):
        year = request.GET.get('year')
        page_i = request.GET.get('page', 1)
        limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)
        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).only('id',
                                                                                                'customer_group_name',
                                                                                                'gross_sale_usd',
                                                                                                'pocket_margin_percentage')
        all_pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).only('id',
                                                                                                    'customer_group_name',
                                                                                                    'gross_sale_usd',
                                                                                                    'pocket_margin_percentage')
        sum = PocketMarginData.objects.filter(year_info_id=year_obj.id).aggregate(
            total_gross_sale_usd=Sum('gross_sale_usd'))

        total_count = pocket_margin_data_set.count()
        if limit == "-1":
            limit = total_count
        pocket_margin_data_set = slicer(pocket_margin_data_set, int(page_i), limit)

        serializers = PriceBandHistogramViewSerializer(pocket_margin_data_set, many=True,
                                                       context={'sum': sum['total_gross_sale_usd'],
                                                                'pocket_margin_data_set': all_pocket_margin_data_set})
        response = {
            "data": serializers.data,
            "total_count": total_count,
            "page": page_i
        }
        return Response(response, status=status.HTTP_200_OK)


class HistogramDiagramView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get complete processed operation of PriceBandHistogram data
    def get(self, request, format=None):
        year = request.GET.get('year')
        threshold = int(request.GET.get('threshold', 5))

        if threshold <= 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        year_obj = get_year(year)
        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).only(
            'pocket_margin_percentage', 'gross_sale_usd')

        sum = PocketMarginData.objects.filter(year_info_id=year_obj.id).aggregate(
            total_gross_sale_usd=Sum('gross_sale_usd'))
        serializers = HistogramDiagramViewSerializer(year_obj, many=False,
                                                     context={'sum': sum['total_gross_sale_usd'],
                                                              'pocket_margin_data_set': pocket_margin_data_set,
                                                              'threshold': threshold})
        return Response(serializers.data, status.HTTP_200_OK)


class DashboardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get default Dashboard data
    def get(self, request):
        year = request.GET.get('year')
        number_of_top_data = request.GET.get('number_of_top_data')
        year_obj = get_year_for_dashboard(year)
        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).all()
        serializers = DashboardSerializer(year_obj, context={'pocket_margin_data_set': pocket_margin_data_set,
                                                             'number_of_top_data': number_of_top_data})
        return Response(serializers.data, status=status.HTTP_200_OK)


class ChangeDataStatusView(APIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get(self, request):
        year_id = request.GET.get('year_id')
        data_status = request.GET.get('status')
        year_obj = YearInfo.objects.filter(id=year_id, status=0).last()
        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if data_status == '0':
            # old requirements START
            # is_pocket_data_deleted = PocketMarginData.objects.filter(id=year_obj.id).delete()
            # is_year_deleted = year_obj.delete()
            # old requirements END

            # new requirements START
            previous_years_deleted = YearInfo.objects.filter(year=year_obj.year).delete()
            # new requirements END
        elif data_status == '1':
            updated = YearInfo.objects.filter(id=year_obj.id).update(status=1)

            # removing previous year
            previous_year_deleted = YearInfo.objects.filter(year=year_obj.year).exclude(id=year_obj.id).delete()

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class GetYearInfoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get default Dashboard data
    def get(self, request):
        year = request.GET.get('year')
        year_obj = YearInfo.objects.filter(year=year).last()
        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers = YearSerializer(year_obj)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ScatterplotCalculatedView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get paginared and processed(calculated_result) data of Scatterplot=(volume_pareto,band,floor,ceiling,target)
    def get(self, request):
        year = request.GET.get('year')
        page_i = request.GET.get('page', 1)
        limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)
        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sorted_pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).order_by(
            'sales_volume_mt')

        sum = PocketMarginData.objects.filter(year_info_id=year_obj.id).aggregate(
            total_sales_volume_mt=Sum('sales_volume_mt'))
        total_count = sorted_pocket_margin_data_set.count()

        pocket_margin_data_set = slicer(sorted_pocket_margin_data_set, int(page_i), limit)

        serializers = ScatterplotCalculatedSerializer(pocket_margin_data_set,
                                                      context={'sum': sum['total_sales_volume_mt'],
                                                               'sorted_pocket_margin_data_set': sorted_pocket_margin_data_set},
                                                      many=True)

        response = {
            "data": serializers.data,
            "total_count": total_count,
            "page": page_i
        }

        return Response(response, status=status.HTTP_200_OK)


class UniqueCustomerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get unique_customer paginared data
    def get(self, request, format=None):
        keyword = request.GET.get('keyword')
        year = request.GET.get('year')
        page_i = request.GET.get('page', 1)
        year_obj = get_year(year)

        limit = request.GET.get('limit', None)

        need_all_data = False

        if limit == None:
            limit = settings.DATA_NO_PER_PAGE
        elif limit == '-1':
            need_all_data = True

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if keyword is not None:
            striped_keyword = keyword.strip(' ')
            customer_group_name_set = PocketMarginData.objects.filter(year_info_id=year_obj.id,
                                                                      customer_group_name=striped_keyword).values_list(
                'customer_group_name', flat=True)

        else:
            customer_group_name_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).values_list(
                'customer_group_name', flat=True)

        unique_customer_group_name = set(customer_group_name_set)

        arr = []
        for customer in unique_customer_group_name:
            arr.append(customer)

        total_count = len(arr)
        if need_all_data is False:
            unique_customer_group_name = slicer(arr, int(page_i), limit)

            data = []
            for single_customer in unique_customer_group_name:
                data.append(single_customer)

            response = {
                "data": data,
                "total_count": total_count,
                "page": page_i,
                "keyword": keyword
            }
        else:
            data = []
            for single_customer in arr:
                data.append(single_customer)

            response = {
                "data": data,
                "total_count": total_count,
                "page": 1,
                "keyword": keyword
            }

        return Response(response, status=status.HTTP_200_OK)


class UniqueProducFamiliestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get unique_product_families paginared data
    def get(self, request, format=None):
        keyword = request.GET.get('keyword')
        year = request.GET.get('year')
        page_i = request.GET.get('page', 1)
        limit = request.GET.get('limit', None)

        need_all_data = False

        if limit == None:
            limit = settings.DATA_NO_PER_PAGE
        elif limit == '-1':
            need_all_data = True

        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        arr = []

        if keyword is not None:
            striped_keyword = keyword.strip(' ')

            query = "SELECT id, product_family, SUM(sales_volume_mt) AS total_sales_volume_mt," \
                    " SUM(gross_sale_usd) AS total_gross_sale_usd, COUNT(gross_sale_usd) AS number_of_customer " \
                    "FROM (SELECT * FROM data_pocketmargindata WHERE product_family ='" + striped_keyword + "' AND year_info_id=" + str(
                year_obj.id) + ") AS filtered_data " \
                               "GROUP BY product_family"

        else:

            query = "SELECT id, product_family, SUM(sales_volume_mt) AS total_sales_volume_mt," \
                    " SUM(gross_sale_usd) AS total_gross_sale_usd, COUNT(gross_sale_usd) AS number_of_customer " \
                    "FROM (SELECT * FROM data_pocketmargindata WHERE year_info_id=" + str(
                year_obj.id) + ") AS filtered_data " \
                               "GROUP BY product_family"


        result = PocketMarginData.objects.raw(query)

        for row in result:
            temp = {}
            temp['product_family'] = row.product_family
            temp['total_sales_volume_mt'] = row.total_sales_volume_mt
            temp['total_gross_sale_usd'] = row.total_gross_sale_usd
            temp['number_of_customer'] = row.number_of_customer

            arr.append(temp)

        total_count = len(arr)
        if need_all_data is False:
            unique_product_family_set = slicer(arr, int(page_i), limit)

            data = []
            for single_product_family in unique_product_family_set:
                data.append(single_product_family)

            response = {
                "data": data,
                "total_count": total_count,
                "page": page_i,
                "keyword": keyword
            }
        else:
            data = []
            for single_product_family in arr:
                data.append(single_product_family)

            response = {
                "data": data,
                "total_count": total_count,
                "page": 1,
                "keyword": keyword
            }

        return Response(response, status=status.HTTP_200_OK)


class PieChartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # get view of PieChart(data)
    def get(self, request):
        year = request.GET.get('year')
        year_obj = get_year_for_dashboard(year)
        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id).only('sales_volume_mt',
                                                                                                'profit_center_name',
                                                                                                'freight_costs',
                                                                                                'freight_types')
        serializers = PieChartSerializer(year_obj, context={'pocket_margin_data_set': pocket_margin_data_set})
        return Response(serializers.data, status.HTTP_200_OK)


class AllActiveYearView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        page_i = request.GET.get('page', 1)
        limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)

        years = YearInfo.objects.filter(status=1).order_by('-year')
        total_count = years.count()
        years = slicer(years, int(page_i), limit)

        serializers = YearSerializer(years, many=True)

        response = {
            "data": serializers.data,
            "total_count": total_count,
            "page": page_i
        }
        return Response(response, status=status.HTTP_200_OK)


class GetDraftActiveView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        page_i = request.GET.get('page', 1)
        limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)

        all_years = YearInfo.objects.all()

        year_arr = []
        id_arr = []
        for single_year in all_years:
            if single_year.status == 0 or single_year.status == 1:
                if single_year.year not in year_arr:
                    year_arr.append(single_year.year)
                    id_arr.append(single_year.id)

        filtered_years = YearInfo.objects.filter(id__in=id_arr).order_by('-year')

        total_count = len(filtered_years)

        serializers = YearSerializer(filtered_years, many=True)

        response = {
            "data": serializers.data,
            "total_count": total_count,
            "page": page_i,
            "limit": limit
        }
        return Response(response, status=status.HTTP_200_OK)


# class CalculationView(APIView):

#     def get(self, request):
#         year = request.GET.get('year')
#         product = request.GET.get('product')

#         page_i = request.GET.get('page', 1)
#         floor_percentage_threshold = int(request.GET.get('floor_percentage_threshold', 90))
#         ceiling_percentage_threshold = int(request.GET.get('ceiling_percentage_threshold', 110))
        
#         limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)
#         year_obj = get_year(year)

#         if year_obj is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         sorted_pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id, product_family=product).order_by(
#             'sales_volume_mt')
#         total_sum = PocketMarginData.objects.filter(year_info_id=year_obj.id, product_family=product).aggregate(Sum('sales_volume_mt'))
#         low_indecator = total_sum['sales_volume_mt__sum'] * 0.2  # 20 %
#         mid_indecator = total_sum['sales_volume_mt__sum'] * 0.8  # 80 %

#         # volumn break
#         low_vol_break = 0
#         mid_vol_break = 0
#         high_vol_break = 0

#         sum = 0
#         low_band_sales_volume_mt_list = []
#         mid_band_sales_volume_mt_list = []
#         high_band_sales_volume_mt_list = []
#         arr = []
#         for obj in sorted_pocket_margin_data_set:
#             temp = {}
#             sum += obj.sales_volume_mt
#             if sum < low_indecator:
#                 low = 'Low'
#                 temp['id'] = obj.id
#                 temp['sum_sales_volume_mt'] = sum
#                 temp['Band'] = low
#                 arr.append(temp)

#                 low_vol_break = sum

#                 low_band_sales_volume_mt_list.append(obj.sales_volume_mt)

#             elif sum > low_indecator and sum < mid_indecator:
#                 medium = 'Mid'
#                 temp['id'] = obj.id
#                 temp['sum_sales_volume_mt'] = sum
#                 temp['Band'] = medium
#                 arr.append(temp)

#                 mid_vol_break = sum

#                 mid_band_sales_volume_mt_list.append(obj.sales_volume_mt)

#             elif sum > mid_indecator:
#                 high = 'High'
#                 temp['id'] = obj.id
#                 temp['sum_sales_volume_mt'] = sum
#                 temp['Band'] = high
#                 arr.append(temp)

#                 high_vol_break = sum

#                 high_band_sales_volume_mt_list.append(obj.sales_volume_mt)

#         temp_low_band_data = {}
#         temp_mid_band_data = {}
#         temp_high_band_data = {}

#         # LOW BAND DATA
#         if low_band_sales_volume_mt_list != []:
#             low_band_target = np.mean(low_band_sales_volume_mt_list)
#             low_band_floor = low_band_target * (floor_percentage_threshold / 100)  # 90 % default
#             low_band_ceiling = low_band_target * (ceiling_percentage_threshold / 100)  # +10%

#             temp_low_band_data['target'] = low_band_target
#             temp_low_band_data['floor'] = low_band_floor
#             temp_low_band_data['ceiling'] = low_band_ceiling
#             temp_low_band_data['volumn_break'] = low_vol_break

#         # MID BAND DATA
#         if mid_band_sales_volume_mt_list != []:
#             mid_band_target = np.mean(mid_band_sales_volume_mt_list)
#             mid_band_floor = mid_band_target * (floor_percentage_threshold / 100)  # 90 % default
#             mid_band_ceiling = mid_band_target * (ceiling_percentage_threshold / 100)  # +10%

#             temp_mid_band_data['target'] = mid_band_target
#             temp_mid_band_data['floor'] = mid_band_floor
#             temp_mid_band_data['ceiling'] = mid_band_ceiling
#             temp_mid_band_data['volumn_break'] = mid_vol_break

#         # HIGH BAND DATA
#         if high_band_sales_volume_mt_list != []:
#             high_band_target = np.mean(high_band_sales_volume_mt_list)
#             high_band_floor = high_band_target * (floor_percentage_threshold / 100)  # 90 % default
#             high_band_ceiling = high_band_target * (ceiling_percentage_threshold / 100)  # +10%

#             temp_high_band_data['target'] = high_band_target
#             temp_high_band_data['floor'] = high_band_floor
#             temp_high_band_data['ceiling'] = high_band_ceiling
#             temp_high_band_data['volumn_break'] = high_vol_break

#         data = []
#         data_temp = {}
#         data_temp['low'] = temp_low_band_data
#         data_temp['mid'] = temp_mid_band_data
#         data_temp['high'] = temp_high_band_data
#         data.append(data_temp)

#         total_count = sorted_pocket_margin_data_set.count()
#         limit = total_count
#         pocket_margin_data_set = slicer(arr, int(page_i), limit)
#         response = {
#             "data": data,
#             "table_data": pocket_margin_data_set,
#             "total_count": total_count,
#             "page": page_i
#         }

#         return Response(response, status=status.HTTP_200_OK)


class CalculationView(APIView):

    def get(self, request):
        year = request.GET.get('year')
        product = request.GET.get('product')

        page_i = request.GET.get('page', 1)
        floor_percentage_threshold = int(request.GET.get('floor_percentage_threshold', 90))
        ceiling_percentage_threshold = int(request.GET.get('ceiling_percentage_threshold', 110))
        
        limit = request.GET.get('limit', settings.DATA_NO_PER_PAGE)
        year_obj = get_year(year)

        if year_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sorted_pocket_margin_data_set = PocketMarginData.objects.filter(year_info_id=year_obj.id, product_family=product).order_by(
            'sales_volume_mt')
        total_sum = PocketMarginData.objects.filter(year_info_id=year_obj.id, product_family=product).aggregate(Sum('sales_volume_mt'))
        low_indecator = total_sum['sales_volume_mt__sum'] * 0.2  # 20 %
        mid_indecator = total_sum['sales_volume_mt__sum'] * 0.8  # 80 %

        # volumn break
        low_vol_break = 0
        mid_vol_break = 0
        high_vol_break = 0

        sum = 0
        low_band_sales_volume_mt_list = []
        mid_band_sales_volume_mt_list = []
        high_band_sales_volume_mt_list = []
        arr = []
        for obj in sorted_pocket_margin_data_set:
            temp = {}
            sum += obj.sales_volume_mt
            if sum < low_indecator:
                low = 'Low'
                temp['id'] = obj.id
                temp['sum_sales_volume_mt'] = sum
                temp['Band'] = low
                arr.append(temp)

                low_vol_break = obj.sales_volume_mt
                mid_vol_break = obj.sales_volume_mt
                high_vol_break = obj.sales_volume_mt

                low_band_sales_volume_mt_list.append(obj.pocket_margin_percentage)

            elif sum >= low_indecator and sum <= mid_indecator:
                medium = 'Mid'
                temp['id'] = obj.id
                temp['sum_sales_volume_mt'] = sum
                temp['Band'] = medium
                arr.append(temp)

                mid_vol_break = obj.sales_volume_mt
                high_vol_break = obj.sales_volume_mt

                mid_band_sales_volume_mt_list.append(obj.pocket_margin_percentage)

            elif sum > mid_indecator:
                high = 'High'
                temp['id'] = obj.id
                temp['sum_sales_volume_mt'] = sum
                temp['Band'] = high
                arr.append(temp)

                high_vol_break = obj.sales_volume_mt

                high_band_sales_volume_mt_list.append(obj.pocket_margin_percentage)

        # print(low_vol_break, mid_vol_break, high_vol_break)
        # print(low_band_sales_volume_mt_list)
        # print(mid_band_sales_volume_mt_list)
        # print(high_band_sales_volume_mt_list)

        temp_low_band_data = {}
        temp_mid_band_data = {}
        temp_high_band_data = {}

        # LOW BAND DATA
        if low_band_sales_volume_mt_list != []:
            a = np.array(low_band_sales_volume_mt_list)
            temp_low_band_data['target'] = np.percentile(a, 75)
            temp_low_band_data['floor'] = np.percentile(a, 50)
            temp_low_band_data['ceiling'] = np.percentile(a, 90)
            temp_low_band_data['volumn_break'] = low_vol_break



        # MID BAND DATA
        if mid_band_sales_volume_mt_list != []:
            a = np.array(mid_band_sales_volume_mt_list)
            temp_mid_band_data['target'] = np.percentile(a, 75)
            temp_mid_band_data['floor'] = np.percentile(a, 50)
            temp_mid_band_data['ceiling'] = np.percentile(a, 90)
            temp_mid_band_data['volumn_break'] = mid_vol_break


        # HIGH BAND DATA
        if high_band_sales_volume_mt_list != []:
            a = np.array(high_band_sales_volume_mt_list)
            temp_high_band_data['target'] = np.percentile(a, 75)
            temp_high_band_data['floor'] = np.percentile(a, 50)
            temp_high_band_data['ceiling'] = np.percentile(a, 90)
            temp_high_band_data['volumn_break'] = high_vol_break


        data = []
        data_temp = {}
        data_temp['low'] = temp_low_band_data
        data_temp['mid'] = temp_mid_band_data
        data_temp['high'] = temp_high_band_data
        data.append(data_temp)

        total_count = sorted_pocket_margin_data_set.count()
        limit = total_count
        pocket_margin_data_set = slicer(arr, int(page_i), limit)
        response = {
            "data": data,
            "table_data": pocket_margin_data_set,
            "total_count": total_count,
            "page": page_i
        }

        return Response(response, status=status.HTTP_200_OK)
