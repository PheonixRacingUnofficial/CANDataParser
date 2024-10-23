import tkinter as tk
import queue


# Function to start the tkinter GUI
def start_gui(data_queue):
    # Function to update data in the GUI
    def update_data():
        try:
            # Try to get data from the queue (non-blocking)
            new_data = data_queue.get_nowait()

            # Update text fields with new data
            text1.set(new_data['text1'])
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
    text1 = tk.StringVar()
    text2 = tk.StringVar()
    text3 = tk.StringVar()

    # Set initial text
    text1.set("Initial text 1")
    text2.set("Initial text 2")
    text3.set("Initial text 3")

    # Create labels to display the text fields
    label1 = tk.Label(root, textvariable=text1, font=("Helvetica", 14))
    label2 = tk.Label(root, textvariable=text2, font=("Helvetica", 14))
    label3 = tk.Label(root, textvariable=text3, font=("Helvetica", 14))

    # Pack the labels into the window
    label1.pack(pady=10)
    label2.pack(pady=10)
    label3.pack(pady=10)

    # Start the data update loop
    update_data()

    # Start the main loop (this will run in the separate thread)
    root.mainloop()
