
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper  # Ensure this module contains your database functions
import logging
import generic_helper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Sample in-progress orders (replace this with your database logic)
inprogress_orders = {
    "session_id_1": {"pizzas": 2, "samosa": 1},
    "session_id_2": {"chhole": 2, "mango lassi": 3},
}

@app.post("/")
async def handle_request(request: Request):
    try:
        # Retrieve JSON data from the request body
        payload = await request.json()

        # Extract intent, parameters, and output contexts from the request
        intent = payload['queryResult']['intent']['displayName']
        parameters = payload['queryResult']['parameters']
        output_contexts = payload['queryResult'].get('outputContexts', [])

        # Extract session_id if available in output contexts
        session_id = generic_helper.extract_session_id(output_contexts[0]['name']) if output_contexts else ""

        # Define a mapping of intents to their respective handler functions
        intent_handler_dict = {
            'order.add-context:ongoing-order': add_to_order,
            'track.order-context:ongoing-tracking': track_order,
            'order.complete-context:ongoing-order': complete_order,
            'order.remove-context:ongoing-order':remove_from_order,
        }

        # Call the corresponding function based on the intent directly
        return await intent_handler_dict[intent](parameters, session_id)

    except KeyError:
        # Handle the case where the intent is not found in the dictionary
        logger.error(f"Intent '{intent}' not recognized.")
        return JSONResponse(content={"fulfillmentText": "Intent not recognized."}, status_code=400)

    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return JSONResponse(content={"fulfillmentText": "An internal server error occurred."}, status_code=500)



async def add_to_order(parameters: dict, session_id: str):
    food_items = parameters.get("food-item", [])
    quantities = parameters.get("number", [])  # Use 'number' instead of 'number1'

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry, I didn't understand. Can you please specify food items and quantities?"
    else:
        # Add the items to the in-progress order
        new_food_dict = dict(zip(food_items, quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

async def remove_from_order(parameters:dict,session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! can you place a new order?"
        })
    current_order=inprogress_orders[session_id]
    food_items = parameters["food-item"]

    removed_items=[]
    no_such_items=[]
    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            del current_order[item]
    if len(removed_items)>0:
        fulfillment_text = f'Removed{",".join(removed_items)} from your order'
    if len(no_such_items)>0:
        fulfillment_text = f"Your current order doesn't have {",".join(no_such_items)}"

    if len(current_order.keys()) == 0:
        fulfillment_text= fulfillment_text+"Your order is empty !"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text = f"Your current order is: {order_str}."
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

async def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having trouble finding your order. Sorry! Can you place a new order?"
    else:
        order = inprogress_orders[session_id]
        
        # Save the order to the database and get the next available order ID
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. "\
                               "Please place a new order again."
        else:
            # Retrieve the total order price from the database
            order_total = db_helper.get_total_order_price(order_id)

            # Ensure the order ID and total are correctly formatted in the response
            fulfillment_text = f"Awesome. Your order is placed! Here is your order ID: {order_id}.\n"\
                               f"Your total is ₹{order_total}. You can pay at the time of delivery!"
            
        # Remove the in-progress order after completion
        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1
    
    db_helper.insert_order_tracking(next_order_id, "in progress")
    return next_order_id


async def track_order(parameters: dict, session_id: str):
    try:
        order_id = int(parameters['number'])  # Use 'number', not 'number1'
        order_status = db_helper.get_order_status(order_id)  # Get order status from the database

        if order_status:
            fulfillment_text = f"The order status for order ID: {order_id} is: {order_status}."
        else:
            fulfillment_text = f"No order found with order ID: {order_id}."

        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return JSONResponse(content={"fulfillmentText": "Error tracking order. Please provide a valid order ID."})
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JSONResponse(content={"fulfillmentText": "An unexpected error occurred."})
