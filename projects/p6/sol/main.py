# # Version 1
# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import cross_val_score
# from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder

# # project: p7
# # submitter: paytonfife
# # partner: none
# # hours: 3

# class UserPredictor():
#     def __init__(self):
#         self.xcols = ["past_purchase_amt", "duration", "age"]
#         self.model = LogisticRegression()
    
#     def fit(self, df1, df2, df3):
#         self.train_df = pd.merge(df1, df2[["id", "duration"]].groupby("id").sum(),how = "left", on = "id").fillna(0)
#         self.train_df = pd.merge(self.train_df, df3, on = "id")
#         self.model.fit(self.train_df[self.xcols], self.train_df["clicked"])
#         scores = cross_val_score(self.model, self.train_df[self.xcols], self.train_df["clicked"])
#         return f"AVG: {scores.mean()}, STD: {scores.std()}"
    
#     def predict(self, df1, df2):
#         self.test_df = pd.merge(df1, df2[["id", "duration"]].groupby("id").sum(), how = "left", on = "id").fillna(0)
#         return self.model.predict(self.test_df[self.xcols])



# # Version 2
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression

# class UserPredictor:
#     def __init__(self):
#         self.model = LogisticRegression(fit_intercept=False)

#     def fit(self, users, logs, y):
#         # Prepare the dataset
#         users = self.setup(users, logs).merge(y, how="left", on="id")
#         # Split into training and testing sets
#         train, test = train_test_split(users)
#         # Fit the model
#         self.model.fit(train[["past_purchase_amt", "total_time", "const"]], train["clicked"])

#     def predict(self, users, logs):
#         # Prepare the dataset
#         users = self.setup(users, logs)
#         # Make predictions
#         users["predict"] = self.model.predict(users[["past_purchase_amt", "total_time", "const"]])
#         return users["predict"].to_numpy()

#     def setup(self, users, logs):
#         # Filter and set index
#         users = users[["id", "past_purchase_amt"]].set_index("id")
#         # Add constant column
#         users["const"] = 1
#         # Compute total time spent by each user on logs
#         logs_grouped = logs.groupby("id")["duration"].sum()
#         users["total_time"] = logs_grouped.reindex(users.index).fillna(0)

#         return users



# # Version 3
# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import cross_val_score, train_test_split

# class UserPredictor:
#     def __init__(self):
#         self.xcols = ["past_purchase_amt", "duration", "age", "const"]
#         self.model = LogisticRegression(fit_intercept=False)

#     def fit(self, df1, df2, df3):
#         # Preparing the dataset
#         self.train_df = self.prepare_data(df1, df2, df3)
#         # Splitting into train and test
#         train, test = train_test_split(self.train_df)
#         # Fitting the model
#         self.model.fit(train[self.xcols], train["clicked"])
#         # Evaluating performance with cross-validation
#         scores = cross_val_score(self.model, self.train_df[self.xcols], self.train_df["clicked"])
#         return f"AVG: {scores.mean()}, STD: {scores.std()}"

#     def predict(self, df1, df2):
#         # Preparing the test data
#         self.test_df = self.prepare_data(df1, df2)
#         # Making predictions
#         return self.model.predict(self.test_df[self.xcols])

#     def prepare_data(self, df1, df2, df3=None):
#         # Merge df1 with summed 'duration' from df2
#         data = pd.merge(df1, df2[["id", "duration"]].groupby("id").sum(), how="left", on="id").fillna(0)
#         if df3 is not None:
#             # Merge with labels if available
#             data = pd.merge(data, df3, on="id")
#         # Add a constant column
#         data["const"] = 1
#         return data



# # Version 4 - bad
# import pandas as pd
# import numpy as np
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler, PolynomialFeatures
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split, cross_val_score

# class UserPredictor:
#     def __init__(self):
#         # Defining features for model input
#         self.xcols = ["past_purchase_amt", "total_time", "const", "num_tv_visits"]
#         # Initializing the model pipeline
#         self.model = Pipeline([
#             ("scaler", StandardScaler()),
#             ("poly", PolynomialFeatures(degree=2, interaction_only=True)),
#             ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
#         ])

#     def fit(self, df1, df2, df3):
#         # Preparing the dataset
#         self.train_df = self.prepare_data(df1, df2).merge(df3, how="left", on="id")
#         # Fitting the model
#         self.model.fit(self.train_df[self.xcols], self.train_df["clicked"])
#         # Cross-validation
#         scores = cross_val_score(self.model, self.train_df[self.xcols], self.train_df["clicked"])
#         print(f"AVG: {scores.mean()}, STD: {scores.std()}\n")

#     def predict(self, df1, df2):
#         # Preparing the test data
#         self.test_df = self.prepare_data(df1, df2)
#         # Making predictions
#         return self.model.predict(self.test_df[self.xcols])

#     def prepare_data(self, df1, df2):
#         # Merging user and logs data
#         users = pd.merge(df1, df2.groupby("id")["duration"].sum().reset_index(name="total_time"), how="left", on="id").fillna(0)
#         # Adding a constant column
#         users["const"] = 1
#         # Adding additional features
#         users["num_tv_visits"] = df2[df2["url"].str.contains("tv")].groupby("id").size().reindex(users["id"]).fillna(0)
#         return users


# # Version 5 - so far best
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import Pipeline

# class UserPredictor:
#     def __init__(self):
#         # Features we consider directly from users data
#         self.xcols = ['past_purchase_amt', 'age']
#         # Additional computed features
#         self.log_features = ['total_duration', 'tv_page_visits', 'total_visits']
#         # Setup the pipeline with preprocessing and logistic regression
#         self.pipeline = Pipeline([
#             ('scaler', StandardScaler()),
#             ('logistic', LogisticRegression())
#         ])

#     def fit(self, users, logs, clicked):
#         # Prepare the full training dataset
#         full_train = self.prepare_data(users, logs)
#         full_train = full_train.merge(clicked, on='id')
        
#         # Training the model with cross-validation
#         X_train = full_train[self.xcols + self.log_features]
#         y_train = full_train['clicked']
#         self.pipeline.fit(X_train, y_train)
#         scores = cross_val_score(self.pipeline, X_train, y_train, cv=5)
#         print(f"Training Completed. AVG: {scores.mean()}, STD: {scores.std()}")

#     def predict(self, users, logs):
#         # Prepare test dataset
#         test_data = self.prepare_data(users, logs)
#         return self.pipeline.predict(test_data[self.xcols + self.log_features])

#     def prepare_data(self, users, logs):
#         # Sum durations and count visits
#         duration_sum = logs.groupby('id')['duration'].sum().rename('total_duration')
#         page_visits = logs[logs['url'].str.contains('tv.html')].groupby('id').size().rename('tv_page_visits')
        
#         # Total visits per user
#         total_visits = logs.groupby('id').size().rename('total_visits')
        
#         # Merge logs stats back to users
#         users = users.merge(duration_sum, on='id', how='left')
#         users = users.merge(page_visits, on='id', how='left')
#         users = users.merge(total_visits, on='id', how='left')
        
#         # Fill missing values for users with no logs data
#         users.fillna({
#             'total_duration': 0,
#             'tv_page_visits': 0,
#             'total_visits': 0
#         }, inplace=True)
        
#         return users


# # Version 6
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import cross_val_score, train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.pipeline import Pipeline, FeatureUnion
# from sklearn.compose import ColumnTransformer
# from sklearn.impute import SimpleImputer

# class UserPredictor:
#     def __init__(self):
#         # Features directly from user data
#         self.xcols = ['past_purchase_amt', 'age']
#         self.log_features = ['total_duration', 'tv_page_visits', 'total_visits', 'keyboard_visits']
#         # Additional categorical column to handle
#         self.categorical_cols = ['badge']
#         # Column transformer with various preprocessors
#         self.preprocessor = ColumnTransformer([
#             # Standard scaling for numerical columns
#             ('num', StandardScaler(), self.xcols + self.log_features),
#             # One-hot encoding for categorical columns
#             ('cat', OneHotEncoder(drop='first'), self.categorical_cols)
#         ])
#         # Final model pipeline
#         self.pipeline = Pipeline([
#             ('preprocessor', self.preprocessor),
#             ('classifier', LogisticRegression())
#         ])

#     def fit(self, users, logs, clicked):
#         # Prepare the full dataset
#         full_train = self.prepare_data(users, logs)
#         full_train = full_train.merge(clicked, on='id')
        
#         # Train with cross-validation
#         X_train = full_train[self.xcols + self.log_features + self.categorical_cols]
#         y_train = full_train['clicked']
#         self.pipeline.fit(X_train, y_train)
        
#         scores = cross_val_score(self.pipeline, X_train, y_train, cv=5)
#         print(f"Training Completed. AVG: {scores.mean()}, STD: {scores.std()}")

#     def predict(self, users, logs):
#         # Prepare test dataset
#         test_data = self.prepare_data(users, logs)
#         return self.pipeline.predict(test_data[self.xcols + self.log_features + self.categorical_cols])

#     def prepare_data(self, users, logs):
#         # Sum durations and count visits
#         duration_sum = logs.groupby('id')['duration'].sum().rename('total_duration')
#         page_visits = logs[logs['url'].str.contains('tv.html')].groupby('id').size().rename('tv_page_visits')
#         keyboard_visits = logs[logs['url'].str.contains('keyboard.html')].groupby('id').size().rename('keyboard_visits')
#         total_visits = logs.groupby('id').size().rename('total_visits')
        
#         # Merge log stats to users
#         users = users.merge(duration_sum, on='id', how='left')
#         users = users.merge(page_visits, on='id', how='left')
#         users = users.merge(keyboard_visits, on='id', how='left')
#         users = users.merge(total_visits, on='id', how='left')
        
#         # Fill missing values for users with no logs data
#         users.fillna({
#             'total_duration': 0,
#             'tv_page_visits': 0,
#             'keyboard_visits': 0,
#             'total_visits': 0
#         }, inplace=True)
        
#         return users


# # Version 7
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

class UserPredictor:
    def __init__(self):
        # Features directly from user data
        self.xcols = ['past_purchase_amt', 'age']
        self.log_features = [
            'total_duration', 'tv_page_visits', 'total_visits', 
            'keyboard_visits', 'blender_visits', 'cleats_visits', 'tablet_visits'
        ]
        # Additional categorical column to handle
        self.categorical_cols = ['badge']
        # Column transformer with various preprocessors
        self.preprocessor = ColumnTransformer([
            # Standard scaling for numerical columns
            ('num', StandardScaler(), self.xcols + self.log_features),
            # One-hot encoding for categorical columns
            ('cat', OneHotEncoder(drop='first'), self.categorical_cols)
        ])
        # Final model pipeline
        self.pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', LogisticRegression())
        ])

    def fit(self, users, logs, clicked):
        # Prepare the full dataset
        full_train = self.prepare_data(users, logs)
        full_train = full_train.merge(clicked, on='id')
        
        # Train with cross-validation
        X_train = full_train[self.xcols + self.log_features + self.categorical_cols]
        y_train = full_train['clicked']
        self.pipeline.fit(X_train, y_train)
        
        scores = cross_val_score(self.pipeline, X_train, y_train, cv=5)
        print(f"Training Completed. AVG: {scores.mean()}, STD: {scores.std()}")

    def predict(self, users, logs):
        # Prepare test dataset
        test_data = self.prepare_data(users, logs)
        return self.pipeline.predict(test_data[self.xcols + self.log_features + self.categorical_cols])

    def prepare_data(self, users, logs):
        # Sum durations and count visits
        duration_sum = logs.groupby('id')['duration'].sum().rename('total_duration')
        tv_visits = logs[logs['url'].str.contains('tv.html')].groupby('id').size().rename('tv_page_visits')
        keyboard_visits = logs[logs['url'].str.contains('keyboard.html')].groupby('id').size().rename('keyboard_visits')
        blender_visits = logs[logs['url'].str.contains('blender.html')].groupby('id').size().rename('blender_visits')
        cleats_visits = logs[logs['url'].str.contains('cleats.html')].groupby('id').size().rename('cleats_visits')
        tablet_visits = logs[logs['url'].str.contains('tablet.html')].groupby('id').size().rename('tablet_visits')
        total_visits = logs.groupby('id').size().rename('total_visits')
        
        # Merge log stats to users
        users = users.merge(duration_sum, on='id', how='left')
        users = users.merge(tv_visits, on='id', how='left')
        users = users.merge(keyboard_visits, on='id', how='left')
        users = users.merge(blender_visits, on='id', how='left')
        users = users.merge(cleats_visits, on='id', how='left')
        users = users.merge(tablet_visits, on='id', how='left')
        users = users.merge(total_visits, on='id', how='left')
        
        # Fill missing values for users with no logs data
        users.fillna({
            'total_duration': 0,
            'tv_page_visits': 0,
            'keyboard_visits': 0,
            'blender_visits': 0,
            'cleats_visits': 0,
            'tablet_visits': 0,
            'total_visits': 0
        }, inplace=True)
        
        return users
