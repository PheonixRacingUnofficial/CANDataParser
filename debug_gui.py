import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import queue

class UpdatingGraph:
    def __init__(self, data_queue):
        # Use the provided data_queue to receive data
        self.data_queue = data_queue

        # Two lists to hold time and voltage data
        self.time_values = []
        self.voltage_values = []

        # Create the Tkinter window
        self.root = tk.Tk()
        self.root.title("Time vs Voltage Graph")

        # Create a Matplotlib figure
        self.fig, self.ax = plt.subplots()

        # Create a Tkinter-compatible canvas to embed the Matplotlib graph
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Start consuming values from the queue
        self.consume_values()

        # Use Matplotlib's animation to update the graph every 1000ms (1 second)
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=10)

        self.ax.set_ylim(-1, 6)

    def consume_values(self):
        """Consume values from the queue and update the time and voltage lists."""
        while not self.data_queue.empty():
            # Retrieve the new data point (which should be [time, voltage])
            new_data = self.data_queue.get()

            if isinstance(new_data, list) and len(new_data) == 2:
                time_value, voltage_value = new_data  # Unpack the list
                self.time_values.append(time_value)
                self.voltage_values.append(voltage_value)

                # Limit the list to 20 values to avoid overcrowding
                if len(self.time_values) > 20:
                    self.time_values.pop(0)
                    self.voltage_values.pop(0)

        # Schedule the next call of this function
        self.root.after(10, self.consume_values)

    def animate(self, i):
        """Animation function for updating the graph."""
        self.ax.clear()  # Clear the previous plot
        self.ax.plot(self.time_values, self.voltage_values)  # Plot time vs voltage
        self.ax.set_title('Time vs Voltage')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.set_xlabel('Time (s)')

        self.ax.set_ylim(-1, 6)

    def start(self):
        """Start the Tkinter mainloop and show the GUI."""
        self.root.mainloop()
