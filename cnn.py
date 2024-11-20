from keras.models import Sequential
from keras.layers import (
    Conv2D, MaxPooling2D, AveragePooling2D, Flatten, Dense, BatchNormalization, Dropout, ReLU
)
from sklearn.metrics import classification_report

class CNN():
    def __init__(self, x_train, x_test, y_train, y_test):
        model = Sequential([
            # 1st Conv Layer
            Conv2D(32, (3, 3), padding="same", input_shape=(512, 512, 3)),
            BatchNormalization(),
            ReLU(),
            MaxPooling2D(pool_size=(2, 2)),

            # 2nd Conv Layer
            Conv2D(64, (3, 3), padding="same"),
            BatchNormalization(),
            ReLU(),
            MaxPooling2D(pool_size=(2, 2)),

            # 3rd Conv Layer
            Conv2D(128, (3, 3), padding="same"),
            BatchNormalization(),
            ReLU(),
            MaxPooling2D(pool_size=(2, 2)),

            # Average Pooling Layer
            AveragePooling2D(pool_size=(2, 2)),
            
            # Flatten and Fully Connected Layer
            Flatten(),
            Dropout(0.5),  # Dropout to reduce overfitting
            Dense(1, activation="sigmoid")  # Binary classification
        ])
        self.history = model.fit(
            x_train, y_train,  # Training data
            batch_size=32,  # Number of samples per batch
            epochs=20,  # Number of training epochs
            verbose=1  # Display training progress
        )
        self.test_loss, self.test_acc = model.evaluate(x_test, y_test)
    