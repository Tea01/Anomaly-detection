# Anomaly-detection
In data analysis, *anomaly detection* (also referred to as outlier detection and sometimes as novelty detection) is generally understood to be the identification of rare items, events or observations which deviate significantly from the majority of the data and do not conform to a well defined notion of normal behaviour.

###Short competition

Our aim is to detect frauds in finantial transactions. The dataset consists of features related to financial transactions, some of which may involve fraudulent activity. The data has been normalized and dimentionality reduced to prevent the use of heuristics based on human knowledge. Your task is to identify anomalies in order to detect possible fraud. Frauds are frequently atypical transactions. It is worth noting that atypical transactions are not necessarily fraudulent. Let us now examine the data.

The dataset comprises 5 columns, with the first 4 columns providing transaction features such as transaction value, time, and agent's salary. The fifth column contains three distinct values: 0, 1, and nan. The value 0 indicates that the transaction is not fraudulent, while 1 indicates that it is fraudulent. The "nan" value denotes instances where the financial institution is unsure whether the transaction is fraudulent or not.
