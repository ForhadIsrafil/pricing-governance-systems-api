
#Pricing Governance Systems-API (Last Update : 16 November,2018)

## Base url: http://127.0.0.1:8000/api/

By using the following endpoint, URL is formed by baseurl + endpoint and API communication is performed.

### To import initial data
$ docker-compose run -p 8000:8020 web python manage.py loaddata seed_data.json

## Main endpoints

| Endpoint name |  Link  | Method |  Purpose |  
|---|---|---|---|---|---|---|
 
|  SignIn | /signin | POST | For login into system |   
|  Add new user | /new-user | POST | For adding new user |   
|  Upload excel file | /upload-file | POST | For uploading new file on system |   
|  Get year data | /get-file-data | GET | All year wise data |  
|  Get scatterplot data | /get-scatterplot-data | GET | All year wise scatterplot data | 
|  Get scatterplot data | /get-paginated-scatterplot-data | GET | All year wise scatterplot data with pagination | 
|  Get watterfall year data | /get-waterfall-data | GET | All year wise waterfall data |   
|  Get watterfall single data | /get-waterfall-data/id | GET | Get single watterfall data |   
|  Get customer scatterplot data | /get-customer-scatterplot-data | GET | All year wise data |   
|  Get Uploading Progress | /get-progress | GET | For getting file uploading progrss data |   
|  Get paginated histogram data | /get-paginated-pocket-price-band-histogram | GET | For getting paginated histogram data |  
|  Dashboard  | /dashboard-data | GET | For getting dashboard data |   
|  Scatterplot Calculated Data | /get-scatterplot-calculated-data | GET | For getting scatterplot calculate data |   
|  Unique Customer  | /get-unique-customer | GET | For getting unique customer|   
|  Unique Product  | /get-unique-product | GET | For getting unique product|   
|  Dashboard Piechart | /get-piechart | GET | For getting Dashboard piechart|   
|  Year Information | /get-year-info | GET | For getting Year Information |   
|  Change Data Status | /change-data-status | GET | For Changing data status |   
|  Get All Active Year info | /all-active-year | GET | For getting all active year info |   
|  Get Draft and Active Year info | /get-draft-active-year | GET | For getting all draft and active year unique info |   
|  Histogram Diagram | /get-histogram-diagram | GET | For getting histogram diagram |   
|  Calculation data | /calculation-data | GET | For getting calculation data |   



##### Sample response list for Whole project:

1. HTTP_201_CREATED
2. HTTP_400_BAD_REQUEST
3. HTTP_401_UNAUTHORIZED
4. HTTP_403_FORBIDDEN
5. HTTP_415_UNSUPPORTED_MEDIA_TYPE
6. HTTP_409_CONFLICT
7. HTTP_404_NOT_FOUND
8. HTTP_204_NO_CONTENT
9. HTTP_500_INTERNAL_SERVER_ERROR
10. HTTP_200_OK



### HTTP REQUEST :  **POST  /signin**

###### params
```json
{
   "username": "Mr Asad",
   "password": "ahsy555777"
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| username      | true | |
| password      | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "token": "2064c54f7d0180c2867f233ece156bc5a8715330",
    "id": 1,
    "name": "admin",
    "image_url": "http://127.0.0.1:8000/media/profile-image/thumbs/no-img.jpeg",
    "email": "admin@gmail.com"
}
```


### HTTP REQUEST :  **POST  /new-user**

###### params
```json
{
   "username": "Mr Asad",
   "email":"sample@gmail.com",
   "password": "ahsy555777",
   "confirm_password":"ahsy555777",
   "type": 2
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| username      | true | |
| email      | true | |
| password      | true | |
| confirm_password      | true | | 
| type      | false  | 1= General User, 2= Account rep, 3= System Administrative |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 3,
    "username": "Mr Asad",
    "email": "sample@gmail.com",
    "type": 3
}
```


### HTTP REQUEST :  **POST  /upload-file**

###### params
```json
{
   "file": "File object" 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| file      | true | | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
 {
 }
```
### HTTP REQUEST :  **GET  /get-file-data**

###### params
```json
{
   "page": 1,
   "year":2012, 
   "limit": 5
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page      | false | | 
| year      | true | | 
| limit     | false | | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
 {
    "page": 1,
    "data": [        
        {
            "id": 1,
            "profit_center_code": 1,
            "profit_center_name": "Profit Center 1",
            "product_segmentation": "Differentiated",
            "channel_partnar_ind": "",
            "business_segment_group": "Petrochemical",
            "customer_group_code": 138,
            "customer_group_name": "Customer SoldTo 138",
            "material_number_code": 385,
            "material_name": "Material 385",
            "freight_type_code": "51",
            "freight_types": "Prepaid",
            "best_fit_acc_man": "Sales Person 32",
            "manf_plant": "EU",
            "sold_to_region": "EU",
            "business_segment": "Petrochemical",
            "product_family": "Category 1",
            "sales_volume_mt": 0.875,
            "gross_sale_usd": 1977.97372824188,
            "invoice_price": 2260.541403705,
            "freight_costs": -332.248248041694,
            "freight_revenue": "0",
            "other_discounts_and_rebates": -0.882694942265224,
            "pocket_price": 1927.41046072104,
            "cogs": -735.813679240276,
            "pocket_margin": 1191.59678148077,
            "pocket_margin_percentage": 0.527128934479038,
            "volume_bands": "1. Low",
            "floor_pocket_margin_corresponding_band": 0.572375862265906,
            "target_pocket_margin_corresponding_band": 0.619903629276617,
            "lower_than_floor_flag": "FLAG",
            "lower_than_target_flag": "FLAG",
            "change_in_invoice_price_per_mt_if_using_floor": "239.18797988028336",
            "change_in_invoice_price_per_mt_if_using_target": "551.757540875466",
            "opportunity_to_floor": 209.289482395248,
            "opportunity_to_target": 482.787848266033,
            "percentage_change_in_invoice_price_or_mt_if_using_floor_margin": "0.1058100415627235",
            "percentage_change_in_invoice_price_or_mt_if_using_target_margin": "0"
        }
    ],
    "total_count": 6347,
    "page": 1
}
```


### HTTP REQUEST :  **GET  /get-scatterplot-data**

###### params
```json
{ 
   "year":2012 ,
   "customer": "Customer SoldTo 1",
   "product_family": "Category 1"
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
 
| year      | true | | 
| customer      | false | | 
| product_family| false | | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
[
    {
        "id": 1,
        "product_family": "Category 1",
        "customer_group_name": "Customer SoldTo 138",
        "sales_volume_mt": 0.875,
        "sold_to_region": "EU",
        "pocket_margin_percentage": 1.192
    },
    {
        "id": 2,
        "product_family": "Category 1",
        "customer_group_name": "Customer SoldTo 1279",
        "sales_volume_mt": 5.4,
        "sold_to_region": "EU",
        "pocket_margin_percentage": 2.130
    }
 
]
```

### HTTP REQUEST :  **GET  /get-paginated-scatterplot-data**

###### params
```json
{
   "year":2012 ,
   "customer": "Customer SoldTo 1",
   "product_family": "Category 1",
   "limit": 2
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page      | false | | 
| year      | true | | 
| customer      | false | | 
| product_family| false | | 
| limit      | false | | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
 {
    "page": 1,
    "total_count":1222,
    "data": [        
        {
            "id": 1,
            "product_family": "Category 1",
            "customer_group_name": "Customer SoldTo 138",
            "sales_volume_mt": 0.875,
            "sold_to_region": "EU",
            "pocket_margin": 1192
        },
        {
            "id": 2,
            "product_family": "Category 1",
            "customer_group_name": "Customer SoldTo 1279",
            "sales_volume_mt": 5.4,
            "sold_to_region": "EU",
            "pocket_margin": 2130
        }
    ],
}
```
### HTTP REQUEST :  **GET  /get-waterfall-data**

###### params
```json
{
   "page": 1,
   "year":2012,
   "customer": "Customer SoldTo 1",
   "product_family": "Category 1"
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page      | false | | 
| year      | true | | 
| customer      | true | | 
| product      | true | | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "single": {
        "other_discounts_and_rebates": -0.772358074482071,
        "freight_costs": -290.7172170364823,
        "cogs": -643.8369693352415,
        "freight_revenue": 0,
        "pocket_margin": 1042.6471837956738,
        "invoice_price": 1977.973728241875,
        "pocket_price": 1686.48415313091,
        "pocket_margin_percentage": 0.527128934479038
    },
    "total": {
        "other_discounts_and_rebates": -0.882694942265224,
        "freight_costs": -332.248248041694,
        "cogs": -735.813679240276,
        "freight_revenue": 0,
        "pocket_margin": 1191.59678148077,
        "invoice_price": 2260.541403705,
        "pocket_price": 1927.41046072104,
        "pocket_margin_percentage": 0.527128934479038
    },
    "customer_group_name": "Customer SoldTo 138",
    "product_family": "Category 1",
    "sales_volume_mt": 0.875
}
```
### HTTP REQUEST :  **GET  /get-waterfall-data/id**

###### params
```json
{
   "page": 1 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "id": 410,
    "invoice_price": 10943.338897936,
    "freight_costs": -598.013025757914,
    "freight_revenue": "0",
    "other_discounts_and_rebates": 0,
    "pocket_price": 10345.3258721781,
    "cogs": -3640.43770329997,
    "pocket_margin": 6704.88816887812,
    "pocket_margin_percentage": 0.612691266478343
}
```

### HTTP REQUEST :  **GET  /get-customer-scatterplot-data**

###### params
```json
{
   "year": 2016 ,
   "customer": "Customer SoldTo 1246",
   "sold_to_region": "EU"
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| page      | false | | 
| year      | true | | 
| customer| false | | 
| sold_to_region | false | | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
 {
    "page": 1,
    "data": [        
    {
        "id": 3,
        "product_family": "Category 1",
        "sales_volume_mt": 6,
        "pocket_margin_percentage": 0.572375862265906
    },
    {
        "id": 8,
        "product_family": "Category 10",
        "sales_volume_mt": 0.02,
        "pocket_margin_percentage": 0.46153098701232
    }
    ],
}
```

### HTTP REQUEST :  **GET  /get-progress**

###### params
```json
{
   
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{     
     97.009
}
```
 

### HTTP REQUEST :  **GET  /get-paginated-pocket-price-band-histogram**

###### params
```json
{
    "year": 2018,
    "limit": 2
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year      | true | | 
| limit      | false | | 


###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "data": [
        {
            "id": 1,
            "customer_group_name": "Customer SoldTo 138",
            "gross_sale_usd": 1977.97372824188,
            "pocket_margin_percentage": 0.527128934479038,
            "calculated_total_sale": 0.0005295712363830441
        },
        {
            "id": 2,
            "customer_group_name": "Customer SoldTo 1279",
            "gross_sale_usd": 17235.7587642492,
            "pocket_margin_percentage": 0.667431396287328,
            "calculated_total_sale": 0.004614602281343929
        }
    ],
    "total_count": 7761,
    "page": 1
}
```


### HTTP REQUEST :  **GET  /dashboard-data**

###### params
```json
{
   "year":2000,
   "number_of_top_data":5
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year      | true | | 
| number_of_top_data  | false | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "id": 4,
    "unique_metarial": 993,
    "unique_product_families": 355,
    "unique_customer": 2569,
    "total_freight_costs": -5144210,
    "total_freight_revenue": 1668282,
    "other_discounts_and_rebates": -65155,
    "product_families_less_than_25_customer": [
        {
            "product_family": "Category 1",
            "total_customer": 7
        },
        {
            "product_family": "Category 100",
            "total_customer": 14
        },
        {
            "product_family": "Category 101",
            "total_customer": 11
        }
        ]
    "number_of_recordes": {
        "number_of_missing_sales": 17,
        "number_of_sales": 6330
    },
    "top_product_families_by_annual_volume": [
        {
            "product_family": "Category 4",
            "total_sales_volume": 29263.839016
        },
        {
            "product_family": "Category 50",
            "total_sales_volume": 11716.999
        },
        {
            "product_family": "Category 28",
            "total_sales_volume": 6604.435525000001
        },
        {
            "product_family": "Category 9",
            "total_sales_volume": 6572.375
        },
        {
            "product_family": "Category 2",
            "total_sales_volume": 3992.707589
        }
    ],
        "top_product_families_by_annual_sales": [
        {
            "total_gross_sale_usd": 12307611.19574953,
            "product_family": "Category 9"
        },
        {
            "total_gross_sale_usd": 10833663.964284837,
            "product_family": "Category 2"
        },
        {
            "total_gross_sale_usd": 10554123.505959192,
            "product_family": "Category 8"
        },
        {
            "total_gross_sale_usd": 10183411.727030734,
            "product_family": "Category 11"
        },
        {
            "total_gross_sale_usd": 9687922.606957017,
            "product_family": "Category 38"
        }
    ],
    "top_customer_by_annual_volume": [
        {
            "customer_group_name": "Customer SoldTo 4",
            "total_sales_volume": 29149.411404000006
        },
        {
            "customer_group_name": "Customer SoldTo 54",
            "total_sales_volume": 6450.5
        },
        {
            "customer_group_name": "Customer SoldTo 1",
            "total_sales_volume": 5768.541628945578
        },
        {
            "customer_group_name": "Customer SoldTo 2",
            "total_sales_volume": 4152.646268
        },
        {
            "customer_group_name": "Customer SoldTo 6",
            "total_sales_volume": 3958.5310939999995
        }
    ],
        "top_customer_by_annual_sales": [
        {
            "total_gross_sale_usd": 15570257.10121716,
            "customer_group_name": "Customer SoldTo 6"
        },
        {
            "total_gross_sale_usd": 11014012.689664748,
            "customer_group_name": "Customer SoldTo 1"
        },
        {
            "total_gross_sale_usd": 9200804.459293786,
            "customer_group_name": "Customer SoldTo 2"
        },
        {
            "total_gross_sale_usd": 8100238.574401646,
            "customer_group_name": "Customer SoldTo 29"
        },
        {
            "total_gross_sale_usd": 5873097.373445965,
            "customer_group_name": "Customer SoldTo 33"
        }
    ],
    "total_customer_product": 6347
}
```

### HTTP REQUEST :  **GET  /get-scatterplot-calculated-data**

###### params
```json
{
   "year": 2018,
   "limit": 2
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year      | true  | |
| limit     | false | |

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "data": [
        {
            "id": 5372,
            "volume_pareto_percentage": 28.615098092496595,
            "volume_bands": "2. Mid",
            "floor_pocket_margin_corresponding_band": 0.0819213980861982,
            "target_pocket_margin_corresponding_band": 0.0819213980861982,
            "ceiling_pocket_margin_corresponding_band": 0.7576132525566162
        },
        {
            "id": 1485,
            "volume_pareto_percentage": 28.661599698302858,
            "volume_bands": "3. High",
            "floor_pocket_margin_corresponding_band": 0.502983565335744,
            "target_pocket_margin_corresponding_band": 0.681771318976369,
            "ceiling_pocket_margin_corresponding_band": 0.7697273084466971
        },
        {
            "id": 1842,
            "volume_pareto_percentage": 28.708113267475678,
            "volume_bands": "2. Mid",
            "floor_pocket_margin_corresponding_band": 0.281439483482492,
            "target_pocket_margin_corresponding_band": 0.281439483482492,
            "ceiling_pocket_margin_corresponding_band": 0.7576132525566162
        }
    ],
    "total_count": 7761,
    "page": 1
}
```


### HTTP REQUEST :  **GET  /get-unique-customer**

###### params
```json
{
   "year": 2018,
   "page": 5,
   "limit": 2,
   "keyword": "asad"  
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year      | true  | |
| page      | false  | |
| limit     | false | |
| keyword     | false | |

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "data": [
        "Customer SoldTo 1687",
        "Customer SoldTo 1350"
    ],
    "total_count": 2569,
    "page": 1,
    "keyword": "asad",
}
``` 

### HTTP REQUEST :  **GET  /get-unique-product**

###### params
```json
{
    "year": 2018,
    "page": 5,
    "limit": 2,
    "keyword": "asad"  
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year      | true  | |
| page      | false  | |
| limit     | false | |
| keyword     | false | |

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "data": [  
      {
            "total_gross_sale_usd": 325120.98787799006,
            "number_of_customer": 8,
            "product_family": "Category 182",
            "total_sales_volume_mt": 60.177732
        }
    ],
    "total_count": 355,
    "page": 1,
    "keyword": "asad",
}
```

### HTTP REQUEST :  **GET  /get-piechart**

###### params
```json
{
    "year": 2018 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year      | true  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "sales_by_profit_center": [
        {
            "ratio": 0.15955033533719595,
            "profit_center_name": "Profit Center 5",
            "total_sales_volume": 266.7315
        },
        {
            "ratio": 11.46835944455363,
            "profit_center_name": "Profit Center 3",
            "total_sales_volume": 19172.461848607712
        },
        {
            "ratio": 24.933664462087094,
            "profit_center_name": "Profit Center 4",
            "total_sales_volume": 41683.35784699997
        },
        {
            "ratio": 13.970806135442857,
            "profit_center_name": "Profit Center 2",
            "total_sales_volume": 23355.977716
        },
        {
            "ratio": 49.46761962257957,
            "profit_center_name": "Profit Center 1",
            "total_sales_volume": 82698.49358495226
        }
    ],
    "freight_costs_by_freight_types": [
        {
            "ratio": 0.0062264468370210645,
            "freight_types": "CP Ready Mix Prodr.",
            "total_freight_costs": -320.3014798373249
        },
        {
            "ratio": 0.0038104574628805184,
            "freight_types": "Prepaid-Separate",
            "total_freight_costs": -196.017921001271
        },
        {
            "ratio": 3.6625005197711045,
            "freight_types": "Regular",
            "total_freight_costs": -188406.70563709622
        },
        {
            "ratio": 30.801908704693055,
            "freight_types": "Prepd & Add @StdRate",
            "total_freight_costs": -1584514.7639046626
        },
        {
            "ratio": 15.829492884629639,
            "freight_types": "Not assigned",
            "total_freight_costs": -814302.3025387354
        },
        {
            "ratio": 0.22253903969977185,
            "freight_types": "Customer Pickup",
            "total_freight_costs": -11447.874783673027
        },
        {
            "ratio": 41.31122386871546,
            "freight_types": "Prepaid",
            "total_freight_costs": -2125135.970063341
        },
        {
            "ratio": 1.3780123561370436,
            "freight_types": "Collect",
            "total_freight_costs": -70887.84477857748
        },
        {
            "ratio": 6.784285722053738,
            "freight_types": "Indent",
            "total_freight_costs": -348997.88166386867
        }
    ],
    "sum_of_all_sales_volume": 167177.02249655937,
    "sum_of_all_freight_costs": -5144209.662770808
}
```



### HTTP REQUEST :  **GET  /get-year-info

###### params
```json
{
    "year": 2018 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year      | true  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "id": 2,
    "year": 2018,
    "file_name": "2bba5725-2977-46cb-8ba2-31df6313c58a.xlsx",
    "status": 2            # 0= draft, 1= Active, 2= Pending
}
```


### HTTP REQUEST :  **GET  /change-data-status**

###### params
```json
{
    "year_id": 4,
    "status": 1 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| year_id      | true  | | 
| status      | true  | # 0= draft, 1= Active, 2= Pending | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
 
```

### HTTP REQUEST :  **GET  /all-active-year**

###### params
```json
{
    "page": 4,
    "limit": 1 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| page      | false  | | 
| limit      | false  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "data": [
        {
            "id": 2,
            "year": 2018,
            "file_name": "2bba5725-2977-46cb-8ba2-31df6313c58a.xlsx",
            "status": 1
        }
    ],
    "total_count": 1,
    "page": 1
}
 
```


### HTTP REQUEST :  **GET  /get-draft-active-year**

###### params
```json
{
    "page": 4,
    "limit": 1 
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| page      | false  | | 
| limit      | false  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "page": 1,
    "limit": 10,
    "total_count": 2,
    "data": [
        {
            "id": 1,
            "year": 2018,
            "file_name": "ddbcc2a8-78db-42ee-b829-34be0dcb926a.xlsx",
            "status": 0
        },
        {
            "id": 3,
            "year": 2017,
            "file_name": "05c894ff-f7e0-45b0-9ff9-9bb5e2de2e58.xlsx",
            "status": 0
        }
    ]
}
 
```


### HTTP REQUEST :  **GET  /get-histogram-diagram**

###### params
```json
{ 
    "threshold": 10,
    "year": 2018
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| threshold      | false  | | 
| year      | True  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "data": [
        {
            "last_range": 5,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 10,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 15,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 20,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 25,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 30,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 35,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 40,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 45,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 50,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 55,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 60,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 65,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 70,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 75,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 80,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 85,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 90,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 95,
            "calculated_total_percentage": 164796.7715355596
        },
        {
            "last_range": 100,
            "calculated_total_percentage": 164796.7715355596
        }
    ]
}
 
```


### HTTP REQUEST :  **GET  /calculation-data**

###### params
```json
{ 
    "page": 10,
    "limit": 10,
    "year": 2018,
    "floor_percentage_threshold": 90,
    "ceiling_percentage_threshold": 110
}

```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- | 
| page      | false  | | 
| limit      | false  | | 
| floor_percentage_threshold      | false  |  default 90  | 
| ceiling_percentage_threshold      | false  | default 110 | 
| year      | True  | | 

###### output

### possible response list:

1. HTTP_200_OK ----- success 

``` json
{
    "total_count": 6347,
    "data": [
        {
            "low": {
                "ceiling": 6.399050412250782,
                "floor": 5.2355867009324575,
                "volumn_break": 33408.860470505584,
                "target": 5.817318556591619
            },
            "high": {
                "ceiling": 18806.438725800002,
                "floor": 15387.0862302,
                "volumn_break": 167177.0224965601,
                "target": 17096.762478
            },
            "mid": {
                "ceiling": 181.94701125757453,
                "floor": 148.86573648347007,
                "volumn_break": 132983.49754056009,
                "target": 165.4063738705223
            }
        }
    ],
    "page": "600",
    "table_data": [
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 47837.86897550556,
            "id": 5372
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 47915.60897550556,
            "id": 1485
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 47993.36897550556,
            "id": 1842
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 48071.24897550556,
            "id": 2117
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 48149.15897550556,
            "id": 5079
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 48227.15897550556,
            "id": 537
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 48305.24897550556,
            "id": 4410
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 48383.36897550556,
            "id": 4411
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 48461.90897550556,
            "id": 5308
        },
        {
            "Band": "Mid",
            "sum_sales_volume_mt": 48540.65897550556,
            "id": 1292
        }
    ]
}
```