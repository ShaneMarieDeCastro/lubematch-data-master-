from email.policy import default
import sqlite3
from collections import defaultdict
import pandas as pd
import json
import os

from cli.sql.commands import dvr

view_prod_sku = """
CREATE TEMP VIEW IF NOT EXISTS prod_sku
AS
    SELECT
        ps.PRODUCT_ID,
        psc.COUNTRY_CODE,
        skucountrystat.STATUS_SUB_GROUP_NAME as SKU_COUNTRY_STATUS,
        skustat.STATUS_SUB_GROUP_NAME as SKU_STATUS,
        pack.PACK_CODE,
        pack.PACK_NAME,
        psize.PACK_SIZE_NAME,
        puom.PACK_UOM_NAME,
        ps.PRODUCT_SKU_GSAP_CODE
    FROM
        PRODUCT_SKU as ps
    INNER JOIN PROD_SKU_COUNTRY as psc ON ps.PRODUCT_SKU_ID=psc.PRODUCT_SKU_ID
    LEFT JOIN STAT_HIER as skucountrystat ON psc.STATUS_SUB_GROUP_ID=skucountrystat.STATUS_SUB_GROUP_ID
    LEFT JOIN STAT_HIER as skustat ON ps.STATUS_SUB_GROUP_ID=skustat.STATUS_SUB_GROUP_ID
    LEFT JOIN PACK as pack ON ps.PACK_ID=pack.PACK_ID
    LEFT JOIN PACK_SIZE as psize ON pack.PACK_SIZE_ID=psize.PACK_SIZE_ID
    LEFT JOIN PACK_UOM as puom ON psize.PACK_UOM_ID=puom.PACK_UOM_ID
    WHERE skucountrystat.EXP_EPC='Y';
"""

view_prod_country = """
CREATE TEMP VIEW IF NOT EXISTS prod_country
AS
    SELECT
        sp.PRODUCT_ID,
        spc.COUNTRY_CODE,
        sp.GLOBALPRODUCTCODE,
        sp.PRODUCTDESCRIPTION,
        sp.EXTERNALNAME,
        sp.PRODUCT_ID,
        spc.SALEABLE_PRODUCT_COUNTRY_ID,
        stat.STATUS_SUB_GROUP_NAME as SPC_STATUS,
        spstat.STATUS_SUB_GROUP_NAME as SP_STATUS,
        mhier.PROD_MARKET_NAME,
        pclass.PROD_GROUP_NAME,
        pclass.PROD_SUB_GROUP_NAME,
        pclass.PROD_CLASSFTN_ID,
        phier.PROD_FAMILY_NAME,
        g.GRADE_NAME,
        gn.GRADETYPE_PRINTABLE_NAME as GRADETYPE_NAME,
        bfg.BASE_FLUID_PRINTABLE_NAME as BASE_FLUID_GROUP_NAME,
        bfsg.BASE_FLUID_PRINTABLE_NAME as BASE_FLUID_SUB_GROUP_NAME,
        sl.MATERIAL_STANDARD_NAME,
        sl.MATERIAL_STANDARD_ID,
        cn.CARBON_NEUTRAL,
        sp.PROD_CLASSFTN_ID,
        psg.parentCategory as PARENT_CATEGORY,
        pks.URL,
        dvr.DVR_ID,
        ec.ECOMMERCE_LINK
    FROM
        SALEABLEPRODUCT as sp
    INNER JOIN SALEPRODCOUNTRY as spc ON sp.PRODUCT_ID=spc.PRODUCT_ID
    LEFT JOIN PACKSHOTS as pks on pks.COUNTRY_CODE=spc.COUNTRY_CODE and pks.PRODUCT_ID=spc.PRODUCT_ID
    LEFT JOIN PRODUCT_SUB_GROUP as psg on psg.PROD_CLASSFTN_ID = sp.PROD_CLASSFTN_ID and psg.COUNTRY_CODE = spc.COUNTRY_CODE
    LEFT JOIN DVR as dvr on dvr.GLOBALPRODUCTCODE = sp.GLOBALPRODUCTCODE
    LEFT JOIN ECOMMERCE_LINK as ec on ec.GLOBALPRODUCTCODE = sp.GLOBALPRODUCTCODE AND spc.COUNTRY_CODE = ec.COUNTRY_CODE
    LEFT JOIN STAT_HIER as stat ON spc.STATUS_SUB_GROUP_ID=stat.STATUS_SUB_GROUP_ID
    LEFT JOIN STAT_HIER as spstat ON sp.STATUS_SUB_GROUP_ID=spstat.STATUS_SUB_GROUP_ID
    LEFT JOIN PROD_MARKET_HIER as mhier ON sp.PROD_MARKET_TYPE_ID=mhier.PROD_MARKET_TYPE_ID
    LEFT JOIN PROD_CLASSFTN as pclass ON sp.PROD_CLASSFTN_ID=pclass.PROD_CLASSFTN_ID
    LEFT JOIN PROD_NAME_HIER as phier ON sp.PROD_NAME_ID=phier.PROD_NAME_HIER_ID
    LEFT JOIN GRADE_HIER as g ON sp.GRADE_ID=g.GRADE_ID
    LEFT JOIN GRADE_NAME as gn on g.GRADETYPE_ID=gn.GRADETYPE_ID
    LEFT JOIN BASE_OIL_SUB_GROUP as bfsg ON sp.BASE_FLUID_SUB_GROUP_ID=bfsg.BASE_FLUID_SUB_GROUP_ID
    LEFT JOIN BASE_OIL_GROUP as bfg ON bfsg.BASE_FLUID_GROUP_ID=bfg.BASE_FLUID_GROUP_ID
    LEFT JOIN CARBON_NEUTRAL as cn ON spc.PRODUCT_ID = cn.PRODUCT_ID AND spc.COUNTRY_CODE = cn.COUNTRY_CODE
    LEFT JOIN SPECS_PRODUCT as scp on scp.PRODUCT_ID = sp.PRODUCT_ID
    LEFT JOIN SPECS_LOOKUP as sl on sl.MATERIAL_STANDARD_ID = scp.MATERIAL_STANDARD_ID

    
    WHERE stat.EXP_EPC='Y' AND spstat.EXP_EPC='Y';
"""

view_most_recent_local_docs = """
CREATE TEMP VIEW IF NOT EXISTS most_recent_local_docs
AS
	SELECT
		*
	FROM (
		SELECT
            spcd.*,
            ROW_NUMBER() OVER (PARTITION BY SALEABLE_PRODUCT_COUNTRY_ID, LANGUAGE_CODE, DOCUMENTTYPE_CODE ORDER BY LATEST_CHANGE_DATE DESC) AS recency
		FROM SP_COUNTRY_DOC AS spcd
 		WHERE EXTERNAL_URL IS NOT NULL
	) as recent_docs
	LEFT JOIN STAT_HIER as stat ON recent_docs.STATUS_SUB_GROUP_ID=stat.STATUS_SUB_GROUP_ID
WHERE EXP_EPC='Y' AND recency = 1;
"""

view_most_recent_global_docs = """
CREATE TEMP VIEW IF NOT EXISTS most_recent_global_docs
AS
	SELECT
		*
	FROM (
		SELECT
			d.*,
			ROW_NUMBER() OVER (PARTITION BY PRODUCT_ID, DOCUMENTTYPE_CODE ORDER BY LATEST_CHANGE_DATE DESC) AS recency
		FROM DOCUMENT AS d
 		WHERE EXTERNAL_URL IS NOT NULL
	) as recent_docs
	LEFT JOIN STAT_HIER as stat ON recent_docs.STATUS_SUB_GROUP_ID=stat.STATUS_SUB_GROUP_ID
WHERE EXP_EPC='Y' AND recency = 1;
"""

view_valid_prod_country = """
CREATE TEMP VIEW IF NOT EXISTS view_valid_prod_country
AS
    SELECT
        ps.*,
        pc.*,
        local_docs.TITLE as local_docs_TITLE,
        local_docs.EXTERNAL_URL as local_docs_EXTERNAL_URL,
        local_docs.DOCUMENTTYPE_CODE as local_docs_DOCUMENTTYPE_CODE,
        local_docs.LANGUAGE_CODE as local_docs_LANGUAGE_CODE,
        global_docs.TITLE as global_docs_TITLE,
        global_docs.EXTERNAL_URL as global_docs_EXTERNAL_URL,
        global_docs.DOCUMENTTYPE_CODE as global_docs_DOCUMENTTYPE_CODE,
        global_docs.LANGUAGE_CODE as global_docs_LANGUAGE_CODE
    FROM
        prod_sku as ps
    INNER JOIN prod_country as pc ON ps.PRODUCT_ID=pc.PRODUCT_ID AND PS.COUNTRY_CODE=pc.COUNTRY_CODE
    LEFT JOIN most_recent_local_docs as local_docs ON pc.SALEABLE_PRODUCT_COUNTRY_ID=local_docs.SALEABLE_PRODUCT_COUNTRY_ID
    LEFT JOIN most_recent_global_docs as global_docs ON pc.PRODUCT_ID=global_docs.PRODUCT_ID
"""

prod_sku_stat = ['Active - Planned Withdrawal',
                 'Active & GSAP',
                 'Active & Non GSAP',
                 'Active & GSAP Automate']
sp_stat = ['Active - Generic',
           'Active - Global Restriction',
           'To be deleted']
spc_stat = ['Available - Generic',
            'Available - Planned withdrawal',
            'Available - Under Review']
sku_c_stat = ['Available - Generic',
              'Available - Planned Withdrawal']

tdg_country_to_langauge = {
    "en-AU": ["en", "en-AU"],
    "en-CA": ["en", "en-CA"],
    "fr-CA": ["en", "fr-CA"],
    "en-GB": ["en", "en-GB"],
    "en-IN": ["en", "en-IN"],
    "en-MY": ["en", "en-MY"],
    "en-SG": ["en", "en-SG"],
    "en-US": ["en", "en-US"],
    "zh-CN": ["en", "zh-CN", ],
    "id-ID": ["en", "id-ID"],
    "de-DE": ["en", "de-DE", "de"],
    "ru-RU": ["en", "ru-RU", "ru"],
    "en-PH": ["en"],
    "en-IE": ["en"],
    "en-NZ": ["en"],
    "fr-FR": ["en", "fr-FR", "fr"],
    "nl-NL": ["en", "nl-NL", "nl"],
    "pl-PL": ["en", "pl-PL", "pl"],
    "it-IT": ["en", "it-IT", "it"],
    "es-ES": ["en", "es-ES", "es"],
    "tr-TR": ["en", "tr-TR", "tr"]
}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ProductsPacksDocs():

    def __init__(self, path, sub_groups, marketing, phys, specs, packs, locale, apps, dvrs):
        self.path = path
        self.sub_groups = load_sub_group(sub_groups)
        self.applications = load_applications(apps)
        self.specs = load_specs(specs)
        self.marketing = load_marketing(marketing)
        self.country = locale.split("-")[1]
        self.phys = load_phys(phys)
        self.packs = load_packs(packs)
        self.dvrs = load_dvr(dvrs)
        self.locale = locale
        self.conn = None
        self.__connect()

    def __connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = dict_factory

    def lube_products(self):
        """
        Generate all products with pack sizes per country
        """
        c = self.conn.cursor()
        c.execute(view_prod_sku)
        c.execute(view_prod_country)
        c.execute(view_most_recent_local_docs)
        c.execute(view_most_recent_global_docs)
        c.execute(view_valid_prod_country)

        query = """
        SELECT DISTINCT
            PRODUCT_ID,
            COUNTRY_CODE,
            EXTERNALNAME,
            GLOBALPRODUCTCODE,
            PACK_CODE,
            PACK_NAME,
            PACK_SIZE_NAME,
            PACK_UOM_NAME,
            PRODUCT_SKU_GSAP_CODE,
            PRODUCTDESCRIPTION,
            PROD_FAMILY_NAME,
            PROD_GROUP_NAME,
            PROD_MARKET_NAME,
            PROD_SUB_GROUP_NAME,
            PROD_CLASSFTN_ID,
            PARENT_CATEGORY,
            SKU_COUNTRY_STATUS,
            SKU_STATUS,
            SPC_STATUS,
            SP_STATUS,
            GRADE_NAME,
            GRADETYPE_NAME,
            MATERIAL_STANDARD_NAME,
            MATERIAL_STANDARD_ID,
            BASE_FLUID_GROUP_NAME,
            BASE_FLUID_SUB_GROUP_NAME,
            CARBON_NEUTRAL,
            ECOMMERCE_LINK,
            URL,
            DVR_ID,
            local_docs_EXTERNAL_URL as local_doc,
            local_docs_DOCUMENTTYPE_CODE as local_doc_type,
            local_docs_TITLE as local_doc_title,
            local_docs_LANGUAGE_CODE as local_doc_language,
            global_docs_EXTERNAL_URL as global_doc,
            global_docs_DOCUMENTTYPE_CODE as global_doc_type,
            global_docs_TITLE as global_doc_title,
            global_docs_LANGUAGE_CODE as global_doc_language
        FROM view_valid_prod_country
        WHERE COUNTRY_CODE='{country}'
        """.format(country=self.country)

        ps = defaultdict()
        activeProducts = defaultdict()
        for row in c.execute(query):
            gpc = row['GLOBALPRODUCTCODE']
            if gpc not in ps:
                ps[gpc] = {
                    'id': gpc,
                    'countryCode': row['COUNTRY_CODE'],
                    'locale': self.locale,
                    'name': row['EXTERNALNAME'],
                    'description': row['PRODUCTDESCRIPTION'],
                    'family': row['PROD_FAMILY_NAME'],
                    'parentCategory': row['PARENT_CATEGORY'],
                    'category': self.get_sub_group_names(row),
                    'applicationKeys': self.get_applications(row).split(','),
                    'position': row['PROD_MARKET_NAME'],
                    'viscosityGrade': row['GRADE_NAME'],
                    'viscosityType': row['GRADETYPE_NAME'],
                    'fluidType': row['BASE_FLUID_GROUP_NAME'],
                    'fluidSubType': row['BASE_FLUID_SUB_GROUP_NAME'],
                    'globalDocs': [],
                    'localDocs': [],
                    'packs': [],
                    'globalSpecs': [],
                    'localSpecs': [],
                    'marketing': '',
                    'physicalCharacteristics': [],
                    'active': False,
                    'carbonNeutral': row['CARBON_NEUTRAL'],
                    'packShot': row['URL'],
                    'valueRecord': [],
                    'commerce': row['ECOMMERCE_LINK']
                }

            #  Add specs
            material_standard_id = row["MATERIAL_STANDARD_ID"]
            if material_standard_id is not None:
                ps[gpc]['globalSpecs'].append(
                    self.specs[int(material_standard_id)]
                )
                ps[gpc]['globalSpecs'] = ps[gpc]['globalSpecs']


            # Add DVRs
            dvr_id = row["DVR_ID"]
            if dvr_id is not None:
                if self.dvrs[dvr_id] not in ps[gpc]['valueRecord']:
                    ps[gpc]['valueRecord'].append(
                        self.dvrs[dvr_id]
                    )


            #  Add Physical Characterstics
            for lang, value in self.phys[gpc].items():
                if lang in tdg_country_to_langauge[self.locale]:
                    ps[gpc]['physicalCharacteristics'] = value

            for mt in self.get_tdg_market_text(gpc):
                ps[gpc]['marketing'] = mt['TEXT']

            for lang, value in self.marketing[gpc].items():
                if lang in tdg_country_to_langauge[self.locale]:
                    ps[gpc]['marketing'] = value

            # Calculate active country
            sku_status = row['SKU_STATUS']
            sp_status = row['SP_STATUS']
            spc_status = row['SPC_STATUS']
            sku_c_status = row['SKU_COUNTRY_STATUS']
            active = False

            if row['PRODUCT_SKU_GSAP_CODE'] not in ps[gpc]['packs']:
                pack_code = row['PACK_CODE']
                pack_gsap = row['PRODUCT_SKU_GSAP_CODE']
                pack_id = self.locale.replace('-', '_')

                if pack_code is not None:
                    pack_id = pack_id + pack_code

                
                material_code = self.get_material(
                    gpc, self.country, row['PRODUCT_SKU_GSAP_CODE'])
                margin = self.get_margin(
                    gpc, self.country, row['PRODUCT_SKU_GSAP_CODE'])
                pack = self.packs[pack_id]
                if pack is not None:
                    if material_code is not None and len(material_code) > 0:
                        active = True
                        ps[gpc]['packs'].append({
                            'code': pack_gsap,
                            'name': pack.get('pack_name_localised', ''),
                            'size': pack.get('printable_pack_size', ''),
                            'uom': pack.get('printable_local_unit', ''),
                            'pack': pack.get('printable_local_pack', ''),
                            'materialCode': material_code,
                            'margin': margin,
                            'packShot': ''
                        })
                else:
                    if material_code is not None and len(material_code) > 0:
                        active = True
                        ps[gpc]['packs'].append({
                            'code': pack_gsap,
                            'name': row['PACK_NAME'],
                            'size': row['PACK_SIZE_NAME'],
                            'uom': row['PACK_UOM_NAME'],
                            'materialCode': material_code,
                            'margin': margin,
                            'packShot': ''
                        })

            if sku_status in prod_sku_stat and sp_status in sp_stat and spc_status in spc_stat and sku_c_status in sku_c_stat and active is True:
                ps[gpc]['active'] = True

            if row['global_doc'] is not None:
                ps[gpc]['globalDocs'].append({
                    'href': row['global_doc'],
                    'type': row['global_doc_type'],
                    'name': row['global_doc_title'],
                    'language': row['global_doc_language'],
                })

            if row['local_doc'] is not None:
                ps[gpc]['localDocs'].append({
                    'href': row['local_doc'],
                    'type': row['local_doc_type'],
                    'name': row['local_doc_title'],
                    'language': row['local_doc_language'],
                })

        for r in ps.values():
            r['globalSpecs'] = [dict(t) for t in {tuple(
                d.items()) for d in r['globalSpecs']}]

            r['globalDocs'] = [dict(t) for t in {tuple(
                d.items()) for d in r['globalDocs']}]

            r['localDocs'] = [dict(t) for t in {tuple(
                d.items()) for d in r['localDocs']}]

            r['packs'] = [dict(t) for t in {tuple(
                d.items()) for d in r['packs']}]

            r['valueRecord'] = [dict(t) for t in {tuple(
                d.items()) for d in r['valueRecord']}]

        for key, product in ps.items():
            activeProducts[key] = product

        return activeProducts

    def get_sub_group_names(self, row):
        trans = row['PROD_SUB_GROUP_NAME']
        id = int(row['PROD_CLASSFTN_ID'])
        for langauge, value in self.sub_groups[id].items():
            if langauge in tdg_country_to_langauge[self.locale]:
                trans = value
        return trans

    def get_applications(self, row):
        prod = ""
        id = int(row['PRODUCT_ID'])
        for app_key in self.applications[id].items():
            prod = app_key[1]
        return prod

    def get_specs(self, code):
        c = self.conn.cursor()
        query = '''
        SELECT MATERIAL_STANDARD_NAME, sl.MATERIAL_STANDARD_ID
        FROM SALEABLEPRODUCT slp
        LEFT JOIN SPECS_PRODUCT as sp on sp.PRODUCT_ID = slp.PRODUCT_ID
        LEFT JOIN SPECS_LOOKUP as sl on sl.MATERIAL_STANDARD_ID = sp.MATERIAL_STANDARD_ID
        WHERE slp.GLOBALPRODUCTCODE = '{}'
        '''.format(code)
        for row in c.execute(query):
            yield row

    def get_tdg_market_text(self, code):
        c = self.conn.cursor()
        query = '''
        SELECT DISTINCT
            LANGUAGE, TEXT
        FROM TDG_MARKETING_TEXT AS MT
        WHERE GLOBALPRODUCTCODE = '{}' AND LANGUAGE IN ({})
        '''.format(code, ', '.join('"' + item + '"' for item in tdg_country_to_langauge[self.locale]))
        for row in c.execute(query):
            yield row

    def get_tdg_descriptions(self, code):
        c = self.conn.cursor()
        query = '''
        SELECT DISTINCT
            LANGUAGE, TEXT
        FROM TDG_DESCRIPTIONS AS D
        WHERE GLOBALPRODUCTCODE = '{}' AND LANGUAGE IN ({})
        '''.format(code, ', '.join('"' + item + '"' for item in tdg_country_to_langauge[self.locale]))
        for row in c.execute(query):
            yield row

    def get_physical(self, code):
        c = self.conn.cursor()
        query = '''
        SELECT DISTINCT
            PROPERTY AS property, METHOD as method, UNITOFMEASURE as uom, UNITS as units, NAME as name, VALUE
        FROM TDG_PHYS_CHAR AS PC
        WHERE GLOBALPRODUCTCODE = '{}'
        '''.format(code)
        for row in c.execute(query):
            yield row

    def get_material(self, code, country, gsap_code):
        c = self.conn.cursor()
        query = '''
        SELECT DISTINCT
            GSAP_MATERIAL_CODE
        FROM MATERIAL_CODES
        WHERE GLOBALPRODUCTCODE = '{}'
            AND COUNTRY_CODE = '{}'
            AND PRODUCT_SKU_GSAP_CODE = '{}'
        '''.format(code, country, gsap_code)
        row = c.execute(query).fetchone()
        if row is not None:
            return row['GSAP_MATERIAL_CODE']

        return None

    def get_margin(self, code, country, gsap_code):
        c = self.conn.cursor()
        query = '''
        SELECT 
            MARGIN
        FROM MATERIAL_CODES
        WHERE GLOBALPRODUCTCODE = '{}'
            AND COUNTRY_CODE = '{}'
            AND PRODUCT_SKU_GSAP_CODE = '{}'
        '''.format(code, country, gsap_code)
        row = c.execute(query).fetchone()
        if row is not None:
            return row['MARGIN']

        return None

    def close(self):
        self.conn.close()


class ProductsPerCountry():

    def __init__(self, path, country):
        self.path = path
        self.country = country
        self.conn = None
        self.__connect()

    def __connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = dict_factory

    def lube_products(self):
        """
        Generate all products with pack sizes per country
        """
        c = self.conn.cursor()
        query = """
        SELECT DISTINCT
            sp.EXTERNALNAME,
            spc.COUNTRY_CODE,
            grade.GRADE_NAME,
            grade.GRADETYPE_NAME,
            pc.PROD_SUB_GROUP_NAME,
            pmh.PROD_MARKET_NAME,
            pnh.PROD_FAMILY_NAME
        FROM SALEPRODCOUNTRY AS spc
        LEFT JOIN SALEABLEPRODUCT AS sp ON spc.PRODUCT_ID=sp.PRODUCT_ID
        LEFT JOIN STAT_HIER AS spcstat ON spc.STATUS_SUB_GROUP_ID=spcstat.STATUS_SUB_GROUP_ID
        LEFT JOIN STAT_HIER AS spstat ON sp.STATUS_SUB_GROUP_ID=spstat.STATUS_SUB_GROUP_ID
        LEFT JOIN GRADE_HIER AS grade ON sp.GRADE_ID=grade.GRADE_ID
        LEFT JOIN PROD_CLASSFTN AS pc ON sp.PROD_CLASSFTN_ID=pc.PROD_CLASSFTN_ID
        LEFT JOIN PROD_MARKET_HIER AS pmh ON sp.PROD_MARKET_TYPE_ID=pmh.PROD_MARKET_TYPE_ID
        LEFT JOIN PROD_NAME_HIER AS pnh ON sp.PROD_NAME_ID=pnh.PROD_NAME_HIER_ID
        WHERE spcstat.EXP_EPC='Y' AND spstat.EXP_EPC='Y' AND spc.COUNTRY_CODE='{country}'
        """.format(country=self.country)

        df = pd.read_sql_query(query, self.conn)
        print(df)

    def close(self):
        self.conn.close()


def load_sub_group(path):
    i18n = defaultdict(dict)
    df = pd.read_excel(path, keep_default_na=False)
    for _index, row in df.iterrows():
        if row['Language'] not in ['SH', 'ATT']:
            if row['Value'] != '':
                i18n[row['PROD_CLASSFTN_ID']][row['Language']] = row['Value']
    return i18n


def load_applications(path):
    apps = defaultdict(dict)
    for index, row in pd.read_excel(path, keep_default_na=False).iterrows():
        apps[row['PRODUCT_ID']][row['PROD_CODE']] = row['app_key']
    return apps


def load_packs(path):
    packs = defaultdict(dict)
    for index, pack in pd.read_excel(path, keep_default_na=False).iterrows():
        pack_id = pack.locale + pack.pack_code
        if packs[pack_id] is None:
            packs[pack_id] = defaultdict(dict)
        packs[pack_id] = pack
    return packs


def load_specs(path):
    specs = defaultdict(dict)
    specs_excel_data = pd.read_excel(path, keep_default_na=False)
    for _, row in specs_excel_data.iterrows():
        spec_entry = defaultdict(dict)
        material_id = row['MATERIAL_STANDARD_ID']
        specs[material_id] = spec_entry
        spec_entry['name'] = row.MATERIAL_STANDARD_NAME
        spec_entry['organisation'] = row.materialStandardParent
        spec_entry['spec'] = row.materialStandardChild
    return specs

def load_dvr(path):
    dvrs = defaultdict(dict)
    dvr_excel_data = pd.read_excel(path, keep_default_na=False)
    for _, row in dvr_excel_data.iterrows():
        dvr_entry = defaultdict(dict)
        dvr_id = row['DVR_ID']
        dvrs[dvr_id] = dvr_entry
        dvr_entry['href'] = row.DVR_URL
        dvr_entry['family'] = row.PROD_FAMILY_NAME
        dvr_entry['savings'] = row.DVR_SAVINGS_USD
        dvr_entry['title'] = row.DVR_URL_NAME


    return dvrs


def load_marketing(path):
    i18n = defaultdict(dict)
    df = pd.read_excel(path,
                       keep_default_na=False).set_index('SP Code')
    for index, row in df.iterrows():
        i18n[index][row['Language']] = row['Value']
    return i18n


def load_phys(path):
    i18n = defaultdict(lambda: defaultdict(list))
    df = pd.read_excel(path,
                       keep_default_na=False).set_index('SP Code')
    for index, row in df.iterrows():
        i18n[index][row['Language']].append({
            'property': row['Property'],
            'method': row['Method'],
            'uom': row['UnitOfMeasurement'],
            'units': row['Units'],
            'value': row['Value'],
        })
    return i18n
