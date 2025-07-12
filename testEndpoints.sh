#!/bin/bash

POST_ID=$(curl -X POST http://localhost:5000/api/timeline_post -d 'name=Test&email=example@ex.com&content=automated test' | jq '.id')

if [[ $POST_ID -ne 0 ]]; then 
    echo "Post ID: $POST_ID"

    GET_RESPONSE=$(curl -s -o dev/null -w "\n%{http_code}" http://localhost:5000/api/timeline_post)
    echo "GET Status: $GET_RESPONSE"

    if [[ "$GET_RESPONSE" -eq 200 ]];  then
        DELETE_RESPONSE=$(curl -s -X DELETE http://localhost:5000/api/timeline_post -d "post_id=$POST_ID" | jq '.status' )
        
        if [[ "$DELETE_RESPONSE" == "Success" ]]; then 
            echo "Deleted successfully: $DELETE_RESPONSE"

        else
            echo "Delete Error: $DELETE_RESPONSE"
        fi
    else
        echo "GET Error: $GET_RESPONSE"
    fi
else
    echo "POST Error: $POST_ID"
fi