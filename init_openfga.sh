#!/bin/bash

# Wait for OpenFGA to be ready
echo "Waiting for OpenFGA to be ready..."
until curl -s http://openfga:8080 > /dev/null; do
    sleep 1
done
echo "OpenFGA is ready."

# Create a store
echo "Creating OpenFGA store..."
STORE_RESPONSE=$(curl -s -X POST http://openfga:8080/stores -H "Content-Type: application/json" -d '{"name":"my-store"}')
STORE_ID=$(echo $STORE_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
if [ -z "$STORE_ID" ]; then
    echo "Failed to create store. Response: $STORE_RESPONSE"
    exit 1
fi
echo "Store created with ID: $STORE_ID"
# Create directory for storing IDs
mkdir -p /tmp/ids
# Save store ID to a file
echo "$STORE_ID" > /tmp/ids/openfga_store_id.txt

# Apply the authorization model
echo "Applying authorization model..."
MODEL_RESPONSE=$(curl -s -X POST http://openfga:8080/stores/$STORE_ID/authorization-models -H "Content-Type: application/json" -d @/openfga_model.json)
MODEL_ID=$(echo $MODEL_RESPONSE | grep -o '"authorization_model_id":"[^"]*' | cut -d'"' -f4)
if [ -z "$MODEL_ID" ]; then
    echo "Failed to apply model. Response: $MODEL_RESPONSE"
    exit 1
fi
echo "Model applied with ID: $MODEL_ID"

# Write tuples
echo "Writing tuples..."
curl -s -X POST http://openfga:8080/stores/$STORE_ID/write -H "Content-Type: application/json" -d '{
    "writes": {
        "tuple_keys": [
            {
                "user": "user:alice",
                "relation": "can_access",
                "object": "document:123"
            }
        ]
    }
}'
echo "Tuples written."
