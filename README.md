Admin Endpoints:
All Admin endpoints are to be used by hypothetical restaurant staff. Requests are designed to manage a queue of customers waiting to be seated.
All Admin endpoints require an adminkey to be passed as a part of the JSON body. This key is currently "apipassword" but a feature that allows the admin to update their password will be added soon.
Admin endpoints are preceded by a lowercase "admin" to denote its authorization status.

######################################################

POST /adminJoinWaitlist:
Endpoint: https://restaurant-waitlist.herokuapp.com/adminJoinWaitlist
Request Method: POST
Request Body:
name: The name of the customer joining the waitlist.
email: The email of the customer joining the waitlist.
adminkey: The password required for authorization.
System Action: Emails the customer with a link to the waitlist. (Currently no frontend for this so it is raw data). Adds customer to the waitlist with a timestamp of when they joined.
Returns: Client token which can be added to the end of a client URL for access to the waitlist (e.g. /getwaitlist/ or /leavequeue/). Client tokens expire in 90 minutes.

######################################################

GET /adminGetWaitlist:
Endpoint: https://restaurant-waitlist.herokuapp.com/adminGetWaitlist
Request Method: GET
Request Body:
adminkey: The password required for authorization.
Returns: Returns current user which will be "admin" and a waitlist array of users in the queue.

######################################################

DELETE /adminRemoveUser:
Endpoint: https://restaurant-waitlist.herokuapp.com/adminRemoveUser
Request Method: DELETE
Request Body:
adminkey: The password required for authorization.
name: The name of the user to be removed from the queue.
email: The email of the user to be removed from the queue.
System Action: Removes particular user from queue.
Returns: Confirmation that user was removed.

######################################################

POST /adminTableReady:
Endpoint: https://restaurant-waitlist.herokuapp.com/adminTableReady
Request Method: POST
Request Body:
adminkey: The password required for authorization.
name: The name of the customer whose table is ready.
email: The email of the customer whose table is ready.
System Action: Emails the customer notifying them that their table is ready. Then removes them from the queue automatically.
Returns: Confirmation that customer was notified and removed from queue.

######################################################

POST /adminClearQueue:
Endpoint: https://restaurant-waitlist.herokuapp.com/adminClearQueue
Request Method: POST
Request Body:
adminkey: The password required for authorization.
System Action: Clears all users from waitlist.
Returns: Confirmation that waitlist has been cleared.

######################################################

POST /adminMsgCustomer:
Endpoint: https://restaurant-waitlist.herokuapp.com/adminMsgCustomer
Request Method: POST
Request Body:
adminkey: The password required for authorization.
customer_email: The email of the customer who will receive the message.
adminMsg: The message to be sent to the customer.
System Action: Emails the customer with a custom message.
Returns: Confirmation that email was sent.
