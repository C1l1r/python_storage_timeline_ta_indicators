from aggregation import data_aggregation
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pandas as pd
import json
import numpy as np


class lstm_anomaly_detection():

    def __init__(self, url,  model_name = "models/lstm_for_ad.h5"):
        self.ad_model = tf.keras.models.load_model(model_name)
        self.aggregated_data = data_aggregation(url)

        with open(model_name+".json", "r") as file:
            self.metadata = json.load(file)


    def detect_anomalies(self, threshold  = 1.25):
        aggregated_data = self.aggregated_data.get_data()

        scaler = StandardScaler()
        scaler = scaler.fit(aggregated_data[['reserve_0']])
        aggregated_data['reserve_0'] = scaler.transform(aggregated_data[['reserve_0']])


        def create_dataset(X, y, time_steps=1):
            Xs, ys = [], []
            for i in range(len(X) - time_steps):
                v = X.iloc[i:(i + time_steps)].values
                Xs.append(v)
                ys.append(y.iloc[i + time_steps])
            return np.array(Xs), np.array(ys)

        TIME_STEPS = self.metadata["TIME_STEPS"]

        X_test, y_test = create_dataset(
            aggregated_data[['reserve_0']],
            aggregated_data.reserve_0,
            TIME_STEPS
        )

        X_test_pred = self.ad_model.predict(X_test)
        test_mae_loss = np.mean(np.abs(X_test_pred - X_test), axis=1)
        test_score_df = pd.DataFrame(index=aggregated_data[TIME_STEPS:].index)
        test_score_df['loss'] = test_mae_loss
        test_score_df['threshold'] = threshold
        test_score_df['anomaly'] = test_score_df.loss > test_score_df.threshold
        test_score_df['reserve_0'] = aggregated_data[TIME_STEPS:].reserve_0
        anomalies = test_score_df[test_score_df.anomaly == True]
        print(anomalies)

        plt.plot(
            aggregated_data[TIME_STEPS:].index,
            scaler.inverse_transform(aggregated_data[TIME_STEPS:].reserve_0.values.reshape(1, -1)).reshape(-1),
            label='reserve'
        );
        sns.scatterplot(
            x=anomalies.index,
            y=scaler.inverse_transform(anomalies.reserve_0.values.reshape(1, -1)).reshape(-1),
            label='anomaly',
            color=sns.color_palette()[3]
        );
        plt.xticks(rotation=25)
        plt.show()


anms = lstm_anomaly_detection(url = 'https://europe-west1-hype-dev.cloudfunctions.net/storage-timeline-all?format=string&schema=ethereum.lovelyswap-v4.lovely.finance&timeLine=0x3aB9323992DFf9231D40E45C4AE009db1a35e40b')
anms.detect_anomalies(threshold=1.25)


