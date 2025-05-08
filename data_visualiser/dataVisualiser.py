import plotly.express as px



class PlotCreator:
    def box_plot(self, data, y):
        fig = px.box(data, y=y)
        fig.show()


