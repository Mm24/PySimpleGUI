from random import randint
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.backends.tkagg as tkagg
import tkinter as tk


def main():
    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.grid()

    canvas_elem = sg.Canvas(size=(640, 480))  # get the canvas we'll be drawing on
    slider_elem = sg.Slider(range=(0, 10000), size=(60, 10), orientation='h')
    # define the form layout
    layout = [[sg.Text('Animated Matplotlib', size=(40, 1), justification='center', font='Helvetica 20')],
              [canvas_elem],
              [slider_elem],
              [sg.ReadFormButton('Exit', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]

    # create the form and show it without the plot
    form = sg.FlexForm('Demo Application - Embedding Matplotlib In PySimpleGUI')
    form.Layout(layout)
    form.ReadNonBlocking()

    graph = FigureCanvasTkAgg(fig, master=canvas_elem.TKCanvas)
    canvas = canvas_elem.TKCanvas

    dpts = [randint(0, 10) for x in range(10000)]
    for i in range(len(dpts)):
        button, values = form.ReadNonBlocking()
        if button is 'Exit' or values is None:
            exit(69)

        slider_elem.Update(i)
        ax.cla()
        ax.grid()
        DATA_POINTS_PER_SCREEN = 40
        ax.plot(range(DATA_POINTS_PER_SCREEN), dpts[i:i+DATA_POINTS_PER_SCREEN],  color='purple')
        graph.draw()
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

        canvas.create_image(640/2, 480/2, image=photo)

        figure_canvas_agg = FigureCanvasAgg(fig)
        figure_canvas_agg.draw()

        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # time.sleep(.1)


if __name__ == '__main__':
    main()
