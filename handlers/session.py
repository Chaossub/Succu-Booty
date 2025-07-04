user_sessions = {}  # key: (chat_id, user_id) → value: {"flow": str, "step": int, "data": dict}

def start_session(chat_id, user_id, flow):
    user_sessions[(chat_id, user_id)] = {"flow": flow, "step": 1, "data": {}}

def get_session(chat_id, user_id):
    return user_sessions.get((chat_id, user_id))

def set_session_step(chat_id, user_id, step):
    if (chat_id, user_id) in user_sessions:
        user_sessions[(chat_id, user_id)]["step"] = step

def set_session_data(chat_id, user_id, key, value):
    if (chat_id, user_id) in user_sessions:
        user_sessions[(chat_id, user_id)]["data"][key] = value

def end_session(chat_id, user_id):
    user_sessions.pop((chat_id, user_id), None)
