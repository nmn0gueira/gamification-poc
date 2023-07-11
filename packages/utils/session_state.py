import streamlit as st

class SessionState:
    """
    SessionState class to store session state variables
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._state = {}  # Dictionary to store session state variables
        return cls._instance

    def __getattr__(self, attr):
        return self._state.get(attr)

    def __setattr__(self, attr, value):
        self._state[attr] = value