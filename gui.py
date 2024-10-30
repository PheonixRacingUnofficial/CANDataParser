import tkinter as tk
import queue


# Function to start the tkinter GUI
def start_gui(data_queue):
    # Function to update data in the GUI
    def update_data():
        try:
            # Try to get data from the queue (non-blocking)
            new_data: dict = data_queue.get_nowait()

            if new_data.__contains__('speed'):
                # Update text fields with new data
                speed_text.set(f"Speed: {new_data['speed']} MPH")



            # Update text fields with new data
            speed_text.set(new_data['text1'])
            text2.set(new_data['text2'])
            text3.set(new_data['text3'])

        except queue.Empty:
            pass

        # Schedule the next update after 100 milliseconds
        root.after(100, update_data)

    # Create the main window
    root = tk.Tk()
    root.title("Live Data Display")

    # Variables to hold text
    speed_text = tk.StringVar()
    text2 = tk.StringVar()
    text3 = tk.StringVar()

    # Set initial text
    speed_text.set("Speed: 0 MPH")
    text2.set("Initial text 2")
    text3.set("Initial text 3")

    # Create labels to display the text fields
    speed_label = tk.Label(root, textvariable=speed_text, font=("Helvetica", 14))
    label2 = tk.Label(root, textvariable=text2, font=("Helvetica", 14))
    label3 = tk.Label(root, textvariable=text3, font=("Helvetica", 14))

    # Pack the labels into the window
    speed_label.pack(pady=10)
    label2.pack(pady=10)
    label3.pack(pady=10)

    # Start the data update loop
    update_data()

    # Start the main loop (this will run in the separate thread)
    root.mainloop()
