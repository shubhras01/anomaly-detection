import logging, json, os
from pprint import pprint
from pint import UnitRegistry, UndefinedUnitError

from group import  PrepareData
from make_clusters import  Cluster
from cat_to_cluster_num import *

logging.basicConfig(level=logging.INFO)
OUTLIER_FRACTION = 0.01

## initialize data
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
print SCRIPT_PATH
prepareData = PrepareData(SCRIPT_PATH + "/../hackathon_price_data.csv")

## initialize unit registry
ureg = UnitRegistry()
Q_ = ureg.Quantity
ureg.define("unit = [] = unit = pc = piece = number = no = box = boxes")


def get_disjoint_units(unit_list):
    unit_to_canon_unit = {}
    for unit in unit_list:
        try:
            if unit.startswith("per "):
                ureg_unit = "".join(unit.split("per ")[1:])
            else: ureg_unit = unit
            canon_unit = ureg.parse_expression(ureg_unit)
            unit_to_canon_unit.setdefault(unit, str(canon_unit))
        except UndefinedUnitError as err:
            logging.error("unknow unit %s" % unit)
            unit_to_canon_unit[unit] = None
    return unit_to_canon_unit


def unit_to_price(cat_grouped_data):
    base_unit_data = []
    for unit in cat_grouped_data:
        data = cat_grouped_data[unit]
        u_unit = "1 per " + unit if not unit.startswith("per ") else unit
        for each in data:
            try:
                price = ureg.parse_expression(str(each['PC_ITEM_FOB_PRICE']) + u_unit)
                price = price.to_base_units()
                each["converted_price"] = price.magnitude
                each["converted_unit"] = price.units
            except UndefinedUnitError as err:
                logging.error("unknow unit %s" % err)
                each["converted_price"] = each['PC_ITEM_FOB_PRICE']
                each["converted_unit"] = u_unit
            finally:
                base_unit_data.append(each)
    base_unit_grouped = {}
    for each in base_unit_data:
        base_unit_grouped.setdefault(each["converted_unit"], [])
        base_unit_grouped[each["converted_unit"]].append(each)

    return base_unit_grouped


def get_elbow_curve():
    prepareData.get_mcat_to_specs()
    cat_list = prepareData.unit_grouped
    # cat_list = [cat_name]
    for cat_name in cat_list:
        cat_grouped_data = prepareData.get_cat(cat_name)
        logging.info("********************** \nelbow curve for %s \n********************** \n" % cat_name)
        logging.info("different units are in %s - %s" % (cat_name, ", ".join(cat_grouped_data.keys())))
        base_unit_grouped = unit_to_price(cat_grouped_data)
        logging.info("base units are %s" % ", ".join(map(repr, base_unit_grouped.keys())))
        for unit in base_unit_grouped.keys():
            logging.info("elbow curve for %s" % unit)
            data = base_unit_grouped[unit]
            if len(data) >= 3:
                price = [x['PC_ITEM_FOB_PRICE'] for x in data]
                k_cluster = Cluster(price)
                k_cluster.elbow_curve(21)
            else:
                logging.error("Not Enough data for %s - %s" % (cat_name, unit))


def get_elbow_curve_cat(cat_name):
    cat_grouped_data = prepareData.get_cat(cat_name)
    logging.info("********************** \nelbow curve for %s \n********************** \n" % cat_name)
    logging.info("different units are in %s - %s" % (cat_name, ", ".join(cat_grouped_data.keys())))
    base_unit_grouped = unit_to_price(cat_grouped_data)
    logging.info("base units are %s" % ", ".join(map(repr, base_unit_grouped.keys())))
    plot_url = None
    for unit in base_unit_grouped.keys():
        logging.info("elbow curve for %s" % unit)
        data = base_unit_grouped[unit]
        if len(data) >= 3:
            price = [x['PC_ITEM_FOB_PRICE'] for x in data]
            k_cluster = Cluster(price)
            plot_url = k_cluster.elbow_curve(21)
        else:
            logging.error("Not Enough data for %s - %s" % (cat_name, unit))

    return plot_url


def get_category_clusters(cat_name):
    cat_grouped_data = prepareData.get_cat(cat_name)
    # logging.info("********************** \nelbow curve for %s \n********************** \n" % cat_name)
    logging.info("different units are in %s - %s" % (cat_name, ", ".join(cat_grouped_data.keys())))
    base_unit_grouped = unit_to_price(cat_grouped_data)
    logging.info("base units are %s" % ", ".join(map(repr, base_unit_grouped.keys())))
    resp = {}
    for unit in base_unit_grouped:
        logging.info("*********************************")
        logging.info("calculating range for %s - %s" % (cat_name, repr(unit)))
        logging.info("*********************************")
        unit_str = str(unit)
        data = base_unit_grouped[unit]
        resp[unit_str] = {"data_len": len(data)}
        if len(data) <= 3:
            logging.error("Not enough data in category - %s for unit - %s.\n Length of data - %s. It should be > 3"
                          % (cat_name, repr(unit), str(len(data))))
            resp[unit_str].update({"error": "Not enough data in category - %s for unit - %s."
                                            "Length of data - %s. It should be > 3"
                                            % (cat_name, repr(unit), str(len(data)))})
        else:
            price = [x['PC_ITEM_FOB_PRICE'] for x in data]
            k_cluster = Cluster(price)
            try:
                num_cluster = cat_to_num_cluster[cat_name][str(unit)]
            except KeyError as err:
                logging.error("this category cluster in not calculated yet through elbow-curve.")
                resp[unit_str].update({"error": "this category cluster in not calculated yet through elbow-curve."})
                return resp
            kmeans = k_cluster.apply_kmeans(num_cluster)
            threshold = k_cluster.get_distance_threshold(kmeans, OUTLIER_FRACTION)
            outliers = k_cluster.get_outliers()
            price_range = k_cluster.remove_outliers()
            logging.info("price range for %s - %s  = %s" % (cat_name, unit, " - ".join(map(str, price_range))))
            resp[unit_str].update({"price_range": " - ".join(map(str, price_range)),
                                    "anomalies": ", ".join(map(str, outliers))})

    return resp


# get_elbow_curve_cat("ladies palazzo")
# resp = get_category_clusters("ladies palazzo")
# pprint(resp)

