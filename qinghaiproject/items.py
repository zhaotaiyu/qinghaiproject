# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class QinghaiprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class CompanyInfomortation(scrapy.Item):
    collection = "companyinformation"
    company_id = scrapy.Field()
    province_company_id = scrapy.Field()
    social_credit_code = scrapy.Field()
    company_name = scrapy.Field()
    url = scrapy.Field()
    ceoname = scrapy.Field()
    ctoname = scrapy.Field()
    regis_address = scrapy.Field()
    leal_person = scrapy.Field()
    business_address = scrapy.Field()
    regis_type = scrapy.Field()
    registered_capital = scrapy.Field()
    build_date = scrapy.Field()
    contact_person = scrapy.Field()
    leal_person_title = scrapy.Field()
    postalcode = scrapy.Field()
    contact_phone = scrapy.Field()
    contact_address = scrapy.Field()
    leal_person_duty = scrapy.Field()
    fax = scrapy.Field()
    tel = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    contact_tel = scrapy.Field()
    enginer = scrapy.Field()
    department = scrapy.Field()
    danweitype = scrapy.Field()
    area_code = scrapy.Field()
    source = scrapy.Field()
    status = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
class CompanyaptitudeItem(scrapy.Item):
    collection = "companyaptitude"
    province_company_id = scrapy.Field()
    aptitude_id = scrapy.Field()
    aptitude_organ = scrapy.Field()
    aptitude_startime = scrapy.Field()
    aptitude_endtime = scrapy.Field()
    aptitude_name = scrapy.Field()
    level = scrapy.Field()
    check_time = scrapy.Field()
    aptitude_small = scrapy.Field()
    aptitude_credit_level = scrapy.Field()
    aptitude_major = scrapy.Field()
    aptitude_large = scrapy.Field()
    aptitude_ser = scrapy.Field()
    approval_number = scrapy.Field()
    aptitude_usefultime = scrapy.Field()
    aptitude_type = scrapy.Field()
    source = scrapy.Field()
    status = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
    company_id = scrapy.Field()
    url = scrapy.Field()
    company_name = scrapy.Field()
class BeianItem(scrapy.Item):
    collection = "beianinformation"
    company_name = scrapy.Field()
    social_credit_code = scrapy.Field()
    record_province = scrapy.Field()
    create_time = scrapy.Field()
    modification_time = scrapy.Field()
    is_delete = scrapy.Field()
    status = scrapy.Field()