import json
import numpy as np
from typing import List
import tensorflow as tf
from tensorflow import keras
import pickle
from fastapi import  WebSocket
import os


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd + "/ml")  # Get all the files in that directory


class ChatBot:

    def openIntents(self):

        with open(cwd + '/ml/intents.json') as file:
            data = json.load(file)
        return data


    def botResponse(self,input):
        # load trained model
        model = keras.models.load_model(cwd + '/ml/chat_model')

        # load tokenizer object
        with open(cwd + '/ml/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        # load label encoder object
        with open(cwd + '/ml/label_encoder.pickle', 'rb') as enc:
            lbl_encoder = pickle.load(enc)

        # parameters
        max_len = 20

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([input]),
                                             truncating='post', maxlen=max_len))
    
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        # print("Tag")
        # print(tag)
        for i in self.openIntents()['intents']:
            if i['tag'] == tag:
                choice = np.random.choice(i['responses'])
                print(choice)
                return choice
        

class ConnectionManager:

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        Create websocket connection and add to
        active connection list.
        
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Remove websocket connection from active
        connections list.
        
        """
        self.active_connections.remove(websocket)  

    async def reply(self, message: str, websocket: WebSocket) -> None:
        """
        Send text message to websocket connection.
        Args:
          message: Text message to send.
          websocket: A Websocket instance addressee.
        """
        
        if message and type(message) is str:
            await websocket.send_text(message)
        elif message and isinstance(message, dict):
            await websocket.send_json(message)

    async def quit(self, message: str, websocket: WebSocket) -> None:
        """
        Send farewell message and disconnect.
        Args:
          message: Farewell text message to send.
          websocket: A Websocket instance addressee and to disconnect.
        """
        await self.reply(message, websocket)
        await websocket.close()
        self.disconnect(websocket)  