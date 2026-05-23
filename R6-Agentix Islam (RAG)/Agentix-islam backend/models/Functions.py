tools = [
    {
        "type": "function",
        "function": {
            "name": "function_search_fatwa",
            "description": "Get questions of the users about Islamic fatwa",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question of the user when asking about Islamic fatwa",
                    },
                },
                "required": ["question"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "function_escalate_to_Sheikh",
            "description": "When user is not satisfied with the answer and ask to talk to human or real Sheikh",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question by the user",
                    },
                },
                "required": ["question"]
            },
        }
    },
]

linkedinTools = [
    {
        "type": "function",
        "function": {
            "name": "function_search_posts",
            "description": "When a user ask a question or say tell me about some topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question of the user",
                    },
                },
                "required": ["question"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "function_write_content",
            "description": "When user is requesting to write content about a certain topic, example: wrtie fr me a content about a topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The topic or request to write a content",
                    },
                },
                "required": ["topic"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "function_write_like_me",
            "description": "When user is requesting to write a content about a certain topic like the style of writing of someone",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The topic",
                    },
                },
                "required": ["topic"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_me_to_email_list",
            "description": "When user is requesting to join the email list",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the user",
                    },
                    "email": {
                        "type": "string",
                        "description": "The email of the user",
                    },
                },
                "required": ["topic"]
            },
        }
    },

]
