from keras.applications import ResNet50
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.optimizers import Adam
from sklearn.metrics import classification_report
from keras.preprocessing.image import ImageDataGenerator

class CNN():
    def __init__(self, x_train, x_test, y_train, y_test):
        # Normalize input data
        x_train = x_train / 255
        x_test = x_test / 255
        y_train = y_train
        y_test = y_test

        # Load ResNet50 as the base model
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(512, 512, 3))
        x = base_model.output
        x = GlobalAveragePooling2D()(x)  # Add global average pooling to reduce feature dimensions
        x = Dense(128, activation='relu')(x)  # Add a dense layer with 128 units
        x = Dropout(0.5)(x)  # Dropout to prevent overfitting
        predictions = Dense(1, activation='sigmoid')(x)  # Output layer for binary classification
        
        # Build the model
        self.model = Model(inputs=base_model.input, outputs=predictions)

        # Freeze the base layers for transfer learning
        for layer in base_model.layers:
            layer.trainable = False

        # Compile the model
        self.model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        # Data augmentation
        datagen = ImageDataGenerator(
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
            horizontal_flip=True
        )
        datagen.fit(x_train)

        # Train the model
        self.history = self.model.fit(
            datagen.flow(x_train, y_train, batch_size=32),
            validation_data=(x_test, y_test),
            epochs=20,
            verbose=1
        )

        # Evaluate the model
        self.test_loss, self.test_acc = self.model.evaluate(x_test, y_test)
        self.y_pred = (self.model.predict(x_test) > 0.5).astype("int32")

        # Display evaluation metrics
        print(classification_report(y_test, self.y_pred))
