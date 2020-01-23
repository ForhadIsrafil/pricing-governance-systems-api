from django.urls import path, re_path
from . import views

app_name = 'data'

urlpatterns = [

    path(r'dashboard-data', views.DashboardView.as_view(), name='dashboard_data'),
    path(r'change-data-status', views.ChangeDataStatusView.as_view(), name='change_data_status'),
    path(r'get-year-info', views.GetYearInfoView.as_view(), name='get_year_info'),
    path(r'get-piechart', views.PieChartView.as_view(), name='get_piechart'),
    path(r'get-file-data', views.GetFileDataView.as_view(), name='get_file_data'),
    path(r'get-scatterplot-data', views.ScatterplotView.as_view(), name='get_scatter_data'),
    path(r'get-paginated-scatterplot-data', views.PaginatedScatterplotView.as_view(),
         name='get_paginated_scatter_data'),

    path(r'get-waterfall-data', views.WaterFallView.as_view(), name='get_waterfall_data'),
    path(r'get-waterfall-data/<id>', views.WaterFallSingleView.as_view(), name='get_waterfall_data_id'),

    path(r'get-customer-scatterplot-data', views.CustomerScatterView.as_view(), name='get_customer_scatterplot_data'),
    path(r'get-histogram-diagram', views.HistogramDiagramView.as_view(), name='get_histogram_diagram'),
    path(r'get-paginated-pocket-price-band-histogram', views.PaginatedPriceBandHistogramView.as_view(),
         name='get_paginated_price_band_histogram'),

    path(r'get-scatterplot-calculated-data', views.ScatterplotCalculatedView.as_view(),
         name='scatterplot_calculate_data'),
    path(r'calculation-data', views.CalculationView.as_view(), name='calculation_data'),

    path(r'get-unique-customer', views.UniqueCustomerView.as_view(), name='get_unique_customer_data'),
    path(r'get-unique-product', views.UniqueProducFamiliestView.as_view(),
         name='get_unique_product_families_data'),

    path(r'all-active-year', views.AllActiveYearView.as_view(), name='all_active_year'),
    path(r'get-draft-active-year', views.GetDraftActiveView.as_view(), name='get_draft_active_year'),



]
