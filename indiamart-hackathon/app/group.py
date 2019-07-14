import pandas as pd
import json, logging
from pprint import pprint

logging.basicConfig(level=logging.INFO)


class PrepareData:
    def __init__(self, filePath):
        df = pd.read_csv(filepath_or_buffer=filePath)
        logging.info(df.head(n=3))
        df["type-value"] = df.apply(lambda row: row['FK_IM_SPEC_MASTER_DESC'] + "_" + str(row["FK_IM_SPEC_OPTIONS_DESC"]), axis=1)
        df = df.drop(['FK_IM_SPEC_MASTER_DESC', 'FK_IM_SPEC_OPTIONS_DESC'], axis=1)
        logging.info(df.head(n=10))
        self.dfj = json.loads(df.to_json(orient="records"))
        self.unit_grouped = None
        logging.info(len(self.dfj))

    def get_id_to_specs(self):
        id_to_specs = {}
        for x in self.dfj:
            xid = x["PC_ITEM_ID"]
            id_to_specs.setdefault(xid, {})
            type_value = x.pop('type-value')
            try:
                xid_type, xid_val = "_".join(type_value.split("_")[:-1]), type_value.split("_")[-1]
                xid_type = xid_type.lower().strip()
                xid_val = xid_val.lower().strip()
                id_to_specs[xid].setdefault(xid_type, [])
                id_to_specs[xid][xid_type].append(xid_val)
            except Exception as e:
                pprint(type_value)
            for each in x.keys():
                id_to_specs[xid].setdefault(each, [])
                id_to_specs[xid][each].append(x[each])
        return id_to_specs

    def get_mcat_to_specs(self):
        id_to_specs = self.get_id_to_specs()
        for x in id_to_specs:
            for each in id_to_specs[x].keys():
                id_to_specs[x][each] = list(set(id_to_specs[x][each]))
        provided_keys = ['Mcat Name', 'PC_ITEM_FOB_PRICE', 'PC_ITEM_ID', 'PC_ITEM_MOQ_UNIT_TYPE', 'PC_ITEM_NAME', 'Subcat name']
        for each in id_to_specs:
            x = id_to_specs[each]
            for key in provided_keys:
                id_to_specs[each][key] = id_to_specs[each][key][0]

        mcat_to_specs = {}
        for each in id_to_specs:
            x = id_to_specs[each]
            mcat = x['Mcat Name'].lower().strip()
            mcat_to_specs.setdefault(mcat, [])
            mcat_to_specs[mcat].append(x)

        unit_grouped = {}
        for each in mcat_to_specs:
            unit_grouped.setdefault(each, {})
            tmp = {}
            for x in mcat_to_specs[each]:
                item_unit = x['PC_ITEM_MOQ_UNIT_TYPE'].lower().strip()
                tmp.setdefault(item_unit, [])
                tmp[item_unit].append(x)
            unit_grouped[each] = tmp
        self.unit_grouped = unit_grouped

    def get_cat(self, cat):
        if not self.unit_grouped:
            self.get_mcat_to_specs()
        return self.unit_grouped[cat]

    def get_gt5_cat(self):
        if not self.unit_grouped:
            self.get_mcat_to_specs()
        unit_grouped = self.unit_grouped
        for each in unit_grouped:
            for unit in unit_grouped[each]:
                max_mcat.append([each, unit, len(unit_grouped[each][unit])])

        max_mcat.sort(key=lambda x: x[2], reverse=True)
        gt_5 = [x for x in max_mcat if x[2] >= 5]
        return gt_5


if __name__ == "__main__":
    m = -1
    max_l = -1
    max_mcat = []
    max_unit = ""
    ob = PrepareData("../hackathon_price_data.csv")
    ob.get_mcat_to_specs()
    unit_grouped = ob.unit_grouped
    for each in unit_grouped:
        for unit in unit_grouped[each]:
            max_mcat.append([each, unit, len(unit_grouped[each][unit])])

    max_mcat.sort(key=lambda x: x[2], reverse=True)
    gt_5 = [x for x in max_mcat if x[2] >= 5]


    test_set = unit_grouped['ladies palazzo'].keys()



