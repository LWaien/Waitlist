# Admin Endpoints

All Admin endpoints are to be used by hypothetical restaurant staff. Requests are designed to manage a queue of customers waiting to be seated. All Admin endpoints require an `adminkey` to be passed as a part of the JSON body. This key is currently set to "apipassword," but a feature that allows the admin to update their password will be added soon. Admin endpoints are preceded by a lowercase "admin" to denote their authorization status. Please note tha the emailing function is working but disabled due to security reasons. (The email service can be made functional by providing an email authorization key) 

## `POST /adminJoinWaitlist`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/adminJoinWaitlist](https://restaurant-waitlist.herokuapp.com/adminJoinWaitlist)
- **Request Method:** POST
- **Request Body:**
  - `name`: The name of the customer joining the waitlist.
  - `email`: The email of the customer joining the waitlist.
  - `adminkey`: The password required for authorization.
- **System Action:**
  - Emails the customer with a link to the waitlist. (Currently, no frontend for this, so it is raw data).
  - Adds the customer to the waitlist with a timestamp of when they joined.
- **Returns:** Client token which can be added to the end of a client URL for access to the waitlist (e.g., `/getwaitlist/` or `/leavequeue/`). Client tokens expire in 90 minutes.

## `GET /adminGetWaitlist`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/adminGetWaitlist](https://restaurant-waitlist.herokuapp.com/adminGetWaitlist)
- **Request Method:** GET
- **Request Body:**
  - `adminkey`: The password required for authorization.
- **Returns:** Current user, which will be "admin," and a waitlist array of users in the queue.

## `DELETE /adminRemoveUser`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/adminRemoveUser](https://restaurant-waitlist.herokuapp.com/adminRemoveUser)
- **Request Method:** DELETE
- **Request Body:**
  - `adminkey`: The password required for authorization.
  - `name`: The name of the user to be removed from the queue.
  - `email`: The email of the user to be removed from the queue.
- **System Action:** Removes the particular user from the queue.
- **Returns:** Confirmation that the user was removed.

## `POST /adminTableReady`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/adminTableReady](https://restaurant-waitlist.herokuapp.com/adminTableReady)
- **Request Method:** POST
- **Request Body:**
  - `adminkey`: The password required for authorization.
  - `name`: The name of the customer whose table is ready.
  - `email`: The email of the customer whose table is ready.
- **System Action:**
  - Emails the customer notifying them that their table is ready.
  - Removes them from the queue automatically.
- **Returns:** Confirmation that the customer was notified and removed from the queue.

## `POST /adminClearQueue`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/adminClearQueue](https://restaurant-waitlist.herokuapp.com/adminClearQueue)
- **Request Method:** POST
- **Request Body:**
  - `adminkey`: The password required for authorization.
- **System Action:** Clears all users from the waitlist.
- **Returns:** Confirmation that the waitlist has been cleared.

## `POST /adminMsgCustomer`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/adminMsgCustomer](https://restaurant-waitlist.herokuapp.com/adminMsgCustomer)
- **Request Method:** POST
- **Request Body:**
  - `adminkey`: The password required for authorization.
  - `customer_email`: The email of the customer who will receive the message.
  - `adminMsg`: The message to be sent to the customer.
- **System Action:** Emails the customer with a custom message.
- **Returns:** Confirmation that the email was sent.


# Client Endpoints

Designed to accept client tokens in the URL and give customers the ability to both see their place in the waitlist or willingly leave the queue.
These endpoints are designed to allow the system to provide customers with a URL to access the waitlist in an email. Client tokens are automatically added to the url and emailed to the customer
upon joining the queue. A front end to present this client information is currently being built. 

## `DELETE /leavequeue/<token>`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/leavequeue/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI5IiwibmFtZSI6IkxvZ2FuIiwidXNlcmVtYWlsIjoibGF3YWllbjE0QGdtYWlsLmNvbSIsImV4cCI6MTY4MzQ5Njc3OH0.qikXNiRo1d0Tshi-ubEFJPevCauHVvKCm3lab91p3rE](https://restaurant-waitlist.herokuapp.com/leavequeue/<token>)
- **Request Method:** DELETE
- **Description:** Allows customers to willingly leave the waitlist by using their client token.
- **Returns:** No specific return value, but the customer will be removed from the waitlist.

## `GET /getwaitlist/<token>`

- **Endpoint:** [https://restaurant-waitlist.herokuapp.com/getwaitlist/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI5IiwibmFtZSI6IkxvZ2FuIiwidXNlcmVtYWlsIjoibGF3YWllbjE0QGdtYWlsLmNvbSIsImV4cCI6MTY4MzQ5NTgzOH0.drIv1uG2E2ZchvHQ9f-H0K-CjeFdOCA7_2WvgcotQ0c](https://restaurant-waitlist.herokuapp.com/getwaitlist/<token>)
- **Request Method:** GET
- **Description:** Allows customers to see their place in the waitlist using their client token.
- **Returns:** The customer's place in the waitlist and related information.

Please note that the token in the URL is a placeholder and should be replaced with the actual client token obtained from the `/adminJoinWaitlist` endpoint or another relevant authentication process.
