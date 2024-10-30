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
                speed_text.set(f"Speed: {new_data['speed']} MPH")
            if new_data.__contains__('mppt1_i_v'):
                mppt1_input_voltage.set(f"MPPT1 Input Voltage: {new_data['mppt1_i_v']} V")
            if new_data.__contains__('mppt1_i_c'):
                mppt1_input_current.set(f"MPPT1 Input Current: {new_data['mppt1_i_c']} A")
            if new_data.__contains__('mppt2_i_v'):
                mppt2_input_voltage.set(f"MPPT2 Input Voltage: {new_data['mppt2_i_v']} V")
            if new_data.__contains__('mppt2_i_c'):
                mppt2_input_current.set(f"MPPT2 Input Current: {new_data['mppt2_i_c']} A")
            if new_data.__contains__('pack_soc'):
                pack_soc_text.set(f"Pack SOC: {new_data['pack_soc']} Ah")
            if new_data.__contains__('pack_soc_percentage'):
                pack_soc_percentage_text.set(f"Pack SOC Percentage: {new_data['pack_soc_percentage']}%")



        except queue.Empty:
            pass

        # Schedule the next update after 100 milliseconds
        root.after(100, update_data)

    # Create the main window
    root = tk.Tk()
    root.title("Live Data Display")

    # Variables to hold text
    speed_text = tk.StringVar()
    pack_soc_text = tk.StringVar()
    pack_soc_percentage_text = tk.StringVar()
    mppt1_input_voltage = tk.StringVar()
    mppt1_input_current = tk.StringVar()
    mppt2_input_voltage = tk.StringVar()
    mppt2_input_current = tk.StringVar()

    # Set initial text
    speed_text.set("Speed: 0 MPH")
    pack_soc_text.set("Pack SOC: 0 Ah")
    pack_soc_percentage_text.set("Pack SOC Percentage: 0%")
    mppt1_input_voltage.set("MPPT1 Input Voltage: 0 V")
    mppt1_input_current.set("MPPT1 Input Current: 0 A")
    mppt2_input_voltage.set("MPPT2 Input Voltage: 0 V")
    mppt2_input_current.set("MPPT2 Input Current: 0 A")

    # Create labels to display the text fields
    speed_label = tk.Label(root, textvariable=speed_text, font=("Helvetica", 14))
    pack_soc_label = tk.Label(root, textvariable=pack_soc_text, font=("Helvetica", 14))
    pack_soc_percentage_label = tk.Label(root, textvariable=pack_soc_percentage_text, font=("Helvetica", 14))
    mppt1_input_v_label = tk.Label(root, textvariable=mppt1_input_voltage, font=("Helvetica", 14))
    mppt1_input_c_label = tk.Label(root, textvariable=mppt1_input_current, font=("Helvetica", 14))
    mppt2_input_v_label = tk.Label(root, textvariable=mppt2_input_voltage, font=("Helvetica", 14))
    mppt2_input_c_label = tk.Label(root, textvariable=mppt2_input_current, font=("Helvetica", 14))

    # Pack the labels into the window
    speed_label.pack(pady=10)
    pack_soc_label.pack(pady=10)
    pack_soc_percentage_label.pack(pady=10)
    mppt1_input_v_label.pack(pady=10)
    mppt1_input_c_label.pack(pady=10)
    mppt2_input_v_label.pack(pady=10)
    mppt2_input_c_label.pack(pady=10)

    # Start the data update loop
    update_data()

    # Start the main loop (this will run in the separate thread)
    root.mainloop()
