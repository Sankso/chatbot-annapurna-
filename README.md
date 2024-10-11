# Food Delivery Chatbot Development using Dialogflow and FastAPI


https://github.com/user-attachments/assets/198aa89f-d1a4-4bfb-8d4c-23084ff14715


Developed an intelligent **food delivery chatbot** leveraging **Dialogflow** for natural language processing (NLP) and user interactions. This project covers the fundamentals of Dialogflow, including:

- **Intents**
- **Entities**
- **Contexts**

These components were used to enhance user engagement in the food delivery domain. The project also involved building a robust **backend using Python and FastAPI** to manage requests and responses efficiently.

Interactions with a **MySQL database** were implemented to enable dynamic data storage and retrieval, providing personalized user experiences such as order tracking and menu browsing.

This project provided practical experience in:
- Integrating **NLP** with backend technologies.
- Managing database interactions effectively.

---

## Directory Structure
backend: Contains Python FastAPI backend code
db: Contains the dump of the database. You need to import this into your MySQL DB using the MySQL Workbench tool.
dialogflow_assets: Contains training phrases, intents, and other Dialogflow-related assets.
frontend: Website code

---

## Running the FastAPI Backend Server

To start the backend server:

1. Open your command prompt and navigate to the `backend` directory.
2. Run the following command:
   ```bash
   uvicorn main:app --reload
## ngrok for HTTPS Tunneling

If you need to expose your FastAPI server to the internet for development, you can use **ngrok** for HTTPS tunneling.

### Steps to Set Up ngrok:

1. Download **ngrok** from the [ngrok download page](https://ngrok.com/download) and install the version suitable for your operating system.
2. Extract the zip file and place `ngrok.exe` in a convenient folder.
3. Open a command prompt, navigate to that folder, and run the following command to start ngrok:
   ```bash
   ngrok http 8000
This will create a public URL for your local FastAPI server.
> **Note:** ngrok sessions can timeout. If you see a "session expired" message, you will need to restart the session.

## Features

- **Natural Language Processing (NLP)**: The chatbot uses Dialogflow to understand user inputs and handle various intents related to food delivery.
- **FastAPI Backend**: A Python-based backend that processes incoming requests from the chatbot and returns appropriate responses.
- **MySQL Integration**: Dynamic data storage and retrieval are handled using MySQL, enabling features like order tracking and menu browsing.

---

## Key Technologies

- **Dialogflow**: For natural language processing and handling user intents.
- **FastAPI**: For building a high-performance backend.
- **MySQL**: For database management.
- **ngrok**: For exposing the local server to the internet for development and testing.

---

## Future Improvements

- **Enhancing the NLP model**: Improve the chatbot's ability to understand complex user queries by adding more training data and refining intents.
- **Adding more functionalities**: Implement additional user features, such as payment processing or location-based services.
- **Improving database optimization**: Optimize the MySQL queries to handle larger datasets and more complex operations.
