import time

# Define the action to be performed
def specific_action():
    print("Performing specific action...")

# Define the duration of the action in seconds
duration_seconds = 5

# Get the current time
start_time = time.time()

# Perform the action if the elapsed time is less than the specified duration
while time.time() - start_time < duration_seconds:
    specific_action()

print("Action completed.")