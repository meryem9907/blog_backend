#!/bin/bash

# Requiremnts jq
# flush before running whole script: python manage.py flush

curl -X POST http://127.0.0.1:8000/auth/register/  -H "Content-Type: application/json" -d '{"username":"alice","email":"alice@example.com","password":"StrongPass123!","password2":"StrongPass123!"}'

# Registration with missing required fields: username, password, email
curl -X POST http://127.0.0.1:8000/auth/register/  -H "Content-Type: application/json" -d '{"email":"john@example.com","password":"StrongPass123!","password2":"StrongPass123!"}'
curl -X POST http://127.0.0.1:8000/auth/register/  -H "Content-Type: application/json" -d '{"username":"john","email":"john@example.com"}'
curl -X POST http://127.0.0.1:8000/auth/register/  -H "Content-Type: application/json" -d '{"username":"john", "password":"StrongPass123!","password2":"StrongPass123!"}'

# login 
RESPONSE=$(curl -X POST http://127.0.0.1:8000/auth/login/ -H "Content-Type: application/json"  -d '{"email":"alice@example.com","password":"StrongPass123!"}')

REFRESH=$(echo $RESPONSE | jq -r '.refresh')
ACCESS=$(echo $RESPONSE | jq -r '.access')

curl -X POST http://127.0.0.1:8000/auth/token/refresh/ -H "Content-Type: application/json"  -d "{\"refresh\":\"$REFRESH\"}" | jq

curl -s -X PATCH http://127.0.0.1:8000/auth/update/user/  -H "Content-Type: application/json" -d '{"username": "alice_new_new","email": "alice_new_new@example.com"}' -H "Authorization: Bearer $ACCESS" | jq

curl -s -X DELETE http://127.0.0.1:8000/auth/delete/user/ -H "Authorization: Bearer $ACCESS" | jq 

curl -s http://127.0.0.1:8000/auth/me/ -H "Authorization: Bearer $ACCESS" | jq

# logout 
curl -s -X POST http://127.0.0.1:8000/auth/logout/ -H "Content-Type: application/json"  -d "{\"refresh\":\"$REFRESH\"}" | jq

### POSTS
# CREATE
curl -X POST http://127.0.0.1:8000/post/create/ -H "Content-Type: application/json" -H "Authorization: Bearer $ACCESS" -d '{"title": "My First Blog Post","body": "This is the content of the post.","status": "DRAFT","created_at": "2025-10-18T09:30:00Z"}'
curl -X POST http://127.0.0.1:8000/post/create/ -H "Content-Type: application/json" -H "Authorization: Bearer $ACCESS"  -d '{"title": "My Second Blog Post", "body": "This is the content of the post.", "status": "DRAFT", "created_at": "2025-10-28T09:30:00Z" }'
# draft with pub date
curl -X POST http://127.0.0.1:8000/post/create/ -H "Content-Type: application/json" -H "Authorization: Bearer $ACCESS" -d '{"title": "My First Blog Post","body": "This is the content of the post.","status": "DRAFT","published_at": "2025-10-18T09:30:00Z", "created_at": "2025-10-20T09:30:00Z"}'

# LIST
curl -X GET http://127.0.0.1:8000/post/list/  | jq

# READ
curl -X GET http://127.0.0.1:8000/post/read/1/ -H "Authorization: Bearer $ACCESS" | jq

# UPDATE
curl -X PATCH http://127.0.0.1:8000/post/update/1/  -H "Content-Type: application/json"  -H "Authorization: Bearer $ACCESS"  -d '{ "title": "Updated Post Title",  "body": "Revised post content.","status": "PUBLIC", "published_at": "2025-10-18T12:00:00Z"}'

# DELETE
curl -X DELETE http://127.0.0.1:8000/post/delete/1/ -H "Authorization: Bearer $ACCESS"

### TAGS
curl -X POST http://127.0.0.1:8000/tags/create/  -H "Content-Type: application/json"  -H "Authorization: Bearer $ACCESS"  -d '{ "name": "Ruby",  "slug": "ruby"}'

curl -X GET http://127.0.0.1:8000/tags/read/1/  -H "Content-Type: application/json"  -H "Authorization: Bearer $ACCESS" 

curl -s -X POST http://127.0.0.1:8000/tags/create/tag/1/post/1/ -H "Content-Type: application/json" -H "Authorization: Bearer $ACCESS" | jq

curl -s -X  GET http://127.0.0.1:8000/tags/list/post-tags/1/  -H "Content-Type: application/json"  -H "Authorization: Bearer $ACCESS" | jq

curl -s -X GET http://127.0.0.1:8000/tags/list/  -H "Content-Type: application/json"  -H "Authorization: Bearer $ACCESS" | jq

curl -s -i -X DELETE http://127.0.0.1:8000/tags/delete/1/ -H "Authorization: Bearer $ACCESS"| jq

curl -s -X GET http://127.0.0.1:8000/tags/list/ -H "Content-Type: application/json"  -H "Authorization: Bearer $ACCESS" | jq


### COMMENTS

curl -s -X POST http://127.0.0.1:8000/comment/create/1/  -H "Content-Type: application/json"  -d '{"body": "Nice post!",  "guestname": "bob",  "created_at": "2025-10-28T09:30:00Z" }' | jq

curl -s -X POST http://127.0.0.1:8000/comment/create/1/  -H "Content-Type: application/json"  -H "Authorization: Bearer $ACCESS"  -d '{  "body": "Author here thanks for reading!", "guestname": "bob",  "created_at": "2025-10-28T09:35:00Z" }' | jq

curl -s -X GET http://127.0.0.1:8000/comment/list/1/ -H "Accept: application/json" | jq

curl -s -X GET http://127.0.0.1:8000/comment/read/1/ -H "Accept: application/json" | jq

curl -s -X DELETE http://127.0.0.1:8000/comment/delete/1/ -H "Authorization: Bearer $ACCESS" | jq

curl -s -X GET http://127.0.0.1:8000/comment/read/1/ -H "Accept: application/json" | jq
