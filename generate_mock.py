import tensorflow as tf
from tensorflow.keras import layers, models

# This model is locked to standard 3-channel RGB data
model = models.Sequential([
    layers.Input(shape=(128, 128, 3)),  
    layers.Flatten(),
    layers.Dense(2, activation='softmax') 
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.save('mock_model.keras')
print("Successfully created a clean, standard mock_model.keras file!")