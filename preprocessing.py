import pandas as pd

from data_cleaning import remove_columns, convert_list_into_len, get_non_mercado_pago_info, get_shipping_mode_info
from data_cleaning import col_to_remove, col_to_len

def convert_condition(df):
    df["condition"] = df["condition"].map({"new": 0, "used":1})
    return df

def convert_listing_type_id(df):
    df["listing_type_id"] = df["listing_type_id"].map({"free":0, "bronze":1, "silver":2, "gold":3, "gold_special":4, "gold_premium":5, "gold_pro":6})
    return df

def convert_buying_mode(df):
    df = df.join(pd.get_dummies(df.buying_mode, prefix='buy_mode.'))
    df.drop(["buying_mode"], axis=1, inplace=True)
    return df

def convert_tags(df):
    df = df.join(pd.json_normalize(df.pop("tags").apply(lambda x: {el: 1 for el in x})).fillna(0).add_prefix("tag."))
    return df
    
def convert_category_id(df):
    vc = df["category_id"].value_counts(dropna=False)
    others_list = vc[vc<400].index.to_list()
    df["category_id"] = df["category_id"].apply(lambda x: "others" if x in others_list else x)
    df = df.join(pd.get_dummies(df.pop("category_id"), prefix='cat.'))
    
    return df

def convert_accepts_mercadopago(df):
    df["accepts_mercadopago"] = df["accepts_mercadopago"].apply(lambda x: int(x))
    return df

def convert_automatic_relist(df):
    df["automatic_relist"] = df["automatic_relist"].apply(lambda x: int(x))
    return df

def convert_non_mercado_pago(df):
    df = df.join(pd.json_normalize(df.pop("non_mercado_pago").apply(lambda x: {el: 1 for el in x})).fillna(0).add_prefix("nmp."))
    return df

def convert_shipping_mode(df):
    df = df.join(pd.get_dummies(df.pop("shipping_mode"), prefix='shim.'))
    return df

    
def fill_nan_texts():
    df["warranty"] = df["warranty"].fillna("")
    df["title"] = df["title"].fillna("")
    
def remove_text_columns(df, columns):
    df = df.drop(columns, axis=1)
    return df

def normalize(df):
    normalized_df=(df-df.min())/(df.max()-df.min())
    return normalized_df

def drop_duplicates(df):
   df = df.drop_duplicates()
   return df

def remove_outliers(df, columns):
   for col in columns:
      avg = df[col].mean()
      std = df[col].std()
      low = avg - 2 * std
      high = avg + 2 * std
      df = df[df[col].between(low, high, inclusive=True)]
   return df
    
def preprocess_training(df):
    df_processed = (df.
                        pipe(remove_columns, col_to_remove).
                        pipe(convert_list_into_len, col_to_len).
                        pipe(get_non_mercado_pago_info).
                        pipe(get_shipping_mode_info).
                    
                        pipe(convert_condition).
                        pipe(convert_listing_type_id).
                        pipe(convert_buying_mode).
                        pipe(convert_tags).
                        pipe(convert_category_id).
                        pipe(convert_accepts_mercadopago).
                        pipe(convert_automatic_relist).
                        pipe(convert_non_mercado_pago).
                        pipe(convert_shipping_mode).
                    
                        pipe(remove_text_columns, ["warranty", "title"]).
                        pipe(drop_duplicates).
                        pipe(remove_outliers, ["price"]).
                        pipe(normalize)
                   )

    return df_processed

def preprocess_testing(df):
    df_processed = (df.
                        pipe(remove_columns, col_to_remove).
                        pipe(convert_list_into_len, col_to_len).
                        pipe(get_non_mercado_pago_info).
                        pipe(get_shipping_mode_info).

                        pipe(convert_listing_type_id).
                        pipe(convert_buying_mode).
                        pipe(convert_tags).
                        pipe(convert_category_id).
                        pipe(convert_accepts_mercadopago).
                        pipe(convert_automatic_relist).
                        pipe(convert_non_mercado_pago).
                        pipe(convert_shipping_mode).
                    
                        pipe(remove_text_columns, ["warranty", "title"]).
                        pipe(drop_duplicates).
                        pipe(normalize)
                   )

    return df_processed
