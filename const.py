from django.conf import settings
import os
import smtplib
from email.mime.text import MIMEText
import base64
from django.apps import apps
import uuid
from rest_framework.response import Response
from PIL import Image
from data.models import YearInfo
from django.http import Http404


class Email():
    def send_email(self, subject, to_address, from_address, message):

        try:

            sender = from_address
            recipient = to_address
            message = message

            msg = MIMEText(message, 'html')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient

            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(sender, [recipient], msg.as_string())
            server.quit()
            # END confirmation email
            return True
        except:
            return False


DATA_NO_PER_PAGE = settings.DATA_NO_PER_PAGE


def slicer(data, page_i, limit=DATA_NO_PER_PAGE):
    limit = int(limit)
    start_idx = (page_i - 1) * limit
    end_idx = start_idx + limit
    return data[start_idx:end_idx]


# ================== CONVERTED to USD USING CONSTANT EXCHANGE RATE ================
# column AT
def get_convert_to_usd_invoice_price(invoice_price, current_xchange_rate):
    return float(invoice_price) / float(current_xchange_rate)


# column AU
def get_convert_to_usd_freight_costs(freight_costs, current_xchange_rate):
    return float(freight_costs) / float(current_xchange_rate)


# column AV
def get_convert_to_usd_freight_revernue(freight_revenue, current_xchange_rate):
    return float(freight_revenue) / float(current_xchange_rate)


# column AW
def get_convert_to_usd_other_doc_and_rebates(other_discounts_and_rebates, current_xchange_rate):
    return float(other_discounts_and_rebates) / float(current_xchange_rate)


# column AX
def get_convert_to_usd_pocket_price(pocket_price, current_xchange_rate):
    return float(pocket_price) / float(current_xchange_rate)


# column AY
def get_convert_to_usd_cogs(cogs, current_xchange_rate):
    return float(cogs) / float(current_xchange_rate)


# column AZ
def get_convert_to_usd_pocket_margin(pocket_margin, current_xchange_rate):
    return float(pocket_margin) / float(current_xchange_rate)


# column BA
def get_convert_to_usd_pocket_margin_percentage(ilc_pocket_margin, current_xchange_rate, ilc_invoice_price):
    try:
        converted_to_usd_u_c_e_r_pocket_margin_percentage = (float(ilc_pocket_margin) / float(
            current_xchange_rate)) / (float(ilc_invoice_price) / float(current_xchange_rate))
        return float(converted_to_usd_u_c_e_r_pocket_margin_percentage * 100)
    except:
        return float(0)


# =============================== FLAGS & OPPORTUNITY =========================
# column CA
def get_lower_than_floor_flag(pocket_margin_percentege, floor_pocket_margin_for_corresponding_band):
    if pocket_margin_percentege < floor_pocket_margin_for_corresponding_band:
        return 'FLAG'
    else:
        return ''


# column CB
def get_lower_than_target_floor(pocket_margin_percentege, target_pocket_margin_for_corresponding_band):
    if pocket_margin_percentege < target_pocket_margin_for_corresponding_band:
        return 'FLAG'
    else:
        return ''


# ========================== #DIV/0! =============================
# column CE
def get_opportunity_to_floor(sales_volume_mt, increase_in_invoice_price_using_floor_margin):
    if sales_volume_mt > 0:
        return float(increase_in_invoice_price_using_floor_margin) * float(sales_volume_mt)
    else:
        return float(0)


# ==========================  #DIV/0! =============================
# column CF
def get_opportunity_to_target(sales_volume_mt, increase_in_invoice_price_using_target_margin):
    if sales_volume_mt > 0:
        return float(increase_in_invoice_price_using_target_margin) * float(sales_volume_mt)
    else:
        return float(0)


def get_sum(eval_value):
    sum = 0
    for single_data in eval_value:
        if single_data is None or single_data == '':
            pass
        else:
            sum += float(single_data)
    return round(sum)


def get_year_for_dashboard(year_value):
    year = YearInfo.objects.filter(year=year_value, status =0).last()   # first searching draft

    if year is None:
        year = YearInfo.objects.filter(year=year_value, status =1).last()    # then searching active

    return year


def get_year(year):
    return YearInfo.objects.filter(year=year, status =1).last()
