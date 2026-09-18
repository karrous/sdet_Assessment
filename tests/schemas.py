"""JSON schemas for the resources with full response-shape validation."""

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["userId", "id", "title", "body"],
    "additionalProperties": False,
}

COMMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "postId": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+$"},
        "body": {"type": "string"},
    },
    "required": ["postId", "id", "name", "email", "body"],
}

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+$"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {"lat": {"type": "string"}, "lng": {"type": "string"}},
                    "required": ["lat", "lng"],
                },
            },
            "required": ["street", "suite", "city", "zipcode", "geo"],
        },
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"},
            },
            "required": ["name", "catchPhrase", "bs"],
        },
    },
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
}
