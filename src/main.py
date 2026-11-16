import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
import logging
import warnings
import math
import os

# مسیرهای ورودی و خروجی (نسبت به ریشه پروژه؛ اسکریپت از ریشه اجرا شود)
INPUT_REGIONS = "data/mahale.shp"
OUTPUT_DIR = "results"
OUTPUT_NAME = "tehran_15min_justice_scores"

# غیرفعال کردن هشدارهای هندسی و CRS
warnings.filterwarnings("ignore")

logging.basicConfig(
    filename="15min_city_tehran.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =====================================================================
# ۱. پیکربندی وزن‌ها و سرانه‌های ایده‌آل برای ۲۷ متغیر پرسشنامه
# =====================================================================
# این دیکشنری باید با خروجی نهایی مدل MCDA شما (AHP * Likert) جایگزین شود.
# مجموع این وزن‌ها باید ۱.۰ باشد.
global_weights = {
    "q1_doctor": 0.04, "q2_pharmacy": 0.04, "q3_clinic": 0.04, "q4_hospital": 0.05,
    "q5_kindergarten": 0.03, "q6_school_edu": 0.05, "q8_university": 0.02,
    "q9_local_grocer": 0.05, "q10_supermarket": 0.05, "q11_appliance": 0.03,
    "q12_local_market": 0.04, "q13_mall": 0.03, "q14_park": 0.06, "q15_sports": 0.04,
    "q16_culture": 0.03, "q17_public_space": 0.04, "q18_bus_stop": 0.05,
    "q19_taxi": 0.03, "q20_subway": 0.06, "q21_terminal": 0.02, "q22_main_street": 0.04,
    "q23_post_office": 0.02, "q24_police_fire": 0.04, "q25_worship": 0.03,
    "q26_local_gov": 0.02, "q27_workplace": 0.05
    # (توجه: سوالات 6 و 7 مقاطع تحصیلی در OSM معمولاً با یک تگ school شناخته می‌شوند، لذا در q6_school_edu ادغام شدند)
}

# مقادیر سرانه ایده‌آل (Capping Thresholds) برای جلوگیری از امتیاز بی‌نهایت.
# مثال: 0.003 برای بیمارستان یعنی ۳ تخت به ازای هر ۱۰۰۰ نفر ایده‌آل است.
# برای مواردی که با تعداد (Count) سنجیده می‌شوند، نسبت ۱ مرکز به ازای جمعیت نوشته شده است.
ideal_ratios = {
    "q1_doctor": 1/2000, "q2_pharmacy": 1/3000, "q3_clinic": 1/5000, "q4_hospital": 0.003,
    "q5_kindergarten": 1/1500, "q6_school_edu": 2.0, "q8_university": 1/20000,
    "q9_local_grocer": 1/1000, "q10_supermarket": 1/2000, "q11_appliance": 1/3000,
    "q12_local_market": 1/5000, "q13_mall": 1/15000, "q14_park": 9.0, "q15_sports": 1.5,
    "q16_culture": 1/10000, "q17_public_space": 1/4000, "q18_bus_stop": 1/1000,
    "q19_taxi": 1/3000, "q20_subway": 1/15000, "q21_terminal": 1/50000, "q22_main_street": 1/500,
    "q23_post_office": 1/10000, "q24_police_fire": 1/10000, "q25_worship": 1/3000,
    "q26_local_gov": 1/15000, "q27_workplace": 1/500
}

# کاربری‌هایی که ظرفیتشان «مساحت (m²)» است؛ سرانه ایده‌آل آن‌ها در ideal_ratios
# باید برحسب «متر مربع به ازای هر نفر» باشد. بقیه دسته‌ها شمارشی (۱ مرکز به ازای جمعیت) هستند.
# (مهدکودک، دانشگاه و محل کار شمارشی شدند تا با سرانه‌های 1/1500، 1/20000 و 1/500 هم‌واحد باشند.)
AREA_BASED_CATEGORIES = ["q14_park", "q6_school_edu", "q15_sports"]

# برچسب فارسی هر دسته برای دیکشنری فیلدهای خروجی
category_labels = {
    "q1_doctor": "پزشک عمومی", "q2_pharmacy": "داروخانه", "q3_clinic": "کلینیک",
    "q4_hospital": "بیمارستان", "q5_kindergarten": "مهدکودک", "q6_school_edu": "مدرسه",
    "q8_university": "دانشگاه", "q9_local_grocer": "نانوایی و میوه‌فروشی",
    "q10_supermarket": "سوپرمارکت", "q11_appliance": "پوشاک و لوازم",
    "q12_local_market": "بازارچه محلی", "q13_mall": "مرکز خرید", "q14_park": "پارک",
    "q15_sports": "فضای ورزشی", "q16_culture": "فرهنگی", "q17_public_space": "فضای عمومی",
    "q18_bus_stop": "ایستگاه اتوبوس", "q19_taxi": "تاکسی", "q20_subway": "مترو",
    "q21_terminal": "پایانه", "q22_main_street": "خیابان اصلی", "q23_post_office": "پست و شهرداری",
    "q24_police_fire": "پلیس و آتش‌نشانی", "q25_worship": "مذهبی",
    "q26_local_gov": "ادارات دولتی", "q27_workplace": "محل کار"
}

assert abs(sum(global_weights.values()) - 1.0) < 1e-6, "مجموع وزن‌ها باید ۱ باشد"
assert set(global_weights) == set(ideal_ratios) == set(category_labels), "کلیدهای دیکشنری‌ها یکسان نیستند"

# نام ستون‌ها: نام کامل برای GeoPackage، نام کوتاه (حداکثر ۱۰ کاراکتر) برای Shapefile
INDEX_COL, INDEX_COL_SHORT = "Index_15Min", "IDX15"

def score_col(cat):
    return f"score_{cat}"

def short_score_col(cat):
    """مثال: q14_park -> s_q14"""
    return f"s_{cat.split('_')[0]}"

# =====================================================================
# ۲. توابع کمکی برای استخراج دسته‌بندی و ظرفیت از دیتافریم OSM
# =====================================================================
def get_category_from_tags(row):
    """نگاشت تگ‌های OpenStreetMap به ۲۷ متغیر پرسشنامه"""
    amenity = row.get('amenity', '')
    shop = row.get('shop', '')
    leisure = row.get('leisure', '')
    highway = row.get('highway', '')
    station = row.get('station', '')
    office = row.get('office', '')
    
    # 1-4. Healthcare
    if amenity in ['doctors']: return "q1_doctor"
    if amenity == 'pharmacy': return "q2_pharmacy"
    if amenity == 'clinic' or row.get('healthcare') == 'clinic': return "q3_clinic"
    if amenity == 'hospital' or row.get('healthcare') == 'hospital': return "q4_hospital"
    
    # 5-8. Education
    if amenity == 'kindergarten': return "q5_kindergarten"
    if amenity == 'school': return "q6_school_edu"
    if amenity in ['university', 'college']: return "q8_university"
    
    # 9-13. Commercial
    if shop in ['bakery', 'greengrocer']: return "q9_local_grocer"
    if shop in ['supermarket', 'convenience']: return "q10_supermarket"
    if shop in ['clothes', 'appliance']: return "q11_appliance"
    if amenity == 'marketplace' or shop == 'department_store': return "q12_local_market"
    if shop == 'mall': return "q13_mall"
    
    # 14-17. Leisure & Public
    if leisure == 'park': return "q14_park"
    if leisure in ['sports_centre', 'pitch']: return "q15_sports"
    if amenity in ['library', 'cinema', 'arts_centre', 'theatre']: return "q16_culture"
    if amenity == 'cafe' or highway == 'pedestrian': return "q17_public_space"
    
    # 18-22. Transit
    if highway == 'bus_stop': return "q18_bus_stop"
    if amenity == 'taxi': return "q19_taxi"
    if station == 'subway' or row.get('railway') == 'station': return "q20_subway"
    if amenity == 'bus_station' or row.get('aeroway') == 'terminal': return "q21_terminal"
    if highway in ['primary', 'secondary']: return "q22_main_street"
    
    # 23-27. Civic & Work
    if amenity in ['post_office', 'townhall']: return "q23_post_office"
    if amenity in ['police', 'fire_station']: return "q24_police_fire"
    if amenity == 'place_of_worship': return "q25_worship"
    if office == 'government': return "q26_local_gov"
    if office == 'company' or row.get('landuse') == 'commercial': return "q27_workplace"
    
    return None

def get_capacity(row, category):
    """محاسبه ظرفیت هر کاربری (مساحت برای پارک/مدرسه، تعداد برای ایستگاه‌ها)"""
    area = row.get('area_sqm', 100.0)
    if pd.isna(area) or area == 0: area = 100.0
        
    # کاربری‌هایی که مساحت محور هستند (سرانه ایده‌آل برحسب m² به ازای هر نفر)
    if category in AREA_BASED_CATEGORIES:
        return area
    # بیمارستان (سعی در دریافت تعداد تخت، در غیر اینصورت تخمین از مساحت)
    elif category == "q4_hospital":
        beds = row.get('beds')
        if pd.notna(beds):
            try: return float(beds)
            except: pass
        return area * 0.02
    # کاربری‌هایی که شمارش و حضورشان مهم‌تر از مساحت فیزیکی آن‌هاست
    else:
        return 1.0

# =====================================================================
# ۳. فرآیند اصلی محاسبه
# =====================================================================
def main():
    # الف) بارگذاری محلات
    logging.info("Loading Neighborhoods (Regions)...")
    regions = gpd.read_file(INPUT_REGIONS)
    
    # اطمینان از وجود ستون جمعیت (اگر در شیپ‌فایل شما نام دیگری دارد، اینجا اصلاح کنید)
    if "population" not in regions.columns:
        logging.warning("Population column missing. Using mock data of 5000 per region.")
        regions["population"] = 5000

    regions["lon"] = regions.geometry.centroid.x
    regions["lat"] = regions.geometry.centroid.y

    # ب) دانلود شبکه معابر پیاده
    place_name = "Tehran, Iran"
    logging.info(f"Downloading street network for {place_name}...")
    G = ox.graph_from_place(place_name, network_type='walk')
    
    # پ) دانلود POIهای مرتبط با ۲۷ متغیر (برای جلوگیری از دانلود بی‌رویه، تگ‌ها محدود شده‌اند)
    osm_tags = {
        "amenity": ["doctors", "clinic", "pharmacy", "hospital", "kindergarten", "school", "university", "college", "marketplace", "library", "cinema", "arts_centre", "theatre", "cafe", "taxi", "bus_station", "post_office", "townhall", "police", "fire_station", "place_of_worship"],
        "shop": ["bakery", "greengrocer", "supermarket", "convenience", "clothes", "appliance", "mall", "department_store"],
        "leisure": ["park", "sports_centre", "pitch"],
        "highway": ["bus_stop", "pedestrian", "primary", "secondary"],
        "station": ["subway"],
        "office": ["government", "company"],
        "landuse": ["commercial"]
    }
    
    logging.info("Downloading POIs from OpenStreetMap...")
    data = ox.features_from_place(place_name, osm_tags)
    
    # محاسبه مساحت به متر مربع
    data_proj = data.to_crs(data.estimate_utm_crs())
    data["area_sqm"] = data_proj.geometry.area
    
    data["geometry_point"] = data.geometry.apply(
        lambda geom: geom if geom.geom_type == "Point" else geom.centroid
    )
    data["lon"] = data.geometry_point.x
    data["lat"] = data.geometry_point.y
    data = data.set_geometry("geometry_point")

    # ت) تخصیص دسته‌بندی، استخراج گره‌ها و ظرفیت
    logging.info("Categorizing POIs and mapping to network...")
    poi_info = {}
    poi_id_counter = 0
    
    for idx, row in data.iterrows():
        cat = get_category_from_tags(row)
        if cat and cat in global_weights:
            node = ox.distance.nearest_nodes(G, X=row["lon"], Y=row["lat"])
            poi_info[poi_id_counter] = {
                "category": cat,
                "node": node,
                "capacity": get_capacity(row, cat)
            }
            poi_id_counter += 1

    # ث) تنظیمات الگوریتم و دایکسترا
    beta = 0.002
    distance_threshold = 1200 # ۱۵ دقیقه ضربدر ۸۰ متر
    region_to_pois = {}
    
    logging.info("Step 1/3: Running Network Routing (Dijkstra) for all regions...")
    for idx, row in regions.iterrows():
        ref_node = ox.distance.nearest_nodes(G, X=row["lon"], Y=row["lat"])
        accessible_nodes = nx.single_source_dijkstra_path_length(
            G, ref_node, cutoff=distance_threshold, weight='length'
        )
        
        region_to_pois[idx] = {}
        for pid, info in poi_info.items():
            if info["node"] in accessible_nodes:
                region_to_pois[idx][pid] = accessible_nodes[info["node"]]

    # ج) گام اول 2SFCA: محاسبه ارزش سرانه هر امکانات با توجه به رقابت جمعیتی
    logging.info("Step 2/3: Calculating 2SFCA Supply/Demand Ratios...")
    poi_supply_ratios = {}
    for pid, info in poi_info.items():
        potential_demand = 0.0
        for idx, row in regions.iterrows():
            if pid in region_to_pois[idx]:
                dist = region_to_pois[idx][pid]
                potential_demand += row["population"] * math.exp(-beta * dist)
                
        poi_supply_ratios[pid] = (info["capacity"] / potential_demand) if potential_demand > 0 else 0.0

    # چ) گام دوم 2SFCA، اعمال سقف اشباع و محاسبه شاخص کلان
    logging.info("Step 3/3: Computing Capped Scores and 15-Min City Index...")
    
    for idx, row in regions.iterrows():
        # جمع‌آوری امتیاز سرانه خام برای هر ۲۷ متغیر در این محله
        raw_scores = {cat: 0.0 for cat in global_weights.keys()}
        
        for pid, dist in region_to_pois[idx].items():
            cat = poi_info[pid]["category"]
            raw_scores[cat] += poi_supply_ratios[pid] * math.exp(-beta * dist)

        total_weighted_index = 0.0
        
        for cat in global_weights.keys():
            raw_ratio = raw_scores[cat]
            ideal = ideal_ratios[cat]
            
            # نرمال‌سازی با سقف اشباع (عدد بین ۰ و ۱)
            capped_ratio = min(raw_ratio / ideal, 1.0)
            
            # ذخیره امتیاز این دسترسی (از ۰ تا ۱۰۰) در دیتافریم برای تحلیل‌های جزئی
            regions.at[idx, score_col(cat)] = round(capped_ratio * 100, 2)
            
            # ضرب در وزن لیکرت/AHP
            total_weighted_index += capped_ratio * global_weights[cat]

        # تبدیل شاخص کل به مقیاس ۰ تا ۱۰۰
        regions.at[idx, INDEX_COL] = round(total_weighted_index * 100, 2)

    # ح) خروجی نهایی
    logging.info("Saving results...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # اعتبارسنجی بازه امتیازها پیش از ذخیره
    score_cols = [score_col(cat) for cat in global_weights]
    assert regions[score_cols].ge(0).all().all() and regions[score_cols].le(100).all().all()
    assert regions[INDEX_COL].between(0, 100).all()
    
    # حذف ستون‌های موقت برای جلوگیری از خطای ذخیره‌سازی شیپ‌فایل
    columns_to_drop = ['lon', 'lat']
    regions_out = regions.drop(columns=[c for c in columns_to_drop if c in regions.columns])

    # GeoPackage: نام‌های کامل ستون‌ها
    gpkg_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_NAME}.gpkg")
    regions_out.to_file(gpkg_path, driver="GPKG", encoding="utf-8")

    # Shapefile: نام فیلد DBF حداکثر ۱۰ کاراکتر است، پس از نام‌های کوتاه استفاده می‌شود
    rename_map = {score_col(cat): short_score_col(cat) for cat in global_weights}
    rename_map[INDEX_COL] = INDEX_COL_SHORT
    shp_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_NAME}.shp")
    regions_out.rename(columns=rename_map).to_file(shp_path, encoding="utf-8")

    # دیکشنری فیلدها: نگاشت نام کوتاه Shapefile به نام کامل و توضیح فارسی
    field_rows = [
        {"short_name": short_score_col(cat), "full_name": score_col(cat),
         "description": f"امتیاز دسترسی ۰ تا ۱۰۰ به {category_labels[cat]} (بدون وزن)"}
        for cat in global_weights
    ]
    field_rows.append({"short_name": INDEX_COL_SHORT, "full_name": INDEX_COL,
                       "description": "شاخص کلان شهر ۱۵ دقیقه‌ای ۰ تا ۱۰۰ (وزن‌دار با MCDA)"})
    dict_path = os.path.join(OUTPUT_DIR, "field_dictionary.csv")
    pd.DataFrame(field_rows).to_csv(dict_path, index=False, encoding="utf-8-sig")

    logging.info(f"Process Complete! Outputs saved to: {shp_path}, {gpkg_path}, {dict_path}")

if __name__ == "__main__":
    main()