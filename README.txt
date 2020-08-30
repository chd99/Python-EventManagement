*Sending notice mail function is not fully finished. 
====================
Initial run maually 
====================
Run below script to create SQlite Database initially:
    createTable.py


Endpoints List:
--------------------------------------------------------------
    	GET http://127.0.0.1:5001/events
	GET http://127.0.0.1:5001/event/<event_id>
    	POST http://127.0.0.1:5001/event/<event_id>
    	PUT http://127.0.0.1:5001/event/<event_id>
    	DELETE http://127.0.0.1:5001/event/<event_id>
    	POST http://127.0.0.1:5001/register/<event_id>
	GET http://127.0.0.1:5001/user/<user_mail>
    	DELETE http://127.0.0.1:5001/delete/
--------------------------------------------------------------

Endpoints Detail:
====================
    Event Management:
====================
--------------------------------------------------------------
    events list: 
    	GET http://127.0.0.1:5001/events
--------------------------------------------------------------
	##return all events list (200)

--------------------------------------------------------------
    veiw particular event:
	GET http://127.0.0.1:5001/event/<event_id>
--------------------------------------------------------------
	##return event information (200)
                if the event not exists, return error message (400)
	{
	    "message": "Event is not found."
	}

--------------------------------------------------------------
    create event:
    	POST http://127.0.0.1:5001/event/<event_id>
--------------------------------------------------------------
                 ##sample request:
		Headers: Content-Type: application/json
		Body:
			{
			   "event_id": "ev0002",
 			   "name": "Matrix"
 			   "location": "Tokyo",
 			   "startDate": "2020-12-30",
 			   "endDate": "2020-12-31"
			}

	##return error message when insert failed. (500)
	     {
	        "message": "An error occurred inserting the event."
	     }

--------------------------------------------------------------
    create/update event:
    	PUT http://127.0.0.1:5001/event/<event_id>
--------------------------------------------------------------
                 ##sample request:
		Headers: Content-Type: application/json
		Body:
			{
			    "evnetid": "ev0002",
			    "name": "Three Bodies",
			    "location": "Beijing",
			    "startDate": "2021-1-1",
			    "endDate": "2021-1-2"
			}

--------------------------------------------------------------
    delete event:
    	DELETE http://127.0.0.1:5001/event/<event_id>
--------------------------------------------------------------
	return Json messsage when delete sucessfully.
	{
 	   "message": "event deleted."
	}

====================
    Event Register:
====================
--------------------------------------------------------------
    	POST http://127.0.0.1:5001/register/<event_id>
--------------------------------------------------------------
                 ##sample request:
		Headers: Content-Type: application/json
		Body:
		{
		    "user_mail": "eric.ch@gmail.com",
		    "event_id": "ev0002"
		}

	##return error message when user has registered the event. (200)
	{
	    "message": "This user(eric.ch@gmail.com) has registered the event with event_id(ev0002)."
	}

====================
    Veiw by User:
====================
--------------------------------------------------------------
	GET http://127.0.0.1:5001/user/<user_mail>
--------------------------------------------------------------	
	##sample: http://127.0.0.1:5001/user/eric.ch@gmail.com
                ##return:
	return Registered Events info :
		{
		    "RegisteredEvents": [
		        {
		            "register_id": 2,
		            "user_mail": "eric.ch@gmail.com",
		            "event_id": "ev0002",
		            "event_name": "Three Bodies",
		            "event_location": "Beijing",
 		            "startDate": "2021-1-1",
		            "endDate": "2021-1-2"
		        }
		    ]
		}	

	##return: 
	if the user registered event no found, return below error message. (404)
	{
	    "message": "The user has no registered event."
	}

====================
    Delete Register:
====================
--------------------------------------------------------------	
    	DELETE http://127.0.0.1:5001/delete/
--------------------------------------------------------------	
                 ##sample request:
		Headers: Content-Type: application/json
		Body:
		{
		    "user_mail": "eric.ch@gmail.com",
		    "event_id": "ev0002"
		}

                ##return
	If the register exist and deleted successfully, return below message. (200)
		{
		    "message": "register deleted."
		}

	If the register no exist, return below error message. (400)
		{
		    "message": "This register does not exist."
		}
