col_to_remove = ["start_time", "stop_time", "date_created", "permalink", "thumbnail", "secure_thumbnail", 
                 "geolocation", "seller_contact", "seller_address", "last_updated", "seller_id", 
                 "sub_status", "deal_ids", "site_id", "listing_source", "coverage_areas", 
                 "international_delivery_mode", "official_store_id", "differential_pricing", 
                 "original_price", "currency_id", "status", "video_id", "catalog_product_id", 
                 "subtitle", "descriptions", "id", "parent_item_id", "location", "base_price"]

def remove_columns(df, columns):
    return df.drop(columns, axis=1)

col_to_len = ["pictures", "variations", "attributes"]

def convert_list_into_len(df, columns):
    df2 = df.copy()
    for col in columns:
        df2[f"num_{col[:3]}"] = df2.pop(col).apply(lambda x: len(x) if x else 0)

    return df2

def get_non_mercado_pago_info(df):
    df2 = df.copy()
    df2["non_mercado_pago"] = df2.pop("non_mercado_pago_payment_methods").apply(lambda x: [d["description"] for d in x] if x else ["N/a"])
    
    return df2

def get_shipping_mode_info(df):
    df2 = df.copy()
    df2["shipping_mode"] = df2.pop("shipping").apply(lambda x: x["mode"])
    
    return df2
