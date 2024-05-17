# models/__init__.py

"""
Initialize the models package.
"""

from models.engine.file_storage import FileStorage

storage = FileStorage()

storage.reload()
