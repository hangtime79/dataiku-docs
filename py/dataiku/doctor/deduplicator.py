import logging

def perform_dedup(df, preprocessing_params):
    if preprocessing_params["deduplication"]["enabled"] == True:
        feature = preprocessing_params["deduplication"]["deduplicate_on"]
        if feature == "__ALL__":
            logging.info("Deduplication on all features")
            return df.drop_duplicates()
        else:
            if feature in df.columns:
                logging.info("Deduplication on feature %s" % feature)
                return df.drop_duplicates(feature)
            else:
                logging.warn("Deduplication asked on %s, but not found in dataset, deduplicating all..." % feature)
                return df.drop_duplicates()
    else:
        return df