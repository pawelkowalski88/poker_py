API Routes description

- /api/game 
    - GET gets the current game state. The cards of the other users are hidden.
        - parameters:
            - table_id
            - user_id
        - 
    - POST sends the player move information.
    
- /api/tables
    - GET get all the tables available.
    
- /api/table/{id}
    - GET get the information about the table represented by the id.
    - POST joins the table. Player data encoded in the request header.
    - DELETE leave the table. Player data encoded in the request header.
     
- /api/login
    - POST logs in with the current player/user data.
    
- /api/logout
    - POST logs out the player/user.
    
- /api/state
    - GET state of the api.
   
