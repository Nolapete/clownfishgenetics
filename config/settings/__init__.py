import os

from split_settings.tools import include, optional

# Include common settings
include(
    "base.py",
)

# Include environment-specific settings based on
# an environment variable, if set.
# You will need to define DJANGO_ENV in your environment,
# e.g., 'development' or 'production'.
# If you don't define it, it might default to a safe value
# or you can make it required.

# Example structure using an environment variable 'DJANGO_ENV'

DJANGO_ENV = os.environ.get("DJANGO_ENV")

if DJANGO_ENV:
    include(f"{DJANGO_ENV}.py")
else:
    # Default to development if not specified,
    # but make it optional
    include(optional("development.py"))

# You can also use 'optional()' for a local settings
# file that overrides all others
# and is not committed to version control.
include(optional("local_settings.py"))
