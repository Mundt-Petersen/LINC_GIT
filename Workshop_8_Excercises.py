import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.graph_objects as go


#Data
years = np.array([2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)
profits = np.array([885, 1480, 1243, 2785, 3580, 5933, 5463, 6470, 7518, 8065])

# Sopig data för test R^2
weird_profits = np.array([885, 234, 1643, 2785, 3580, 933, 5463, 2470, 7518, 165])


# Future years for extension
future_years = np.array([2024, 2025, 2026, 2027, 2028, 2029, 2030]).reshape(-1, 1)
all_years = np.vstack((years, future_years))

def plot(x, y):
    newmodel = LinearRegression().fit(x, y)

    newslope = newmodel.coef_[0]
    newintercept = newmodel.intercept_

    new_predicted_profits = newmodel.predict(x)


    future_years = np.array([2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]).reshape(-1,1)
    future_predicted_profits = newmodel.predict(future_years)


    r2 = r2_score(y, new_predicted_profits)


    plt.scatter(x, y, color='blue', label='Original Data')


    plt.plot(x, new_predicted_profits, color='red', label='Best-Fit Line (sklearn)')
    plt.plot(future_years, future_predicted_profits, color='green', label='Best-Fit Line for future (sklearn)')

    plt.xlabel('Years')
    plt.ylabel('Profits')
    plt.title('Yearly Profits with Best-Fit Line (sklearn)')
    plt.legend()

    plt.text(2014, 2000, f'R^2 = {r2:.2f}', fontsize=12, color='green')


    plt.show()




def create_figure(x, y):
    # Create a figure
    fig = go.Figure()

    # Add initial scatter plot
    fig.add_trace(go.Scatter(x=x.flatten(), y=y, mode='markers', name='Original Data'))

    # Create frames
    frames = []
    for i in range(2, len(x) + 1):
        # Fit the model with the first i data points
        model = LinearRegression().fit(x[:i], y[:i])
        
        # Predict profits for the available and future years
        extended_predicted_profits = model.predict(all_years[:i + len(future_years)])

        # Add a frame
        frames.append(go.Frame(
            data=[
                go.Scatter(x=x[:i].flatten(), y=y[:i], mode='markers', name='Original Data'),
                go.Scatter(x=all_years[:i + len(future_years)].flatten(), y=extended_predicted_profits, mode='lines', name='Best-Fit Line')
            ],
            name=f'Frame {i}'
        ))

    # Add frames to the figure
    fig.frames = frames

    # Configure animation settings
    fig.update_layout(
        updatemenus=[dict(type='buttons', showactive=False,
                        buttons=[dict(label='Play',
                                        method='animate',
                                        args=[None, dict(frame=dict(duration=500, redraw=True),
                                                        fromcurrent=True,
                                                        mode='immediate')])])])

    # Add layout details
    fig.update_layout(
        title="Progression of Linear Regression with Future Predictions",
        xaxis_title="Years",
        yaxis_title="Profits",
        showlegend=True
    )

    # Display the figure in Jupyter Notebook
    fig.show()

plot(years, profits)
create_figure(years, profits)
